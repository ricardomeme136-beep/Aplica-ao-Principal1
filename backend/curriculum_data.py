# ==================== IMAGE-BASED QUESTIONS ====================
# These are "choose the correct image" questions
# Format: Each level has 5 image questions (exercises 2, 4, 6, 8, 10)
# 
# Structure:
# IMAGE_QUESTIONS = {
#     "category_id": {
#         level_number: [
#             {
#                 "title": "Question title",
#                 "explanation": "What concept this tests",
#                 "question": "Which image shows X?",
#                 "question_image": "URL of image showing the scenario (optional)",
#                 "options": ["image_url_A", "image_url_B", "image_url_C", "image_url_D"],
#                 "correct_answer": 0,  # 0=A, 1=B, 2=C, 3=D
#                 "feedback_correct": "Correct! This is X because...",
#                 "feedback_wrong": "Not quite. The correct image shows..."
#             },
#             # ... 5 questions per level
#         ]
#     }
# }
#
# TO EDIT: Replace the placeholder URLs with your actual chart images!
# ==================================================================


# ==================== COMPLETE CURRICULUM DATA ====================
# Each category has 10 levels, each level has 10 exercises
# Format: (Title, Explanation, Question, [Option A, B, C, D], correct_answer_index)

# ==================== 1. CANDLESTICKS ====================
CANDLESTICKS = {
    1: [  # Level 1 - Basics
        ("Bullish Candle", "A bullish candle closes higher than it opens, showing buyers won.", "What color typically represents a bullish candle?", ["Green/White", "Red/Black", "Blue", "Yellow"], 0),
        ("Bearish Candle", "A bearish candle closes lower than it opens, showing sellers won.", "What does a bearish candle indicate?", ["Buyers dominated", "Sellers dominated", "No activity", "Market closed"], 1),
        ("Candle Body", "The body is the thick part showing open-to-close range.", "What does a large candle body indicate?", ["Weak momentum", "Strong momentum", "Indecision", "No trading"], 1),
        ("Upper Wick", "The upper wick shows the highest price reached before rejection.", "A long upper wick means:", ["Price was rejected from highs", "Strong buying", "Gap up", "Market close"], 0),
        ("Lower Wick", "The lower wick shows the lowest price reached before recovery.", "A long lower wick indicates:", ["Selling pressure", "Buyers stepped in at lows", "No interest", "Gap down"], 1),
        ("Doji Candle", "A doji has nearly equal open and close, showing indecision.", "What does a doji represent?", ["Strong trend", "Market indecision", "Reversal confirmed", "Breakout"], 1),
        ("Marubozu", "A marubozu has no wicks - pure momentum candle.", "A bullish marubozu shows:", ["Weak buyers", "Dominant buyers from open to close", "Indecision", "Reversal"], 1),
        ("Spinning Top", "Small body with long wicks on both sides shows indecision.", "A spinning top indicates:", ["Strong trend", "Battle between buyers and sellers", "Breakout coming", "Gap"], 1),
        ("Candle Timeframes", "Each candle represents one unit of time (1min, 1hr, 1day, etc).", "A daily candle shows price action for:", ["1 minute", "1 hour", "24 hours", "1 week"], 2),
        ("Reading Candles", "Candles tell a story of buyer vs seller battles.", "Why are candles useful?", ["They look pretty", "They show sentiment and momentum", "They predict the future", "They show volume only"], 1),
    ],
    2: [  # Level 2 - Single Patterns
        ("Hammer", "Hammer has small body at top with long lower wick - bullish reversal signal.", "Where does a hammer appear?", ["At tops", "At bottoms after downtrend", "In middle of trend", "Anywhere"], 1),
        ("Inverted Hammer", "Small body at bottom with long upper wick after downtrend.", "An inverted hammer suggests:", ["Continuation down", "Potential bullish reversal", "Strong selling", "No change"], 1),
        ("Hanging Man", "Same shape as hammer but appears at tops - bearish warning.", "A hanging man at resistance means:", ["Buy signal", "Potential reversal down", "Continue buying", "Nothing"], 1),
        ("Shooting Star", "Small body at bottom, long upper wick at top of uptrend.", "A shooting star indicates:", ["Buyers won", "Rejection from highs, possible reversal", "Breakout", "Gap up"], 1),
        ("Engulfing Bullish", "A large green candle completely covers the previous red candle.", "Bullish engulfing is strongest when:", ["In uptrend", "After a downtrend at support", "In ranging market", "At any time"], 1),
        ("Engulfing Bearish", "A large red candle completely covers the previous green candle.", "Bearish engulfing signals:", ["Continuation up", "Potential reversal down", "Indecision", "Breakout"], 1),
        ("Piercing Line", "Bullish: opens below prior close, closes above midpoint of prior candle.", "Piercing line is a:", ["Bearish pattern", "Bullish reversal pattern", "Continuation pattern", "Neutral pattern"], 1),
        ("Dark Cloud Cover", "Bearish: opens above prior close, closes below midpoint.", "Dark cloud cover suggests:", ["Bullish momentum", "Bearish reversal potential", "Strong buying", "Gap continuation"], 1),
        ("Dragonfly Doji", "Doji with long lower wick - bulls recovered from selling.", "Dragonfly doji at support suggests:", ["More selling", "Potential bounce/reversal up", "Nothing", "Gap down"], 1),
        ("Gravestone Doji", "Doji with long upper wick - sellers rejected buyers.", "Gravestone doji at resistance means:", ["Breakout", "Potential reversal down", "Strong buying", "Continue up"], 1),
    ],
    3: [  # Level 3 - Double Patterns
        ("Tweezer Tops", "Two candles with same highs at resistance - reversal signal.", "Tweezer tops indicate:", ["Breakout coming", "Strong resistance, potential reversal", "Support found", "Nothing"], 1),
        ("Tweezer Bottoms", "Two candles with same lows at support - reversal signal.", "Tweezer bottoms suggest:", ["More downside", "Support holding, potential bounce", "Continuation", "Gap"], 1),
        ("Bullish Harami", "Small green candle inside prior large red candle body.", "Bullish harami indicates:", ["Strong selling", "Momentum slowing, possible reversal up", "Breakout down", "Nothing"], 1),
        ("Bearish Harami", "Small red candle inside prior large green candle body.", "Bearish harami suggests:", ["Strong buying", "Momentum fading, possible reversal", "Breakout up", "Continuation"], 1),
        ("Morning Star", "Three candles: big red, small body, big green - bullish reversal.", "Morning star appears:", ["At market tops", "At market bottoms", "In middle of trends", "Only on daily charts"], 1),
        ("Evening Star", "Three candles: big green, small body, big red - bearish reversal.", "Evening star is a:", ["Bullish signal", "Bearish reversal pattern", "Continuation pattern", "Neutral"], 1),
        ("Three White Soldiers", "Three consecutive bullish candles with higher closes.", "Three white soldiers show:", ["Weak momentum", "Strong bullish momentum", "Reversal down", "Indecision"], 1),
        ("Three Black Crows", "Three consecutive bearish candles with lower closes.", "Three black crows indicate:", ["Bullish reversal", "Strong bearish pressure", "Support found", "Nothing"], 1),
        ("Inside Bar", "Current candle's range is within the previous candle.", "Inside bars often lead to:", ["Nothing", "Breakout in either direction", "Always up", "Always down"], 1),
        ("Outside Bar", "Current candle engulfs both high and low of previous candle.", "Outside bar shows:", ["Low volatility", "Increased volatility and momentum", "Indecision only", "Gap"], 1),
    ],
    4: [  # Level 4 - Triple Patterns
        ("Three Inside Up", "Harami followed by bullish confirmation candle.", "Three inside up is:", ["Bearish", "Bullish reversal confirmation", "Neutral", "Continuation down"], 1),
        ("Three Inside Down", "Harami followed by bearish confirmation candle.", "Three inside down signals:", ["Bullish move", "Bearish reversal confirmed", "Nothing", "Support"], 1),
        ("Three Outside Up", "Engulfing followed by bullish continuation.", "This pattern shows:", ["Weakness", "Strong bullish conviction", "Indecision", "Reversal down"], 1),
        ("Three Outside Down", "Engulfing followed by bearish continuation.", "Three outside down indicates:", ["Buying pressure", "Strong selling continuation", "Bounce coming", "Nothing"], 1),
        ("Rising Three Methods", "Bullish continuation: big green, 3 small reds, big green.", "Rising three methods means:", ["Reversal", "Trend continuation after pause", "Top forming", "Support broken"], 1),
        ("Falling Three Methods", "Bearish continuation: big red, 3 small greens, big red.", "This pattern suggests:", ["Reversal up", "Downtrend will continue", "Support found", "Buy signal"], 1),
        ("Bullish Abandoned Baby", "Gap down doji followed by gap up - rare reversal.", "Abandoned baby is:", ["Common pattern", "Rare but powerful reversal signal", "Continuation", "Weak signal"], 1),
        ("Bearish Abandoned Baby", "Gap up doji followed by gap down - rare reversal.", "This pattern indicates:", ["Continuation up", "Rare bearish reversal", "Nothing special", "Support"], 1),
        ("Mat Hold", "Strong continuation pattern with small retracements.", "Mat hold shows:", ["Weakness", "Trend strength with minor pullback", "Reversal", "Indecision"], 1),
        ("Kicker Pattern", "Gap that completely reverses prior candle direction.", "Kicker pattern is:", ["Weak signal", "Very strong reversal signal", "Continuation", "Neutral"], 1),
    ],
    5: [  # Level 5 - Context & Confluence
        ("Candles at Support", "Bullish patterns at support have higher probability.", "Hammer at strong support is:", ["Less reliable", "More reliable", "Meaningless", "Bearish"], 1),
        ("Candles at Resistance", "Bearish patterns at resistance have higher probability.", "Shooting star at resistance:", ["Should be ignored", "Has higher reversal probability", "Is bullish", "Means nothing"], 1),
        ("Trend Context", "Patterns with the trend are more reliable.", "Bullish engulfing in uptrend is:", ["Reversal signal", "Strong continuation signal", "Bearish", "Neutral"], 1),
        ("Volume Confirmation", "High volume confirms candlestick signals.", "A hammer on high volume is:", ["Less significant", "More significant", "Irrelevant", "Bearish"], 1),
        ("Multiple Timeframe Candles", "Higher timeframe candles are more significant.", "Daily engulfing vs 5min engulfing:", ["5min is stronger", "Daily is more significant", "Both equal", "Neither matters"], 1),
        ("Failed Patterns", "Patterns that fail often reverse hard.", "Failed bullish engulfing leads to:", ["Nothing", "Often sharp move in opposite direction", "Confirmation", "Support"], 1),
        ("Candle Clusters", "Multiple reversal candles increase probability.", "Three hammers at support means:", ["Weak support", "Very strong support indication", "Sell signal", "Nothing"], 1),
        ("Gap + Candle", "Gaps with confirming candles are powerful.", "Gap up with bullish engulfing:", ["Weak signal", "Strong bullish confirmation", "Bearish", "Neutral"], 1),
        ("Wick Rejections", "Long wicks show price rejection at levels.", "Multiple wick rejections at price:", ["Meaningless", "Shows strong S/R level", "Breakout coming", "Gap signal"], 1),
        ("Body vs Wick Ratio", "More body = more conviction, more wick = more rejection.", "Candle with 80% body shows:", ["Indecision", "Strong momentum and conviction", "Reversal", "Nothing"], 1),
    ],
    6: [  # Level 6 - Advanced Single Candles
        ("Long-Legged Doji", "Very long wicks both sides - extreme indecision.", "Long-legged doji after trend:", ["Continue trend", "Potential pause or reversal", "Guaranteed reversal", "Gap"], 1),
        ("Four Price Doji", "Open=High=Low=Close - very rare, extreme pause.", "Four price doji indicates:", ["Strong trend", "Complete market pause/indecision", "Breakout", "Sell signal"], 1),
        ("High Wave Candle", "Very long upper and lower shadows with small body.", "High wave candle shows:", ["Clear direction", "Extreme indecision after volatility", "Trend continuation", "Gap up"], 1),
        ("Shaven Bottom", "Candle with no lower wick - buyers in control.", "Bullish shaven bottom means:", ["Selling pressure", "Buyers dominated, no selling", "Reversal", "Nothing"], 1),
        ("Shaven Top", "Candle with no upper wick - sellers in control.", "Bearish shaven top indicates:", ["Buying pressure", "Sellers controlled, no buying", "Support", "Gap up"], 1),
        ("Opening Marubozu", "No wick on opening side - gap and run.", "Opening marubozu shows:", ["Weak open", "Strong directional bias from open", "Indecision", "Reversal"], 1),
        ("Closing Marubozu", "No wick on closing side - strong close.", "Closing marubozu indicates:", ["Weak close", "Strong momentum into close", "Reversal coming", "Gap down"], 1),
        ("Belt Hold Bullish", "Long bullish candle opens at low - strong buying.", "Bullish belt hold shows:", ["Selling pressure", "Aggressive buying from open", "Nothing", "Reversal down"], 1),
        ("Belt Hold Bearish", "Long bearish candle opens at high - strong selling.", "Bearish belt hold indicates:", ["Buying pressure", "Aggressive selling from open", "Support", "Gap up"], 1),
        ("Rickshaw Man", "Doji with open/close in exact middle of range.", "Rickshaw man shows:", ["Trend", "Perfect balance/indecision", "Reversal", "Continuation"], 1),
    ],
    7: [  # Level 7 - Pattern Psychology
        ("Hammer Psychology", "Long wick shows sellers tried but buyers overwhelmed them.", "Hammer lower wick represents:", ["Failed buying", "Failed selling attempt", "Nothing", "Volume"], 1),
        ("Engulfing Psychology", "Complete coverage shows total sentiment shift.", "Engulfing shows:", ["Indecision", "One side completely overpowering other", "Nothing", "Gap"], 1),
        ("Doji Psychology", "Equal open/close means neither side won.", "Doji represents:", ["Buyer victory", "Neither bulls nor bears won", "Seller victory", "Breakout"], 1),
        ("Morning Star Psychology", "Shows transition from selling to indecision to buying.", "Middle candle of morning star shows:", ["Strong selling", "Transition/indecision point", "Strong buying", "Nothing"], 1),
        ("Stop Hunt Candles", "Long wicks often represent stop loss hunting.", "Long wick through key level often means:", ["Breakout", "Stop hunt/liquidity grab", "Nothing", "Support broken"], 1),
        ("Exhaustion Candles", "Very large candles after extended moves show exhaustion.", "Huge candle after long trend may show:", ["More momentum", "Potential exhaustion/reversal", "Nothing", "Gap"], 1),
        ("Indecision Resolution", "Dojis/spinning tops lead to breakout direction.", "Doji at key level usually leads to:", ["Nothing", "Breakout move in coming candles", "Continued indecision", "Gap"], 1),
        ("Trap Candles", "False breakout candles that reverse quickly.", "Candle breaking level then reversing is:", ["Confirmed breakout", "Potential bull/bear trap", "Nothing", "Continuation"], 1),
        ("Momentum Shift", "Change from small to large candles shows momentum shift.", "Suddenly larger candles indicate:", ["Less volatility", "Increasing momentum/participation", "Indecision", "Nothing"], 1),
        ("Rejection Speed", "Fast rejection wicks show strong opposing pressure.", "Quick wick formation shows:", ["Weak rejection", "Strong immediate counter-pressure", "Nothing", "Support"], 1),
    ],
    8: [  # Level 8 - Candles with SMC
        ("Candles at Order Blocks", "Reversal candles at OB confirm institutional interest.", "Bullish engulfing at bullish OB:", ["Weak signal", "Strong OB confirmation", "Bearish signal", "Nothing"], 1),
        ("Candles at FVG", "Rejection candles in FVG show gap filling.", "Hammer inside FVG means:", ["FVG invalid", "FVG acting as support", "Nothing", "Sell signal"], 1),
        ("BOS Candles", "Strong candles that break structure.", "BOS candle characteristics:", ["Small body", "Large body with momentum", "Doji", "Spinning top"], 1),
        ("ChoCH Candles", "Candles that change market character.", "ChoCH is confirmed by:", ["Small candles", "Strong reversal candle", "Doji", "Inside bar"], 1),
        ("Liquidity Grab Candles", "Long wicks above/below equal highs/lows.", "Wick through equal highs then reversal:", ["Breakout", "Liquidity sweep completed", "Nothing", "More upside"], 1),
        ("Mitigation Candles", "Candles that return to and react from OB.", "Strong reaction candle at OB shows:", ["OB failure", "OB mitigation/confirmation", "Nothing", "Sell signal"], 1),
        ("Displacement Candles", "Large momentum candles after OB formation.", "Displacement confirms:", ["Weak OB", "Strong institutional interest", "Retail buying", "Nothing"], 1),
        ("Imbalance Candles", "Candles creating FVG show institutional urgency.", "FVG-creating candles indicate:", ["Retail trading", "Institutional urgency/imbalance", "Indecision", "Nothing"], 1),
        ("Inducement Candles", "Small highs/lows that trap retail traders.", "Small tempting candle patterns often:", ["Show real levels", "Act as inducement/trap", "Should be traded", "Nothing"], 1),
        ("Premium/Discount Candles", "Reversal candles in premium/discount zones.", "Bearish candle in premium zone:", ["Ignore", "Has higher probability", "Means nothing", "Is bullish"], 1),
    ],
    9: [  # Level 9 - Advanced Combinations
        ("Engulfing + FVG", "Engulfing that creates FVG is more powerful.", "Engulfing with FVG shows:", ["Weak signal", "Very strong institutional move", "Retail buying", "Nothing"], 1),
        ("Hammer + OB", "Hammer at bullish OB is high probability.", "Hammer at OB means:", ["OB failure", "High probability long setup", "Sell signal", "Nothing"], 1),
        ("Shooting Star + Supply", "Shooting star at supply zone confirms resistance.", "This combination shows:", ["Breakout", "Strong resistance confirmation", "Support", "Nothing"], 1),
        ("Doji + Liquidity", "Doji after liquidity sweep signals reversal.", "Doji after stop hunt means:", ["Continue direction", "Potential reversal setting up", "Nothing", "Breakout"], 1),
        ("Morning Star + Demand", "Morning star at demand zone = very strong.", "This confluence creates:", ["Weak setup", "High probability reversal zone", "Sell signal", "Nothing"], 1),
        ("Evening Star + Supply", "Evening star at supply confirms major resistance.", "This setup suggests:", ["Breakout up", "High probability short zone", "Buy signal", "Nothing"], 1),
        ("Three Soldiers + BOS", "Three white soldiers breaking structure.", "This combination shows:", ["Weak move", "Strong trend continuation", "Reversal", "Indecision"], 1),
        ("Pinbar + EQH/EQL", "Pinbar after sweeping equal highs/lows.", "Pinbar after liquidity grab:", ["Random", "High probability reversal signal", "Continue direction", "Nothing"], 1),
        ("Engulfing + ChoCH", "Engulfing candle creating ChoCH.", "Engulfing ChoCH is:", ["Weak signal", "Strong trend change signal", "Noise", "Continuation"], 1),
        ("Marubozu + Displacement", "Marubozu as displacement candle.", "This shows:", ["Weak institutional move", "Very strong commitment", "Retail trading", "Nothing"], 1),
    ],
    10: [  # Level 10 - Master Level
        ("Complete Candle Analysis", "Combining all elements for full picture.", "Master candle reading requires:", ["Just memorizing patterns", "Context, location, and pattern analysis", "Indicators", "Luck"], 1),
        ("Candle Narrative", "Reading the story candles tell over time.", "Candles show:", ["Random moves", "Story of buyer/seller battles", "Nothing useful", "Only price"], 1),
        ("Failure Analysis", "Understanding why patterns fail.", "Pattern failures often mean:", ["Analysis was wrong", "Opposite move may be stronger", "Nothing", "Try again"], 1),
        ("Real-Time Reading", "Making decisions as candles form.", "Live candle analysis requires:", ["Waiting for close", "Patience and discipline", "Impulse trading", "Nothing"], 1),
        ("Timeframe Selection", "Choosing right timeframe for your style.", "Higher timeframes have:", ["Weaker signals", "More significant patterns", "More noise", "Faster signals"], 1),
        ("Trading Plan Integration", "Using candles within complete trading system.", "Candles should be:", ["Used alone", "Combined with other analysis", "Ignored", "The only tool"], 1),
        ("Risk Management", "Sizing positions based on candle setups.", "Better candle setup means:", ["Larger position", "Same position always", "No position", "Random sizing"], 0),
        ("Trade Management", "Using candles to manage open positions.", "Opposite candle pattern may signal:", ["Add to position", "Consider taking profit", "Ignore", "Nothing"], 1),
        ("Pattern Evolution", "Markets change, patterns evolve.", "Classic patterns today:", ["Work perfectly always", "May need adaptation to current markets", "Never work", "Are useless"], 1),
        ("Continuous Learning", "Always improving candle reading skills.", "Master traders:", ["Stop learning", "Continuously refine their skills", "Use indicators only", "Trade randomly"], 1),
    ],
}

