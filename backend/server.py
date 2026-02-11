from fastapi import FastAPI, APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import secrets
from mailersend import EmailBuilder, MailerSendClient
from supabase import create_client, Client
from lesson_intros import get_lesson_intro, LESSON_INTROS
from category_lessons import get_category_lesson, get_lesson_page, CATEGORY_LESSONS
from real_market import (
    generate_realistic_candles, AVAILABLE_ASSETS, validate_entry,
    calculate_risk_reward, calculate_result_in_r, calculate_discipline_score,
    generate_insights, Candle, ORBRange, TradeEntry, TradeResult, ReplaySession
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Supabase connection
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://sjvhumpezgbtbtrxjrwp.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create the main app
app = FastAPI(title="TradeLingo API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Serve static files (images) from /api/static/
STATIC_DIR = ROOT_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)
(STATIC_DIR / "images").mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== MODELS ====================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    password_hash: str
    xp: int = 0
    level: int = 1
    completed_lessons: List[str] = Field(default_factory=list)
    subscription: str = "free"  # free, standard, pro
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # Email verification fields
    is_verified: bool = False
    verification_token: Optional[str] = None
    verification_token_expires: Optional[datetime] = None
    # Admin field
    is_admin: bool = False

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    xp: int
    level: int
    completed_lessons: List[str]
    subscription: str
    rank: str
    is_verified: bool = False
    is_admin: bool = False

class VerifyEmailRequest(BaseModel):
    token: str

class ResendVerificationRequest(BaseModel):
    email: EmailStr

class Lesson(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    level: int
    order: int
    title: str
    description: str
    content: str
    quiz: dict
    xp_reward: int

class LessonResponse(BaseModel):
    id: str
    level: int
    order: int
    title: str
    description: str
    content: str
    quiz: dict
    xp_reward: int
    is_completed: bool = False
    is_unlocked: bool = False

class JournalEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    win: bool
    confluences: List[str] = Field(default_factory=list)
    description: str
    photo: Optional[str] = None  # Base64 image
    reflection_change: Optional[str] = None
    reflection_mistakes: Optional[str] = None
    reflection_proud: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class JournalCreate(BaseModel):
    user_id: str
    win: bool
    confluences: List[str] = Field(default_factory=list)
    description: str
    photo: Optional[str] = None
    reflection_change: Optional[str] = None
    reflection_mistakes: Optional[str] = None
    reflection_proud: Optional[str] = None

class SubscriptionUpgrade(BaseModel):
    user_id: str
    plan: str  # standard, pro

class LessonComplete(BaseModel):
    user_id: str

# ==================== HELPER FUNCTIONS ====================

def is_admin_user(user_id: str) -> bool:
    """Check if user has admin privileges (everything unlocked for testing)"""
    if not user_id:
        return False
    result = supabase.table('users').select('is_admin').eq('id', user_id).execute()
    if result.data:
        return result.data[0].get('is_admin', False)
    return False

def calculate_rank(xp: int) -> str:
    """Calculate user rank based on XP"""
    if xp < 500:
        return "Retail Trader"
    elif xp < 1500:
        return "Aware Trader"
    elif xp < 3000:
        return "SMC Student"
    elif xp < 6000:
        return "Pro Trader"
    else:
        return "Market Engineer"

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def get_user_response(user_doc: dict) -> UserResponse:
    """Convert user document to UserResponse with rank"""
    return UserResponse(
        id=user_doc['id'],
        username=user_doc['username'],
        email=user_doc['email'],
        xp=user_doc['xp'],
        level=user_doc['level'],
        completed_lessons=user_doc['completed_lessons'],
        subscription=user_doc['subscription'],
        rank=calculate_rank(user_doc['xp']),
        is_verified=user_doc.get('is_verified', False),
        is_admin=user_doc.get('is_admin', False)
    )

# ==================== EMAIL SERVICE ====================

MAILERSEND_API_KEY = os.environ.get('MAILERSEND_API_KEY', '')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

def generate_verification_token() -> str:
    """Generate a secure random verification token"""
    return secrets.token_urlsafe(32)

async def send_verification_email(to_email: str, username: str, verification_token: str):
    """Send verification email using Mailersend"""
    if not MAILERSEND_API_KEY:
        logger.warning("MAILERSEND_API_KEY not set, skipping email")
        return False
    
    try:
        client = MailerSendClient(api_key=MAILERSEND_API_KEY)
        
        verification_link = f"{FRONTEND_URL}/verify?token={verification_token}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 30px; border-radius: 10px; text-align: center;">
                <h1 style="color: #00d4ff; margin: 0;">TradeLingo</h1>
                <p style="color: #888; margin: 10px 0 0 0;">Master Trading Like a Pro</p>
            </div>
            
            <div style="padding: 30px 0;">
                <h2 style="color: #333;">Welcome, {username}!</h2>
                <p>Thanks for signing up for TradeLingo. To complete your registration and start your trading education journey, please verify your email address.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_link}" 
                       style="display: inline-block; padding: 15px 40px; background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                        Verify Email Address
                    </a>
                </div>
                
                <p style="color: #666; font-size: 14px;">Or copy this link into your browser:</p>
                <p style="word-break: break-all; background-color: #f5f5f5; padding: 10px; border-radius: 5px; font-size: 12px;">
                    {verification_link}
                </p>
                
                <p style="color: #999; font-size: 12px; margin-top: 30px;">
                    This link expires in 24 hours. If you didn't create a TradeLingo account, you can safely ignore this email.
                </p>
            </div>
            
            <div style="border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #999; font-size: 12px;">
                <p>© 2024 TradeLingo. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to TradeLingo, {username}!
        
        Please verify your email address by clicking this link:
        {verification_link}
        
        This link expires in 24 hours.
        
        If you didn't create a TradeLingo account, you can safely ignore this email.
        """
        
        email = (EmailBuilder()
            .from_email("noreply@trial-neqvygm07z7g0p7w.mlsender.net", "TradeLingo")
            .to_many([{"email": to_email, "name": username}])
            .subject("Verify your TradeLingo account")
            .html(html_content)
            .text(text_content)
            .build())
        
        response = client.emails.send(email)
        logger.info(f"Verification email sent to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send verification email to {to_email}: {str(e)}")
        return False

# ==================== LESSONS DATA ====================

# ==================== LESSONS DATA ====================
# HOW TO EDIT:
# - Each lesson has: id, level, order, title, description, content, quiz, xp_reward
# - Quiz format: question, options (4 choices), correct (0=A, 1=B, 2=C, 3=D), explanation
# - Levels: 1-4, each with 5 lessons (20 total)

LESSONS_DATA = [
    # ========== LEVEL 1 - SMC Basics (5 lessons) ==========
    {
        "id": "l1-1",
        "level": 1,
        "order": 1,
        "title": "Lesson 1 Title",
        "description": "Lesson 1 description here",
        "content": """Lesson 1 content placed here.

Add your educational content with bullet points:
• Point 1
• Point 2
• Point 3""",
        "quiz": {
            "question": "Question placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,  # 0=A, 1=B, 2=C, 3=D
            "explanation": "Explanation of correct answer here."
        },
        "xp_reward": 10
    },
    {
        "id": "l1-2",
        "level": 1,
        "order": 2,
        "title": "Lesson 2 Title",
        "description": "Lesson 2 description here",
        "content": """Lesson 2 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 2 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 2 here."
        },
        "xp_reward": 10
    },
    {
        "id": "l1-3",
        "level": 1,
        "order": 3,
        "title": "Lesson 3 Title",
        "description": "Lesson 3 description here",
        "content": """Lesson 3 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 3 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 3 here."
        },
        "xp_reward": 10
    },
    {
        "id": "l1-4",
        "level": 1,
        "order": 4,
        "title": "Lesson 4 Title",
        "description": "Lesson 4 description here",
        "content": """Lesson 4 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 4 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 4 here."
        },
        "xp_reward": 10
    },
    {
        "id": "l1-5",
        "level": 1,
        "order": 5,
        "title": "Lesson 5 Title",
        "description": "Lesson 5 description here",
        "content": """Lesson 5 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 5 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 5 here."
        },
        "xp_reward": 15
    },
    {
        "id": "l2-1",
        "level": 2,
        "order": 1,
        "title": "Lesson 6 Title",
        "description": "Lesson 6 description here",
        "content": """Lesson 6 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 6 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 6 here."
        },
        "xp_reward": 15
    },
    {
        "id": "l2-2",
        "level": 2,
        "order": 2,
        "title": "Lesson 7 Title",
        "description": "Lesson 7 description here",
        "content": """Lesson 7 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 7 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 7 here."
        },
        "xp_reward": 15
    },
    {
        "id": "l2-3",
        "level": 2,
        "order": 3,
        "title": "Lesson 8 Title",
        "description": "Lesson 8 description here",
        "content": """Lesson 8 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 8 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 8 here."
        },
        "xp_reward": 15
    },
    {
        "id": "l2-4",
        "level": 2,
        "order": 4,
        "title": "Lesson 9 Title",
        "description": "Lesson 9 description here",
        "content": """Lesson 9 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 9 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 9 here."
        },
        "xp_reward": 15
    },
    {
        "id": "l2-5",
        "level": 2,
        "order": 5,
        "title": "Lesson 10 Title",
        "description": "Lesson 10 description here",
        "content": """Lesson 10 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 10 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 10 here."
        },
        "xp_reward": 20
    },
    {
        "id": "l3-1",
        "level": 3,
        "order": 1,
        "title": "Lesson 11 Title",
        "description": "Lesson 11 description here",
        "content": """Lesson 11 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 11 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 11 here."
        },
        "xp_reward": 20
    },
    {
        "id": "l3-2",
        "level": 3,
        "order": 2,
        "title": "Lesson 12 Title",
        "description": "Lesson 12 description here",
        "content": """Lesson 12 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 12 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 12 here."
        },
        "xp_reward": 20
    },
    {
        "id": "l3-3",
        "level": 3,
        "order": 3,
        "title": "Lesson 13 Title",
        "description": "Lesson 13 description here",
        "content": """Lesson 13 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 13 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 13 here."
        },
        "xp_reward": 20
    },
    {
        "id": "l3-4",
        "level": 3,
        "order": 4,
        "title": "Lesson 14 Title",
        "description": "Lesson 14 description here",
        "content": """Lesson 14 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 14 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 14 here."
        },
        "xp_reward": 20
    },
    {
        "id": "l3-5",
        "level": 3,
        "order": 5,
        "title": "Lesson 15 Title",
        "description": "Lesson 15 description here",
        "content": """Lesson 15 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 15 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 15 here."
        },
        "xp_reward": 25
    },
    {
        "id": "l4-1",
        "level": 4,
        "order": 1,
        "title": "Lesson 16 Title",
        "description": "Lesson 16 description here",
        "content": """Lesson 16 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 16 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 16 here."
        },
        "xp_reward": 25
    },
    {
        "id": "l4-2",
        "level": 4,
        "order": 2,
        "title": "Lesson 17 Title",
        "description": "Lesson 17 description here",
        "content": """Lesson 17 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 17 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 17 here."
        },
        "xp_reward": 25
    },
    {
        "id": "l4-3",
        "level": 4,
        "order": 3,
        "title": "Lesson 18 Title",
        "description": "Lesson 18 description here",
        "content": """Lesson 18 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 18 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 18 here."
        },
        "xp_reward": 25
    },
    {
        "id": "l4-4",
        "level": 4,
        "order": 4,
        "title": "Lesson 19 Title",
        "description": "Lesson 19 description here",
        "content": """Lesson 19 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 19 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 19 here."
        },
        "xp_reward": 25
    },
    {
        "id": "l4-5",
        "level": 4,
        "order": 5,
        "title": "Lesson 20 Title",
        "description": "Lesson 20 description here",
        "content": """Lesson 20 content placed here.

Add your educational content here.""",
        "quiz": {
            "question": "Question 20 placed here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Explanation for question 20 here."
        },
        "xp_reward": 30
    }
]

# Prop Firm Ads Data
PROP_FIRM_ADS = [
    {
        "id": "apex",
        "name": "Apex Trader Funding",
        "description": "Get funded up to $300K. No minimum trading days!",
        "url": "https://apextraderfunding.com",
        "discount": "Use code TRADELINGO for 80% off"
    },
    {
        "id": "topstep",
        "name": "TopStep",
        "description": "Trade the combine, get funded. Trusted by 100K+ traders.",
        "url": "https://topstep.com",
        "discount": "Start your journey today!"
    },
    {
        "id": "tradeify",
        "name": "Tradeify",
        "description": "Fast funding, keep up to 90% of profits.",
        "url": "https://tradeify.com",
        "discount": "Special offer for TradeLingo users"
    }
]

# ==================== AUTH ROUTES ====================

# Set to True when you have a verified email domain
EMAIL_VERIFICATION_ENABLED = False

@api_router.post("/auth/register")
async def register(user_data: UserCreate, background_tasks: BackgroundTasks):
    """Register a new user"""
    # Check if email already exists
    existing_email = supabase.table('users').select('id').eq('email', user_data.email).execute()
    if existing_email.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username exists
    existing_username = supabase.table('users').select('id').eq('username', user_data.username).execute()
    if existing_username.data:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Generate verification token (for future use)
    verification_token = generate_verification_token()
    token_expires = datetime.now(timezone.utc) + timedelta(hours=24)
    
    # Create new user - auto-verified if email verification is disabled
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        is_verified=not EMAIL_VERIFICATION_ENABLED,  # Auto-verify if disabled
        verification_token=verification_token if EMAIL_VERIFICATION_ENABLED else None,
        verification_token_expires=token_expires if EMAIL_VERIFICATION_ENABLED else None
    )
    
    user_dict = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password_hash': user.password_hash,
        'xp': user.xp,
        'level': user.level,
        'completed_lessons': user.completed_lessons,
        'subscription': user.subscription,
        'is_verified': user.is_verified,
        'verification_token': verification_token if EMAIL_VERIFICATION_ENABLED else None,
        'verification_token_expires': token_expires.isoformat() if EMAIL_VERIFICATION_ENABLED else None,
        'is_admin': user.is_admin,
        'created_at': user.created_at.isoformat()
    }
    
    supabase.table('users').insert(user_dict).execute()
    
    # Send verification email only if enabled
    if EMAIL_VERIFICATION_ENABLED:
        background_tasks.add_task(
            send_verification_email,
            user_data.email,
            user_data.username,
            verification_token
        )
        logger.info(f"New user registered (pending verification): {user_data.email}")
        return {
            "message": "Registration successful! Please check your email to verify your account.",
            "user_id": user.id,
            "email": user_data.email
        }
    else:
        logger.info(f"New user registered (auto-verified): {user_data.email}")
        # Return user data so they can login immediately
        return get_user_response(user_dict)
    
    return {
        "message": "Registration successful! Please check your email to verify your account.",
        "user_id": user.id,
        "email": user_data.email
    }

@api_router.post("/auth/verify-email")
async def verify_email(request: VerifyEmailRequest):
    """Verify user email with token"""
    result = supabase.table('users').select('*').eq('verification_token', request.token).execute()
    
    if not result.data:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    user = result.data[0]
    
    # Check if token is expired
    token_expires = user.get('verification_token_expires')
    if token_expires:
        if isinstance(token_expires, str):
            token_expires = datetime.fromisoformat(token_expires.replace('Z', '+00:00'))
        if datetime.now(timezone.utc) > token_expires:
            raise HTTPException(status_code=400, detail="Verification token has expired. Please request a new one.")
    
    # Mark user as verified
    supabase.table('users').update({
        'is_verified': True,
        'verification_token': None,
        'verification_token_expires': None
    }).eq('id', user['id']).execute()
    
    logger.info(f"User verified: {user['email']}")
    
    # Return user data so they can be logged in
    updated_result = supabase.table('users').select('*').eq('id', user['id']).execute()
    updated_user = updated_result.data[0] if updated_result.data else user
    return {
        "message": "Email verified successfully! You can now log in.",
        "user": get_user_response(updated_user)
    }

@api_router.post("/auth/resend-verification")
async def resend_verification(request: ResendVerificationRequest, background_tasks: BackgroundTasks):
    """Resend verification email"""
    result = supabase.table('users').select('*').eq('email', request.email).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = result.data[0]
    
    if user.get('is_verified', False):
        raise HTTPException(status_code=400, detail="Email is already verified")
    
    # Generate new token
    verification_token = generate_verification_token()
    token_expires = datetime.now(timezone.utc) + timedelta(hours=24)
    
    supabase.table('users').update({
        'verification_token': verification_token,
        'verification_token_expires': token_expires.isoformat()
    }).eq('id', user['id']).execute()
    
    # Send verification email
    background_tasks.add_task(
        send_verification_email,
        user['email'],
        user['username'],
        verification_token
    )
    
    return {"message": "Verification email sent. Please check your inbox."}

@api_router.post("/auth/login", response_model=UserResponse)
async def login(login_data: UserLogin):
    """Login user"""
    result = supabase.table('users').select('*').eq('email', login_data.email).execute()
    
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    user = result.data[0]
    
    if not verify_password(login_data.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Check if email is verified (only if verification is enabled)
    if EMAIL_VERIFICATION_ENABLED and not user.get('is_verified', False):
        raise HTTPException(
            status_code=403, 
            detail="Please verify your email before logging in. Check your inbox for the verification link."
        )
    
    logger.info(f"User logged in: {login_data.email}")
    return get_user_response(user)

# ==================== USER ROUTES ====================

@api_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get user by ID"""
    result = supabase.table('users').select('*').eq('id', user_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return get_user_response(result.data[0])

# ==================== LESSON ROUTES ====================

@api_router.get("/lessons")
async def get_lessons(user_id: Optional[str] = None):
    """Get all lessons with optional user progress"""
    lessons = []
    completed_lessons = []
    admin_mode = False
    
    if user_id:
        result = supabase.table('users').select('completed_lessons, is_admin').eq('id', user_id).execute()
        if result.data:
            completed_lessons = result.data[0].get('completed_lessons', []) or []
            admin_mode = result.data[0].get('is_admin', False)
    
    for i, lesson in enumerate(LESSONS_DATA):
        # Admin users get everything unlocked for testing
        if admin_mode:
            is_unlocked = True
        else:
            # Determine if lesson is unlocked
            is_unlocked = False
            if i == 0:
                is_unlocked = True  # First lesson always unlocked
            elif i > 0:
                prev_lesson_id = LESSONS_DATA[i-1]['id']
                is_unlocked = prev_lesson_id in completed_lessons
        
        lessons.append({
            **lesson,
            "is_completed": lesson['id'] in completed_lessons,
            "is_unlocked": is_unlocked
        })
    
    return lessons

@api_router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: str, user_id: Optional[str] = None):
    """Get a specific lesson"""
    lesson = next((l for l in LESSONS_DATA if l['id'] == lesson_id), None)
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    is_completed = False
    is_unlocked = True
    admin_mode = False
    
    if user_id:
        result = supabase.table('users').select('completed_lessons, is_admin').eq('id', user_id).execute()
        if result.data:
            completed_lessons = result.data[0].get('completed_lessons', []) or []
            admin_mode = result.data[0].get('is_admin', False)
            is_completed = lesson_id in completed_lessons
            
            # Admin users get everything unlocked
            if admin_mode:
                is_unlocked = True
            else:
                # Check if previous lesson is completed
                lesson_index = LESSONS_DATA.index(lesson)
                if lesson_index > 0:
                    prev_lesson_id = LESSONS_DATA[lesson_index - 1]['id']
                    is_unlocked = prev_lesson_id in completed_lessons or is_completed
    
    return {
        **lesson,
        "is_completed": is_completed,
        "is_unlocked": is_unlocked
    }

@api_router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(lesson_id: str, data: LessonComplete):
    """Complete a lesson and award XP"""
    lesson = next((l for l in LESSONS_DATA if l['id'] == lesson_id), None)
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    result = supabase.table('users').select('*').eq('id', data.user_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = result.data[0]
    completed_lessons = user.get('completed_lessons', []) or []
    
    # Check if already completed
    if lesson_id in completed_lessons:
        return {
            "message": "Lesson already completed",
            "xp_gained": 0,
            "total_xp": user['xp'],
            "level": user['level'],
            "rank": calculate_rank(user['xp'])
        }
    
    # Update user
    new_xp = user['xp'] + lesson['xp_reward']
    new_level = (new_xp // 100) + 1
    completed_lessons = completed_lessons + [lesson_id]
    
    supabase.table('users').update({
        'xp': new_xp,
        'level': new_level,
        'completed_lessons': completed_lessons
    }).eq('id', data.user_id).execute()
    
    logger.info(f"User {data.user_id} completed lesson {lesson_id}, gained {lesson['xp_reward']} XP")
    
    return {
        "message": "Lesson completed!",
        "xp_gained": lesson['xp_reward'],
        "total_xp": new_xp,
        "level": new_level,
        "rank": calculate_rank(new_xp)
    }

# ==================== JOURNAL ROUTES ====================

@api_router.get("/journal/{user_id}")
async def get_journal_entries(user_id: str):
    """Get all journal entries for a user"""
    result = supabase.table('journal_entries').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
    
    # Transform data to match frontend expectations
    entries = []
    for entry in result.data:
        entries.append({
            'id': entry.get('id'),
            'user_id': entry.get('user_id'),
            'win': entry.get('outcome') == 'win',
            'confluences': entry.get('setup_type', '').split(', ') if entry.get('setup_type') else [],
            'description': entry.get('notes', ''),
            'photo': entry.get('screenshot_url'),
            'reflection_change': entry.get('lessons_learned'),
            'reflection_mistakes': entry.get('mistakes', [None])[0] if entry.get('mistakes') else None,
            'reflection_proud': entry.get('emotions'),
            'created_at': entry.get('created_at')
        })
    
    return entries

@api_router.post("/journal")
async def create_journal_entry(entry_data: JournalCreate):
    """Create a new journal entry"""
    entry = JournalEntry(**entry_data.model_dump())
    
    entry_dict = {
        'id': entry.id,
        'user_id': entry.user_id,
        'outcome': 'win' if entry.win else 'loss',
        'notes': entry.description,
        'pair': 'N/A',  # Default value
        'direction': 'N/A',  # Default value
        'setup_type': ', '.join(entry.confluences) if entry.confluences else None,
        'screenshot_url': entry.photo,
        'lessons_learned': entry.reflection_change,
        'mistakes': [entry.reflection_mistakes] if entry.reflection_mistakes else [],
        'emotions': entry.reflection_proud,
        'created_at': entry.created_at.isoformat()
    }
    
    result = supabase.table('journal_entries').insert(entry_dict).execute()
    
    logger.info(f"New journal entry created for user {entry_data.user_id}")
    
    # Return in the format frontend expects
    response_data = result.data[0] if result.data else entry_dict
    return {
        'id': response_data.get('id', entry.id),
        'user_id': response_data.get('user_id', entry.user_id),
        'win': entry.win,
        'confluences': entry.confluences,
        'description': entry.description,
        'photo': entry.photo,
        'reflection_change': entry.reflection_change,
        'reflection_mistakes': entry.reflection_mistakes,
        'reflection_proud': entry.reflection_proud,
        'created_at': response_data.get('created_at', entry.created_at.isoformat())
    }


@api_router.delete("/journal/{entry_id}")
async def delete_journal_entry(entry_id: str):
    """Delete a journal entry"""
    result = supabase.table('journal_entries').delete().eq('id', entry_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    return {"message": "Entry deleted"}

# ==================== SUBSCRIPTION ROUTES ====================

@api_router.post("/subscription/upgrade")
async def upgrade_subscription(data: SubscriptionUpgrade):
    """Upgrade user subscription"""
    if data.plan not in ['standard', 'pro']:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    result = supabase.table('users').select('id').eq('id', data.user_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    supabase.table('users').update({
        'subscription': data.plan
    }).eq('id', data.user_id).execute()
    
    logger.info(f"User {data.user_id} upgraded to {data.plan}")
    
    return {"message": f"Upgraded to {data.plan}", "subscription": data.plan}

# ==================== PROP FIRM ADS ====================

@api_router.get("/ads/propfirms")
async def get_prop_firm_ads():
    """Get prop firm advertisements"""
    return PROP_FIRM_ADS

# ==================== INIT DATA ROUTE ====================

@api_router.post("/init-lessons")
async def init_lessons():
    """Initialize lessons in database (for reference)"""
    return {"message": "Lessons are stored in memory", "count": len(LESSONS_DATA)}

# ==================== SECURITY MODELS ====================

class PasswordChangeRequest(BaseModel):
    user_id: str
    current_password: str
    new_password: str
    confirm_password: str

class TwoFactorEnableRequest(BaseModel):
    user_id: str
    email: EmailStr

class TwoFactorVerifyRequest(BaseModel):
    user_id: str
    otp_code: str

class TwoFactorDisableRequest(BaseModel):
    user_id: str
    password: str

class Session(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    device_info: str = "Unknown Device"
    ip_address: str = "Unknown"
    location: str = "Unknown"
    is_current: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SecurityLog(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    event_type: str  # password_change, login, logout, 2fa_enabled, 2fa_disabled, session_logout
    description: str
    ip_address: str = "Unknown"
    device_info: str = "Unknown"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TwoFactorSettings(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    is_enabled: bool = False
    backup_codes: List[str] = Field(default_factory=list)
    pending_otp: Optional[str] = None
    otp_expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ==================== SECURITY HELPER FUNCTIONS ====================

import secrets
import random
from datetime import timedelta

def generate_otp() -> str:
    """Generate a 6-digit OTP code"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def generate_backup_codes(count: int = 8) -> List[str]:
    """Generate backup codes for 2FA recovery"""
    return [secrets.token_hex(4).upper() for _ in range(count)]

async def log_security_event(user_id: str, event_type: str, description: str, ip_address: str = "Unknown", device_info: str = "Unknown"):
    """Log a security event - disabled until security_logs table is created"""
    logger.info(f"Security event: {event_type} for user {user_id} - {description}")

async def create_session(user_id: str, device_info: str = "Web Browser", ip_address: str = "Unknown", is_current: bool = True) -> str:
    """Create a new session for user - simplified for now"""
    return str(uuid.uuid4())

# ==================== SECURITY ROUTES ====================

@api_router.post("/security/change-password")
async def change_password(data: PasswordChangeRequest):
    """Change user password"""
    # Validate new password confirmation
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    
    # Validate password length
    if len(data.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    # Get user from Supabase
    result = supabase.table('users').select('*').eq('id', data.user_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user = result.data[0]
    
    # Verify current password
    if not verify_password(data.current_password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    # Check new password is different
    if verify_password(data.new_password, user['password_hash']):
        raise HTTPException(status_code=400, detail="New password must be different from current password")
    
    # Update password in Supabase
    new_hash = hash_password(data.new_password)
    supabase.table('users').update({
        'password_hash': new_hash
    }).eq('id', data.user_id).execute()
    
    # Log security event
    await log_security_event(
        user_id=data.user_id,
        event_type="password_change",
        description="Password was changed successfully"
    )
    
    logger.info(f"Password changed for user {data.user_id}")
    return {"message": "Password changed successfully"}

@api_router.post("/security/2fa/enable")
async def enable_2fa(data: TwoFactorEnableRequest):
    """Enable 2FA - sends OTP to email"""
    user_result = supabase.table('users').select('*').eq('id', data.user_id).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already enabled
    existing_2fa_result = supabase.table('two_factor').select('*').eq('user_id', data.user_id).execute()
    existing_2fa = existing_2fa_result.data[0] if existing_2fa_result.data else None
    if existing_2fa and existing_2fa.get('is_enabled'):
        raise HTTPException(status_code=400, detail="2FA is already enabled")
    
    # Generate OTP
    otp = generate_otp()
    otp_expires = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    # Store or update 2FA settings
    if existing_2fa:
        supabase.table('two_factor').update({
            'pending_otp': otp,
            'otp_expires_at': otp_expires.isoformat()
        }).eq('user_id', data.user_id).execute()
    else:
        backup_codes = generate_backup_codes()
        two_fa = TwoFactorSettings(
            user_id=data.user_id,
            is_enabled=False,
            backup_codes=backup_codes,
            pending_otp=otp,
            otp_expires_at=otp_expires
        )
        two_fa_dict = two_fa.model_dump()
        two_fa_dict['created_at'] = two_fa_dict['created_at'].isoformat()
        two_fa_dict['otp_expires_at'] = two_fa_dict['otp_expires_at'].isoformat() if two_fa_dict['otp_expires_at'] else None
        supabase.table('two_factor').insert(two_fa_dict).execute()
    
    # In production, send OTP via email. For now, return it (demo purposes)
    logger.info(f"2FA OTP generated for user {data.user_id}: {otp}")
    
    return {
        "message": "OTP sent to your email",
        "otp_demo": otp,  # Remove in production - only for demo
        "expires_in_minutes": 10
    }

@api_router.post("/security/2fa/verify")
async def verify_2fa(data: TwoFactorVerifyRequest):
    """Verify OTP to complete 2FA setup"""
    two_fa_result = supabase.table('two_factor').select('*').eq('user_id', data.user_id).execute()
    if not two_fa_result.data:
        raise HTTPException(status_code=404, detail="2FA setup not initiated")
    two_fa = two_fa_result.data[0]
    
    # Check if OTP expired
    if two_fa.get('otp_expires_at'):
        expires_at = datetime.fromisoformat(two_fa['otp_expires_at'].replace('Z', '+00:00')) if isinstance(two_fa['otp_expires_at'], str) else two_fa['otp_expires_at']
        if datetime.now(timezone.utc) > expires_at:
            raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")
    
    # Verify OTP
    if two_fa.get('pending_otp') != data.otp_code:
        raise HTTPException(status_code=400, detail="Invalid OTP code")
    
    # Enable 2FA
    supabase.table('two_factor').update({
        'is_enabled': True,
        'pending_otp': None,
        'otp_expires_at': None
    }).eq('user_id', data.user_id).execute()
    
    # Log security event
    await log_security_event(
        user_id=data.user_id,
        event_type="2fa_enabled",
        description="Two-factor authentication was enabled"
    )
    
    logger.info(f"2FA enabled for user {data.user_id}")
    return {
        "message": "2FA enabled successfully",
        "backup_codes": two_fa.get('backup_codes', [])
    }

@api_router.post("/security/2fa/disable")
async def disable_2fa(data: TwoFactorDisableRequest):
    """Disable 2FA with password verification"""
    user_result = supabase.table('users').select('*').eq('id', data.user_id).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_result.data[0]
    
    # Verify password
    if not verify_password(data.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # Check if 2FA exists
    two_fa_result = supabase.table('two_factor').select('*').eq('user_id', data.user_id).execute()
    two_fa = two_fa_result.data[0] if two_fa_result.data else None
    if not two_fa or not two_fa.get('is_enabled'):
        raise HTTPException(status_code=400, detail="2FA is not enabled")
    
    # Disable 2FA
    supabase.table('two_factor').update({
        'is_enabled': False
    }).eq('user_id', data.user_id).execute()
    
    # Log security event
    await log_security_event(
        user_id=data.user_id,
        event_type="2fa_disabled",
        description="Two-factor authentication was disabled"
    )
    
    logger.info(f"2FA disabled for user {data.user_id}")
    return {"message": "2FA disabled successfully"}

@api_router.get("/security/2fa/status/{user_id}")
async def get_2fa_status(user_id: str):
    """Get 2FA status for user"""
    two_fa_result = supabase.table('two_factor').select('*').eq('user_id', user_id).execute()
    if not two_fa_result.data:
        return {"is_enabled": False, "has_backup_codes": False}
    two_fa = two_fa_result.data[0]
    
    return {
        "is_enabled": two_fa.get('is_enabled', False),
        "has_backup_codes": len(two_fa.get('backup_codes', [])) > 0
    }

@api_router.get("/security/2fa/backup-codes/{user_id}")
async def get_backup_codes(user_id: str):
    """Get backup codes for 2FA recovery"""
    two_fa_result = supabase.table('two_factor').select('*').eq('user_id', user_id).execute()
    if not two_fa_result.data:
        raise HTTPException(status_code=404, detail="2FA not configured")
    two_fa = two_fa_result.data[0]
    
    return {"backup_codes": two_fa.get('backup_codes', [])}

@api_router.post("/security/2fa/regenerate-codes/{user_id}")
async def regenerate_backup_codes(user_id: str):
    """Regenerate backup codes"""
    two_fa_result = supabase.table('two_factor').select('*').eq('user_id', user_id).execute()
    if not two_fa_result.data:
        raise HTTPException(status_code=404, detail="2FA not configured")
    
    new_codes = generate_backup_codes()
    supabase.table('two_factor').update({
        'backup_codes': new_codes
    }).eq('user_id', user_id).execute()
    
    # Log security event
    await log_security_event(
        user_id=user_id,
        event_type="backup_codes_regenerated",
        description="2FA backup codes were regenerated"
    )
    
    return {"backup_codes": new_codes, "message": "Backup codes regenerated"}

@api_router.get("/security/sessions/{user_id}")
async def get_sessions(user_id: str):
    """Get all active sessions for user"""
    sessions_result = supabase.table('sessions').select('*').eq('user_id', user_id).order('last_active', desc=True).limit(100).execute()
    return sessions_result.data if sessions_result.data else []

@api_router.post("/security/sessions/create")
async def create_new_session(user_id: str, device_info: str = "Web Browser", ip_address: str = "Unknown"):
    """Create a new session (called during login)"""
    session_id = await create_session(user_id, device_info, ip_address, True)
    
    # Log security event
    await log_security_event(
        user_id=user_id,
        event_type="login",
        description=f"New login from {device_info}",
        ip_address=ip_address,
        device_info=device_info
    )
    
    return {"session_id": session_id}

@api_router.post("/security/sessions/logout-all/{user_id}")
async def logout_all_sessions(user_id: str):
    """Logout from all devices"""
    # Count sessions before deleting
    count_result = supabase.table('sessions').select('id', count='exact').eq('user_id', user_id).execute()
    deleted_count = count_result.count if count_result.count else len(count_result.data)
    
    # Delete all sessions
    supabase.table('sessions').delete().eq('user_id', user_id).execute()
    
    # Log security event
    await log_security_event(
        user_id=user_id,
        event_type="logout_all",
        description=f"Logged out from all {deleted_count} sessions"
    )
    
    logger.info(f"User {user_id} logged out from all sessions")
    return {"message": f"Logged out from {deleted_count} sessions"}

@api_router.delete("/security/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a specific session"""
    session_result = supabase.table('sessions').select('*').eq('id', session_id).execute()
    if not session_result.data:
        raise HTTPException(status_code=404, detail="Session not found")
    session = session_result.data[0]
    
    supabase.table('sessions').delete().eq('id', session_id).execute()
    
    # Log security event
    await log_security_event(
        user_id=session['user_id'],
        event_type="session_logout",
        description="Logged out from a specific session"
    )
    
    return {"message": "Session terminated"}

@api_router.get("/security/activity/{user_id}")
async def get_security_activity(user_id: str, limit: int = 50):
    """Get security activity log for user"""
    logs_result = supabase.table('security_logs').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
    return logs_result.data if logs_result.data else []

# ==================== CURRICULUM ROUTES (NEW LEARNING SYSTEM) ====================

from curriculum import (
    CURRICULUM_STRUCTURE,
    get_all_categories,
    get_category_by_id,
    generate_exercises_with_ai,
    generate_fallback_exercises
)

class ExerciseComplete(BaseModel):
    user_id: str
    exercise_id: str
    is_correct: bool

@api_router.get("/curriculum/tiers")
async def get_curriculum_tiers():
    """Get all curriculum tiers with categories"""
    result = []
    for tier_id, tier_data in CURRICULUM_STRUCTURE.items():
        result.append({
            "id": tier_id,
            "name": tier_data['name'],
            "order": tier_data['order'],
            "categories": tier_data['categories']
        })
    return sorted(result, key=lambda x: x['order'])

@api_router.get("/curriculum/categories")
async def get_categories():
    """Get all categories with metadata"""
    return get_all_categories()

@api_router.get("/curriculum/categories/{category_id}")
async def get_category(category_id: str):
    """Get a specific category"""
    category = get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@api_router.get("/curriculum/categories/{category_id}/levels")
async def get_category_levels(category_id: str, user_id: Optional[str] = None):
    """Get all levels for a category with user progress"""
    category = get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Get user progress and admin status if user_id provided
    user_progress = {}
    admin_mode = False
    if user_id:
        # Check if admin
        user_result = supabase.table('users').select('is_admin').eq('id', user_id).execute()
        if user_result.data:
            admin_mode = user_result.data[0].get('is_admin', False)
        
        result = supabase.table('user_progress').select('*').eq('user_id', user_id).eq('category_id', category_id).execute()
        if result.data:
            # Build levels dict from progress
            for prog in result.data:
                user_progress[str(prog.get('level', 1))] = {
                    'completed': prog.get('exercises_completed', 0)
                }
    
    levels = []
    for level_num in range(1, 11):
        level_key = str(level_num)
        level_progress = user_progress.get(level_key, {})
        completed_exercises = level_progress.get('completed', 0)
        
        # Admin users get everything unlocked for testing
        if admin_mode:
            is_unlocked = True
        else:
            # Level is unlocked if it's level 1 OR previous level has 10 completed
            is_unlocked = level_num == 1
            if level_num > 1:
                prev_level_progress = user_progress.get(str(level_num - 1), {})
                is_unlocked = prev_level_progress.get('completed', 0) >= 10
        
        levels.append({
            "level": level_num,
            "category_id": category_id,
            "total_exercises": 10,
            "completed_exercises": completed_exercises,
            "is_completed": completed_exercises >= 10,
            "is_unlocked": is_unlocked,
            "xp_per_exercise": 5 + (level_num * 2)
        })
    
    return levels

@api_router.get("/curriculum/categories/{category_id}/levels/{level}/intro")
async def get_level_intro(category_id: str, level: int):
    """Get the lesson introduction for a category and level"""
    intro = get_lesson_intro(category_id, level)
    return intro

@api_router.get("/curriculum/categories/{category_id}/lesson")
async def get_category_lesson_info(category_id: str):
    """Get the full lesson/book for a category"""
    lesson = get_category_lesson(category_id)
    return lesson

@api_router.get("/curriculum/categories/{category_id}/lesson/page/{page_number}")
async def get_category_lesson_page(category_id: str, page_number: int):
    """Get a specific page of the category lesson"""
    page = get_lesson_page(category_id, page_number)
    return page

@api_router.get("/curriculum/categories/{category_id}/levels/{level}/exercises")
async def get_level_exercises(category_id: str, level: int, user_id: Optional[str] = None):
    """Get exercises for a specific level - generates if not cached"""
    category = get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if level < 1 or level > 10:
        raise HTTPException(status_code=400, detail="Level must be between 1 and 10")
    
    # Check if exercises are cached in DB
    cache_key = f"{category_id}-level-{level}"
    cached_result = supabase.table('interactive_exercise_cache').select('*').eq('cache_key', cache_key).execute()
    
    if cached_result.data and cached_result.data[0].get('exercises'):
        exercises = cached_result.data[0]['exercises']
    else:
        # Generate exercises
        logger.info(f"Generating exercises for {category_id} level {level}")
        exercises = await generate_exercises_with_ai(category_id, category['name'], level)
        
        # Cache the exercises (upsert)
        cache_data = {
            "cache_key": cache_key,
            "category_id": category_id,
            "level": level,
            "exercises": exercises,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        if cached_result.data:
            supabase.table('interactive_exercise_cache').update(cache_data).eq('cache_key', cache_key).execute()
        else:
            supabase.table('interactive_exercise_cache').insert(cache_data).execute()
    
    # Add user completion status if user_id provided
    if user_id:
        progress_result = supabase.table('user_progress').select('*').eq('user_id', user_id).eq('category_id', category_id).eq('level', level).execute()
        completed_ids = []
        if progress_result.data:
            completed_ids = progress_result.data[0].get('completed_exercises', []) or []
        
        for ex in exercises:
            ex['is_completed'] = ex.get('id') in completed_ids
    
    return exercises

class ExerciseImageUpdate(BaseModel):
    exercise_id: str
    image_url: str

@api_router.put("/curriculum/exercises/{exercise_id}/image")
async def update_exercise_image(exercise_id: str, data: ExerciseImageUpdate):
    """Update the image URL for a specific exercise"""
    # Parse exercise ID: category-Llevel-Eexercise (e.g., candlesticks-L1-E1)
    parts = exercise_id.split('-')
    if len(parts) < 3:
        raise HTTPException(status_code=400, detail="Invalid exercise ID format")
    
    category_id = '-'.join(parts[:-2])
    level_part = parts[-2]
    exercise_part = parts[-1]
    
    if not level_part.startswith('L') or not exercise_part.startswith('E'):
        raise HTTPException(status_code=400, detail="Invalid exercise ID format")
    
    level = int(level_part[1:])
    exercise_num = int(exercise_part[1:])
    
    cache_key = f"{category_id}-level-{level}"
    
    # Get cached exercises
    cached_result = supabase.table('interactive_exercise_cache').select('*').eq('cache_key', cache_key).execute()
    if not cached_result.data or not cached_result.data[0].get('exercises'):
        raise HTTPException(status_code=404, detail="Exercises not found. Generate them first by accessing the level.")
    
    exercises = cached_result.data[0]['exercises']
    
    # Find and update the specific exercise
    updated = False
    for ex in exercises:
        if ex.get('id') == exercise_id or ex.get('exercise_number') == exercise_num:
            ex['image_url'] = data.image_url
            ex['custom_image'] = True
            updated = True
            break
    
    if not updated:
        raise HTTPException(status_code=404, detail=f"Exercise {exercise_id} not found")
    
    # Save back to database
    supabase.table('interactive_exercise_cache').update({
        'exercises': exercises,
        'updated_at': datetime.now(timezone.utc).isoformat()
    }).eq('cache_key', cache_key).execute()
    
    logger.info(f"Updated image for exercise {exercise_id}")
    return {"message": "Image updated successfully", "exercise_id": exercise_id, "image_url": data.image_url}

@api_router.get("/curriculum/exercises/{exercise_id}")
async def get_single_exercise(exercise_id: str):
    """Get a single exercise by ID"""
    parts = exercise_id.split('-')
    if len(parts) < 3:
        raise HTTPException(status_code=400, detail="Invalid exercise ID format")
    
    category_id = '-'.join(parts[:-2])
    level_part = parts[-2]
    
    if not level_part.startswith('L'):
        raise HTTPException(status_code=400, detail="Invalid exercise ID format")
    
    level = int(level_part[1:])
    cache_key = f"{category_id}-level-{level}"
    
    cached_result = supabase.table('interactive_exercise_cache').select('*').eq('cache_key', cache_key).execute()
    if not cached_result.data or not cached_result.data[0].get('exercises'):
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    for ex in cached_result.data[0]['exercises']:
        if ex.get('id') == exercise_id:
            return ex
    
    raise HTTPException(status_code=404, detail="Exercise not found")

@api_router.post("/curriculum/exercises/complete")
async def complete_exercise(data: ExerciseComplete):
    """Mark an exercise as complete and award XP"""
    # Parse exercise ID: category-Llevel-Eexercise
    parts = data.exercise_id.split('-')
    if len(parts) < 3:
        raise HTTPException(status_code=400, detail="Invalid exercise ID format")
    
    category_id = '-'.join(parts[:-2])  # Handle category IDs with hyphens
    level_part = parts[-2]  # e.g., "L1"
    
    if not level_part.startswith('L'):
        raise HTTPException(status_code=400, detail="Invalid exercise ID format")
    
    level = int(level_part[1:])
    
    # Get user from Supabase
    user_result = supabase.table('users').select('*').eq('id', data.user_id).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_result.data[0]
    
    # Get or create progress for this level
    progress_result = supabase.table('user_progress').select('*').eq('user_id', data.user_id).eq('category_id', category_id).eq('level', level).execute()
    
    if progress_result.data:
        progress = progress_result.data[0]
        exercises_completed = progress.get('exercises_completed', 0)
    else:
        # Create new progress record
        exercises_completed = 0
    
    # Calculate XP (only if correct)
    xp_reward = (5 + (level * 2)) if data.is_correct else 2  # Partial XP for wrong answers
    
    # Update exercises completed
    new_exercises_completed = exercises_completed + 1
    
    # Update or insert progress
    if progress_result.data:
        supabase.table('user_progress').update({
            'exercises_completed': new_exercises_completed,
            'xp_earned': progress.get('xp_earned', 0) + xp_reward,
            'updated_at': datetime.now(timezone.utc).isoformat()
        }).eq('id', progress['id']).execute()
    else:
        supabase.table('user_progress').insert({
            'user_id': data.user_id,
            'category_id': category_id,
            'level': level,
            'exercises_completed': new_exercises_completed,
            'xp_earned': xp_reward,
            'created_at': datetime.now(timezone.utc).isoformat()
        }).execute()
    
    # Update user XP
    new_xp = user['xp'] + xp_reward
    new_level = (new_xp // 100) + 1
    
    supabase.table('users').update({
        'xp': new_xp,
        'level': new_level
    }).eq('id', data.user_id).execute()
    
    logger.info(f"User {data.user_id} completed exercise {data.exercise_id}, XP: +{xp_reward}")
    
    return {
        "message": "Exercise completed!",
        "xp_gained": xp_reward,
        "total_xp": new_xp,
        "user_level": new_level,
        "level_completed": new_exercises_completed,
        "is_level_complete": new_exercises_completed >= 10,
        "is_correct": data.is_correct,
        "rank": calculate_rank(new_xp)
    }

@api_router.get("/curriculum/progress/{user_id}")
async def get_user_curriculum_progress(user_id: str):
    """Get overall curriculum progress for a user"""
    progress_result = supabase.table('user_progress').select('*').eq('user_id', user_id).execute()
    
    result = {}
    for doc in progress_result.data:
        category_id = doc['category_id']
        
        total_completed = doc.get('exercises_completed', 0)
        
        result[category_id] = {
            "category_id": category_id,
            "levels_progress": {str(doc.get('level', 1)): {'completed': total_completed}},
            "total_completed": total_completed,
            "total_exercises": 100,  # 10 levels × 10 exercises
            "completion_percentage": (total_completed / 100) * 100
        }
    
    return result

@api_router.get("/curriculum/progress/{user_id}/{category_id}")
async def get_category_progress(user_id: str, category_id: str):
    """Get progress for a specific category"""
    progress_result = supabase.table('user_progress').select('*').eq('user_id', user_id).eq('category_id', category_id).execute()
    
    if not progress_result.data:
        return {
            "category_id": category_id,
            "levels_progress": {},
            "total_completed": 0,
            "total_exercises": 100
        }
    
    # Build levels progress from all level records
    levels_progress = {}
    total_completed = 0
    for prog in progress_result.data:
        level_key = str(prog.get('level', 1))
        completed = prog.get('exercises_completed', 0)
        levels_progress[level_key] = {'completed': completed}
        total_completed += completed
    
    return {
        "category_id": category_id,
        "levels_progress": levels_progress,
        "total_completed": total_completed,
        "total_exercises": 100
    }


# ==================== REAL MARKET - DISCIPLINE ZONE ====================

# In-memory storage for active sessions (in production, use database)
active_replay_sessions = {}

class StartReplayRequest(BaseModel):
    user_id: str
    asset: str = "EURUSD"
    timeframe: str = "15m"

class MarkORBRequest(BaseModel):
    session_id: str
    high: float
    low: float

class EnterTradeRequest(BaseModel):
    session_id: str
    direction: str  # "BUY" or "SELL"
    entry_price: float
    stop_loss: float
    take_profit: Optional[float] = None

class CompleteTradeRequest(BaseModel):
    session_id: str
    exit_price: float
    emotion_before: str
    emotion_after: str
    rule_violation: bool
    violation_types: List[str] = []

@api_router.get("/real-market/assets")
async def get_available_assets():
    """Get list of available assets for replay"""
    return AVAILABLE_ASSETS

@api_router.post("/real-market/start-session")
async def start_replay_session(data: StartReplayRequest):
    """Start a new market replay session with specified timeframe"""
    # Generate candles for the session
    base_prices = {
        "EURUSD": 1.08,
        "GBPUSD": 1.26,
        "BTCUSD": 42000,
        "SPX500": 4800,
        "GOLD": 2000,
        "AAPL": 180
    }
    
    # Validate timeframe
    valid_timeframes = ["1m", "5m", "15m"]
    timeframe = data.timeframe if data.timeframe in valid_timeframes else "15m"
    
    base_price = base_prices.get(data.asset, 100)
    candles = generate_realistic_candles(100, base_price, timeframe)
    
    session = ReplaySession(
        user_id=data.user_id,
        asset=data.asset,
        timeframe=timeframe,
        candles=candles,
        current_candle_index=20
    )
    
    active_replay_sessions[session.id] = session
    
    # Return only visible candles
    visible_candles = candles[:session.current_candle_index]
    
    return {
        "session_id": session.id,
        "asset": data.asset,
        "timeframe": "15m",
        "candles": [c.model_dump() for c in visible_candles],
        "current_index": session.current_candle_index,
        "total_candles": len(candles),
        "orb_range": None,
        "active_trade": None
    }

@api_router.get("/real-market/session/{session_id}")
async def get_session_state(session_id: str):
    """Get current state of a replay session"""
    session = active_replay_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    visible_candles = session.candles[:session.current_candle_index]
    
    return {
        "session_id": session.id,
        "asset": session.asset,
        "timeframe": session.timeframe,
        "candles": [c.model_dump() for c in visible_candles],
        "current_index": session.current_candle_index,
        "total_candles": len(session.candles),
        "orb_range": session.orb_range.model_dump() if session.orb_range else None,
        "active_trade": session.active_trade.model_dump() if session.active_trade else None,
        "trades_completed": session.trades_completed
    }

@api_router.post("/real-market/advance-candle")
async def advance_candle(session_id: str):
    """Advance the market by one candle"""
    session = active_replay_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.current_candle_index >= len(session.candles):
        return {"message": "No more candles", "finished": True}
    
    session.current_candle_index += 1
    
    # Check if active trade hit stop or take profit
    trade_closed = None
    if session.active_trade:
        current_candle = session.candles[session.current_candle_index - 1]
        trade = session.active_trade
        
        if trade.direction == "BUY":
            # Check stop loss hit
            if current_candle.low <= trade.stop_loss:
                trade_closed = {"exit_price": trade.stop_loss, "reason": "stop_loss"}
            # Check take profit hit
            elif trade.take_profit and current_candle.high >= trade.take_profit:
                trade_closed = {"exit_price": trade.take_profit, "reason": "take_profit"}
        else:  # SELL
            if current_candle.high >= trade.stop_loss:
                trade_closed = {"exit_price": trade.stop_loss, "reason": "stop_loss"}
            elif trade.take_profit and current_candle.low <= trade.take_profit:
                trade_closed = {"exit_price": trade.take_profit, "reason": "take_profit"}
    
    visible_candles = session.candles[:session.current_candle_index]
    new_candle = session.candles[session.current_candle_index - 1]
    
    return {
        "new_candle": new_candle.model_dump(),
        "current_index": session.current_candle_index,
        "total_candles": len(session.candles),
        "trade_closed": trade_closed,
        "finished": session.current_candle_index >= len(session.candles)
    }

@api_router.post("/real-market/mark-orb")
async def mark_orb_range(data: MarkORBRequest):
    """Mark the Opening Range Breakout high and low"""
    session = active_replay_sessions.get(data.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.orb_range = ORBRange(
        high=data.high,
        low=data.low,
        marked_at_candle=session.current_candle_index
    )
    
    return {
        "message": "ORB range marked",
        "orb_range": session.orb_range.model_dump()
    }

@api_router.post("/real-market/enter-trade")
async def enter_trade(data: EnterTradeRequest):
    """Enter a trade in the replay session"""
    session = active_replay_sessions.get(data.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.active_trade:
        raise HTTPException(status_code=400, detail="Already have an active trade")
    
    if not session.orb_range:
        raise HTTPException(status_code=400, detail="Must mark ORB range before entering trade")
    
    # Validate entry
    violations = []
    if not data.stop_loss:
        violations.append("no_stop_loss")
    
    trade = TradeEntry(
        entry_price=data.entry_price,
        direction=data.direction,
        stop_loss=data.stop_loss,
        take_profit=data.take_profit,
        entry_candle=session.current_candle_index,
        orb_high=session.orb_range.high,
        orb_low=session.orb_range.low
    )
    
    # Check ORB rule violations
    entry_violations = validate_entry(trade, session.orb_range)
    violations.extend(entry_violations)
    
    session.active_trade = trade
    
    rr = calculate_risk_reward(
        data.entry_price, 
        data.stop_loss, 
        data.take_profit, 
        data.direction
    )
    
    return {
        "message": "Trade entered",
        "trade": trade.model_dump(),
        "risk_reward": rr,
        "violations": violations,
        "has_violations": len(violations) > 0
    }

@api_router.post("/real-market/close-trade")
async def close_trade(data: CompleteTradeRequest):
    """Close a trade and record the evaluation"""
    session = active_replay_sessions.get(data.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.active_trade:
        raise HTTPException(status_code=400, detail="No active trade to close")
    
    trade = session.active_trade
    
    # Calculate result
    rr = calculate_risk_reward(trade.entry_price, trade.stop_loss, trade.take_profit, trade.direction)
    result_r = calculate_result_in_r(trade.entry_price, data.exit_price, trade.stop_loss, trade.direction)
    
    # Create trade result
    trade_result = TradeResult(
        user_id=session.user_id,
        session_id=session.id,
        asset=session.asset,
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        timeframe=session.timeframe,
        orb_high=trade.orb_high,
        orb_low=trade.orb_low,
        entry_price=trade.entry_price,
        direction=trade.direction,
        stop_loss=trade.stop_loss,
        take_profit=trade.take_profit,
        exit_price=data.exit_price,
        risk_reward=rr,
        result_in_r=result_r,
        emotion_before=data.emotion_before,
        emotion_after=data.emotion_after,
        rule_violation=data.rule_violation,
        violation_types=data.violation_types
    )
    
    # Store in database
    try:
        supabase.table('real_market_trades').insert(trade_result.model_dump()).execute()
    except Exception as e:
        logger.warning(f"Could not save trade to database: {e}")
    
    # Update session
    session.active_trade = None
    session.trades_completed += 1
    if data.rule_violation:
        session.rule_violations += 1
    
    return {
        "message": "Trade closed and recorded",
        "trade_result": trade_result.model_dump(),
        "session_stats": {
            "trades_completed": session.trades_completed,
            "rule_violations": session.rule_violations
        }
    }

@api_router.get("/real-market/history/{user_id}")
async def get_trade_history(user_id: str, limit: int = 50):
    """Get user's trade history"""
    try:
        result = supabase.table('real_market_trades').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
        return result.data if result.data else []
    except Exception:
        return []

@api_router.get("/real-market/discipline-score/{user_id}")
async def get_discipline_score(user_id: str):
    """Calculate and return user's discipline metrics"""
    try:
        result = supabase.table('real_market_trades').select('*').eq('user_id', user_id).execute()
        trades = result.data if result.data else []
    except Exception:
        trades = []
    
    # Convert to TradeResult objects
    trade_objects = []
    for t in trades:
        try:
            trade_objects.append(TradeResult(**t))
        except:
            pass
    
    score = calculate_discipline_score(trade_objects)
    insights = generate_insights(trade_objects)
    
    return {
        "score": score.model_dump(),
        "insights": insights
    }

@api_router.delete("/real-market/session/{session_id}")
async def end_session(session_id: str):
    """End and cleanup a replay session"""
    if session_id in active_replay_sessions:
        del active_replay_sessions[session_id]
    return {"message": "Session ended"}


# ==================== ROOT & HEALTH ====================

@api_router.get("/")
async def root():
    return {"message": "TradeLingo API", "version": "1.0.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy"}

# ==================== SEED/ADMIN ENDPOINTS ====================

@api_router.post("/seed/test-user")
async def seed_test_user():
    """Create a test user for development (won't overwrite existing)"""
    existing = supabase.table('users').select('id').eq('email', 'demo@tradelingo.com').execute()
    
    if existing.data:
        return {
            "message": "Test user already exists",
            "email": "demo@tradelingo.com",
            "password": "demo1234",
            "user_id": existing.data[0]['id']
        }
    
    test_user = User(
        username="demo",
        email="demo@tradelingo.com",
        password_hash=hash_password("demo1234"),
        is_verified=True,  # Pre-verified for demo
        is_admin=False
    )
    
    user_dict = {
        'id': test_user.id,
        'username': test_user.username,
        'email': test_user.email,
        'password_hash': test_user.password_hash,
        'xp': test_user.xp,
        'level': test_user.level,
        'completed_lessons': test_user.completed_lessons,
        'subscription': test_user.subscription,
        'is_verified': test_user.is_verified,
        'is_admin': test_user.is_admin,
        'created_at': test_user.created_at.isoformat()
    }
    
    supabase.table('users').insert(user_dict).execute()
    
    return {
        "message": "Test user created successfully",
        "email": "demo@tradelingo.com",
        "password": "demo1234",
        "user_id": test_user.id
    }

@api_router.post("/seed/super-admin")
async def seed_super_admin():
    """Create or update the super admin account with full unrestricted access"""
    admin_email = "ricardomeme136@gmail.com"
    admin_password = "MHG_RSilva124_"
    
    existing = supabase.table('users').select('*').eq('email', admin_email).execute()
    
    if existing.data:
        # Update existing user to be super admin with pro subscription
        supabase.table('users').update({
            'password_hash': hash_password(admin_password),
            'is_admin': True,
            'is_verified': True,
            'subscription': 'pro'
        }).eq('email', admin_email).execute()
        
        return {
            "message": "Super admin updated successfully",
            "email": admin_email,
            "user_id": existing.data[0]['id'],
            "access": "FULL UNRESTRICTED ACCESS"
        }
    
    # Create new super admin
    admin_user = User(
        username="Ricardo_Admin",
        email=admin_email,
        password_hash=hash_password(admin_password),
        is_verified=True,
        is_admin=True,
        subscription="pro"  # Pro subscription for full access
    )
    
    user_dict = {
        'id': admin_user.id,
        'username': admin_user.username,
        'email': admin_user.email,
        'password_hash': admin_user.password_hash,
        'xp': 9999,  # High XP for admin
        'level': 100,  # High level for admin
        'completed_lessons': [],
        'subscription': 'pro',
        'is_verified': True,
        'is_admin': True,
        'created_at': admin_user.created_at.isoformat()
    }
    
    supabase.table('users').insert(user_dict).execute()
    
    return {
        "message": "Super admin created successfully",
        "email": admin_email,
        "user_id": admin_user.id,
        "access": "FULL UNRESTRICTED ACCESS"
    }

@api_router.get("/seed/status")
async def get_seed_status():
    """Check database status - useful for debugging"""
    users_result = supabase.table('users').select('id', count='exact').execute()
    journal_result = supabase.table('journal_entries').select('id', count='exact').execute()
    verified_result = supabase.table('users').select('id', count='exact').eq('is_verified', True).execute()
    test_user_result = supabase.table('users').select('id').eq('email', 'demo@tradelingo.com').execute()
    
    user_count = users_result.count if users_result.count else len(users_result.data)
    journal_count = journal_result.count if journal_result.count else len(journal_result.data)
    verified_count = verified_result.count if verified_result.count else len(verified_result.data)
    
    return {
        "status": "connected",
        "database": "supabase",
        "users_count": user_count,
        "verified_users_count": verified_count,
        "journal_entries_count": journal_count,
        "test_user_exists": len(test_user_result.data) > 0,
        "test_credentials": {
            "email": "demo@tradelingo.com",
            "password": "demo1234"
        } if user_count > 0 else None
    }

# ==================== ADMIN PANEL ENDPOINTS ====================

# Admin credentials from environment
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@tradelingo.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

@api_router.post("/admin/login")
async def admin_login(login_data: AdminLogin):
    """Admin login - separate from user auth"""
    # Check hardcoded admin credentials
    if login_data.email == ADMIN_EMAIL and login_data.password == ADMIN_PASSWORD:
        return {
            "success": True,
            "admin": True,
            "email": ADMIN_EMAIL
        }
    
    # Also check if user has is_admin flag
    result = supabase.table('users').select('*').eq('email', login_data.email).execute()
    if result.data:
        user = result.data[0]
        if user.get('is_admin', False):
            if verify_password(login_data.password, user['password_hash']):
                return {
                    "success": True,
                    "admin": True,
                    "email": user['email'],
                    "user_id": user['id']
                }
    
    raise HTTPException(status_code=401, detail="Invalid admin credentials")

@api_router.get("/admin/stats")
async def get_admin_stats():
    """Get admin dashboard statistics"""
    # Get counts using Supabase
    all_users = supabase.table('users').select('id, is_verified, subscription, created_at').execute()
    journal_result = supabase.table('journal_entries').select('id', count='exact').execute()
    
    users_data = all_users.data or []
    total_users = len(users_data)
    verified_users = len([u for u in users_data if u.get('is_verified')])
    unverified_users = total_users - verified_users
    
    # Users by subscription
    free_users = len([u for u in users_data if u.get('subscription') == 'free'])
    standard_users = len([u for u in users_data if u.get('subscription') == 'standard'])
    pro_users = len([u for u in users_data if u.get('subscription') == 'pro'])
    
    # Recent signups (last 7 days)
    week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    recent_signups = len([u for u in users_data if u.get('created_at', '') >= week_ago])
    
    # Journal entries
    total_journal_entries = journal_result.count if journal_result.count else len(journal_result.data)
    
    return {
        "users": {
            "total": total_users,
            "verified": verified_users,
            "unverified": unverified_users,
            "recent_signups_7d": recent_signups
        },
        "subscriptions": {
            "free": free_users,
            "standard": standard_users,
            "pro": pro_users
        },
        "activity": {
            "total_journal_entries": total_journal_entries
        }
    }

@api_router.get("/admin/users")
async def get_admin_users(
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
    verified_only: bool = False
):
    """Get list of users for admin panel"""
    offset = (page - 1) * limit
    
    # Build query
    query = supabase.table('users').select('id, username, email, xp, level, subscription, is_verified, is_admin, created_at', count='exact')
    
    if search:
        query = query.or_(f"email.ilike.%{search}%,username.ilike.%{search}%")
    
    if verified_only:
        query = query.eq('is_verified', True)
    
    result = query.order('created_at', desc=True).range(offset, offset + limit - 1).execute()
    
    users = result.data or []
    total = result.count if result.count else len(users)
    
    # Add rank to each user
    for user in users:
        user['rank'] = calculate_rank(user.get('xp', 0))
    
    return {
        "users": users,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }

@api_router.post("/admin/users/{user_id}/verify")
async def admin_verify_user(user_id: str):
    """Manually verify a user's email"""
    result = supabase.table('users').update({
        'is_verified': True,
        'verification_token': None,
        'verification_token_expires': None
    }).eq('id', user_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User verified successfully"}

@api_router.post("/admin/users/{user_id}/make-admin")
async def make_user_admin(user_id: str):
    """Grant admin privileges to a user"""
    result = supabase.table('users').update({
        'is_admin': True
    }).eq('id', user_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User is now an admin"}

@api_router.delete("/admin/users/{user_id}")
async def delete_user(user_id: str):
    """Delete a user"""
    # First delete their journal entries
    supabase.table('journal_entries').delete().eq('user_id', user_id).execute()
    
    # Then delete the user
    result = supabase.table('users').delete().eq('id', user_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}

# ==================== INTERACTIVE CHART EXERCISES ====================

from interactive_exercises import get_interactive_exercises, validate_click_answer

class InteractiveAnswerSubmit(BaseModel):
    user_id: str
    exercise_id: str
    clicked_price: float
    clicked_time: Optional[str] = None
    zone_high: Optional[float] = None  # For FVG drawing
    zone_low: Optional[float] = None   # For FVG drawing

@api_router.get("/interactive/exercises/{category_id}/level/{level}")
async def get_interactive_level_exercises(category_id: str, level: int, user_id: Optional[str] = None, refresh: bool = False):
    """Get interactive chart exercises for a category and level"""
    if level < 1 or level > 10:
        raise HTTPException(status_code=400, detail="Level must be between 1 and 10")
    
    # Check cache first (unless refresh=True)
    cache_key = f"interactive-{category_id}-level-{level}"
    
    if not refresh:
        cached_result = supabase.table('interactive_exercise_cache').select('*').eq('cache_key', cache_key).execute()
        if cached_result.data and cached_result.data[0].get("exercises"):
            exercises = cached_result.data[0]["exercises"]
        else:
            refresh = True  # Force generate if not cached
    
    if refresh:
        # Generate fresh exercises
        exercises = get_interactive_exercises(category_id, level)
        
        # Cache them
        cache_data = {
            "cache_key": cache_key,
            "category_id": category_id,
            "level": level,
            "exercises": exercises,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        # Upsert
        existing = supabase.table('interactive_exercise_cache').select('cache_key').eq('cache_key', cache_key).execute()
        if existing.data:
            supabase.table('interactive_exercise_cache').update(cache_data).eq('cache_key', cache_key).execute()
        else:
            supabase.table('interactive_exercise_cache').insert(cache_data).execute()
    
    # Add user progress if user_id provided
    if user_id:
        progress_result = supabase.table('user_progress').select('*').eq('user_id', user_id).eq('category_id', category_id).eq('level', level).execute()
        completed_count = 0
        if progress_result.data:
            completed_count = progress_result.data[0].get('exercises_completed', 0)
        
        for i, ex in enumerate(exercises):
            ex["is_completed"] = i < completed_count
    
    return exercises

@api_router.delete("/interactive/exercises/cache")
async def clear_interactive_cache():
    """Clear all interactive exercise cache - forces regeneration with latest config"""
    supabase.table('interactive_exercise_cache').delete().neq('cache_key', '').execute()
    return {"message": "Cache cleared. Exercises will regenerate with latest config."}

@api_router.post("/interactive/exercises/submit")
async def submit_interactive_answer(data: InteractiveAnswerSubmit):
    """Submit an answer for an interactive exercise"""
    import re
    
    # Parse exercise ID - format: category_id-L{level}-E{num}
    match = re.match(r'^(.+)-L(\d+)-E(\d+)$', data.exercise_id)
    if not match:
        raise HTTPException(status_code=400, detail=f"Invalid exercise ID format: {data.exercise_id}")
    
    category_id = match.group(1)
    level = int(match.group(2))
    
    # Get the exercise from cache
    cache_key = f"interactive-{category_id}-level-{level}"
    cached_result = supabase.table('interactive_exercise_cache').select('*').eq('cache_key', cache_key).execute()
    
    if not cached_result.data:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    cached = cached_result.data[0]
    exercise = next((e for e in cached["exercises"] if e["id"] == data.exercise_id), None)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Validate the answer
    result = validate_click_answer(
        exercise, 
        data.clicked_price, 
        data.clicked_time,
        zone_high=data.zone_high,
        zone_low=data.zone_low
    )
    
    # Get user
    user_result = supabase.table('users').select('*').eq('id', data.user_id).execute()
    if not user_result.data:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_result.data[0]
    
    xp_gained = 0
    if result["is_correct"]:
        # Calculate XP
        xp_per_exercise = 5 + (level * 2)
        xp_gained = xp_per_exercise
        
        # Update user progress
        progress_result = supabase.table('user_progress').select('*').eq('user_id', data.user_id).eq('category_id', category_id).eq('level', level).execute()
        
        if progress_result.data:
            progress = progress_result.data[0]
            new_completed = progress.get('exercises_completed', 0) + 1
            supabase.table('user_progress').update({
                'exercises_completed': new_completed,
                'xp_earned': progress.get('xp_earned', 0) + xp_gained,
                'updated_at': datetime.now(timezone.utc).isoformat()
            }).eq('id', progress['id']).execute()
        else:
            # Check if there's already a record for this user+category (different level)
            existing_result = supabase.table('user_progress').select('*').eq('user_id', data.user_id).eq('category_id', category_id).execute()
            if existing_result.data:
                # Update existing record
                existing = existing_result.data[0]
                supabase.table('user_progress').update({
                    'level': level,
                    'exercises_completed': existing.get('exercises_completed', 0) + 1,
                    'xp_earned': existing.get('xp_earned', 0) + xp_gained,
                    'updated_at': datetime.now(timezone.utc).isoformat()
                }).eq('id', existing['id']).execute()
            else:
                # Insert new record
                supabase.table('user_progress').insert({
                    'user_id': data.user_id,
                    'category_id': category_id,
                    'level': level,
                    'exercises_completed': 1,
                    'xp_earned': xp_gained,
                    'created_at': datetime.now(timezone.utc).isoformat()
                }).execute()
        
        # Update user XP
        new_xp = user['xp'] + xp_gained
        new_level = (new_xp // 100) + 1
        supabase.table('users').update({
            'xp': new_xp,
            'level': new_level
        }).eq('id', data.user_id).execute()
        
        user['xp'] = new_xp
        user['level'] = new_level
    
    return {
        **result,
        "xp_gained": xp_gained,
        "total_xp": user['xp'],
        "rank": calculate_rank(user['xp'])
    }

@api_router.get("/interactive/progress/{user_id}")
async def get_interactive_progress(user_id: str):
    """Get user's interactive exercise progress"""
    progress_result = supabase.table('user_progress').select('*').eq('user_id', user_id).execute()
    
    result = {}
    for doc in progress_result.data:
        category_id = doc['category_id']
        level = doc.get('level', 1)
        
        if category_id not in result:
            result[category_id] = {"levels": {}, "total_completed": 0}
        
        completed = doc.get('exercises_completed', 0)
        result[category_id]["levels"][str(level)] = {
            "completed": completed,
            "total": 10
        }
        result[category_id]["total_completed"] += completed
    
    return result

# Include router
    
    return result

# Include the router in the main app
app.include_router(api_router)

# Mount static files AFTER router so images are served at /api/static/images/
app.mount("/api/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Get CORS origins - if not set, allow all origins
cors_origins_str = os.environ.get('CORS_ORIGINS', '')
if cors_origins_str:
    cors_origins = cors_origins_str.split(',')
else:
    cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True if cors_origins != ["*"] else False,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== STARTUP: SEED TEST USER ====================

@app.on_event("startup")
async def startup_seed_data():
    """Seed a test user on startup if database is empty"""
    try:
        # Check if any users exist
        result = supabase.table('users').select('id', count='exact').limit(1).execute()
        user_count = result.count if result.count else len(result.data)
        
        if user_count == 0:
            # Create a default test user (pre-verified for demo)
            test_user = User(
                username="demo",
                email="demo@tradelingo.com",
                password_hash=hash_password("demo1234"),
                is_verified=True,  # Pre-verified for demo
                is_admin=False
            )
            
            user_dict = {
                'id': test_user.id,
                'username': test_user.username,
                'email': test_user.email,
                'password_hash': test_user.password_hash,
                'xp': test_user.xp,
                'level': test_user.level,
                'completed_lessons': test_user.completed_lessons,
                'subscription': test_user.subscription,
                'is_verified': test_user.is_verified,
                'is_admin': test_user.is_admin,
                'created_at': test_user.created_at.isoformat()
            }
            
            supabase.table('users').insert(user_dict).execute()
            logger.info("✅ Created default test user: demo@tradelingo.com / demo1234")
        else:
            logger.info(f"📊 Database has {user_count} existing users")
            
    except Exception as e:
        logger.error(f"Error seeding data: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    # Supabase client doesn't need explicit close
    logger.info("Shutting down TradeLingo API")

