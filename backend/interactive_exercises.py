"""
Interactive Chart Exercise System - SMC Edition
TradeLingo - Hands-on Trading Education with Repetition
"""
import uuid
import random
from typing import List, Dict, Optional

# ============================================================
# IMPORTAR CONFIG EDITÁVEL
# ============================================================
try:
    from interactive_config import (
        CANDLES_OHLC,
        SWING_SCENARIOS as CONFIG_SWING_SCENARIOS,
        LIQUIDITY_SCENARIOS as CONFIG_LIQUIDITY_SCENARIOS,
        BOS_SCENARIOS as CONFIG_BOS_SCENARIOS,
        CHOCH_SCENARIOS as CONFIG_CHOCH_SCENARIOS,
        ORDER_BLOCK_SCENARIOS as CONFIG_ORDER_BLOCK_SCENARIOS,
        FVG_SCENARIOS as CONFIG_FVG_SCENARIOS,
        PREMIUM_DISCOUNT_SCENARIOS as CONFIG_PREMIUM_DISCOUNT_SCENARIOS,
    )
    USE_CONFIG = True
except ImportError:
    USE_CONFIG = False

# ============================================================
# CHART SCENARIOS - Multiple examples for repetition learning
# ============================================================

# Different candle scenarios for OHLC practice (variety for repetition)
CANDLE_SCENARIOS = [
    # Bullish candles
    {"time": "2024-01-01", "open": 100.00, "high": 105.50, "low": 99.20, "close": 104.80, "type": "bullish"},
    {"time": "2024-01-01", "open": 98.50, "high": 103.20, "low": 97.80, "close": 102.50, "type": "bullish"},
    {"time": "2024-01-01", "open": 95.00, "high": 99.80, "low": 94.50, "close": 99.00, "type": "bullish"},
    {"time": "2024-01-01", "open": 102.00, "high": 108.50, "low": 101.20, "close": 107.80, "type": "bullish"},
    {"time": "2024-01-01", "open": 110.00, "high": 115.00, "low": 109.50, "close": 114.20, "type": "bullish"},
    # Bearish candles
    {"time": "2024-01-01", "open": 105.00, "high": 106.30, "low": 99.50, "close": 100.20, "type": "bearish"},
    {"time": "2024-01-01", "open": 112.00, "high": 113.50, "low": 107.00, "close": 108.00, "type": "bearish"},
    {"time": "2024-01-01", "open": 98.00, "high": 99.20, "low": 94.00, "close": 95.50, "type": "bearish"},
    {"time": "2024-01-01", "open": 120.00, "high": 121.00, "low": 115.50, "close": 116.20, "type": "bearish"},
    {"time": "2024-01-01", "open": 88.00, "high": 89.50, "low": 84.00, "close": 85.00, "type": "bearish"},
    # Doji candles
    {"time": "2024-01-01", "open": 100.00, "high": 103.00, "low": 97.00, "close": 100.10, "type": "doji"},
    {"time": "2024-01-01", "open": 95.00, "high": 98.50, "low": 92.00, "close": 95.20, "type": "doji"},
    # Pin bars
    {"time": "2024-01-01", "open": 100.00, "high": 100.80, "low": 95.00, "close": 100.50, "type": "pin_bar_bull"},
    {"time": "2024-01-01", "open": 100.00, "high": 105.00, "low": 99.20, "close": 99.50, "type": "pin_bar_bear"},
]