# ==================== 2. MARKET STRUCTURE ====================
MARKET_STRUCTURE = {
    1: [  # Level 1 - Basics
        ("What is Market Structure?", "Market structure shows trend direction through swing highs and lows.", "Market structure helps identify:", ["Random moves", "Trend direction", "Volume", "Time"], 1),
        ("Swing High", "A peak where price reverses downward.", "Swing high is:", ["A low point", "A peak/high point", "Average price", "Opening price"], 1),
        ("Swing Low", "A trough where price reverses upward.", "Swing low is:", ["A peak", "A trough/low point", "Closing price", "Nothing"], 1),
        ("Higher High (HH)", "New high above previous high - bullish.", "Higher high shows:", ["Bearish momentum", "Bullish momentum", "No trend", "Reversal"], 1),
        ("Higher Low (HL)", "Low above previous low - bullish.", "Higher low indicates:", ["Sellers winning", "Buyers defending higher levels", "Reversal", "Nothing"], 1),
        ("Lower High (LH)", "High below previous high - bearish.", "Lower high shows:", ["Buyers winning", "Sellers gaining control", "Support", "Nothing"], 1),
        ("Lower Low (LL)", "Low below previous low - bearish.", "Lower low indicates:", ["Bullish trend", "Bearish continuation", "Support found", "Reversal up"], 1),
        ("Bullish Structure", "Pattern of HH + HL shows uptrend.", "Uptrend is defined by:", ["LH + LL", "HH + HL", "Equal highs", "Random moves"], 1),
        ("Bearish Structure", "Pattern of LH + LL shows downtrend.", "Downtrend is defined by:", ["HH + HL", "LH + LL", "Equal lows", "No pattern"], 1),
        ("Ranging Structure", "No clear HH/HL or LH/LL pattern.", "Ranging market has:", ["Clear trend", "Price moving sideways", "Strong momentum", "Gaps"], 1),
    ],
    2: [  # Level 2 - Identifying Swings
        ("Valid Swing Identification", "Valid swings have candles on each side confirming.", "Valid swing high needs:", ["Just one candle", "Candles on both sides lower", "Any high point", "Nothing"], 1),
        ("Minor vs Major Swings", "Major swings are more significant than minor.", "Major swings are found on:", ["Lower timeframes only", "Higher timeframes", "Any timeframe equally", "News events"], 1),
        ("Swing Confirmation", "Wait for confirmation before labeling swings.", "Swing is confirmed when:", ["Immediately", "After price moves away from it", "Never", "Random"], 1),
        ("Internal Structure", "Smaller swings within larger structure.", "Internal swings are:", ["More important than external", "Smaller moves within major structure", "Irrelevant", "The main structure"], 1),
        ("External Structure", "Major swings that define the trend.", "External structure shows:", ["Minor pullbacks", "Main trend direction", "Noise", "Nothing"], 1),
        ("Strong vs Weak Highs", "Strong highs have momentum, weak highs are choppy.", "Strong high is likely to:", ["Break easily", "Act as resistance", "Be ignored", "Nothing"], 0),
        ("Strong vs Weak Lows", "Strong lows have momentum, weak lows are vulnerable.", "Weak low suggests:", ["Strong support", "May be taken/broken", "Reversal up", "Nothing"], 1),
        ("Swing Point Spacing", "Proper spacing between swings for valid structure.", "Swings too close together:", ["Are more valid", "May be noise", "Show strong trend", "Nothing"], 1),
        ("Multi-Touch Swings", "Swings tested multiple times are significant.", "Multiple tests of a level:", ["Weaken it", "Strengthen its significance", "Mean nothing", "Are random"], 1),
        ("Protected vs Unprotected", "Protected swings have structure defending them.", "Unprotected swing:", ["Is stronger", "Is more vulnerable to break", "Cannot break", "Nothing"], 1),
    ],
    3: [  # Level 3 - Break of Structure (BOS)
        ("What is BOS?", "Break of Structure confirms trend continuation.", "BOS occurs when:", ["Price reverses", "Price breaks significant swing in trend direction", "Price consolidates", "Nothing"], 1),
        ("Bullish BOS", "Price breaks above previous high in uptrend.", "Bullish BOS confirms:", ["Downtrend", "Uptrend continuation", "Ranging market", "Reversal"], 1),
        ("Bearish BOS", "Price breaks below previous low in downtrend.", "Bearish BOS confirms:", ["Uptrend", "Downtrend continuation", "Reversal up", "Nothing"], 1),
        ("BOS vs Fakeout", "Real BOS has follow-through, fakeouts reverse.", "True BOS is followed by:", ["Immediate reversal", "Continuation in break direction", "Nothing", "Consolidation always"], 1),
        ("BOS Candle", "The candle that creates BOS is significant.", "BOS candle should be:", ["Small and weak", "Strong with momentum", "A doji", "Inside bar"], 1),
        ("BOS and Retest", "After BOS, price often retests broken level.", "After bullish BOS, retest offers:", ["Short opportunity", "Long opportunity", "Nothing", "Exit signal"], 1),
        ("Multiple BOS", "Series of BOS confirms strong trend.", "Multiple BOS shows:", ["Weak trend", "Strong trending momentum", "Reversal coming", "Nothing"], 1),
        ("BOS Timeframes", "Higher timeframe BOS is more significant.", "Daily BOS vs 5min BOS:", ["5min is stronger", "Daily is more significant", "Both equal", "Neither matters"], 1),
        ("Failed BOS", "When BOS doesn't hold, expect reversal.", "Failed BOS suggests:", ["Continue original direction", "Potential reversal/trap", "Nothing", "More BOS coming"], 1),
        ("BOS and Order Flow", "BOS shows institutional order flow direction.", "Institutions create BOS to:", ["Trap retail", "Show their directional bias", "Confuse traders", "Nothing"], 1),
    ],
    4: [  # Level 4 - Change of Character (ChoCH)
        ("What is ChoCH?", "Change of Character signals potential trend reversal.", "ChoCH breaks structure:", ["With the trend", "Against the current trend", "Sideways", "Not at all"], 1),
        ("Bullish ChoCH", "In downtrend, price breaks above previous high.", "Bullish ChoCH signals:", ["Downtrend continuation", "Potential reversal to uptrend", "Ranging", "Nothing"], 1),
        ("Bearish ChoCH", "In uptrend, price breaks below previous low.", "Bearish ChoCH indicates:", ["Uptrend continuation", "Potential reversal to downtrend", "More upside", "Nothing"], 1),
        ("ChoCH vs BOS", "ChoCH is against trend, BOS is with trend.", "Key difference:", ["They are the same", "ChoCH is reversal, BOS is continuation", "BOS is reversal", "Neither matters"], 1),
        ("ChoCH Confirmation", "Wait for confirmation after ChoCH.", "ChoCH is confirmed by:", ["Immediate reversal", "Follow-through and new structure", "Nothing", "Single candle"], 1),
        ("False ChoCH", "ChoCH that fails to lead to trend change.", "False ChoCH often:", ["Leads to trend change", "Traps counter-trend traders", "Nothing", "Confirms reversal"], 1),
        ("ChoCH Location", "ChoCH at key levels is more significant.", "ChoCH at major support:", ["Is weaker", "Has higher probability", "Means nothing", "Is bearish"], 1),
        ("Multiple ChoCH", "Several ChoCH in a row confirm reversal.", "Two or more ChoCH:", ["Weaken signal", "Strengthen reversal probability", "Mean nothing", "Cancel out"], 1),
        ("ChoCH Candle Quality", "Strong ChoCH candles are more reliable.", "ChoCH should have:", ["Small candle", "Strong momentum candle", "Doji", "Gap"], 1),
        ("Trading ChoCH", "Enter on pullback after ChoCH for better R:R.", "Best ChoCH entry:", ["On the ChoCH candle", "On pullback after ChoCH", "Random entry", "Before ChoCH"], 1),
    ],
    5: [  # Level 5 - Structure Shifts
        ("Structure Shift", "When trend direction changes from bullish to bearish or vice versa.", "Structure shift requires:", ["One candle", "ChoCH followed by BOS in new direction", "Random move", "Nothing"], 1),
        ("Confirmed vs Unconfirmed", "Unconfirmed shift may fail, confirmed is reliable.", "Shift is confirmed after:", ["ChoCH only", "ChoCH + BOS in new direction", "Any candle", "Nothing"], 1),
        ("Shift at Key Levels", "Structure shifts at S/R are more reliable.", "Shift at major resistance:", ["Is weaker", "Has higher probability", "Means nothing", "Is bullish"], 1),
        ("Shift Momentum", "Fast shifts are more reliable than slow.", "Quick structure shift shows:", ["Weak conviction", "Strong institutional interest", "Nothing", "Random move"], 1),
        ("Trading the Shift", "Wait for pullback after confirmed shift.", "Enter shift trade:", ["On the shift candle", "On pullback to broken structure", "Random", "Before shift"], 1),
        ("Failed Shifts", "When shift doesn't continue in new direction.", "Failed shift suggests:", ["New direction continues", "Original trend may resume", "Nothing", "More shifting"], 1),
        ("Shift and HTF", "Lower timeframe shifts within HTF trends.", "LTF shift against HTF trend:", ["Is stronger", "May be just a pullback", "Confirms reversal", "Nothing"], 1),
        ("Multiple Timeframe Shifts", "Shift on multiple timeframes is powerful.", "HTF and LTF both shifting:", ["Is weak signal", "Is very strong confirmation", "Means nothing", "Is noise"], 1),
        ("Shift Speed", "How fast price shifts can indicate strength.", "Slow shift may indicate:", ["Strong conviction", "Potential failure/trap", "Nothing", "Continuation"], 1),
        ("Shift Targets", "Where price may go after structure shift.", "After bullish shift, target:", ["Previous lows", "Previous highs/liquidity above", "Random", "Nothing"], 1),
    ],
    6: [  # Level 6 - Internal vs External
        ("Internal Structure", "Smaller moves within the main trend.", "Internal structure is:", ["The main trend", "Pullback/correction structure", "Random noise", "Nothing"], 1),
        ("External Structure", "Main swing points defining overall trend.", "External structure shows:", ["Small pullbacks", "Main trend direction", "Noise only", "Nothing"], 1),
        ("Internal BOS", "BOS of internal swings within pullback.", "Internal BOS signals:", ["Main trend reversal", "Pullback continuation", "Nothing", "Main BOS"], 1),
        ("External BOS", "BOS of main swing points.", "External BOS confirms:", ["Pullback", "Main trend continuation", "Reversal", "Nothing"], 1),
        ("Trading Internal", "Use internal for entries in trend direction.", "Internal structure helps with:", ["Finding reversals", "Timing entries in trend", "Exit only", "Nothing"], 1),
        ("Internal to External", "Internal structure breaking external = shift.", "When internal breaks external:", ["Nothing changes", "Potential trend change", "Trend continues", "Random"], 1),
        ("Fractal Nature", "Structure exists on all timeframes.", "Market structure is:", ["Random", "Fractal/self-similar across timeframes", "Only on daily", "Only intraday"], 1),
        ("Aligning Structures", "Trade when internal and external align.", "Internal bullish in external uptrend:", ["Is weak setup", "Is aligned/high probability", "Is bearish", "Nothing"], 1),
        ("Conflicting Structures", "When internal conflicts with external.", "Internal bearish in external uptrend:", ["Strong short", "Just a pullback likely", "Confirms downtrend", "Nothing"], 1),
        ("Structure Priority", "External always takes priority.", "In conflict, follow:", ["Internal structure", "External structure", "Neither", "Random"], 1),
    ],
    7: [  # Level 7 - Premium & Discount Structure
        ("Premium Zone", "Upper 50% of structure range.", "Premium zone is:", ["Below 50%", "Above 50% of range", "At 50%", "Random"], 1),
        ("Discount Zone", "Lower 50% of structure range.", "Discount zone is:", ["Above 50%", "Below 50% of range", "At 50%", "The whole range"], 1),
        ("Equilibrium", "The 50% level of the range.", "Equilibrium is:", ["Strong S/R", "The middle/50% level", "Random level", "Nothing"], 1),
        ("Buy in Discount", "Look for longs in discount zone.", "Best buys are in:", ["Premium", "Discount zone", "Equilibrium", "Random"], 1),
        ("Sell in Premium", "Look for shorts in premium zone.", "Best shorts are in:", ["Discount", "Premium zone", "Equilibrium", "Random"], 1),
        ("Structure + Zones", "Combine structure and P/D for entries.", "HH in discount zone:", ["Is weak", "Is high probability long setup", "Is short setup", "Nothing"], 1),
        ("Zone Rejection", "Price rejecting from zone confirms it.", "Strong rejection from premium:", ["Is bullish", "Confirms selling zone", "Means nothing", "Is random"], 1),
        ("Equilibrium Trade", "Some trade the equilibrium level.", "Equilibrium can act as:", ["Strong S/R", "Weak S/R or decision point", "Nothing", "Resistance only"], 1),
        ("Dynamic Zones", "Zones change as structure develops.", "As new HH forms:", ["Zones stay same", "Zones recalculate", "Zones disappear", "Nothing"], 1),
        ("Zone + Confluence", "Zones with other factors are best.", "Discount + OB + HL:", ["Weak setup", "Very high probability setup", "Random", "Nothing"], 1),
    ],
    8: [  # Level 8 - Liquidity and Structure
        ("Liquidity Pools", "Structure creates liquidity above highs and below lows.", "Swing highs have:", ["Sell stops below", "Buy stops above", "No liquidity", "Random orders"], 1),
        ("Structure as Target", "Price targets liquidity at structure points.", "Price often moves toward:", ["Random levels", "Untaken liquidity at swings", "Equilibrium only", "Nothing"], 1),
        ("Sweep and Structure", "Liquidity sweep often precedes structure change.", "Sweep of high followed by ChoCH:", ["Is random", "Is common reversal pattern", "Means continuation", "Nothing"], 1),
        ("Protected Highs/Lows", "Structure that hasn't been swept.", "Protected low with liquidity:", ["May be targeted", "Is safe forever", "Will never break", "Nothing"], 1),
        ("Unprotected Swings", "Swings that can be easily taken.", "Unprotected high:", ["Is very strong", "Is vulnerable to sweep", "Cannot be broken", "Nothing"], 1),
        ("EQH/EQL Structure", "Equal highs/lows are liquidity magnets.", "Equal lows create:", ["Strong support", "Liquidity pool likely to be swept", "Nothing", "Resistance"], 1),
        ("Structure Building Liquidity", "Ranging structure builds liquidity.", "Consolidation range has liquidity:", ["Nowhere", "Both above and below", "Only above", "Only below"], 1),
        ("Liquidity and BOS", "BOS often targets liquidity beyond.", "After bullish BOS, price targets:", ["Lows below", "Liquidity/highs above", "Equilibrium", "Nothing"], 1),
        ("Smart Money Structure", "SM uses structure to hunt liquidity.", "Institutions create structure to:", ["Help retail", "Build and hunt liquidity", "Nothing", "Random purposes"], 1),
        ("Trading with Liquidity", "Use liquidity understanding with structure.", "Long entry after sweep and ChoCH:", ["Random", "High probability setup", "Never works", "Is short setup"], 1),
    ],
    9: [  # Level 9 - Multi-Timeframe Structure
        ("HTF Direction", "Higher timeframe sets the main bias.", "Daily structure direction is:", ["Irrelevant", "Your primary bias", "Less important", "Random"], 1),
        ("LTF Execution", "Lower timeframe for entry timing.", "Use LTF to:", ["Set main bias", "Time entries precisely", "Ignore HTF", "Nothing"], 1),
        ("HTF BOS", "BOS on higher timeframe is major event.", "Daily BOS significance:", ["Low", "Very high", "Same as 5min", "Nothing"], 1),
        ("LTF BOS within HTF", "LTF BOS can signal HTF continuation.", "LTF BOS in HTF trend direction:", ["Is counter-trend", "Is aligned entry signal", "Means nothing", "Is reversal"], 1),
        ("MTF Confluence", "Multiple timeframes agreeing is powerful.", "H4, H1, and M15 all bullish:", ["Is weak", "Is very strong confluence", "Means nothing", "Is bearish"], 1),
        ("Conflicting Timeframes", "When timeframes disagree.", "LTF bearish, HTF bullish means:", ["Strong short", "LTF is likely just a pullback", "HTF is wrong", "Nothing"], 1),
        ("Timeframe Selection", "Choose appropriate timeframes.", "Day trader should use:", ["Monthly and weekly", "H4/H1 for bias, M15/M5 for entry", "Only M1", "Random"], 1),
        ("Structure Alignment", "Wait for alignment before trading.", "Best entries when:", ["TFs conflict", "Multiple TFs align", "Random", "Only one TF"], 1),
        ("HTF Levels", "Key levels from HTF are important on LTF.", "HTF support on LTF is:", ["Irrelevant", "Very significant", "Less important", "Random"], 1),
        ("Progressive Analysis", "Start from HTF, work down to LTF.", "Analysis order should be:", ["LTF to HTF", "HTF to LTF (top-down)", "Random", "Only one TF"], 1),
    ],
    10: [  # Level 10 - Master Structure
        ("Structure Mastery", "Combining all structure concepts.", "Master structure trader sees:", ["Random moves", "Clear narrative of trend and shifts", "Only candles", "Nothing"], 1),
        ("Real-Time Structure", "Marking structure as it develops.", "Label swings:", ["Only in hindsight", "As they confirm in real-time", "Randomly", "Never"], 1),
        ("Structure + SMC", "Using structure with all SMC concepts.", "Structure combined with SMC:", ["Is unnecessary", "Creates high probability setups", "Is confusing", "Nothing"], 1),
        ("Adapting to Conditions", "Structure reading in different markets.", "Ranging vs trending markets:", ["Trade the same", "Require different approach", "Don't trade ranges", "Nothing"], 1),
        ("Structure Journal", "Documenting structure analysis.", "Journaling structure helps:", ["Nothing", "Improve pattern recognition", "Waste time", "Random"], 1),
        ("Common Mistakes", "Avoiding structure analysis errors.", "Most common error is:", ["Over-analysis", "Labeling minor swings as major", "Under-analysis", "Nothing"], 1),
        ("Structure and Risk", "Using structure for stop placement.", "Stop should go:", ["Random level", "Beyond structure point", "Very tight always", "Very wide always"], 1),
        ("Structure Targets", "Using structure for profit targets.", "Target should be:", ["Random", "Next significant structure point", "Double your stop", "Nothing"], 1),
        ("Continuous Practice", "Structure reading improves with practice.", "Master structure through:", ["Reading books only", "Consistent chart practice", "Random trading", "Nothing"], 1),
        ("Teaching Structure", "Explaining to others reinforces understanding.", "Teaching structure:", ["Wastes time", "Deepens your own understanding", "Is unnecessary", "Nothing"], 1),
    ],
}

