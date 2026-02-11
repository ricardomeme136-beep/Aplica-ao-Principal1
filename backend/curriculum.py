"""
TradeLingo Curriculum Generator
Generates Duolingo-style trading education content using AI
"""
import os
import json
import uuid
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timezone
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from curriculum_data import CURRICULUM_DATA

load_dotenv()

# Categories organized by difficulty tier
CURRICULUM_STRUCTURE = {
    "beginner": {
        "name": "Beginner Foundations",
        "order": 1,
        "categories": [
            {
                "id": "candlesticks",
                "name": "Candlesticks",
                "description": "Master the language of price action through candlestick patterns",
                "icon": "🕯️",
                "color": "#FF6B6B",
                "order": 1
            },
            {
                "id": "market-structure",
                "name": "Market Structure",
                "description": "Understand how markets move through highs and lows",
                "icon": "📉",
                "color": "#4ECDC4",
                "order": 2
            },
            {
                "id": "liquidity",
                "name": "Liquidity",
                "description": "Discover where the money flows in the market",
                "icon": "💧",
                "color": "#45B7D1",
                "order": 3
            },
            {
                "id": "bos",
                "name": "Break of Structure",
                "description": "Identify trend continuation signals",
                "icon": "💥",
                "color": "#96CEB4",
                "order": 4
            },
            {
                "id": "choch",
                "name": "Change of Character",
                "description": "Spot potential trend reversals early",
                "icon": "🔄",
                "color": "#FFEAA7",
                "order": 5
            }
        ]
    },
    "intermediate": {
        "name": "Intermediate SMC",
        "order": 2,
        "categories": [
            {
                "id": "order-blocks",
                "name": "Order Blocks",
                "description": "Find institutional entry zones",
                "icon": "📦",
                "color": "#DDA0DD",
                "order": 6
            },
            {
                "id": "fvg",
                "name": "Fair Value Gaps",
                "description": "Identify price imbalances for entries",
                "icon": "📊",
                "color": "#98D8C8",
                "order": 7
            },
            {
                "id": "liquidity-sweeps",
                "name": "Liquidity Sweeps",
                "description": "Trade the smart money hunting patterns",
                "icon": "🎯",
                "color": "#F7DC6F",
                "order": 8
            },
            {
                "id": "premium-discount",
                "name": "Premium & Discount",
                "description": "Buy cheap, sell expensive zones",
                "icon": "💰",
                "color": "#82E0AA",
                "order": 9
            },
            {
                "id": "inducement",
                "name": "Inducement",
                "description": "Avoid retail traps set by institutions",
                "icon": "🪤",
                "color": "#F1948A",
                "order": 10
            }
        ]
    },
    "advanced": {
        "name": "Advanced Trading",
        "order": 3,
        "categories": [
            {
                "id": "multi-timeframe",
                "name": "Multi-Timeframe Analysis",
                "description": "Align multiple timeframes for precision",
                "icon": "⏰",
                "color": "#BB8FCE",
                "order": 11
            },
            {
                "id": "entry-models",
                "name": "SMC Entry Models",
                "description": "Professional entry techniques",
                "icon": "🎪",
                "color": "#85C1E9",
                "order": 12
            },
            {
                "id": "risk-management",
                "name": "Risk Management",
                "description": "Protect your capital like a pro",
                "icon": "🛡️",
                "color": "#F9E79F",
                "order": 13
            },
            {
                "id": "psychology",
                "name": "Trade Psychology",
                "description": "Master your trading mindset",
                "icon": "🧠",
                "color": "#D7BDE2",
                "order": 14
            }
        ]
    },
    "practice": {
        "name": "Chart Practice",
        "order": 4,
        "categories": [
            {
                "id": "chart_candlesticks",
                "name": "Candle OHLC",
                "description": "Practice identifying Open, High, Low, Close on real candles",
                "icon": "🕯️",
                "color": "#58CC02",
                "order": 15
            },
            {
                "id": "chart_market_structure",
                "name": "Swing Points",
                "description": "Find Swing Highs, Swing Lows, HH, HL, LH, LL",
                "icon": "📊",
                "color": "#FF6B6B",
                "order": 16
            },
            {
                "id": "chart_liquidity",
                "name": "Liquidity Zones",
                "description": "Identify Buy Side & Sell Side Liquidity",
                "icon": "💧",
                "color": "#45B7D1",
                "order": 17
            },
            {
                "id": "chart_bos",
                "name": "Break of Structure",
                "description": "Spot BOS continuation signals on charts",
                "icon": "💥",
                "color": "#96CEB4",
                "order": 18
            },
            {
                "id": "chart_choch",
                "name": "Change of Character",
                "description": "Identify CHoCH reversal points",
                "icon": "🔄",
                "color": "#FFEAA7",
                "order": 19
            },
            {
                "id": "chart_order_blocks",
                "name": "Order Blocks",
                "description": "Find institutional Order Block zones",
                "icon": "📦",
                "color": "#DDA0DD",
                "order": 20
            },
            {
                "id": "chart_fvg",
                "name": "Fair Value Gaps",
                "description": "Identify FVG imbalance zones",
                "icon": "📈",
                "color": "#98D8C8",
                "order": 21
            },
            {
                "id": "chart_premium_discount",
                "name": "Premium & Discount",
                "description": "Mark Premium and Discount zones",
                "icon": "💰",
                "color": "#82E0AA",
                "order": 22
            }
        ]
    }
}