# Multi-candle scenarios for structure analysis
SWING_SCENARIOS = [
    {
        "name": "uptrend_swing",
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 102.00, "low": 99.50, "close": 101.50},
            {"time": "2024-01-02", "open": 101.50, "high": 104.00, "low": 101.00, "close": 103.50},
            {"time": "2024-01-03", "open": 103.50, "high": 106.00, "low": 103.00, "close": 105.50},  # Swing High
            {"time": "2024-01-04", "open": 105.50, "high": 106.00, "low": 102.50, "close": 103.00},
            {"time": "2024-01-05", "open": 103.00, "high": 103.50, "low": 101.00, "close": 101.50},  # Swing Low
            {"time": "2024-01-08", "open": 101.50, "high": 104.00, "low": 101.00, "close": 103.50},
            {"time": "2024-01-09", "open": 103.50, "high": 107.00, "low": 103.00, "close": 106.50},
        ],
        "swing_high_idx": 2,
        "swing_low_idx": 4
    },
    {
        "name": "downtrend_swing",
        "candles": [
            {"time": "2024-01-01", "open": 110.00, "high": 111.00, "low": 108.00, "close": 108.50},
            {"time": "2024-01-02", "open": 108.50, "high": 109.50, "low": 106.00, "close": 106.50},
            {"time": "2024-01-03", "open": 106.50, "high": 107.00, "low": 104.00, "close": 104.50},  # Swing Low
            {"time": "2024-01-04", "open": 104.50, "high": 107.50, "low": 104.00, "close": 107.00},
            {"time": "2024-01-05", "open": 107.00, "high": 108.50, "low": 106.50, "close": 108.00},  # Swing High
            {"time": "2024-01-08", "open": 108.00, "high": 108.50, "low": 105.00, "close": 105.50},
            {"time": "2024-01-09", "open": 105.50, "high": 106.00, "low": 102.00, "close": 102.50},
        ],
        "swing_high_idx": 4,
        "swing_low_idx": 2
    },
    {
        "name": "ranging_swing",
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 102.50, "low": 99.00, "close": 102.00},
            {"time": "2024-01-02", "open": 102.00, "high": 104.00, "low": 101.50, "close": 103.50},  # High
            {"time": "2024-01-03", "open": 103.50, "high": 104.50, "low": 101.00, "close": 101.50},
            {"time": "2024-01-04", "open": 101.50, "high": 102.00, "low": 99.00, "close": 99.50},   # Low
            {"time": "2024-01-05", "open": 99.50, "high": 102.50, "low": 99.00, "close": 102.00},
            {"time": "2024-01-08", "open": 102.00, "high": 105.00, "low": 101.50, "close": 104.50}, # High
            {"time": "2024-01-09", "open": 104.50, "high": 105.00, "low": 102.00, "close": 102.50},
        ],
        "swing_high_idx": 5,
        "swing_low_idx": 3
    }
]

# Liquidity scenarios
LIQUIDITY_SCENARIOS = [
    {
        "name": "buy_side_liquidity",
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 102.00, "low": 99.50, "close": 101.50},
            {"time": "2024-01-02", "open": 101.50, "high": 103.50, "low": 101.00, "close": 103.00},
            {"time": "2024-01-03", "open": 103.00, "high": 105.00, "low": 102.50, "close": 104.50},  # Equal highs - BSL
            {"time": "2024-01-04", "open": 104.50, "high": 105.00, "low": 103.00, "close": 103.50},  # Equal highs - BSL
            {"time": "2024-01-05", "open": 103.50, "high": 104.80, "low": 102.50, "close": 104.00},  # Equal highs - BSL
            {"time": "2024-01-08", "open": 104.00, "high": 107.00, "low": 103.50, "close": 106.50},  # Sweep!
        ],
        "liquidity_type": "buy_side",
        "liquidity_level": 105.00,
        "description": "Buy Side Liquidity (BSL) - Stop losses above equal highs"
    },
    {
        "name": "sell_side_liquidity",
        "candles": [
            {"time": "2024-01-01", "open": 105.00, "high": 106.00, "low": 103.50, "close": 104.00},
            {"time": "2024-01-02", "open": 104.00, "high": 105.00, "low": 102.00, "close": 102.50},
            {"time": "2024-01-03", "open": 102.50, "high": 103.50, "low": 100.00, "close": 100.50},  # Equal lows - SSL
            {"time": "2024-01-04", "open": 100.50, "high": 102.00, "low": 100.00, "close": 101.50},  # Equal lows - SSL
            {"time": "2024-01-05", "open": 101.50, "high": 102.50, "low": 100.20, "close": 101.00},  # Equal lows - SSL
            {"time": "2024-01-08", "open": 101.00, "high": 101.50, "low": 98.00, "close": 98.50},    # Sweep!
        ],
        "liquidity_type": "sell_side",
        "liquidity_level": 100.00,
        "description": "Sell Side Liquidity (SSL) - Stop losses below equal lows"
    },
    {
        "name": "double_top_bsl",
        "candles": [
            {"time": "2024-01-01", "open": 98.00, "high": 100.00, "low": 97.50, "close": 99.50},
            {"time": "2024-01-02", "open": 99.50, "high": 103.00, "low": 99.00, "close": 102.50},   # First top
            {"time": "2024-01-03", "open": 102.50, "high": 103.00, "low": 100.00, "close": 100.50},
            {"time": "2024-01-04", "open": 100.50, "high": 101.50, "low": 99.00, "close": 101.00},
            {"time": "2024-01-05", "open": 101.00, "high": 103.00, "low": 100.50, "close": 102.50}, # Second top (BSL)
            {"time": "2024-01-08", "open": 102.50, "high": 102.80, "low": 99.50, "close": 100.00},
        ],
        "liquidity_type": "buy_side",
        "liquidity_level": 103.00,
        "description": "Double Top - Buy Side Liquidity resting above"
    }
]