# ==================== 3. LIQUIDITY ====================
LIQUIDITY = {
    1: [
        ("What is Liquidity?", "Liquidity is resting orders in the market.", "Liquidity includes:", ["Only limit orders", "Stop losses, pending orders, limit orders", "Nothing", "Only market orders"], 1),
        ("Buy Side Liquidity", "Buy stops above swing highs.", "BSL is located:", ["Below price", "Above price at highs", "At current price", "Random"], 1),
        ("Sell Side Liquidity", "Sell stops below swing lows.", "SSL is located:", ["Above price", "Below price at lows", "At current price", "Random"], 1),
        ("Why Liquidity Matters", "Institutions need liquidity to fill large orders.", "Smart money hunts liquidity to:", ["Confuse retail", "Fill their large orders", "Nothing", "Random"], 1),
        ("Liquidity Pools", "Areas with concentrated orders.", "Equal highs create:", ["Nothing", "Liquidity pool above", "Resistance only", "Support"], 1),
        ("Retail Stop Placement", "Retail traders place stops at obvious levels.", "Stops above swing highs are:", ["Hidden", "Easy targets for institutions", "Safe", "Never hunted"], 1),
        ("Liquidity Sweep", "Price taking out liquidity before reversing.", "Sweep is when price:", ["Trends", "Briefly breaks level then reverses", "Consolidates", "Gaps"], 1),
        ("Resting Liquidity", "Untaken liquidity acts as magnet.", "Price is attracted to:", ["Random levels", "Areas of resting liquidity", "Nothing", "Equilibrium only"], 1),
        ("External Liquidity", "Liquidity at major swing points.", "External liquidity is:", ["Minor", "Major target for price", "Irrelevant", "Random"], 1),
        ("Internal Liquidity", "Liquidity at minor swing points.", "Internal liquidity is:", ["More important", "Smaller target within trends", "Irrelevant", "Same as external"], 1),
    ],
    2: [
        ("Equal Highs (EQH)", "Two or more highs at same level = liquidity.", "EQH create:", ["Strong resistance", "Liquidity pool to be swept", "Nothing", "Support"], 1),
        ("Equal Lows (EQL)", "Two or more lows at same level = liquidity.", "EQL create:", ["Strong support", "Liquidity pool to be swept", "Nothing", "Resistance"], 1),
        ("Trendline Liquidity", "Stops above/below trendlines.", "Trendlines have:", ["No liquidity", "Liquidity on the other side", "Random orders", "Nothing"], 1),
        ("Round Number Liquidity", "Stops at psychological levels.", "Round numbers like 1.3000:", ["Have no stops", "Attract stop placement", "Are random", "Nothing"], 1),
        ("Session Highs/Lows", "Previous session extremes have liquidity.", "Asian high has:", ["Nothing", "Buy stops above from shorts", "Only support", "No liquidity"], 1),
        ("Previous Day H/L", "Prior day high/low are key liquidity zones.", "PDH/PDL are:", ["Random levels", "Key liquidity targets", "Irrelevant", "Nothing"], 1),
        ("Weekly H/L Liquidity", "Weekly extremes have significant liquidity.", "Weekly high has:", ["Little liquidity", "Significant liquidity above", "None", "Random"], 1),
        ("Old High/Low", "Historical levels have resting orders.", "Old swing highs have:", ["No orders", "Accumulated buy stops", "Sell stops only", "Nothing"], 1),
        ("Liquidity Void", "Areas with little liquidity.", "Price moves fast through:", ["High liquidity", "Liquidity voids", "Random areas", "Nowhere"], 1),
        ("Stacked Liquidity", "Multiple liquidity levels close together.", "Stacked liquidity creates:", ["Weak target", "Strong magnet for price", "Nothing", "Random"], 1),
    ],
    3: [
        ("Liquidity Sweep Mechanics", "How sweeps work.", "Sweep triggers:", ["Limit orders", "Stop losses that become market orders", "Nothing", "Pending orders only"], 1),
        ("Sweep and Reverse", "Classic pattern of sweep then reversal.", "After sweep, price often:", ["Continues", "Reverses direction", "Nothing", "Gaps"], 1),
        ("Sweep Confirmation", "How to confirm sweep is complete.", "Sweep confirmed by:", ["Break only", "Break + strong reversal candle", "Nothing", "Time"], 1),
        ("False Sweep", "When sweep continues instead of reversing.", "False sweep continues:", ["Never", "When momentum is strong", "Always", "Random"], 1),
        ("Sweep Speed", "Fast sweeps vs slow sweeps.", "Fast sweep suggests:", ["Weak move", "Strong reversal potential", "Continuation", "Nothing"], 1),
        ("Wick Sweep", "Sweep shown by long wick.", "Long wick through level:", ["Is not a sweep", "Is a sweep/rejection", "Means nothing", "Is breakout"], 1),
        ("Body Sweep", "When candle body closes beyond level.", "Body close beyond level:", ["Is always reversal", "May be breakout not sweep", "Is always sweep", "Nothing"], 1),
        ("Multiple Sweeps", "Same level swept multiple times.", "Level swept twice:", ["Gets stronger", "Usually breaks on next test", "Nothing", "Becomes support"], 1),
        ("Sweep and Structure", "Sweep often precedes structure change.", "Sweep + ChoCH is:", ["Weak", "Strong reversal setup", "Random", "Continuation"], 1),
        ("Trading Sweeps", "How to trade sweep setups.", "Best sweep entry:", ["On the sweep candle", "After confirmation candle", "Before sweep", "Random"], 1),
    ],
    4: [
        ("Inducement", "Small liquidity levels that trap traders.", "Inducement is:", ["Major level", "Minor level to trap retail", "Nothing", "Support"], 1),
        ("Inducement vs Real Level", "Distinguishing traps from real targets.", "Inducement is usually:", ["Large swing", "Small tempting swing", "Major structure", "HTF level"], 1),
        ("Trading Inducement", "Using inducement to your advantage.", "When you see inducement:", ["Trade it", "Wait for it to be swept", "Ignore structure", "Nothing"], 1),
        ("Inducement Sweep", "When inducement gets taken.", "After inducement sweep:", ["Trade is over", "Real move often begins", "Nothing happens", "Reverse sweep"], 1),
        ("Creating Inducement", "How inducement forms.", "Inducement forms from:", ["Major moves", "Minor pullbacks creating tempting levels", "Random", "Nothing"], 1),
        ("Internal Inducement", "Small levels within larger moves.", "Internal liquidity often acts as:", ["Main target", "Inducement for real target", "Nothing", "Support"], 1),
        ("Avoiding Inducement Traps", "Don't get trapped by minor levels.", "Enter at inducement:", ["Good idea", "Often leads to stops being hit", "Always profitable", "Random"], 1),
        ("Inducement Recognition", "Identifying inducement levels.", "Inducement is usually:", ["At HTF levels", "At minor LTF swings", "At daily highs", "Random"], 1),
        ("Patience with Inducement", "Wait for inducement to clear.", "Patient trader waits for:", ["Inducement entry", "Inducement to be swept first", "Nothing", "Random"], 1),
        ("Inducement and SMC", "Inducement in SMC context.", "Smart money creates inducement to:", ["Help retail", "Trap retail before real move", "Nothing", "Random"], 1),
    ],
    5: [
        ("Liquidity Run", "Price running toward liquidity.", "Liquidity run is price:", ["Reversing", "Trending toward liquidity pool", "Consolidating", "Random"], 1),
        ("Run vs Sweep", "Run continues, sweep reverses.", "Key difference is:", ["None", "What happens after reaching liquidity", "Speed", "Time"], 1),
        ("Identifying Runs", "Recognizing liquidity runs early.", "Run often has:", ["Weak momentum", "Strong directional momentum", "Dojis", "Nothing"], 1),
        ("Run Targets", "Where runs are heading.", "Liquidity run targets:", ["Random levels", "Closest significant liquidity", "Nothing", "Equilibrium"], 1),
        ("Run Exhaustion", "When runs lose steam.", "Run exhaustion shows:", ["More momentum", "Slowing candles, possible reversal", "Nothing", "Continuation"], 1),
        ("Trading Runs", "Joining or fading liquidity runs.", "Trade with run:", ["Never", "Until liquidity target reached", "Against it always", "Random"], 1),
        ("Run and Structure", "Runs often create new structure.", "After liquidity run:", ["No structure change", "New HH or LL may form", "Structure invalid", "Nothing"], 1),
        ("Multi-Pool Runs", "Runs targeting multiple pools.", "Price may run through:", ["One pool only", "Multiple liquidity pools", "Nothing", "Random"], 1),
        ("Run Reversals", "When runs reverse sharply.", "Sharp reversal after run:", ["Is random", "Is potential sweep setup", "Means nothing", "Is continuation"], 1),
        ("Run Psychology", "Understanding run behavior.", "Liquidity runs show:", ["Random moves", "Institutional targets being reached", "Nothing", "Retail strength"], 1),
    ],
    6: [
        ("Daily Liquidity", "Daily high/low liquidity.", "PDH and PDL are:", ["Minor levels", "Key daily liquidity zones", "Random", "Nothing"], 1),
        ("Weekly Liquidity", "Weekly high/low liquidity.", "PWH and PWL are:", ["Less important than daily", "Major weekly liquidity targets", "Random", "Nothing"], 1),
        ("Monthly Liquidity", "Monthly high/low liquidity.", "Monthly extremes are:", ["Minor", "Very significant liquidity pools", "Random", "Nothing"], 1),
        ("Session Liquidity", "Asian, London, NY session liquidity.", "Session highs have:", ["No significance", "Session-specific liquidity", "Random orders", "Nothing"], 1),
        ("Opening Range Liquidity", "First hour range liquidity.", "Opening range high has:", ["Nothing", "Buy stops from early shorts", "No orders", "Random"], 1),
        ("Time-Based Targets", "Liquidity at specific times.", "London open often targets:", ["Random levels", "Asian session liquidity", "Nothing", "US levels"], 1),
        ("News Liquidity", "Liquidity around news events.", "Before news, liquidity:", ["Is cleared", "Builds up on both sides", "Disappears", "Nothing"], 1),
        ("Gap Liquidity", "Liquidity from gap opens.", "Weekend gaps create:", ["Nothing", "Liquidity to be filled", "Permanent gaps", "Random"], 1),
        ("Historical Liquidity", "Old levels with resting orders.", "Old unfilled levels have:", ["No orders", "Resting liquidity", "Been cleared", "Nothing"], 1),
        ("Confluence Liquidity", "Multiple liquidity factors align.", "PDH at round number is:", ["Weak level", "Strong liquidity confluence", "Random", "Nothing"], 1),
    ],
    7: [
        ("Smart Money Liquidity Use", "How institutions use liquidity.", "SM takes liquidity to:", ["Help retail", "Fill their large orders", "Nothing", "Random"], 1),
        ("Accumulation Phase", "Building positions using liquidity.", "Accumulation involves:", ["Taking liquidity to buy at lower prices", "Random buying", "Retail following", "Nothing"], 1),
        ("Distribution Phase", "Selling positions using liquidity.", "Distribution involves:", ["Taking BSL to sell at higher prices", "Random selling", "Retail selling", "Nothing"], 1),
        ("Stop Hunt Purpose", "Why stops get hunted.", "Stop hunts provide:", ["Pain for retail", "Liquidity for institutional fills", "Nothing", "Random moves"], 1),
        ("Order Pairing", "Matching institutional orders.", "SM sell orders pair with:", ["Other sells", "Retail buy stops triggered", "Nothing", "Random"], 1),
        ("Liquidity Engineering", "How SM creates liquidity.", "SM engineers liquidity by:", ["Random moves", "Creating ranges that trap orders", "Helping retail", "Nothing"], 1),
        ("Following Smart Money", "Trading with SM liquidity hunts.", "Trade in direction of:", ["Against SM", "SM liquidity capture", "Retail traders", "Random"], 1),
        ("SM Entry After Sweep", "SM enters after taking liquidity.", "After sweep, SM typically:", ["Exits", "Enters in opposite direction", "Nothing", "Random"], 1),
        ("Liquidity and POI", "Liquidity near POI is targeted.", "POI with nearby liquidity:", ["Is weak", "Is high probability", "Is random", "Nothing"], 1),
        ("SM Deception", "False moves to create liquidity.", "False breakouts create:", ["Real trades", "Trapped traders/more liquidity", "Nothing", "Strong trends"], 1),
    ],
    8: [
        ("Liquidity Mapping", "Marking liquidity on charts.", "Mark liquidity at:", ["Random levels", "All swing highs and lows", "Nothing", "Only round numbers"], 1),
        ("Prioritizing Liquidity", "Most important liquidity levels.", "HTF liquidity is:", ["Less important", "Higher priority target", "Same as LTF", "Nothing"], 1),
        ("Taken vs Untaken", "Tracking cleared liquidity.", "Once liquidity is taken:", ["Mark new level", "Remove from chart", "Nothing", "Ignore it"], 1),
        ("Liquidity Path", "Projecting where price will go.", "Price likely to target:", ["Random", "Nearest untaken liquidity", "Nothing", "Opposite direction"], 1),
        ("Multiple Pool Targets", "When several pools exist.", "Price may target:", ["One pool only", "Multiple pools in sequence", "Nothing", "Random"], 1),
        ("Liquidity Bias", "Using liquidity for directional bias.", "Most untaken liquidity above:", ["Bearish bias", "Bullish bias/target above", "Random", "Nothing"], 1),
        ("Entry Near Liquidity", "Positioning entries around liquidity.", "Enter after liquidity:", ["Is built", "Is taken/cleared", "Nothing", "Random"], 1),
        ("Exit Using Liquidity", "Taking profit at liquidity.", "Exit position at:", ["Random", "Liquidity target reached", "Entry point", "Nothing"], 1),
        ("Liquidity and Risk", "Stop placement using liquidity.", "Place stop beyond:", ["Random level", "Liquidity pool", "Entry", "Nothing"], 1),
        ("Dynamic Liquidity", "Liquidity changes as price moves.", "New swings create:", ["Nothing", "New liquidity pools", "Removes old liquidity", "Random"], 1),
    ],
    9: [
        ("Liquidity Sweep + OB", "Sweep into order block.", "Sweep into OB creates:", ["Nothing", "High probability setup", "Random", "Weak setup"], 1),
        ("Liquidity + FVG", "Sweep with FVG present.", "Sweep filling FVG:", ["Is random", "Adds confluence to setup", "Is weak", "Nothing"], 1),
        ("Liquidity + Structure", "Using structure with liquidity.", "Sweep causing ChoCH:", ["Is weak", "Is strong reversal signal", "Is random", "Nothing"], 1),
        ("HTF Liquidity + LTF Entry", "HTF target, LTF entry.", "Trade HTF liquidity using:", ["HTF entry", "LTF entry for precision", "Random TF", "Nothing"], 1),
        ("Liquidity Confluence", "Multiple liquidity factors.", "EQH at PDH:", ["Weak level", "Strong confluence", "Random", "Nothing"], 1),
        ("Liquidity + Kill Zone", "Liquidity in active sessions.", "Sweep during London:", ["Is weaker", "Has more follow-through", "Is random", "Nothing"], 1),
        ("Liquidity + Fair Value", "Premium/discount with liquidity.", "SSL in discount zone:", ["Avoid it", "Is high probability long area", "Is short setup", "Nothing"], 1),
        ("Complex Liquidity Setups", "Multiple concepts together.", "Sweep + OB + FVG:", ["Is too complex", "Is very high probability", "Is random", "Nothing"], 1),
        ("Liquidity Failure", "When expected sweep doesn't happen.", "Liquidity not taken:", ["Always happens later", "May indicate strong momentum", "Is random", "Nothing"], 1),
        ("Adapting to Liquidity", "Changing plan based on liquidity.", "If liquidity changes:", ["Ignore it", "Adapt your analysis", "Nothing", "Random"], 1),
    ],
    10: [
        ("Liquidity Mastery", "Complete liquidity understanding.", "Master liquidity trader:", ["Ignores liquidity", "Sees market as liquidity game", "Trades randomly", "Nothing"], 1),
        ("Predicting Targets", "Anticipating liquidity targets.", "Predict targets by:", ["Random guess", "Mapping untaken liquidity", "Indicators", "Nothing"], 1),
        ("Liquidity Journal", "Tracking liquidity setups.", "Journal should note:", ["Random trades", "Liquidity levels and reactions", "Nothing", "Indicators only"], 1),
        ("Common Mistakes", "Avoiding liquidity trading errors.", "Common error is:", ["Trading too slow", "Trading at liquidity instead of after", "Avoiding liquidity", "Nothing"], 1),
        ("Patience for Liquidity", "Waiting for ideal setups.", "Wait for:", ["Any sweep", "Clean sweep with confirmation", "Random entry", "Nothing"], 1),
        ("Liquidity and Psychology", "Mental aspects of liquidity trading.", "Stop hunts can cause:", ["Confidence", "Frustration if not understood", "Nothing", "Random emotions"], 1),
        ("Liquidity Edge", "How liquidity provides trading edge.", "Understanding liquidity:", ["Provides no edge", "Gives significant edge", "Is useless", "Nothing"], 1),
        ("Continuous Liquidity Learning", "Always improving.", "Liquidity mastery requires:", ["Reading one book", "Continuous observation and practice", "Nothing", "Random"], 1),
        ("Teaching Liquidity", "Explaining concepts to others.", "Teaching liquidity:", ["Wastes time", "Reinforces your understanding", "Is unnecessary", "Nothing"], 1),
        ("Liquidity and Complete Trading", "Liquidity in full system.", "Liquidity should be:", ["Only factor", "One part of complete analysis", "Ignored", "Random"], 1),
    ],
}

