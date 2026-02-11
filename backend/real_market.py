# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║              📈 REAL MARKET - Discipline Zone                                ║
# ║                                                                              ║
# ║  Training real execution, discipline, and emotional control                  ║
# ║  Profit is not the main metric. DISCIPLINE is.                              ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

import random
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

# ==================== MODELS ====================

class Candle(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: int = 0

class ORBRange(BaseModel):
    high: float
    low: float
    marked_at_candle: int

class TradeEntry(BaseModel):
    entry_price: float
    direction: str  # "BUY" or "SELL"
    stop_loss: float
    take_profit: Optional[float] = None
    entry_candle: int
    orb_high: float
    orb_low: float

class TradeResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    session_id: str
    asset: str
    date: str
    timeframe: str
    orb_high: float
    orb_low: float
    entry_price: float
    direction: str
    stop_loss: float
    take_profit: Optional[float]
    exit_price: float
    risk_reward: float
    result_in_r: float
    emotion_before: str
    emotion_after: str
    rule_violation: bool
    violation_types: List[str] = []
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ReplaySession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    asset: str
    timeframe: str
    candles: List[Candle]
    current_candle_index: int = 20  # Start with 20 candles visible
    orb_range: Optional[ORBRange] = None
    active_trade: Optional[TradeEntry] = None
    trades_completed: int = 0
    rule_violations: int = 0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class DisciplineScore(BaseModel):
    total_trades: int
    trades_with_stop: int
    trades_without_violations: int
    stop_usage_rate: float
    violation_rate: float
    discipline_score: float
    emotional_consistency_score: float
    most_common_violation: Optional[str]
    emotion_patterns: dict

# ==================== CANDLE GENERATION ====================

def generate_realistic_candles(num_candles: int = 100, base_price: float = 100.0, timeframe: str = "15m") -> List[Candle]:
    """Generate realistic looking candles with trends and volatility for different timeframes"""
    candles = []
    price = base_price
    trend = random.choice([-1, 1])
    
    # Adjust volatility based on timeframe (smaller timeframes = less movement per candle)
    timeframe_settings = {
        "1m": {"volatility": (0.001, 0.004), "trend_strength": (0.0002, 0.0008), "minutes": 1},
        "5m": {"volatility": (0.002, 0.008), "trend_strength": (0.0005, 0.0015), "minutes": 5},
        "15m": {"volatility": (0.005, 0.015), "trend_strength": (0.001, 0.003), "minutes": 15},
    }
    
    settings = timeframe_settings.get(timeframe, timeframe_settings["15m"])
    volatility = random.uniform(*settings["volatility"])
    trend_strength = random.uniform(*settings["trend_strength"])
    minutes_per_candle = settings["minutes"]
    
    start_time = datetime.now(timezone.utc) - timedelta(minutes=num_candles * minutes_per_candle)
    
    for i in range(num_candles):
        # Occasionally change trend
        if random.random() < 0.1:
            trend = -trend
            trend_strength = random.uniform(*settings["trend_strength"])
        
        # Calculate candle
        open_price = price
        
        # Add trend bias
        trend_move = price * trend_strength * trend
        
        # Random movement
        random_move = price * volatility * random.uniform(-1, 1)
        
        close_price = open_price + trend_move + random_move
        
        # High and low
        range_size = abs(close_price - open_price) + price * volatility * random.uniform(0.2, 0.8)
        
        if close_price > open_price:  # Bullish
            high_price = close_price + range_size * random.uniform(0.1, 0.5)
            low_price = open_price - range_size * random.uniform(0.1, 0.5)
        else:  # Bearish
            high_price = open_price + range_size * random.uniform(0.1, 0.5)
            low_price = close_price - range_size * random.uniform(0.1, 0.5)
        
        candle_time = start_time + timedelta(minutes=minutes_per_candle * i)
        
        # More decimal places for forex pairs (typically 4-5 decimals)
        decimal_places = 4 if base_price < 10 else 2
        
        candles.append(Candle(
            timestamp=candle_time.isoformat(),
            open=round(open_price, decimal_places),
            high=round(high_price, decimal_places),
            low=round(low_price, decimal_places),
            close=round(close_price, decimal_places),
            volume=random.randint(1000, 10000)
        ))
        
        price = close_price
    
    return candles

# ==================== ASSETS ====================

AVAILABLE_ASSETS = [
    {"id": "EURUSD", "name": "EUR/USD", "type": "forex"},
    {"id": "GBPUSD", "name": "GBP/USD", "type": "forex"},
    {"id": "BTCUSD", "name": "BTC/USD", "type": "crypto"},
    {"id": "SPX500", "name": "S&P 500", "type": "index"},
    {"id": "GOLD", "name": "Gold", "type": "commodity"},
    {"id": "AAPL", "name": "Apple Inc.", "type": "stock"},
]

# ==================== RULE VALIDATION ====================

def validate_entry(trade: TradeEntry, orb: ORBRange) -> List[str]:
    """Validate trade entry against ORB rules"""
    violations = []
    
    # Check if stop loss is set
    if not trade.stop_loss:
        violations.append("no_stop_loss")
    
    # Check if entry is within ORB logic
    if trade.direction == "BUY":
        # Buy should be above ORB high
        if trade.entry_price < orb.high:
            violations.append("entry_below_orb_high")
    else:
        # Sell should be below ORB low
        if trade.entry_price > orb.low:
            violations.append("entry_above_orb_low")
    
    return violations

def calculate_risk_reward(entry: float, stop: float, take_profit: Optional[float], direction: str) -> float:
    """Calculate risk-reward ratio"""
    if not take_profit:
        return 0.0
    
    if direction == "BUY":
        risk = abs(entry - stop)
        reward = abs(take_profit - entry)
    else:
        risk = abs(stop - entry)
        reward = abs(entry - take_profit)
    
    if risk == 0:
        return 0.0
    
    return round(reward / risk, 2)

def calculate_result_in_r(entry: float, exit_price: float, stop: float, direction: str) -> float:
    """Calculate trade result in R multiples"""
    if direction == "BUY":
        risk = abs(entry - stop)
        pnl = exit_price - entry
    else:
        risk = abs(stop - entry)
        pnl = entry - exit_price
    
    if risk == 0:
        return 0.0
    
    return round(pnl / risk, 2)

# ==================== DISCIPLINE SCORING ====================

def calculate_discipline_score(trades: List[TradeResult]) -> DisciplineScore:
    """Calculate discipline metrics from trade history"""
    if not trades:
        return DisciplineScore(
            total_trades=0,
            trades_with_stop=0,
            trades_without_violations=0,
            stop_usage_rate=0.0,
            violation_rate=0.0,
            discipline_score=0.0,
            emotional_consistency_score=0.0,
            most_common_violation=None,
            emotion_patterns={}
        )
    
    total = len(trades)
    with_stop = sum(1 for t in trades if t.stop_loss > 0)
    without_violations = sum(1 for t in trades if not t.rule_violation)
    
    # Count violations
    violation_counts = {}
    for t in trades:
        for v in t.violation_types:
            violation_counts[v] = violation_counts.get(v, 0) + 1
    
    most_common = max(violation_counts.keys(), key=lambda k: violation_counts[k]) if violation_counts else None
    
    # Emotion analysis
    emotion_before = {}
    emotion_after = {}
    emotion_changes = {"stable": 0, "worse": 0, "better": 0}
    
    emotion_order = ["neutral", "confident", "anxious", "frustrated"]
    
    for t in trades:
        emotion_before[t.emotion_before] = emotion_before.get(t.emotion_before, 0) + 1
        emotion_after[t.emotion_after] = emotion_after.get(t.emotion_after, 0) + 1
        
        # Track emotional stability
        if t.emotion_before == t.emotion_after:
            emotion_changes["stable"] += 1
        elif t.emotion_before in ["neutral", "confident"] and t.emotion_after in ["anxious", "frustrated"]:
            emotion_changes["worse"] += 1
        else:
            emotion_changes["better"] += 1
    
    # Calculate scores
    stop_rate = (with_stop / total) * 100 if total > 0 else 0
    violation_rate = ((total - without_violations) / total) * 100 if total > 0 else 0
    
    # Discipline score: weighted combination
    discipline_score = (
        (stop_rate * 0.4) +  # 40% weight on stop usage
        ((100 - violation_rate) * 0.4) +  # 40% weight on no violations
        (min(total, 10) * 2)  # 20% bonus for experience (max 20 points)
    )
    
    # Emotional consistency: stability percentage
    emotional_consistency = (emotion_changes["stable"] / total) * 100 if total > 0 else 0
    
    return DisciplineScore(
        total_trades=total,
        trades_with_stop=with_stop,
        trades_without_violations=without_violations,
        stop_usage_rate=round(stop_rate, 1),
        violation_rate=round(violation_rate, 1),
        discipline_score=round(min(discipline_score, 100), 1),
        emotional_consistency_score=round(emotional_consistency, 1),
        most_common_violation=most_common,
        emotion_patterns={
            "before": emotion_before,
            "after": emotion_after,
            "changes": emotion_changes
        }
    )

def generate_insights(trades: List[TradeResult]) -> List[str]:
    """Generate discipline-based insights from trade history"""
    insights = []
    
    if not trades:
        return ["Complete some trades to receive personalized insights."]
    
    # Analyze emotions vs results
    anxious_trades = [t for t in trades if t.emotion_before == "anxious"]
    if anxious_trades:
        anxious_losses = sum(1 for t in anxious_trades if t.result_in_r < 0)
        if len(anxious_trades) > 2 and anxious_losses / len(anxious_trades) > 0.6:
            insights.append("⚠️ Most of your losing trades happen when you feel anxious.")
    
    # Analyze rule compliance vs results
    compliant_trades = [t for t in trades if not t.rule_violation]
    if compliant_trades:
        compliant_wins = sum(1 for t in compliant_trades if t.result_in_r > 0)
        win_rate = compliant_wins / len(compliant_trades)
        if win_rate > 0.4:
            insights.append("✅ Trades where rules are respected show positive expectancy.")
    
    # Most common violation
    violation_counts = {}
    for t in trades:
        for v in t.violation_types:
            violation_counts[v] = violation_counts.get(v, 0) + 1
    
    if violation_counts:
        most_common = max(violation_counts.keys(), key=lambda k: violation_counts[k])
        violation_names = {
            "moved_stop": "Moving the stop loss",
            "no_stop_loss": "Trading without a stop loss",
            "entry_outside_plan": "Entry outside the plan",
            "overtrading": "Overtrading",
            "fomo": "FOMO entries"
        }
        insights.append(f"🔴 {violation_names.get(most_common, most_common)} is your most frequent violation.")
    
    # Emotional stability insight
    stable_trades = sum(1 for t in trades if t.emotion_before == t.emotion_after)
    if len(trades) > 3:
        stability_rate = stable_trades / len(trades)
        if stability_rate > 0.7:
            insights.append("😌 You maintain good emotional stability during trades.")
        elif stability_rate < 0.3:
            insights.append("😰 Your emotions fluctuate significantly during trades. Practice staying calm.")
    
    if not insights:
        insights.append("📊 Keep trading to build more data for personalized insights.")
    
    return insights