# BOS scenarios
BOS_SCENARIOS = [
    {
        "name": "bullish_bos",
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 102.00, "low": 99.50, "close": 101.50},
            {"time": "2024-01-02", "open": 101.50, "high": 104.00, "low": 101.00, "close": 103.50},  # Previous high
            {"time": "2024-01-03", "open": 103.50, "high": 104.00, "low": 101.00, "close": 101.50},
            {"time": "2024-01-04", "open": 101.50, "high": 102.50, "low": 100.50, "close": 102.00},
            {"time": "2024-01-05", "open": 102.00, "high": 105.50, "low": 101.80, "close": 105.00},  # BOS candle
        ],
        "bos_type": "bullish",
        "structure_level": 104.00,
        "bos_candle_idx": 4,
        "description": "Bullish BOS - Price breaks above previous swing high"
    },
    {
        "name": "bearish_bos",
        "candles": [
            {"time": "2024-01-01", "open": 105.00, "high": 106.00, "low": 104.00, "close": 104.50},
            {"time": "2024-01-02", "open": 104.50, "high": 105.50, "low": 102.00, "close": 102.50},  # Previous low
            {"time": "2024-01-03", "open": 102.50, "high": 104.50, "low": 102.00, "close": 104.00},
            {"time": "2024-01-04", "open": 104.00, "high": 105.00, "low": 103.00, "close": 103.50},
            {"time": "2024-01-05", "open": 103.50, "high": 104.00, "low": 100.50, "close": 101.00},  # BOS candle
        ],
        "bos_type": "bearish",
        "structure_level": 102.00,
        "bos_candle_idx": 4,
        "description": "Bearish BOS - Price breaks below previous swing low"
    }
]

# CHoCH scenarios
CHOCH_SCENARIOS = [
    {
        "name": "bullish_choch",
        "candles": [
            {"time": "2024-01-01", "open": 105.00, "high": 106.00, "low": 104.00, "close": 104.50},
            {"time": "2024-01-02", "open": 104.50, "high": 105.00, "low": 102.00, "close": 102.50},
            {"time": "2024-01-03", "open": 102.50, "high": 103.50, "low": 100.00, "close": 100.50},  # Lower low
            {"time": "2024-01-04", "open": 100.50, "high": 103.00, "low": 100.00, "close": 102.50},  # Last lower high
            {"time": "2024-01-05", "open": 102.50, "high": 104.50, "low": 102.00, "close": 104.00},  # CHoCH - breaks LH
        ],
        "choch_type": "bullish",
        "structure_level": 103.00,
        "choch_candle_idx": 4,
        "description": "Bullish CHoCH - Downtrend breaks, price makes higher high"
    },
    {
        "name": "bearish_choch",
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 102.00, "low": 99.50, "close": 101.50},
            {"time": "2024-01-02", "open": 101.50, "high": 104.00, "low": 101.00, "close": 103.50},
            {"time": "2024-01-03", "open": 103.50, "high": 106.00, "low": 103.00, "close": 105.50},  # Higher high
            {"time": "2024-01-04", "open": 105.50, "high": 106.00, "low": 103.50, "close": 104.00},  # Last HL
            {"time": "2024-01-05", "open": 104.00, "high": 104.50, "low": 102.50, "close": 103.00},  # CHoCH - breaks HL
        ],
        "choch_type": "bearish",
        "structure_level": 103.50,
        "choch_candle_idx": 4,
        "description": "Bearish CHoCH - Uptrend breaks, price makes lower low"
    }
]

# Order Block scenarios
ORDER_BLOCK_SCENARIOS = [
    {
        "name": "bullish_ob",
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 101.00, "low": 99.00, "close": 100.50},
            {"time": "2024-01-02", "open": 100.50, "high": 101.50, "low": 99.50, "close": 99.80},   # OB candle (last bearish)
            {"time": "2024-01-03", "open": 99.80, "high": 104.00, "low": 99.50, "close": 103.50},   # Displacement
            {"time": "2024-01-04", "open": 103.50, "high": 106.00, "low": 103.00, "close": 105.50},
            {"time": "2024-01-05", "open": 105.50, "high": 108.00, "low": 105.00, "close": 107.50},
        ],
        "ob_type": "bullish",
        "ob_candle_idx": 1,
        "ob_high": 101.50,
        "ob_low": 99.50,
        "description": "Bullish Order Block - Last bearish candle before strong move up"
    },
    {
        "name": "bearish_ob",
        "candles": [
            {"time": "2024-01-01", "open": 105.00, "high": 106.00, "low": 104.00, "close": 104.50},
            {"time": "2024-01-02", "open": 104.50, "high": 106.50, "low": 104.00, "close": 106.00},  # OB candle (last bullish)
            {"time": "2024-01-03", "open": 106.00, "high": 106.50, "low": 102.00, "close": 102.50},  # Displacement
            {"time": "2024-01-04", "open": 102.50, "high": 103.00, "low": 100.00, "close": 100.50},
            {"time": "2024-01-05", "open": 100.50, "high": 101.00, "low": 98.00, "close": 98.50},
        ],
        "ob_type": "bearish",
        "ob_candle_idx": 1,
        "ob_high": 106.50,
        "ob_low": 104.00,
        "description": "Bearish Order Block - Last bullish candle before strong move down"
    }
]