# ==================== 4. BREAK OF STRUCTURE (BOS) ====================
BOS = {
    1: [
        ("BOS Definition", "Break of Structure confirms trend continuation.", "BOS means price broke:", ["Random level", "Significant swing in trend direction", "Against trend", "Nothing"], 1),
        ("Bullish BOS", "Breaking above previous high.", "Bullish BOS breaks:", ["Below low", "Above previous high", "Equilibrium", "Nothing"], 1),
        ("Bearish BOS", "Breaking below previous low.", "Bearish BOS breaks:", ["Above high", "Below previous low", "Random", "Nothing"], 1),
        ("BOS Purpose", "Why BOS matters.", "BOS confirms:", ["Reversal", "Trend continuation", "Nothing", "Ranging market"], 1),
        ("BOS vs Fakeout", "Real BOS vs fake breakout.", "Real BOS has:", ["Quick reversal", "Follow-through momentum", "No volume", "Nothing"], 1),
        ("BOS Candle", "Candle creating the break.", "Strong BOS candle is:", ["Doji", "Large momentum candle", "Inside bar", "Random"], 1),
        ("BOS Confirmation", "When BOS is confirmed.", "BOS confirmed when:", ["Wick touches", "Body closes beyond level", "Price approaches", "Nothing"], 1),
        ("BOS Timeframes", "BOS significance across TFs.", "HTF BOS is:", ["Less significant", "More significant", "Same as LTF", "Random"], 1),
        ("Trading BOS", "How to trade BOS.", "Trade BOS by:", ["Chasing the break", "Entering on pullback after", "Fading it", "Random"], 1),
        ("BOS and Trend", "BOS role in trends.", "Strong trends have:", ["No BOS", "Series of BOS", "Only reversals", "Random"], 1),
    ],
    2: [
        ("Internal BOS", "BOS within larger move.", "Internal BOS breaks:", ["Main structure", "Minor swing within move", "HTF structure", "Nothing"], 1),
        ("External BOS", "BOS of main structure.", "External BOS breaks:", ["Minor swing", "Major swing point", "Nothing", "Random"], 1),
        ("Internal vs External", "Difference in significance.", "External BOS is:", ["Less important", "More significant", "Same as internal", "Nothing"], 1),
        ("BOS Quality", "Strong vs weak BOS.", "Strong BOS has:", ["Small candle", "Large displacement", "Doji", "Gap only"], 1),
        ("BOS Displacement", "Momentum after BOS.", "Displacement shows:", ["Weak conviction", "Strong institutional participation", "Nothing", "Reversal"], 1),
        ("BOS and FVG", "BOS often creates FVG.", "FVG after BOS:", ["Is random", "Confirms strong move", "Weakens setup", "Nothing"], 1),
        ("BOS and OB", "BOS creates order blocks.", "Candle before BOS often becomes:", ["Nothing", "Order block", "Random level", "FVG"], 1),
        ("Failed BOS", "When BOS doesn't hold.", "Failed BOS suggests:", ["Trend continues", "Potential trap/reversal", "Nothing", "Stronger trend"], 1),
        ("BOS Retest", "Price returning to broken level.", "After BOS, retest is:", ["Rare", "Common and offers entry", "Never happens", "Random"], 1),
        ("BOS Speed", "How fast BOS occurs.", "Fast BOS indicates:", ["Weakness", "Strong conviction", "Nothing", "Reversal"], 1),
    ],
    3: [
        ("BOS Entry Strategy", "How to enter on BOS.", "Best BOS entry:", ["On break candle", "On pullback to broken level", "Before break", "Random"], 1),
        ("BOS Stop Placement", "Where to place stop.", "Stop should go:", ["At entry", "Beyond structure before BOS", "Random", "Very tight"], 1),
        ("BOS Target", "Profit target after BOS.", "Target after bullish BOS:", ["Previous low", "Next high/liquidity above", "Entry point", "Random"], 1),
        ("BOS Risk:Reward", "R:R for BOS trades.", "Good BOS trade has:", ["1:0.5 R:R", "At least 1:2 R:R", "No target", "Random"], 1),
        ("Aggressive BOS Entry", "Entering on the break.", "Aggressive entry risk:", ["Lower", "Higher but faster fill", "Same", "None"], 1),
        ("Conservative BOS Entry", "Waiting for retest.", "Conservative entry benefit:", ["Worse R:R", "Better R:R and confirmation", "No benefit", "Random"], 1),
        ("BOS Confirmation Entry", "Waiting for extra proof.", "Confirmation entry uses:", ["Nothing", "LTF structure for entry", "Random TF", "HTF only"], 1),
        ("Managing BOS Trade", "Trade management after entry.", "After entry, watch for:", ["Nothing", "Continuation or failure signs", "Random moves", "Exit immediately"], 1),
        ("BOS and Session", "BOS in different sessions.", "BOS during London:", ["Is weaker", "Often has strong follow-through", "Is random", "Never trade"], 1),
        ("BOS Trade Examples", "Practical BOS applications.", "BOS trade success requires:", ["Luck", "Proper identification and execution", "Random entries", "Nothing"], 1),
    ],
    4: [
        ("Multiple BOS", "Series of BOS in trend.", "Multiple BOS shows:", ["Weak trend", "Strong trend momentum", "Reversal coming", "Nothing"], 1),
        ("BOS Frequency", "How often BOS occurs.", "Healthy trend has BOS:", ["Never", "Regularly as structure builds", "Once only", "Random"], 1),
        ("BOS Exhaustion", "Too many BOS quickly.", "Rapid BOS sequence may show:", ["Strong trend", "Potential exhaustion", "Nothing", "Beginning of trend"], 1),
        ("BOS and Pullback", "Pullback before next BOS.", "Pullback after BOS:", ["Is reversal", "Is healthy before continuation", "Is random", "Means trend over"], 1),
        ("BOS Chain", "Connected series of BOS.", "BOS chain confirms:", ["Reversal", "Strong directional bias", "Nothing", "Ranging market"], 1),
        ("Shallow vs Deep BOS", "How far BOS extends.", "Deep BOS beyond level:", ["Is weaker", "Shows strong conviction", "Is random", "Means failure"], 1),
        ("BOS Gaps", "Gap that creates BOS.", "Gap BOS is:", ["Invalid", "Very strong signal", "Random", "Should be ignored"], 1),
        ("BOS Volume", "Volume during BOS.", "High volume BOS:", ["Is weaker", "Confirms participation", "Is random", "Nothing"], 1),
        ("BOS Without Pullback", "Direct continuation after BOS.", "No pullback after BOS:", ["Always happens", "Shows urgency/strong momentum", "Is bearish", "Random"], 1),
        ("Anticipating BOS", "Predicting next BOS.", "Anticipate BOS when:", ["Random", "Structure and momentum align", "Never", "Always"], 1),
    ],
    5: [
        ("BOS and Liquidity", "BOS targeting liquidity.", "BOS often aims for:", ["Random levels", "Liquidity beyond structure", "Nothing", "Equilibrium"], 1),
        ("BOS After Sweep", "BOS following liquidity grab.", "Sweep then BOS:", ["Is weak", "Is powerful combo", "Is random", "Nothing"], 1),
        ("BOS Creating Liquidity", "New structure creates pools.", "Each BOS creates:", ["Nothing", "New liquidity above/below", "Random pools", "Removes liquidity"], 1),
        ("BOS Through Liquidity", "Breaking multiple pools.", "BOS through stacked liquidity:", ["Stops there", "May continue to next pool", "Is random", "Nothing"], 1),
        ("BOS and Protected Levels", "BOS breaking protected structure.", "BOS of protected level:", ["Is weak", "Is very significant", "Is random", "Nothing"], 1),
        ("BOS and Unprotected", "Breaking vulnerable levels.", "Unprotected level BOS:", ["Is more significant", "Is less significant", "Is the same", "Nothing"], 1),
        ("BOS Target Liquidity", "Using liquidity as BOS target.", "After bullish BOS, target:", ["SSL below", "BSL above", "Random", "Nothing"], 1),
        ("BOS and EQH/EQL", "BOS of equal levels.", "BOS of equal highs:", ["Is random", "Is significant liquidity grab", "Is weak", "Nothing"], 1),
        ("Liquidity BOS Entry", "Entry using liquidity and BOS.", "Best entry is:", ["Before BOS", "On BOS into liquidity then retest", "Random", "Never"], 1),
        ("BOS Liquidity Failure", "When BOS doesn't reach liquidity.", "BOS failing before liquidity:", ["Is bullish", "May indicate reversal", "Is random", "Nothing"], 1),
    ],
    6: [
        ("BOS and Order Blocks", "Relationship with OB.", "BOS candle prior often:", ["Is nothing", "Becomes order block", "Is random", "Disappears"], 1),
        ("BOS Into OB", "Breaking structure into OB.", "BOS followed by pullback to OB:", ["Is weak", "Is high probability entry", "Is random", "Nothing"], 1),
        ("OB Validation via BOS", "BOS confirms OB significance.", "OB with strong BOS:", ["Is weaker", "Is more significant", "Is random", "Nothing"], 1),
        ("BOS and Mitigation", "BOS after OB mitigation.", "OB mitigation followed by BOS:", ["Is random", "Confirms OB held", "Is weak", "Nothing"], 1),
        ("Chained BOS/OB", "Series of BOS creating OBs.", "Each BOS creates:", ["Nothing", "New OB for future reference", "Random level", "Removes OBs"], 1),
        ("BOS and FVG", "FVG during BOS.", "BOS with FVG:", ["Is weaker", "Shows imbalance/strong move", "Is random", "Nothing"], 1),
        ("Trading BOS + OB", "Combined strategy.", "Enter at OB after BOS:", ["Is random", "Is systematic approach", "Is weak", "Nothing"], 1),
        ("Failed BOS and OB", "When BOS fails at OB.", "BOS failing into OB:", ["Is random", "May indicate OB failure", "Confirms OB", "Nothing"], 1),
        ("BOS OB Timeframes", "Multi-TF OB/BOS.", "HTF OB with LTF BOS:", ["Is weak", "Is high probability", "Is random", "Nothing"], 1),
        ("BOS OB Management", "Managing trades.", "After BOS+OB entry:", ["Exit immediately", "Manage based on structure", "Random exit", "Nothing"], 1),
    ],
    7: [
        ("BOS and ChoCH Difference", "Breaking with vs against trend.", "BOS is with trend, ChoCH is:", ["Also with trend", "Against current trend", "The same", "Random"], 1),
        ("BOS After ChoCH", "BOS following ChoCH.", "ChoCH then BOS confirms:", ["Nothing", "New trend direction", "Old trend", "Random"], 1),
        ("BOS vs ChoCH Trading", "Different strategies.", "Trade BOS for continuation, ChoCH for:", ["Continuation", "Reversal", "Both same", "Nothing"], 1),
        ("Identifying BOS vs ChoCH", "Correct identification.", "Key difference is:", ["Candle size", "Direction relative to prior trend", "Volume", "Nothing"], 1),
        ("Mixed Signals", "When confused between two.", "If uncertain, wait for:", ["Random trade", "Confirmation of direction", "Either signal", "Nothing"], 1),
        ("BOS in New Trend", "BOS after ChoCH establishes trend.", "After confirmed ChoCH, next break is:", ["ChoCH", "BOS in new direction", "Random", "Nothing"], 1),
        ("ChoCH Failed BOS", "ChoCH that fails to BOS.", "ChoCH without follow-up BOS:", ["Is strong", "May be false signal", "Is random", "Confirms reversal"], 1),
        ("BOS Confirming ChoCH", "How BOS validates ChoCH.", "BOS after ChoCH:", ["Is weak", "Confirms trend change", "Is random", "Negates ChoCH"], 1),
        ("Trading the Transition", "ChoCH to BOS transition trade.", "Best transition entry:", ["On ChoCH", "On first BOS after ChoCH", "Before ChoCH", "Random"], 1),
        ("Structure Shift Complete", "Full shift requires both.", "Complete shift needs:", ["ChoCH only", "ChoCH + BOS in new direction", "BOS only", "Nothing"], 1),
    ],
    8: [
        ("HTF BOS Importance", "Major timeframe breaks.", "Daily BOS is:", ["Same as 5min", "Much more significant", "Less important", "Random"], 1),
        ("LTF BOS Precision", "Lower TF for entries.", "LTF BOS helps with:", ["Direction", "Entry precision", "Nothing", "Exit only"], 1),
        ("MTF BOS Alignment", "Multiple TF agreement.", "H4, H1, M15 BOS same direction:", ["Is weak", "Is very strong", "Is random", "Means nothing"], 1),
        ("HTF BOS LTF Entry", "Big picture, precise entry.", "Trade HTF BOS using:", ["HTF entry", "LTF entry at pullback", "Random TF", "Nothing"], 1),
        ("Conflicting TF BOS", "Different TF show different BOS.", "LTF bearish BOS, HTF bullish:", ["Strong short", "Probably just pullback", "HTF is wrong", "Random"], 1),
        ("TF Selection for BOS", "Choosing right timeframes.", "Swing trader uses:", ["M1 BOS", "H4/Daily BOS", "Random TF", "All TF equally"], 1),
        ("Cascading BOS", "BOS flowing down timeframes.", "HTF BOS leads to LTF:", ["Random moves", "BOS in same direction", "Opposite moves", "Nothing"], 1),
        ("Intraday BOS", "Session-based BOS.", "Asian high break during London:", ["Is random", "Is session BOS", "Means nothing", "Is reversal"], 1),
        ("Swing BOS", "Multi-day structure breaks.", "Weekly BOS significance:", ["Low", "Very high", "Same as hourly", "Random"], 1),
        ("Position BOS", "Long-term BOS.", "Monthly BOS for:", ["Scalping", "Position trading", "Day trading", "Random"], 1),
    ],
    9: [
        ("BOS Trade Plan", "Complete BOS trading system.", "BOS plan includes:", ["Random entries", "Entry, stop, target rules", "Just entry", "Nothing"], 1),
        ("BOS Checklist", "Pre-trade verification.", "Before BOS trade, check:", ["Nothing", "Trend, structure, confirmation", "Random factors", "Just price"], 1),
        ("BOS Journal", "Recording BOS trades.", "Journal BOS trades to:", ["Waste time", "Improve over time", "Nothing", "Forget them"], 1),
        ("BOS Mistakes", "Common errors.", "Common BOS mistake:", ["Trading too slow", "Trading without confirmation", "Waiting too long", "Nothing"], 1),
        ("BOS Psychology", "Mental aspects.", "BOS requires:", ["Impulse", "Patience for confirmation", "Fear", "Nothing"], 1),
        ("BOS and Risk", "Risk management.", "Risk per BOS trade:", ["100% of account", "1-2% of account", "Random", "All or nothing"], 1),
        ("BOS Win Rate", "Expected success rate.", "Good BOS strategy has:", ["100% win rate", "50-60% win rate with good R:R", "10% win rate", "Random"], 1),
        ("BOS Scaling", "Position sizing for BOS.", "Better BOS setup means:", ["Same size always", "Potentially larger size", "Smaller size", "No trade"], 0),
        ("BOS Review", "Analyzing past BOS trades.", "Review trades to:", ["Feel bad", "Learn and improve", "Waste time", "Nothing"], 1),
        ("BOS Mastery", "Becoming expert at BOS.", "BOS mastery requires:", ["One trade", "Hundreds of observed setups", "Luck", "Nothing"], 1),
    ],
    10: [
        ("Complete BOS Understanding", "Full BOS comprehension.", "Master BOS trader:", ["Sees random breaks", "Sees structure narrative", "Ignores BOS", "Trades randomly"], 1),
        ("Real-Time BOS", "Live BOS identification.", "Mark BOS:", ["Only in hindsight", "As it happens with confirmation", "Randomly", "Never"], 1),
        ("BOS Integration", "BOS in complete system.", "BOS should be:", ["Only strategy", "Part of complete analysis", "Ignored", "Random factor"], 1),
        ("Advanced BOS", "Complex BOS scenarios.", "Complex BOS situations require:", ["Basic knowledge", "Deep understanding", "Luck", "Nothing"], 1),
        ("BOS Adaptation", "Adapting to conditions.", "In ranging markets, BOS:", ["Is the same", "May lead to fakeouts", "Is stronger", "Nothing"], 1),
        ("BOS and News", "BOS during news.", "News-driven BOS:", ["Is always real", "Needs extra confirmation", "Is random", "Should be ignored"], 1),
        ("BOS Edge", "Edge from BOS trading.", "BOS provides edge through:", ["Random entries", "Structured trend trading", "Luck", "Nothing"], 1),
        ("BOS Teaching", "Explaining BOS to others.", "Teaching BOS:", ["Wastes time", "Reinforces understanding", "Is impossible", "Nothing"], 1),
        ("Continuous BOS Learning", "Always improving.", "BOS skills improve through:", ["One course", "Continuous practice", "Luck", "Nothing"], 1),
        ("BOS in Trading Career", "Long-term BOS use.", "BOS will always be:", ["Outdated", "Relevant for trend trading", "Random", "Useless"], 1),
    ],
}

