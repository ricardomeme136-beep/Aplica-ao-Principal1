# TradeLingo - Trading Education Platform PRD

## Original Problem Statement
1. Pull code from GitHub repository
2. Add book/lesson at top of categories with levels below
3. Add password visibility toggle to login form
4. **NEW: Real Market Discipline Zone with ORB Execution Training**

## Architecture
- **Frontend**: React 19 with CRACO, TailwindCSS, shadcn/ui components
- **Backend**: FastAPI with Supabase PostgreSQL
- **Database**: Supabase PostgreSQL (cloud-hosted)

## What's Been Implemented (Jan 28, 2026)

### Real Market Discipline Zone ✅
- **ORB Execution Training**: Candle-by-candle market replay
- **6 Trading Assets**: EUR/USD, GBP/USD, BTC/USD, S&P 500, Gold, Apple Inc.
- **Manual ORB Marking**: User marks Opening Range Breakout high/low
- **Trade Entry System**: 
  - BUY/SELL direction selection
  - Required Stop Loss before entry
  - Optional Take Profit
  - Entry price specification
- **Rule Enforcement**:
  - Entry without stop loss = violation
  - Moving stop after entry = violation flagged
  - Entry outside ORB logic = detectable
- **Trade Evaluation Modal**:
  - Emotion BEFORE trade (Neutral, Anxious, Frustrated, Confident)
  - Emotion AFTER trade
  - Rule violation self-declaration
  - Violation types: Moved stop, Entry outside plan, Overtrading, FOMO, Other
- **Discipline Dashboard**:
  - Discipline Score (0-100)
  - Emotional Consistency Score
  - Stop Loss Usage Rate
  - Trade History
  - Personalized Insights

### Previous Features
- User authentication with password visibility toggle
- Category system with book at top, levels below
- XP/Level gamification
- Trading journal

### Demo Credentials
- Email: demo@tradelingo.com
- Password: demo1234

## Test Results
- Backend: 100% (14/14 tests passed)
- Frontend: 90% (all core features working)

## Files Created
- `/app/backend/real_market.py` - Backend logic for market replay
- `/app/frontend/src/components/RealMarketZone.jsx` - Frontend component

## Database Tables (Supabase)
- users, journal_entries, user_progress
- real_market_trades (new - stores discipline metrics)

## Next Tasks
1. Create real_market_trades table in Supabase for persistence
2. Add more ORB strategies (London breakout, Asian range)
3. Add weekly discipline reports

## Backlog
- P1: Leaderboard for discipline scores
- P2: Export trade history to CSV
- P2: Social sharing of discipline achievements