# ============================================================
# 🖼️ IMAGENS DOS EXERCÍCIOS - EDITE AQUI!
# ============================================================
# Cada categoria tem 10 imagens (1 para cada exercício do level)
# Troque as URLs pelas suas próprias imagens!
# ============================================================

CHART_IMAGES = {
    # =====================================================
    # 🕯️ CANDLESTICKS - Level 1 (10 imagens)
    # =====================================================
    "candlesticks": [
        # Exercício 1 - Bullish Candle Basics
        "https://www.purple-trading.com/getmedia/1c5d4ca8-9a0f-40d7-961a-d575b7b8d0eb/candles-2-EN.png",
        # Exercício 2 - Bearish Candle Basics  
        "https://i.imgur.com/QBcvXjW.gif",
        # Exercício 3 - Candle Bodies
        "https://i.imgur.com/cC4iWtq.gif",
        # Exercício 4 - Candle Wicks
        "https://cdn.pixabay.com/photo/2016/11/27/21/42/stock-1863880_1280.jpg",
        # Exercício 5 - Doji Candles
        "https://cdn.pixabay.com/photo/2021/01/25/12/43/bitcoin-5948838_1280.jpg",
        # Exercício 6 - Pin Bars
        "https://cdn.pixabay.com/photo/2018/02/04/09/09/bitcoin-3129440_1280.jpg",
        # Exercício 7 - Engulfing Pattern
        "https://cdn.pixabay.com/photo/2017/03/17/10/29/chart-2151021_1280.png",
        # Exercício 8 - Momentum Candles
        "https://cdn.pixabay.com/photo/2018/08/08/10/19/chart-3592236_1280.jpg",
        # Exercício 9 - Reading Multiple Candles
        "https://cdn.pixabay.com/photo/2016/09/04/14/47/chart-1644118_1280.png",
        # Exercício 10 - Candle Psychology
        "https://cdn.pixabay.com/photo/2021/02/14/18/28/stock-6014940_1280.png",
    ],
    
    # =====================================================
    # 📈 MARKET STRUCTURE - Level 1 (10 imagens)
    # =====================================================
    "market-structure": [
        # Exercício 1 - Higher Highs
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        # Exercício 2 - Higher Lows
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        # Exercício 3 - Lower Highs
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        # Exercício 4 - Lower Lows
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        # Exercício 5 - Swing Points
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        # Exercício 6 - Bullish Structure
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        # Exercício 7 - Bearish Structure
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        # Exercício 8 - Structure Shifts
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        # Exercício 9 - Ranging Markets
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        # Exercício 10 - Structure Analysis
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 💧 LIQUIDITY - Level 1 (10 imagens)
    # =====================================================
    "liquidity": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 💥 BREAK OF STRUCTURE (BOS) - Level 1 (10 imagens)
    # =====================================================
    "bos": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 🔄 CHANGE OF CHARACTER (CHoCH) - Level 1 (10 imagens)
    # =====================================================
    "choch": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 📦 ORDER BLOCKS - Level 1 (10 imagens)
    # =====================================================
    "order-blocks": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 📊 FAIR VALUE GAPS (FVG) - Level 1 (10 imagens)
    # =====================================================
    "fvg": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 🎯 LIQUIDITY SWEEPS - Level 1 (10 imagens)
    # =====================================================
    "liquidity-sweeps": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 💰 PREMIUM & DISCOUNT - Level 1 (10 imagens)
    # =====================================================
    "premium-discount": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 🪤 INDUCEMENT - Level 1 (10 imagens)
    # =====================================================
    "inducement": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # ⏰ MULTI-TIMEFRAME - Level 1 (10 imagens)
    # =====================================================
    "multi-timeframe": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 🎪 ENTRY MODELS - Level 1 (10 imagens)
    # =====================================================
    "entry-models": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 🛡️ RISK MANAGEMENT - Level 1 (10 imagens)
    # =====================================================
    "risk-management": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 🧠 PSYCHOLOGY - Level 1 (10 imagens)
    # =====================================================
    "psychology": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ],
    
    # =====================================================
    # 🖼️ DEFAULT (usado quando categoria não tem imagens)
    # =====================================================
    "default": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
        "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
        "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
        "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
        "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
    ]
}