# ==================== 5. CHANGE OF CHARACTER (CHOCH) ====================
CHOCH = {
    1: [
        ("ChoCH Definition", "Change of Character signals potential reversal.", "ChoCH means:", ["Trend continues", "Potential trend change", "Nothing", "Ranging market"], 1),
        ("Bullish ChoCH", "Breaking high in downtrend.", "Bullish ChoCH breaks:", ["Lower low", "Previous high in downtrend", "Random level", "Nothing"], 1),
        ("Bearish ChoCH", "Breaking low in uptrend.", "Bearish ChoCH breaks:", ["Higher high", "Previous low in uptrend", "Random", "Nothing"], 1),
        ("ChoCH vs BOS", "Key difference.", "ChoCH is break against trend, BOS is:", ["Also against trend", "Break with current trend", "The same", "Random"], 1),
        ("ChoCH Significance", "Why ChoCH matters.", "ChoCH signals:", ["Continuation", "First sign of possible reversal", "Nothing", "Stronger trend"], 1),
        ("ChoCH Location", "Where ChoCH is most reliable.", "ChoCH at key level is:", ["Less reliable", "More reliable", "Same everywhere", "Random"], 1),
        ("ChoCH Confirmation", "When ChoCH is confirmed.", "ChoCH confirmed by:", ["Wick touch", "Candle body close beyond level", "Nothing", "Time"], 1),
        ("Single ChoCH", "One ChoCH signal.", "Single ChoCH is:", ["Confirmed reversal", "Warning sign, needs confirmation", "Nothing", "Random"], 1),
        ("ChoCH Candle", "The candle creating ChoCH.", "Strong ChoCH candle:", ["Small and weak", "Shows momentum", "Is always doji", "Nothing"], 1),
        ("ChoCH Timeframe", "TF significance.", "HTF ChoCH is:", ["Less significant", "More significant", "Same as LTF", "Random"], 1),
    ],
    2: [
        ("ChoCH After Extended Move", "ChoCH at end of trend.", "ChoCH after long trend is:", ["Less significant", "More significant", "Random", "Nothing"], 1),
        ("ChoCH at Key Levels", "S/R and ChoCH.", "ChoCH at major resistance:", ["Is weak", "Is high probability", "Is random", "Nothing"], 1),
        ("ChoCH and Liquidity", "Sweep before ChoCH.", "Sweep followed by ChoCH:", ["Is weak signal", "Is strong reversal signal", "Is random", "Nothing"], 1),
        ("ChoCH Speed", "Fast vs slow ChoCH.", "Fast ChoCH shows:", ["Weak conviction", "Strong reversal intent", "Nothing", "Continuation"], 1),
        ("ChoCH Depth", "How far ChoCH extends.", "Deep ChoCH is:", ["Weaker", "Stronger confirmation", "Random", "Nothing"], 1),
        ("ChoCH Without Sweep", "ChoCH without prior liquidity grab.", "ChoCH without sweep:", ["Is invalid", "Is valid but less ideal", "Is stronger", "Nothing"], 1),
        ("ChoCH and FVG", "FVG during ChoCH.", "ChoCH with FVG:", ["Is weaker", "Shows strong imbalance", "Is random", "Nothing"], 1),
        ("ChoCH Quality Assessment", "Rating ChoCH signals.", "Best ChoCH has:", ["Weak candle", "Strong candle at key level after sweep", "Random features", "Nothing"], 1),
        ("Minor vs Major ChoCH", "Significance levels.", "Major swing ChoCH vs minor:", ["Minor is stronger", "Major is more significant", "Both equal", "Nothing"], 1),
        ("ChoCH Filtering", "Avoiding weak signals.", "Filter out ChoCH that:", ["Is at key level", "Has no context or confluence", "Is strong", "Has liquidity"], 1),
    ],
    3: [
        ("Trading ChoCH", "How to trade ChoCH signals.", "Trade ChoCH by:", ["Entering on ChoCH candle", "Waiting for pullback after ChoCH", "Fading it", "Random"], 1),
        ("ChoCH Entry Point", "Where to enter.", "Best ChoCH entry:", ["On the break", "On pullback to broken level", "Before break", "Random"], 1),
        ("ChoCH Stop Loss", "Stop placement.", "Stop goes:", ["At entry", "Beyond structure that caused ChoCH", "Random", "Very tight"], 1),
        ("ChoCH Target", "Profit target.", "ChoCH target is often:", ["Entry point", "Opposite liquidity pool", "Random", "Nothing"], 1),
        ("ChoCH R:R", "Risk to reward.", "Aim for at least:", ["1:0.5", "1:2 or better", "1:1", "Random"], 1),
        ("ChoCH Confirmation Entry", "Extra confirmation.", "Use LTF for:", ["Direction", "Precise entry after ChoCH", "Nothing", "Exit only"], 1),
        ("Aggressive ChoCH Entry", "Entry on the break.", "Aggressive entry:", ["Has better R:R", "Has faster fill but more risk", "Is always best", "Never works"], 1),
        ("Conservative ChoCH Entry", "Waiting for retest.", "Conservative approach:", ["Is worse", "Gives better confirmation", "Is random", "Never works"], 1),
        ("Managing ChoCH Trade", "After entry.", "Watch for:", ["Nothing", "BOS in new direction for confirmation", "Random moves", "Exit immediately"], 1),
        ("ChoCH Trade Size", "Position sizing.", "ChoCH trade size based on:", ["Random", "Risk management rules", "All-in always", "Nothing"], 1),
    ],
    4: [
        ("ChoCH + BOS Sequence", "Full reversal confirmation.", "ChoCH followed by BOS:", ["Is weak", "Confirms new trend direction", "Is random", "Means nothing"], 1),
        ("Waiting for BOS", "Why wait for BOS after ChoCH.", "BOS confirms:", ["Original trend", "ChoCH was real, new trend starting", "Nothing", "Reversal failed"], 1),
        ("ChoCH to BOS Timing", "How long to wait.", "BOS should come:", ["Immediately", "Within reasonable structure development", "Never", "After years"], 1),
        ("Failed ChoCH", "ChoCH without follow-through.", "ChoCH without BOS:", ["Confirms reversal", "May be false/trap", "Is stronger", "Always works"], 1),
        ("Multiple ChoCH", "Several ChoCH signals.", "Two or more ChoCH:", ["Weakens signal", "Strengthens reversal probability", "Is random", "Nothing"], 1),
        ("ChoCH BOS Entry", "Trading the sequence.", "Best entry is on:", ["ChoCH", "BOS after ChoCH confirmation", "Before ChoCH", "Random"], 1),
        ("Complete Structure Shift", "Full trend reversal.", "Shift requires:", ["ChoCH only", "ChoCH + BOS in new direction", "BOS only", "Nothing"], 1),
        ("Tracking ChoCH to BOS", "Monitoring the progression.", "After ChoCH, watch:", ["Nothing", "Structure developing in new direction", "Original trend", "Random"], 1),
        ("ChoCH BOS Failure", "When sequence fails.", "If BOS fails after ChoCH:", ["Reversal is confirmed", "Original trend may resume", "Nothing happens", "Random"], 1),
        ("ChoCH BOS Timeframes", "Multi-TF application.", "HTF ChoCH, LTF BOS entry:", ["Is weak", "Is optimal approach", "Is random", "Never works"], 1),
    ],
    5: [
        ("ChoCH and Order Blocks", "OB relationship.", "ChoCH often returns to:", ["Random level", "Order block for entry", "Nothing", "Equilibrium"], 1),
        ("OB Entry After ChoCH", "Using OB for entry.", "After bullish ChoCH, look for:", ["Bearish OB", "Bullish OB for entry", "Random level", "Nothing"], 1),
        ("ChoCH Creating OB", "New OB from ChoCH.", "ChoCH candle can become:", ["Nothing", "New order block", "Random level", "FVG only"], 1),
        ("OB Quality After ChoCH", "Evaluating the OB.", "OB from strong ChoCH:", ["Is weaker", "Is high quality", "Is random", "Doesn't exist"], 1),
        ("Trading ChoCH OB", "Execution strategy.", "Enter at OB after ChoCH when:", ["Price immediately continues", "Price pulls back to OB", "Random", "Never"], 1),
        ("ChoCH and FVG", "FVG during ChoCH.", "FVG with ChoCH:", ["Weakens signal", "Adds confluence", "Is random", "Should be ignored"], 1),
        ("Mitigation After ChoCH", "OB mitigation in new direction.", "OB mitigation confirms:", ["Original trend", "New direction likely to continue", "Nothing", "Random"], 1),
        ("ChoCH OB Stop", "Stop placement.", "Stop beyond:", ["Entry", "OB that price should hold", "Random level", "Nothing"], 1),
        ("ChoCH OB Target", "Profit target.", "Target opposite:", ["Nothing", "Liquidity or structure", "Entry point", "Random"], 1),
        ("Multi-TF ChoCH OB", "Combining timeframes.", "HTF ChoCH, LTF OB entry:", ["Is overcomplicated", "Is precise approach", "Is random", "Never works"], 1),
    ],
    6: [
        ("ChoCH at Supply/Demand", "Zone confluence.", "ChoCH at HTF supply:", ["Is weaker", "Is high probability short", "Is bullish", "Is random"], 1),
        ("Zone ChoCH Entry", "Trading zone ChoCH.", "Enter when:", ["Price breaks zone", "ChoCH occurs at zone", "Random", "Before reaching zone"], 1),
        ("Premium ChoCH", "ChoCH in premium zone.", "Bearish ChoCH in premium:", ["Is weak", "Is aligned/high probability", "Is bullish", "Nothing"], 1),
        ("Discount ChoCH", "ChoCH in discount zone.", "Bullish ChoCH in discount:", ["Is weak", "Is aligned/high probability", "Is bearish", "Nothing"], 1),
        ("ChoCH Zone Quality", "Rating zone setups.", "Best zone ChoCH:", ["Has no confirmation", "Has sweep + strong candle", "Is random", "Is in equilibrium"], 1),
        ("Failed Zone ChoCH", "When ChoCH fails at zone.", "Zone ChoCH failure:", ["Never happens", "Suggests zone may break", "Confirms zone", "Is random"], 1),
        ("Multi-Zone ChoCH", "Multiple zones aligning.", "ChoCH at multiple confluent zones:", ["Is weak", "Is very high probability", "Is random", "Nothing"], 1),
        ("Zone ChoCH Management", "Managing the trade.", "If ChoCH zone trade:", ["Exit immediately", "Manage based on structure", "Random exit", "Never exit"], 1),
        ("Zone Selection for ChoCH", "Which zones to trade.", "Trade ChoCH at:", ["All zones", "High quality HTF zones", "Random zones", "No zones"], 1),
        ("Zone ChoCH Journal", "Recording zone ChoCH.", "Journal to:", ["Waste time", "Track zone ChoCH performance", "Nothing", "Random"], 1),
    ],
    7: [
        ("HTF ChoCH", "Higher timeframe signals.", "Daily ChoCH is:", ["Same as 5min", "Much more significant", "Less important", "Random"], 1),
        ("LTF ChoCH", "Lower timeframe signals.", "LTF ChoCH within HTF trend:", ["Confirms reversal", "May just be pullback", "Is stronger", "Nothing"], 1),
        ("MTF ChoCH Alignment", "Multiple TFs agree.", "H4, H1, M15 ChoCH same direction:", ["Is weak", "Is strong confluence", "Is random", "Nothing"], 1),
        ("HTF ChoCH LTF Entry", "Combined approach.", "Trade HTF ChoCH using:", ["HTF entry", "LTF for precise entry", "Random TF", "Nothing"], 1),
        ("Conflicting TF ChoCH", "Different directions.", "LTF bearish ChoCH, HTF bullish:", ["Strong short setup", "Probably pullback in HTF trend", "HTF is wrong", "Random"], 1),
        ("ChoCH TF Selection", "Right timeframes.", "Swing trader uses:", ["M1 ChoCH", "H4/Daily ChoCH", "Random TF", "All equally"], 1),
        ("Intraday ChoCH", "Session reversals.", "Session high ChoCH:", ["Is major reversal", "Is intraday reversal opportunity", "Is random", "Nothing"], 1),
        ("Swing ChoCH", "Multi-day reversals.", "Weekly ChoCH:", ["Is minor", "Is very significant", "Is random", "Same as hourly"], 1),
        ("Position ChoCH", "Long-term reversals.", "Monthly ChoCH for:", ["Scalping", "Position/investment trades", "Day trading", "Random"], 1),
        ("TF ChoCH Journal", "Recording multi-TF ChoCH.", "Note which TF ChoCH:", ["Is random", "Performs best for your style", "All same", "Nothing"], 1),
    ],
    8: [
        ("Liquidity Sweep ChoCH", "Sweep before ChoCH.", "Sweep + ChoCH is:", ["Random", "Classic reversal setup", "Weak signal", "Nothing"], 1),
        ("EQH Sweep ChoCH", "Equal highs swept then ChoCH.", "EQH sweep then ChoCH down:", ["Is bullish", "Is strong bearish signal", "Is random", "Nothing"], 1),
        ("EQL Sweep ChoCH", "Equal lows swept then ChoCH.", "EQL sweep then ChoCH up:", ["Is bearish", "Is strong bullish signal", "Is random", "Nothing"], 1),
        ("PDH/PDL ChoCH", "Daily level sweep ChoCH.", "PDH sweep then ChoCH:", ["Is random", "Is high probability setup", "Is weak", "Nothing"], 1),
        ("Session Sweep ChoCH", "Session high/low sweeps.", "Asian high sweep + London ChoCH:", ["Is random", "Is classic session reversal", "Is weak", "Nothing"], 1),
        ("ChoCH Without Sweep", "Valid without sweep?", "ChoCH without sweep is:", ["Invalid", "Valid but less ideal", "Stronger", "Random"], 1),
        ("Sweep ChoCH Entry", "Trading the combo.", "Enter after:", ["Sweep only", "Sweep + ChoCH confirmation", "Before sweep", "Random"], 1),
        ("Sweep ChoCH Stop", "Stop placement.", "Stop should be:", ["Very tight", "Beyond sweep/liquidity level", "Random", "At entry"], 1),
        ("Sweep ChoCH Target", "Profit target.", "Target opposite:", ["Nothing", "Liquidity pool", "Entry", "Random"], 1),
        ("Multiple Sweep ChoCH", "Several sweeps before ChoCH.", "Multiple sweeps then ChoCH:", ["Is weaker", "May be stronger signal", "Is random", "Never happens"], 1),
    ],
    9: [
        ("ChoCH Trading Plan", "Complete system.", "ChoCH plan includes:", ["Just entry", "Entry, stop, target, management", "Random rules", "Nothing"], 1),
        ("ChoCH Checklist", "Pre-trade verification.", "Before ChoCH trade, verify:", ["Nothing", "Trend, level, sweep, confirmation", "Random factors", "Just price"], 1),
        ("ChoCH Psychology", "Mental aspects.", "ChoCH trading requires:", ["Impulsive action", "Patience for confirmation", "Fear", "Greed"], 1),
        ("ChoCH Risk Management", "Position sizing.", "Risk per trade:", ["100% account", "1-2% account", "Random", "All-in"], 1),
        ("ChoCH Win Rate", "Expected performance.", "Good ChoCH strategy:", ["Wins 100%", "Wins 40-50% with good R:R", "Loses always", "Random"], 1),
        ("ChoCH Review", "Analyzing trades.", "Review to:", ["Feel bad", "Improve future ChoCH trades", "Waste time", "Nothing"], 1),
        ("ChoCH Mistakes", "Common errors.", "Common mistake is:", ["Trading too slow", "Trading ChoCH without confirmation", "Waiting too long", "Nothing"], 1),
        ("ChoCH Adaptation", "Different market conditions.", "In ranging markets, ChoCH:", ["Is more reliable", "May lead to fakeouts", "Is stronger", "Nothing"], 1),
        ("ChoCH Journal", "Recording trades.", "Journal ChoCH trades to:", ["Waste time", "Track and improve", "Nothing", "Random"], 1),
        ("ChoCH Mastery", "Becoming expert.", "Master ChoCH through:", ["One course", "Hundreds of observations", "Luck", "Nothing"], 1),
    ],
    10: [
        ("Complete ChoCH Understanding", "Full comprehension.", "Master ChoCH trader:", ["Trades all ChoCH", "Selects high probability ChoCH", "Ignores ChoCH", "Random"], 1),
        ("Real-Time ChoCH", "Live identification.", "Mark ChoCH:", ["Only in hindsight", "As it forms with confirmation", "Randomly", "Never"], 1),
        ("ChoCH in System", "Part of complete trading.", "ChoCH is:", ["Complete system", "One tool in complete system", "Useless", "Random"], 1),
        ("Advanced ChoCH", "Complex scenarios.", "Complex ChoCH requires:", ["Basic knowledge", "Deep understanding of context", "Luck", "Nothing"], 1),
        ("ChoCH Edge", "Trading edge.", "ChoCH provides edge through:", ["Random reversals", "Structured reversal trading", "Luck", "Nothing"], 1),
        ("ChoCH and News", "News impact.", "News-driven ChoCH:", ["Is always real", "Needs extra caution", "Is random", "Should be ignored"], 1),
        ("ChoCH Teaching", "Explaining to others.", "Teaching ChoCH:", ["Wastes time", "Reinforces your understanding", "Is impossible", "Nothing"], 1),
        ("Continuous Learning", "Always improving.", "ChoCH mastery needs:", ["One study session", "Continuous practice", "Luck", "Nothing"], 1),
        ("ChoCH Career", "Long-term use.", "ChoCH will be:", ["Outdated soon", "Always relevant for reversals", "Random", "Useless"], 1),
        ("ChoCH Integration", "Full trading integration.", "Combine ChoCH with:", ["Nothing else", "All SMC concepts for best results", "Indicators only", "Random factors"], 1),
    ],
}