# FVG scenarios
FVG_SCENARIOS = [
    {
        "name": "bullish_fvg",
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 101.50, "low": 99.50, "close": 101.00},  # Candle 1
            {"time": "2024-01-02", "open": 101.00, "high": 105.00, "low": 100.80, "close": 104.80}, # Candle 2 (gap creator)
            {"time": "2024-01-03", "open": 104.80, "high": 107.00, "low": 103.50, "close": 106.50}, # Candle 3
        ],
        "fvg_type": "bullish",
        "fvg_high": 103.50,  # Candle 3 low
        "fvg_low": 101.50,   # Candle 1 high
        "description": "Bullish FVG - Gap between candle 1 high and candle 3 low"
    },
    {
        "name": "bearish_fvg",
        "candles": [
            {"time": "2024-01-01", "open": 106.00, "high": 107.00, "low": 105.00, "close": 105.50}, # Candle 1
            {"time": "2024-01-02", "open": 105.50, "high": 106.00, "low": 101.00, "close": 101.50}, # Candle 2 (gap creator)
            {"time": "2024-01-03", "open": 101.50, "high": 103.00, "low": 100.00, "close": 100.50}, # Candle 3
        ],
        "fvg_type": "bearish",
        "fvg_high": 105.00,  # Candle 1 low
        "fvg_low": 103.00,   # Candle 3 high
        "description": "Bearish FVG - Gap between candle 1 low and candle 3 high"
    }
]

# Premium/Discount scenarios
PREMIUM_DISCOUNT_SCENARIOS = [
    {
        "name": "premium_zone",
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 101.50, "low": 99.50, "close": 101.00},
            {"time": "2024-01-02", "open": 101.00, "high": 103.00, "low": 100.50, "close": 102.50},
            {"time": "2024-01-03", "open": 102.50, "high": 105.00, "low": 102.00, "close": 104.50},  # Swing High
            {"time": "2024-01-04", "open": 104.50, "high": 105.00, "low": 102.00, "close": 102.50},
            {"time": "2024-01-05", "open": 102.50, "high": 103.00, "low": 100.00, "close": 100.50},  # Swing Low
        ],
        "swing_high": 105.00,
        "swing_low": 100.00,
        "equilibrium": 102.50,
        "description": "Premium Zone is above equilibrium (50%), Discount Zone is below"
    }
]


# ============================================================
# EXERCISE GENERATORS BY CATEGORY
# ============================================================

def generate_candlestick_exercises(category_id: str, level: int) -> List[Dict]:
    """Generate OHLC identification exercises with repetition"""
    exercises = []
    targets = ["open", "close", "high", "low"]
    
    # Use config file if available, otherwise use built-in scenarios
    if USE_CONFIG:
        scenarios = CANDLES_OHLC.copy()
    else:
        scenarios = CANDLE_SCENARIOS.copy()
    
    random.shuffle(scenarios)
    
    for i in range(10):
        candle = scenarios[i % len(scenarios)]
        target = targets[i % len(targets)]
        
        # Determine correct price based on target
        correct_price = candle[target]
        
        # Create helpful instruction based on candle type
        is_bullish = candle["close"] > candle["open"]
        
        hints = []
        if target == "open":
            hints = [
                f"For {'bullish (green)' if is_bullish else 'bearish (red)'} candles, open is at the {'BOTTOM' if is_bullish else 'TOP'} of the body",
                "The open is where price started for this time period"
            ]
        elif target == "close":
            hints = [
                f"For {'bullish (green)' if is_bullish else 'bearish (red)'} candles, close is at the {'TOP' if is_bullish else 'BOTTOM'} of the body",
                "The close is where price ended for this time period"
            ]
        elif target == "high":
            hints = [
                "The high is at the TOP of the upper wick",
                "This is the highest price reached during this candle"
            ]
        elif target == "low":
            hints = [
                "The low is at the BOTTOM of the lower wick",
                "This is the lowest price reached during this candle"
            ]
        
        exercises.append({
            "id": f"{category_id}-L{level}-E{i+1}",
            "category_id": category_id,
            "level": level,
            "exercise_number": i + 1,
            "exercise_type": "identify_price",
            "title": f"Find the {target.upper()} Price",
            "instruction": f"Click on the {target.upper()} price of this {'bullish' if is_bullish else 'bearish'} candle.",
            "candles": [candle],
            "target_candle_index": 0,
            "target_part": target,
            "correct_answer": {
                "type": "price_level",
                "price": correct_price,
                "label": f"{target.title()} Price"
            },
            "tolerance": 1.0,
            "hints": hints,
            "explanation": f"The {target} price is ${correct_price:.2f}. {'For bullish candles, open < close.' if is_bullish else 'For bearish candles, open > close.'}",
            "xp_reward": 7 + level
        })
    
    return exercises