# Custom images storage - will be populated from database
CUSTOM_EXERCISE_IMAGES = {}

def get_category_prompt(category_id: str, category_name: str, level: int) -> str:
    """Generate the AI prompt for a specific category and level"""
    
    difficulty_descriptions = {
        1: "absolute beginner, no trading experience",
        2: "beginner, just learned basics",
        3: "beginner, can identify basic patterns",
        4: "beginner-intermediate transition",
        5: "intermediate, understands core concepts",
        6: "intermediate, can apply concepts",
        7: "intermediate-advanced transition",
        8: "advanced, complex scenarios",
        9: "advanced, real-world application",
        10: "expert level, mastery test"
    }
    
    content_focus = {
        "candlesticks": "bullish candles, bearish candles, wicks, bodies, indecision candles, momentum candles, rejection candles, doji, engulfing patterns, pin bars, and candle psychology",
        "market-structure": "higher highs, higher lows, lower highs, lower lows, swing points, trend identification, consolidation, ranging markets, and structure shifts",
        "liquidity": "buy-side liquidity, sell-side liquidity, stop hunts, liquidity pools, equal highs/lows, liquidity resting areas, and why price targets liquidity",
        "bos": "break of structure identification, bullish BOS, bearish BOS, valid vs invalid BOS, BOS confirmation, trading after BOS, and structure continuation",
        "choch": "change of character signals, trend reversal identification, CHoCH vs BOS differences, valid CHoCH criteria, early reversal entries, and market turning points",
        "order-blocks": "bullish order blocks, bearish order blocks, OB identification, valid OB criteria, OB zones, institutional footprints, and OB entry strategies",
        "fvg": "fair value gap identification, bullish FVG, bearish FVG, FVG as entry zones, gap fill probability, FVG and OB confluence, and imbalance trading",
        "liquidity-sweeps": "sweep identification, stop hunt patterns, liquidity grab reversals, sweep and reverse, fake breakouts, and institutional manipulation",
        "premium-discount": "premium zones, discount zones, equilibrium, Fibonacci application, optimal entry zones, and buy low sell high with SMC",
        "inducement": "inducement identification, retail traps, false signals, smart money manipulation, avoiding inducement, and patience in trading",
        "multi-timeframe": "HTF bias, MTF structure, LTF entries, timeframe alignment, top-down analysis, and confluence across timeframes",
        "entry-models": "optimal trade entry, risk entry, confirmation entry, breaker blocks, mitigation blocks, and professional entry techniques",
        "risk-management": "position sizing, risk-reward ratios, stop loss placement, take profit levels, account management, and protecting capital",
        "psychology": "trading emotions, discipline, patience, handling losses, overtrading, revenge trading, and developing a winning mindset"
    }
    
    return f"""You are an expert trading educator creating content for a Duolingo-style trading app.

Create exactly 10 exercises for:
CATEGORY: {category_name}
LEVEL: {level} of 10
DIFFICULTY: {difficulty_descriptions.get(level, 'intermediate')}

CONTENT FOCUS: {content_focus.get(category_id, 'Smart Money Concepts trading')}

For each exercise, provide a JSON object with these EXACT fields:
- exercise_number (1-10)
- title (short, catchy title)
- explanation (2-3 sentences, very simple beginner-friendly language)
- image_description (describe a trading chart that visually explains this concept)
- question (clear question testing understanding)
- answer_type (one of: "multiple_choice", "true_false")
- options (array of 4 options for multiple_choice, or ["True", "False"] for true_false)
- correct_answer (index 0-3 for multiple_choice, or 0/1 for true_false)
- feedback_correct (short positive reinforcement)
- feedback_wrong (brief explanation of the correct answer)

RULES:
- Use VERY simple language, explain any trading terms
- One concept per exercise
- Questions should test recognition, not memorization
- Make it feel like a game, not a textbook
- Progress difficulty within the 10 exercises
- Keep explanations under 50 words each

OUTPUT: Return ONLY a valid JSON array of 10 exercise objects, no other text."""