# ==================== REMAINING CATEGORIES ====================
# Adding simplified data for remaining categories

ORDER_BLOCKS = {level: [
    (f"Order Block L{level} Q{i+1}", f"Order block concept level {level}", f"Order block question {i+1}?", ["Option A", "Option B", "Option C", "Option D"], 1)
    for i in range(10)
] for level in range(1, 11)}

FVG = {level: [
    (f"Fair Value Gap L{level} Q{i+1}", f"FVG concept level {level}", f"FVG question {i+1}?", ["Option A", "Option B", "Option C", "Option D"], 1)
    for i in range(10)
] for level in range(1, 11)}

LIQUIDITY_SWEEPS = {level: [
    (f"Liquidity Sweep L{level} Q{i+1}", f"Sweep concept level {level}", f"Sweep question {i+1}?", ["Option A", "Option B", "Option C", "Option D"], 1)
    for i in range(10)
] for level in range(1, 11)}

PREMIUM_DISCOUNT = {level: [
    (f"Premium Discount L{level} Q{i+1}", f"Premium/discount concept level {level}", f"Premium/discount question {i+1}?", ["Option A", "Option B", "Option C", "Option D"], 1)
    for i in range(10)
] for level in range(1, 11)}

INDUCEMENT = {level: [
    (f"Inducement L{level} Q{i+1}", f"Inducement concept level {level}", f"Inducement question {i+1}?", ["Option A", "Option B", "Option C", "Option D"], 1)
    for i in range(10)
] for level in range(1, 11)}

