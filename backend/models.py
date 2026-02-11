"""
SQLAlchemy Models for TradeLingo
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    completed_lessons = Column(JSON, default=list)
    subscription = Column(String(20), default='free')  # free, standard, pro
    
    # Email verification fields
    is_verified = Column(Boolean, default=False, index=True)
    verification_token = Column(String(100), nullable=True)
    verification_token_expires = Column(DateTime(timezone=True), nullable=True)
    
    # Admin field
    is_admin = Column(Boolean, default=False)
    
    # Security fields
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(100), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    # Relationships
    journal_entries = relationship('JournalEntry', back_populates='user', cascade='all, delete-orphan')
    progress = relationship('UserProgress', back_populates='user', cascade='all, delete-orphan')

class JournalEntry(Base):
    __tablename__ = 'journal_entries'
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Trade details
    pair = Column(String(20), nullable=False)
    direction = Column(String(10), nullable=False)  # buy, sell
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    position_size = Column(Float, nullable=True)
    
    # Outcome
    outcome = Column(String(10), nullable=False)  # win, loss, breakeven
    pnl = Column(Float, nullable=True)
    pnl_percent = Column(Float, nullable=True)
    
    # Analysis
    setup_type = Column(String(50), nullable=True)
    timeframe = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
    emotions = Column(String(50), nullable=True)
    mistakes = Column(JSON, default=list)
    lessons_learned = Column(Text, nullable=True)
    
    # Images
    screenshot_url = Column(String(500), nullable=True)
    
    trade_date = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    # Relationships
    user = relationship('User', back_populates='journal_entries')

class UserProgress(Base):
    __tablename__ = 'user_progress'
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    category_id = Column(String(50), nullable=False, index=True)
    level = Column(Integer, default=1)
    exercises_completed = Column(Integer, default=0)
    total_exercises = Column(Integer, default=10)
    xp_earned = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    # Relationships
    user = relationship('User', back_populates='progress')

class InteractiveExerciseCache(Base):
    __tablename__ = 'interactive_exercise_cache'
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    cache_key = Column(String(100), unique=True, nullable=False, index=True)
    category_id = Column(String(50), nullable=False)
    level = Column(Integer, nullable=False)
    exercises = Column(JSON, default=list)
    generated_at = Column(DateTime(timezone=True), default=utc_now)