async def generate_exercises_with_ai(category_id: str, category_name: str, level: int) -> List[Dict]:
    """Generate exercises using AI"""
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
        
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            print(f"No API key found, using fallback exercises for {category_name} level {level}")
            return generate_fallback_exercises(category_id, category_name, level)
        
        chat = LlmChat(
            api_key=api_key,
            session_id=f"curriculum-{category_id}-{level}-{uuid.uuid4().hex[:8]}",
            system_message="You are an expert trading curriculum designer. Always respond with valid JSON only."
        ).with_model("openai", "gpt-4.1-mini")
        
        prompt = get_category_prompt(category_id, category_name, level)
        user_message = UserMessage(text=prompt)
        
        response = await chat.send_message(user_message)
        
        # Parse JSON response
        try:
            # Clean the response - remove markdown code blocks if present
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            cleaned = cleaned.strip()
            
            exercises = json.loads(cleaned)
            
            # Add metadata to each exercise
            for i, ex in enumerate(exercises):
                ex['id'] = f"{category_id}-L{level}-E{i+1}"
                ex['category_id'] = category_id
                ex['level'] = level
                ex['xp_reward'] = 5 + (level * 2)  # 7-25 XP based on level
                # Add placeholder image
                images = CHART_IMAGES.get(category_id, CHART_IMAGES['default'])
                ex['image_url'] = images[i % len(images)]
            
            return exercises
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error for {category_name} level {level}: {e}")
            return generate_fallback_exercises(category_id, category_name, level)
            
    except Exception as e:
        print(f"AI generation error for {category_name} level {level}: {e}")
        return generate_fallback_exercises(category_id, category_name, level)