MULTI_TIMEFRAME = {level: [
    (f"Multi-Timeframe L{level} Q{i+1}", f"MTF concept level {level}", f"MTF question {i+1}?", ["Option A", "Option B", "Option C", "Option D"], 1)
    for i in range(10)
] for level in range(1, 11)}

ENTRY_MODELS = {level: [
    (f"Entry Model L{level} Q{i+1}", f"Entry model concept level {level}", f"Entry question {i+1}?", ["Option A", "Option B", "Option C", "Option D"], 1)
    for i in range(10)
] for level in range(1, 11)}

RISK_MANAGEMENT = {level: [
    (f"Risk Management L{level} Q{i+1}", f"Risk concept level {level}", f"Risk question {i+1}?", ["Option A", "Option B", "Option C", "Option D"], 1)
    for i in range(10)
] for level in range(1, 11)}

PSYCHOLOGY = {level: [
    (f"Psychology L{level} Q{i+1}", f"Psychology concept level {level}", f"Psychology question {i+1}?", ["Option A", "Option B", "Option C", "Option D"], 1)
    for i in range(10)
] for level in range(1, 11)}

# Master mapping of all curriculum data
CURRICULUM_DATA = {
    "candlesticks": CANDLESTICKS,
    "market-structure": MARKET_STRUCTURE,
    "liquidity": LIQUIDITY,
    "bos": BOS,
    "choch": CHOCH,
    "order-blocks": ORDER_BLOCKS,
    "fvg": FVG,
    "liquidity-sweeps": LIQUIDITY_SWEEPS,
    "premium-discount": PREMIUM_DISCOUNT,
    "inducement": INDUCEMENT,
    "multi-timeframe": MULTI_TIMEFRAME,
    "entry-models": ENTRY_MODELS,
    "risk-management": RISK_MANAGEMENT,
    "psychology": PSYCHOLOGY,
}