def generate_swing_exercises(category_id: str, level: int) -> List[Dict]:
    """Generate swing point identification exercises"""
    exercises = []
    
    # Use config if available
    scenarios = CONFIG_SWING_SCENARIOS if USE_CONFIG else SWING_SCENARIOS
    
    for i in range(10):
        scenario = scenarios[i % len(scenarios)]
        candles = scenario["candles"]
        
        # Alternate between swing high and swing low
        if i % 2 == 0:
            target = "swing_high"
            target_idx = scenario.get("swing_high_index", scenario.get("swing_high_idx", 2))
            target_price = scenario.get("swing_high_price", candles[target_idx]["high"])
            title = "Find the Swing High"
            instruction = "Click on the SWING HIGH - the highest point before price reversed down."
        else:
            target = "swing_low"
            target_idx = scenario.get("swing_low_index", scenario.get("swing_low_idx", 4))
            target_price = scenario.get("swing_low_price", candles[target_idx]["low"])
            title = "Find the Swing Low"
            instruction = "Click on the SWING LOW - the lowest point before price reversed up."
        
        exercises.append({
            "id": f"{category_id}-L{level}-E{i+1}",
            "category_id": category_id,
            "level": level,
            "exercise_number": i + 1,
            "exercise_type": "identify_swing",
            "title": title,
            "instruction": instruction,
            "candles": candles,
            "target_candle_index": target_idx,
            "target_part": "high" if target == "swing_high" else "low",
            "correct_answer": {
                "type": "swing_point",
                "price": target_price,
                "label": "Swing High" if target == "swing_high" else "Swing Low"
            },
            "tolerance": 1.0,
            "hints": [
                "A swing high has lower highs on BOTH sides",
                "A swing low has higher lows on BOTH sides",
                "These are key reversal points in market structure"
            ],
            "explanation": f"The {'swing high' if target == 'swing_high' else 'swing low'} is at ${target_price:.2f}. This is where price reversed direction.",
            "xp_reward": 10 + level
        })
    
    return exercises


def generate_liquidity_exercises(category_id: str, level: int) -> List[Dict]:
    """Generate liquidity zone identification exercises"""
    exercises = []
    
    # Use config if available
    scenarios = CONFIG_LIQUIDITY_SCENARIOS if USE_CONFIG else LIQUIDITY_SCENARIOS
    
    for i in range(10):
        scenario = scenarios[i % len(scenarios)]
        candles = scenario["candles"]
        
        if scenario["liquidity_type"] == "buy_side":
            title = "Find Buy Side Liquidity (BSL)"
            instruction = "Click on the BUY SIDE LIQUIDITY level - where stop losses are resting ABOVE equal highs."
        else:
            title = "Find Sell Side Liquidity (SSL)"
            instruction = "Click on the SELL SIDE LIQUIDITY level - where stop losses are resting BELOW equal lows."
        
        exercises.append({
            "id": f"{category_id}-L{level}-E{i+1}",
            "category_id": category_id,
            "level": level,
            "exercise_number": i + 1,
            "exercise_type": "identify_liquidity",
            "title": title,
            "instruction": instruction,
            "candles": candles,
            "correct_answer": {
                "type": "liquidity_zone",
                "price": scenario["liquidity_level"],
                "label": "BSL" if scenario["liquidity_type"] == "buy_side" else "SSL"
            },
            "tolerance": 1.5,
            "hints": [
                "BSL = Stop losses above equal highs (retail longs' stops)",
                "SSL = Stop losses below equal lows (retail shorts' stops)",
                "Smart money hunts these zones to fill large orders"
            ],
            "explanation": scenario["description"] + f" at ${scenario['liquidity_level']:.2f}",
            "xp_reward": 12 + level
        })
    
    return exercises