def generate_fallback_exercises(category_id: str, category_name: str, level: int) -> List[Dict]:
    """Generate exercises using the easy-to-edit exercises_config.py file"""
    
    # PRIMEIRO: Tenta usar o arquivo exercises_config.py (fácil de editar)
    try:
        from exercises_config import get_exercises
        custom_exercises = get_exercises(category_id, level)
        if custom_exercises and len(custom_exercises) > 0:
            return custom_exercises
    except ImportError:
        pass  # Se não existir, usa o fallback antigo
    
    # FALLBACK: Usa o curriculum_data.py antigo
    exercises = []
    
    # Get data for this category and level from CURRICULUM_DATA
    category_data = CURRICULUM_DATA.get(category_id)
    
    if category_data and level in category_data:
        level_data = category_data[level]
    else:
        # Use candlesticks level 1 as default fallback
        level_data = CURRICULUM_DATA.get("candlesticks", {}).get(1, [])
    
    # Get image questions for this category and level
    from curriculum_data import IMAGE_QUESTIONS
    image_questions = IMAGE_QUESTIONS.get(category_id, {}).get(level, [])
    
    for i in range(10):
        exercise_num = i + 1
        
        # Alternating pattern: exercises 2, 4, 6, 8, 10 are image-based (5 image questions)
        is_image_question = (exercise_num % 2 == 0)
        
        if is_image_question and len(image_questions) >= (exercise_num // 2):
            # IMAGE-BASED QUESTION
            img_q_index = (exercise_num // 2) - 1
            img_data = image_questions[img_q_index]
            
            exercises.append({
                "id": f"{category_id}-L{level}-E{exercise_num}",
                "exercise_number": exercise_num,
                "category_id": category_id,
                "level": level,
                "title": img_data.get("title", f"Image Question {exercise_num}"),
                "explanation": img_data.get("explanation", "Identify the correct pattern"),
                "image_description": img_data.get("image_description", "Trading chart pattern"),
                "question": img_data.get("question", "Which image shows the correct pattern?"),
                "question_image": img_data.get("question_image"),  # Image for the question
                "answer_type": "image_choice",  # NEW TYPE
                "options": img_data.get("options", []),  # Array of image URLs
                "correct_answer": img_data.get("correct_answer", 0),
                "feedback_correct": img_data.get("feedback_correct", "Excellent! You identified it correctly! 🎯"),
                "feedback_wrong": img_data.get("feedback_wrong", "Not quite. Look at the pattern more carefully."),
                "xp_reward": 5 + (level * 2) + 2,  # Bonus XP for image questions
                "image_url": img_data.get("question_image", get_level_image(category_id, level, i))
            })
        else:
            # TEXT-BASED QUESTION
            text_q_index = i // 2 if is_image_question else i - (i // 2)
            if text_q_index < len(level_data):
                data = level_data[text_q_index]
                title = data[0]
                explanation = data[1]
                question = data[2]
                options = data[3]
                correct_answer = data[4] if len(data) > 4 else 1
            else:
                title = f"Exercise {exercise_num}"
                explanation = f"Level {level} concept explanation"
                question = f"Question {exercise_num} for level {level}?"
                options = ["Option A", "Option B", "Option C", "Option D"]
                correct_answer = 1
            
            exercises.append({
                "id": f"{category_id}-L{level}-E{exercise_num}",
                "exercise_number": exercise_num,
                "category_id": category_id,
                "level": level,
                "title": title,
                "explanation": explanation,
                "image_description": f"Trading chart showing {title.lower()} concept",
                "question": question,
                "answer_type": "multiple_choice",
                "options": options,
                "correct_answer": correct_answer,
                "feedback_correct": "Excellent! You're getting it! 🎯",
                "feedback_wrong": f"Not quite. {explanation}",
                "xp_reward": 5 + (level * 2),
                "image_url": get_level_image(category_id, level, i)
            })
    
    return exercises


def get_level_image(category_id: str, level: int, exercise_index: int) -> str:
    """Get image URL based on category, level, and exercise index"""
    images = CHART_IMAGES.get(category_id, CHART_IMAGES['default'])
    # Use level and exercise index to vary the image
    # This creates different images for different levels
    index = ((level - 1) * 3 + exercise_index) % len(images)
    return images[index]


def get_all_categories() -> List[Dict]:
    """Get flat list of all categories with metadata"""
    categories = []
    for tier_id, tier_data in CURRICULUM_STRUCTURE.items():
        for cat in tier_data['categories']:
            categories.append({
                **cat,
                "tier": tier_id,
                "tier_name": tier_data['name'],
                "tier_order": tier_data['order'],
                "total_levels": 10,
                "total_exercises": 100
            })
    return sorted(categories, key=lambda x: x['order'])


def get_category_by_id(category_id: str) -> Optional[Dict]:
    """Get a specific category by ID"""
    for cat in get_all_categories():
        if cat['id'] == category_id:
            return cat
    return None