def get_exercises_for_level(category_id: str, level: int):
    """Get exercises for a specific category and level"""
    if category_id in CURRICULUM_DATA:
        if level in CURRICULUM_DATA[category_id]:
            return CURRICULUM_DATA[category_id][level]
    return None


# ==================== IMAGE-BASED QUESTIONS ====================
# Each level has 5 image questions (for exercises 2, 4, 6, 8, 10)
# These alternate with text questions (exercises 1, 3, 5, 7, 9)
#
# HOW TO EDIT:
# 1. Replace "question_image" URL with your question chart image
# 2. Replace "options" URLs with 4 different chart images (one correct)
# 3. Set "correct_answer" to the index of correct image (0=first, 1=second, etc)
# ==================================================================

# Placeholder image URLs - REPLACE THESE WITH YOUR OWN IMAGES!
PLACEHOLDER_IMAGES = {
    "bullish_candle": "https://cdn.pixabay.com/photo/2021/02/14/18/28/stock-6014940_1280.png",
    "bearish_candle": "https://cdn.pixabay.com/photo/2018/08/08/10/19/chart-3592236_1280.jpg",
    "doji": "https://cdn.pixabay.com/photo/2021/01/25/12/43/bitcoin-5948838_1280.jpg",
    "hammer": "https://cdn.pixabay.com/photo/2018/02/04/09/09/bitcoin-3129440_1280.jpg",
    "engulfing": "https://cdn.pixabay.com/photo/2017/03/17/10/29/chart-2151021_1280.png",
    "chart_1": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400",
    "chart_2": "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=400",
    "chart_3": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=400",
    "chart_4": "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=400",
    "chart_5": "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=400",
    "chart_6": "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=400",
    "chart_7": "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=400",
    "chart_8": "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=400",
}

def generate_image_questions_for_level(category_id: str, level: int):
    """Generate 5 image questions for a level"""
    questions = []
    for i in range(5):
        questions.append({
            "title": f"Image Question {i+1}",
            "explanation": f"Identify the correct {category_id} pattern for level {level}",
            "question": f"Which image shows the correct {category_id.replace('-', ' ')} pattern?",
            "question_image": PLACEHOLDER_IMAGES["chart_1"],
            "options": [
                PLACEHOLDER_IMAGES["chart_1"],
                PLACEHOLDER_IMAGES["chart_2"],
                PLACEHOLDER_IMAGES["chart_3"],
                PLACEHOLDER_IMAGES["chart_4"],
            ],
            "correct_answer": 0,  # First image is correct - CHANGE THIS!
            "feedback_correct": "Excellent! You identified the pattern correctly! 🎯",
            "feedback_wrong": "Not quite. Look more carefully at the pattern characteristics."
        })
    return questions

# ==================== CANDLESTICKS IMAGE QUESTIONS ====================
CANDLESTICKS_IMAGES = {
    1: [  # Level 1 - 5 image questions
        {
            "title": "Identify Bullish Candle",
            "explanation": "A bullish candle closes higher than it opens",
            "question": "Which image shows a BULLISH candle?",
            "question_image": None,  # No question image needed
            "options": [
                "https://cdn.pixabay.com/photo/2021/02/14/18/28/stock-6014940_1280.png",  # A - Correct
                "https://cdn.pixabay.com/photo/2018/08/08/10/19/chart-3592236_1280.jpg",  # B
                "https://cdn.pixabay.com/photo/2021/01/25/12/43/bitcoin-5948838_1280.jpg",  # C
                "https://cdn.pixabay.com/photo/2018/02/04/09/09/bitcoin-3129440_1280.jpg",  # D
            ],
            "correct_answer": 0,
            "feedback_correct": "Correct! The green/white candle closing higher is bullish! 🎯",
            "feedback_wrong": "Not quite. Bullish candles are green/white and close above the open."
        },
        {
            "title": "Identify Bearish Candle",
            "explanation": "A bearish candle closes lower than it opens",
            "question": "Which image shows a BEARISH candle?",
            "question_image": None,
            "options": [
                "https://cdn.pixabay.com/photo/2021/02/14/18/28/stock-6014940_1280.png",  # A
                "https://cdn.pixabay.com/photo/2018/08/08/10/19/chart-3592236_1280.jpg",  # B - Correct
                "https://cdn.pixabay.com/photo/2021/01/25/12/43/bitcoin-5948838_1280.jpg",  # C
                "https://cdn.pixabay.com/photo/2018/02/04/09/09/bitcoin-3129440_1280.jpg",  # D
            ],
            "correct_answer": 1,
            "feedback_correct": "Correct! The red/black candle closing lower is bearish! 🎯",
            "feedback_wrong": "Not quite. Bearish candles are red/black and close below the open."
        },
        {
            "title": "Identify Doji",
            "explanation": "A doji has nearly equal open and close",
            "question": "Which image shows a DOJI candle?",
            "question_image": None,
            "options": [
                "https://cdn.pixabay.com/photo/2021/02/14/18/28/stock-6014940_1280.png",  # A
                "https://cdn.pixabay.com/photo/2018/08/08/10/19/chart-3592236_1280.jpg",  # B
                "https://cdn.pixabay.com/photo/2021/01/25/12/43/bitcoin-5948838_1280.jpg",  # C - Correct
                "https://cdn.pixabay.com/photo/2018/02/04/09/09/bitcoin-3129440_1280.jpg",  # D
            ],
            "correct_answer": 2,
            "feedback_correct": "Correct! The doji shows indecision with open ≈ close! 🎯",
            "feedback_wrong": "A doji has a very small or no body (open equals close)."
        },
        {
            "title": "Identify Long Wick",
            "explanation": "Long wicks show price rejection",
            "question": "Which image shows a candle with LONG UPPER WICK?",
            "question_image": None,
            "options": [
                "https://cdn.pixabay.com/photo/2021/02/14/18/28/stock-6014940_1280.png",  # A
                "https://cdn.pixabay.com/photo/2018/08/08/10/19/chart-3592236_1280.jpg",  # B
                "https://cdn.pixabay.com/photo/2021/01/25/12/43/bitcoin-5948838_1280.jpg",  # C
                "https://cdn.pixabay.com/photo/2018/02/04/09/09/bitcoin-3129440_1280.jpg",  # D - Correct
            ],
            "correct_answer": 3,
            "feedback_correct": "Correct! Long upper wick shows rejection from highs! 🎯",
            "feedback_wrong": "Long upper wick extends far above the candle body."
        },
        {
            "title": "Identify Marubozu",
            "explanation": "Marubozu has no wicks - pure momentum",
            "question": "Which image shows a MARUBOZU candle?",
            "question_image": None,
            "options": [
                "https://cdn.pixabay.com/photo/2017/03/17/10/29/chart-2151021_1280.png",  # A - Correct
                "https://cdn.pixabay.com/photo/2018/08/08/10/19/chart-3592236_1280.jpg",  # B
                "https://cdn.pixabay.com/photo/2021/01/25/12/43/bitcoin-5948838_1280.jpg",  # C
                "https://cdn.pixabay.com/photo/2018/02/04/09/09/bitcoin-3129440_1280.jpg",  # D
            ],
            "correct_answer": 0,
            "feedback_correct": "Correct! Marubozu has no wicks - open=low, close=high (or vice versa)! 🎯",
            "feedback_wrong": "Marubozu is a long candle with NO wicks (shadows)."
        },
    ],
    # Levels 2-10 use generated questions - EDIT THESE!
    **{level: generate_image_questions_for_level("candlesticks", level) for level in range(2, 11)}
}

# ==================== MARKET STRUCTURE IMAGE QUESTIONS ====================
MARKET_STRUCTURE_IMAGES = {level: generate_image_questions_for_level("market-structure", level) for level in range(1, 11)}

# ==================== LIQUIDITY IMAGE QUESTIONS ====================
LIQUIDITY_IMAGES = {level: generate_image_questions_for_level("liquidity", level) for level in range(1, 11)}

# ==================== BOS IMAGE QUESTIONS ====================
BOS_IMAGES = {level: generate_image_questions_for_level("bos", level) for level in range(1, 11)}

# ==================== CHOCH IMAGE QUESTIONS ====================
CHOCH_IMAGES = {level: generate_image_questions_for_level("choch", level) for level in range(1, 11)}

# ==================== OTHER CATEGORIES ====================
ORDER_BLOCKS_IMAGES = {level: generate_image_questions_for_level("order-blocks", level) for level in range(1, 11)}
FVG_IMAGES = {level: generate_image_questions_for_level("fvg", level) for level in range(1, 11)}
LIQUIDITY_SWEEPS_IMAGES = {level: generate_image_questions_for_level("liquidity-sweeps", level) for level in range(1, 11)}
PREMIUM_DISCOUNT_IMAGES = {level: generate_image_questions_for_level("premium-discount", level) for level in range(1, 11)}
INDUCEMENT_IMAGES = {level: generate_image_questions_for_level("inducement", level) for level in range(1, 11)}
MULTI_TIMEFRAME_IMAGES = {level: generate_image_questions_for_level("multi-timeframe", level) for level in range(1, 11)}
ENTRY_MODELS_IMAGES = {level: generate_image_questions_for_level("entry-models", level) for level in range(1, 11)}
RISK_MANAGEMENT_IMAGES = {level: generate_image_questions_for_level("risk-management", level) for level in range(1, 11)}
PSYCHOLOGY_IMAGES = {level: generate_image_questions_for_level("psychology", level) for level in range(1, 11)}

# Master mapping of all IMAGE questions
IMAGE_QUESTIONS = {
    "candlesticks": CANDLESTICKS_IMAGES,
    "market-structure": MARKET_STRUCTURE_IMAGES,
    "liquidity": LIQUIDITY_IMAGES,
    "bos": BOS_IMAGES,
    "choch": CHOCH_IMAGES,
    "order-blocks": ORDER_BLOCKS_IMAGES,
    "fvg": FVG_IMAGES,
    "liquidity-sweeps": LIQUIDITY_SWEEPS_IMAGES,
    "premium-discount": PREMIUM_DISCOUNT_IMAGES,
    "inducement": INDUCEMENT_IMAGES,
    "multi-timeframe": MULTI_TIMEFRAME_IMAGES,
    "entry-models": ENTRY_MODELS_IMAGES,
    "risk-management": RISK_MANAGEMENT_IMAGES,
    "psychology": PSYCHOLOGY_IMAGES,
}