def generate_bos_exercises(category_id: str, level: int) -> List[Dict]:
    """Generate Break of Structure exercises"""
    exercises = []
    
    # Use config if available
    scenarios = CONFIG_BOS_SCENARIOS if USE_CONFIG else BOS_SCENARIOS
    
    for i in range(10):
        scenario = scenarios[i % len(scenarios)]
        candles = scenario["candles"]
        
        if scenario["bos_type"] == "bullish":
            title = "Find the Bullish BOS Level"
            instruction = "Click on the STRUCTURE LEVEL that price broke ABOVE to confirm bullish continuation."
        else:
            title = "Find the Bearish BOS Level"
            instruction = "Click on the STRUCTURE LEVEL that price broke BELOW to confirm bearish continuation."
        
        exercises.append({
            "id": f"{category_id}-L{level}-E{i+1}",
            "category_id": category_id,
            "level": level,
            "exercise_number": i + 1,
            "exercise_type": "identify_bos",
            "title": title,
            "instruction": instruction,
            "candles": candles,
            "correct_answer": {
                "type": "structure_break",
                "price": scenario["structure_level"],
                "label": f"{'Bullish' if scenario['bos_type'] == 'bullish' else 'Bearish'} BOS"
            },
            "tolerance": 1.5,
            "hints": [
                "BOS = Break of Structure",
                "Bullish BOS breaks ABOVE previous swing high",
                "Bearish BOS breaks BELOW previous swing low",
                "BOS confirms trend continuation"
            ],
            "explanation": scenario["description"] + f" at ${scenario['structure_level']:.2f}",
            "xp_reward": 13 + level
        })
    
    return exercises


def generate_choch_exercises(category_id: str, level: int) -> List[Dict]:
    """Generate Change of Character exercises"""
    exercises = []
    
    # Use config if available
    scenarios = CONFIG_CHOCH_SCENARIOS if USE_CONFIG else CHOCH_SCENARIOS
    
    for i in range(10):
        scenario = scenarios[i % len(scenarios)]
        candles = scenario["candles"]
        
        if scenario["choch_type"] == "bullish":
            title = "Find the Bullish CHoCH Level"
            instruction = "Click where price broke structure to signal BULLISH reversal (broke above last lower high)."
        else:
            title = "Find the Bearish CHoCH Level"
            instruction = "Click where price broke structure to signal BEARISH reversal (broke below last higher low)."
        
        exercises.append({
            "id": f"{category_id}-L{level}-E{i+1}",
            "category_id": category_id,
            "level": level,
            "exercise_number": i + 1,
            "exercise_type": "identify_choch",
            "title": title,
            "instruction": instruction,
            "candles": candles,
            "correct_answer": {
                "type": "character_change",
                "price": scenario["structure_level"],
                "label": f"{'Bullish' if scenario['choch_type'] == 'bullish' else 'Bearish'} CHoCH"
            },
            "tolerance": 1.5,
            "hints": [
                "CHoCH = Change of Character (trend reversal)",
                "Bullish CHoCH: Downtrend ends, breaks last lower high",
                "Bearish CHoCH: Uptrend ends, breaks last higher low",
                "CHoCH is the FIRST sign of trend reversal"
            ],
            "explanation": scenario["description"] + f" at ${scenario['structure_level']:.2f}",
            "xp_reward": 14 + level
        })
    
    return exercises


def generate_order_block_exercises(category_id: str, level: int) -> List[Dict]:
    """Generate Order Block identification exercises"""
    exercises = []
    
    # Use config if available
    scenarios = CONFIG_ORDER_BLOCK_SCENARIOS if USE_CONFIG else ORDER_BLOCK_SCENARIOS
    
    for i in range(10):
        scenario = scenarios[i % len(scenarios)]
        candles = scenario["candles"]
        
        if scenario["ob_type"] == "bullish":
            title = "Find the Bullish Order Block"
            instruction = "Click on the ORDER BLOCK zone - the last BEARISH candle before the strong move UP."
        else:
            title = "Find the Bearish Order Block"
            instruction = "Click on the ORDER BLOCK zone - the last BULLISH candle before the strong move DOWN."
        
        # Use midpoint of OB for answer
        ob_midpoint = (scenario["ob_high"] + scenario["ob_low"]) / 2
        
        exercises.append({
            "id": f"{category_id}-L{level}-E{i+1}",
            "category_id": category_id,
            "level": level,
            "exercise_number": i + 1,
            "exercise_type": "identify_ob",
            "title": title,
            "instruction": instruction,
            "candles": candles,
            "correct_answer": {
                "type": "order_block",
                "price": ob_midpoint,
                "price_high": scenario["ob_high"],
                "price_low": scenario["ob_low"],
                "label": f"{'Bullish' if scenario['ob_type'] == 'bullish' else 'Bearish'} OB"
            },
            "tolerance": 2.0,
            "hints": [
                "Order Block = Last opposing candle before displacement",
                "Bullish OB: Last RED candle before big GREEN move",
                "Bearish OB: Last GREEN candle before big RED move",
                "Price often returns to test OB zones"
            ],
            "explanation": scenario["description"] + f" Zone: ${scenario['ob_low']:.2f} - ${scenario['ob_high']:.2f}",
            "xp_reward": 15 + level
        })
    
    return exercises


def generate_fvg_exercises(category_id: str, level: int) -> List[Dict]:
    """Generate Fair Value Gap identification exercises"""
    exercises = []
    
    # Use config if available
    scenarios = CONFIG_FVG_SCENARIOS if USE_CONFIG else FVG_SCENARIOS
    
    for i in range(10):
        scenario = scenarios[i % len(scenarios)]
        candles = scenario["candles"]
        
        if scenario["fvg_type"] == "bullish":
            title = "Find the Bullish FVG"
            instruction = "Click INSIDE the Fair Value Gap - the price GAP between candle 1's high and candle 3's low."
        else:
            title = "Find the Bearish FVG"
            instruction = "Click INSIDE the Fair Value Gap - the price GAP between candle 1's low and candle 3's high."
        
        # Use midpoint of FVG for answer
        fvg_midpoint = (scenario["fvg_high"] + scenario["fvg_low"]) / 2
        
        exercises.append({
            "id": f"{category_id}-L{level}-E{i+1}",
            "category_id": category_id,
            "level": level,
            "exercise_number": i + 1,
            "exercise_type": "identify_fvg",
            "title": title,
            "instruction": instruction,
            "candles": candles,
            "correct_answer": {
                "type": "fvg",
                "price": fvg_midpoint,
                "price_high": scenario["fvg_high"],
                "price_low": scenario["fvg_low"],
                "label": f"{'Bullish' if scenario['fvg_type'] == 'bullish' else 'Bearish'} FVG"
            },
            "tolerance": 1.5,
            "hints": [
                "FVG = Fair Value Gap (Imbalance)",
                "Created by a strong candle that leaves a gap",
                "Gap is between wick of candle 1 and wick of candle 3",
                "Price often returns to 'fill' these gaps"
            ],
            "explanation": scenario["description"] + f" Gap: ${scenario['fvg_low']:.2f} - ${scenario['fvg_high']:.2f}",
            "xp_reward": 15 + level
        })
    
    return exercises


def generate_premium_discount_exercises(category_id: str, level: int) -> List[Dict]:
    """Generate Premium/Discount zone exercises"""
    exercises = []
    
    # Use config if available
    scenarios = CONFIG_PREMIUM_DISCOUNT_SCENARIOS if USE_CONFIG else PREMIUM_DISCOUNT_SCENARIOS
    
    for i in range(10):
        scenario = scenarios[0]  # Use the same scenario with different questions
        candles = scenario["candles"]
        
        equilibrium = scenario["equilibrium"]
        
        if i % 2 == 0:
            title = "Find the Equilibrium (50%)"
            instruction = "Click on the EQUILIBRIUM level - the 50% point between swing high and swing low."
            target_price = equilibrium
            label = "Equilibrium"
        else:
            title = "Is this Premium or Discount?"
            if i % 4 == 1:
                instruction = "Click in the PREMIUM zone - the area ABOVE equilibrium (expensive to buy)."
                target_price = (scenario["swing_high"] + equilibrium) / 2
                label = "Premium Zone"
            else:
                instruction = "Click in the DISCOUNT zone - the area BELOW equilibrium (cheap to buy)."
                target_price = (scenario["swing_low"] + equilibrium) / 2
                label = "Discount Zone"
        
        exercises.append({
            "id": f"{category_id}-L{level}-E{i+1}",
            "category_id": category_id,
            "level": level,
            "exercise_number": i + 1,
            "exercise_type": "identify_zone",
            "title": title,
            "instruction": instruction,
            "candles": candles,
            "correct_answer": {
                "type": "zone",
                "price": target_price,
                "label": label
            },
            "tolerance": 2.0,
            "hints": [
                "Premium = Above 50% (expensive)",
                "Discount = Below 50% (cheap)",
                "Smart money buys in discount, sells in premium",
                "Equilibrium = (Swing High + Swing Low) / 2"
            ],
            "explanation": f"Equilibrium is at ${equilibrium:.2f}. Premium is above, Discount is below.",
            "xp_reward": 12 + level
        })
    
    return exercises


# ============================================================
# MAIN GENERATOR
# ============================================================

def get_interactive_exercises(category_id: str, level: int) -> List[Dict]:
    """Get interactive exercises for a category and level"""
    
    # Map categories to generators
    generators = {
        "chart_candlesticks": generate_candlestick_exercises,
        "chart_market_structure": generate_swing_exercises,
        "chart_liquidity": generate_liquidity_exercises,
        "chart_bos": generate_bos_exercises,
        "chart_choch": generate_choch_exercises,
        "chart_order_blocks": generate_order_block_exercises,
        "chart_fvg": generate_fvg_exercises,
        "chart_premium_discount": generate_premium_discount_exercises,
        # Legacy support
        "chart_practice": generate_candlestick_exercises,
    }
    
    generator = generators.get(category_id, generate_candlestick_exercises)
    return generator(category_id, level)


def validate_click_answer(exercise: Dict, clicked_price: float, clicked_time: Optional[str] = None, zone_high: Optional[float] = None, zone_low: Optional[float] = None) -> Dict:
    """Validate user's click answer or drawn zone"""
    correct = exercise["correct_answer"]
    tolerance = exercise.get("tolerance", 1.0)
    
    # Handle zone drawing (for FVG exercises)
    if zone_high is not None and zone_low is not None and "price_high" in correct and "price_low" in correct:
        # Check zone overlap
        correct_high = correct["price_high"]
        correct_low = correct["price_low"]
        
        # Calculate overlap percentage
        overlap_top = min(zone_high, correct_high)
        overlap_bottom = max(zone_low, correct_low)
        overlap = max(0, overlap_top - overlap_bottom)
        
        correct_zone_size = correct_high - correct_low
        user_zone_size = zone_high - zone_low
        
        # Calculate accuracy based on overlap
        if overlap > 0:
            overlap_ratio = overlap / correct_zone_size
            size_ratio = min(user_zone_size, correct_zone_size) / max(user_zone_size, correct_zone_size)
            accuracy = (overlap_ratio * 0.7 + size_ratio * 0.3) * 100
            is_correct = accuracy >= 50  # 50% overlap = correct
        else:
            accuracy = 0
            is_correct = False
        
        target_price = (correct_high + correct_low) / 2
        
        if is_correct:
            feedback = f"✅ Great zone! The {correct.get('label', 'FVG')} is ${correct_low:.2f} - ${correct_high:.2f}"
        else:
            feedback = f"❌ Not quite. The {correct.get('label', 'FVG')} is ${correct_low:.2f} - ${correct_high:.2f}. You drew ${zone_low:.2f} - ${zone_high:.2f}"
        
        return {
            "is_correct": is_correct,
            "feedback": feedback,
            "correct_price": target_price,
            "clicked_price": clicked_price,
            "accuracy": round(accuracy, 1),
            "explanation": exercise.get("explanation", "")
        }
    
    # Get target price (handle zones with high/low for click mode)
    if "price_high" in correct and "price_low" in correct:
        # For zones (OB, FVG), check if click is within the zone
        if correct["price_low"] <= clicked_price <= correct["price_high"]:
            is_correct = True
            accuracy = 100.0
        else:
            # Calculate distance from zone
            target_price = (correct["price_high"] + correct["price_low"]) / 2
            price_diff = abs(clicked_price - target_price)
            zone_size = correct["price_high"] - correct["price_low"]
            is_correct = price_diff <= (zone_size / 2 + tolerance)
            accuracy = max(0, 100 - (price_diff / target_price * 100)) if not is_correct else 100.0
    else:
        target_price = correct.get("price", 0)
        price_diff = abs(clicked_price - target_price)
        price_diff_percent = (price_diff / target_price) * 100 if target_price else 0
        is_correct = price_diff_percent <= tolerance
        accuracy = max(0, 100 - (price_diff_percent / tolerance * 100)) if is_correct else 0
    
    if is_correct:
        feedback = f"✅ Correct! The {correct.get('label', 'answer')} is ${correct.get('price', target_price):.2f}"
    else:
        feedback = f"❌ Not quite. The {correct.get('label', 'answer')} is ${correct.get('price', target_price):.2f}. You clicked ${clicked_price:.2f}"
    
    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "correct_price": correct.get("price", target_price),
        "clicked_price": clicked_price,
        "accuracy": round(accuracy, 1),
        "explanation": exercise.get("explanation", "")
    }
