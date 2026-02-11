# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║              🎯 INTERACTIVE EXERCISES - FÁCIL DE EDITAR                      ║
# ║                                                                              ║
# ║  Este arquivo controla os exercícios interativos onde o usuário             ║
# ║  clica no gráfico para identificar padrões                                   ║
# ║                                                                              ║
# ║  APÓS EDITAR:                                                                ║
# ║  1. Salve o arquivo                                                          ║
# ║  2. Execute: curl -X DELETE .../api/interactive/exercises/cache              ║
# ║  3. Execute: sudo supervisorctl restart backend                              ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝


# ══════════════════════════════════════════════════════════════════════════════
# 
#                         📚 TUTORIAL: COMO CRIAR VELAS
# 
# ══════════════════════════════════════════════════════════════════════════════
#
# Cada vela tem 4 preços principais:
#
#     HIGH (máximo) ───────────────  ← Ponto mais alto (pavio superior)
#           │
#           │  ┌─────────┐
#           │  │         │
#     OPEN ─│──┤         │  ← Preço de abertura
#           │  │  CORPO  │
#     CLOSE─│──┤         │  ← Preço de fechamento  
#           │  │         │
#           │  └─────────┘
#           │
#     LOW (mínimo) ────────────────  ← Ponto mais baixo (pavio inferior)
#
#
# REGRAS IMPORTANTES:
# ───────────────────
# • HIGH deve ser o maior valor (>= open, close, low)
# • LOW deve ser o menor valor (<= open, close, high)
# • Se CLOSE > OPEN = Vela VERDE (bullish/alta)
# • Se CLOSE < OPEN = Vela VERMELHA (bearish/baixa)
# • Se CLOSE ≈ OPEN = Vela DOJI (indecisão)
#
# ══════════════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════════════
#
#                    📊 EXERCÍCIOS DE OHLC (NÍVEL 1)
#
#                    Usuário identifica: Open, High, Low, Close
#
# ══════════════════════════════════════════════════════════════════════════════

CANDLES_OHLC = [
    
    # ══════════════════════════════════════════════════════════════════════════
    # VELA 1 - Bullish (Verde)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "time": "2024-01-01",      # Data (não mude, só para o gráfico funcionar)
        
        "open": 100.00,            # ABERTURA: onde a vela começa
        "high": 105.50,            # MÁXIMO: ponto mais alto (pavio superior)
        "low": 99.20,              # MÍNIMO: ponto mais baixo (pavio inferior)
        "close": 104.80,           # FECHAMENTO: onde a vela termina
        
        "type": "bullish",         # Tipo: bullish (verde), bearish (vermelha), doji
        
        # PERGUNTAS CUSTOMIZADAS (opcional - deixe vazio "" para usar padrão)
        "question_open": "",       # Ex: "Onde está o preço de ABERTURA?"
        "question_high": "",       # Ex: "Clique no ponto MAIS ALTO"
        "question_low": "",        # Ex: "Onde está a MÍNIMA?"
        "question_close": "",      # Ex: "Identifique o FECHAMENTO"
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # VELA 2 - Bullish (Verde)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "time": "2024-01-01",
        
        "open": 98.50,             # Vela começa em 98.50
        "high": 103.20,            # Subiu até 103.20
        "low": 97.80,              # Caiu até 97.80
        "close": 102.50,           # Fechou em 102.50 (acima do open = verde)
        
        "type": "bullish",
        
        "question_open": "",
        "question_high": "",
        "question_low": "",
        "question_close": "",
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # VELA 3 - Bullish Grande (movimento forte)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "time": "2024-01-01",
        
        "open": 95.00,
        "high": 99.80,
        "low": 94.50,
        "close": 99.00,
        
        "type": "bullish",
        
        "question_open": "",
        "question_high": "",
        "question_low": "",
        "question_close": "",
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # VELA 4 - Bullish Marubozu (sem pavios/sombras)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "time": "2024-01-01",
        
        "open": 102.00,
        "high": 108.50,
        "low": 101.20,
        "close": 107.80,
        
        "type": "bullish",
        
        "question_open": "",
        "question_high": "",
        "question_low": "",
        "question_close": "",
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # VELA 5 - Bearish (Vermelha)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "time": "2024-01-01",
        
        "open": 105.00,            # Começa em 105
        "high": 106.30,            # Sobe até 106.30
        "low": 99.50,              # Cai até 99.50
        "close": 100.20,           # Fecha em 100.20 (ABAIXO do open = vermelha)
        
        "type": "bearish",
        
        "question_open": "",
        "question_high": "",
        "question_low": "",
        "question_close": "",
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # VELA 6 - Bearish (Vermelha)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "time": "2024-01-01",
        
        "open": 112.00,
        "high": 113.50,
        "low": 107.00,
        "close": 108.00,
        
        "type": "bearish",
        
        "question_open": "",
        "question_high": "",
        "question_low": "",
        "question_close": "",
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # VELA 7 - Bearish Grande
    # ══════════════════════════════════════════════════════════════════════════
    {
        "time": "2024-01-01",
        
        "open": 98.00,
        "high": 99.20,
        "low": 94.00,
        "close": 95.50,
        
        "type": "bearish",
        
        "question_open": "",
        "question_high": "",
        "question_low": "",
        "question_close": "",
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # VELA 8 - Doji (indecisão - open ≈ close)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "time": "2024-01-01",
        
        "open": 100.00,            # Abre em 100
        "high": 103.00,            # Sobe até 103
        "low": 97.00,              # Cai até 97
        "close": 100.10,           # Fecha quase igual ao open = DOJI
        
        "type": "doji",
        
        "question_open": "",
        "question_high": "",
        "question_low": "",
        "question_close": "",
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # VELA 9 - Hammer (Martelo) - pavio longo para baixo
    # ══════════════════════════════════════════════════════════════════════════
    {
        "time": "2024-01-01",
        
        "open": 100.00,
        "high": 100.80,            # Pavio pequeno para cima
        "low": 95.00,              # Pavio LONGO para baixo (rejeição)
        "close": 100.50,
        
        "type": "hammer",
        
        "question_open": "",
        "question_high": "",
        "question_low": "",
        "question_close": "",
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # VELA 10 - Shooting Star - pavio longo para cima
    # ══════════════════════════════════════════════════════════════════════════
    {
        "time": "2024-01-01",
        
        "open": 100.00,
        "high": 105.00,            # Pavio LONGO para cima (rejeição)
        "low": 99.20,              # Pavio pequeno para baixo
        "close": 99.50,
        
        "type": "shooting_star",
        
        "question_open": "",
        "question_high": "",
        "question_low": "",
        "question_close": "",
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # 
    # 📝 PARA ADICIONAR MAIS VELAS:
    # 
    # 1. Copie um bloco acima (de { até },)
    # 2. Cole aqui
    # 3. Mude os valores de open, high, low, close
    # 4. Lembre: high >= todos, low <= todos
    #
    # ══════════════════════════════════════════════════════════════════════════
]


# ══════════════════════════════════════════════════════════════════════════════
#
#                    📈 EXERCÍCIOS DE SWING POINTS (NÍVEL 2)
#
#                    Usuário identifica: Swing High e Swing Low
#
#                    Swing High = Ponto mais alto antes de cair
#                    Swing Low = Ponto mais baixo antes de subir
#
# ══════════════════════════════════════════════════════════════════════════════

SWING_SCENARIOS = [
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 1 - Uptrend (tendência de alta)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Uptrend",
        
        # PERGUNTA CUSTOMIZADA (deixe "" para usar padrão)
        "question_swing_high": "",  # Ex: "Onde está o SWING HIGH?"
        "question_swing_low": "",   # Ex: "Clique no SWING LOW"
        
        # AS VELAS DO GRÁFICO (7 velas)
        "candles": [
            # Vela 0
            {"time": "2024-01-01", "open": 100.00, "high": 102.00, "low": 99.50, "close": 101.50},
            # Vela 1
            {"time": "2024-01-02", "open": 101.50, "high": 104.00, "low": 101.00, "close": 103.50},
            # Vela 2 ← SWING HIGH (máxima = 106.00)
            {"time": "2024-01-03", "open": 103.50, "high": 106.00, "low": 103.00, "close": 105.50},
            # Vela 3
            {"time": "2024-01-04", "open": 105.50, "high": 106.00, "low": 102.50, "close": 103.00},
            # Vela 4 ← SWING LOW (mínima = 101.00)
            {"time": "2024-01-05", "open": 103.00, "high": 103.50, "low": 101.00, "close": 101.50},
            # Vela 5
            {"time": "2024-01-08", "open": 101.50, "high": 104.00, "low": 101.00, "close": 103.50},
            # Vela 6
            {"time": "2024-01-09", "open": 103.50, "high": 107.00, "low": 103.00, "close": 106.50},
        ],
        
        # RESPOSTAS CORRETAS
        "swing_high_index": 2,      # Qual vela tem o Swing High? (começa em 0)
        "swing_high_price": 106.00, # Qual o preço do Swing High?
        
        "swing_low_index": 4,       # Qual vela tem o Swing Low?
        "swing_low_price": 101.00,  # Qual o preço do Swing Low?
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 2 - Downtrend (tendência de baixa)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Downtrend",
        
        "question_swing_high": "",
        "question_swing_low": "",
        
        "candles": [
            # Vela 0
            {"time": "2024-01-01", "open": 110.00, "high": 111.00, "low": 108.00, "close": 108.50},
            # Vela 1
            {"time": "2024-01-02", "open": 108.50, "high": 109.50, "low": 106.00, "close": 106.50},
            # Vela 2 ← SWING LOW (mínima = 104.00)
            {"time": "2024-01-03", "open": 106.50, "high": 107.00, "low": 104.00, "close": 104.50},
            # Vela 3
            {"time": "2024-01-04", "open": 104.50, "high": 107.50, "low": 104.00, "close": 107.00},
            # Vela 4 ← SWING HIGH (máxima = 108.50)
            {"time": "2024-01-05", "open": 107.00, "high": 108.50, "low": 106.50, "close": 108.00},
            # Vela 5
            {"time": "2024-01-08", "open": 108.00, "high": 108.50, "low": 105.00, "close": 105.50},
            # Vela 6
            {"time": "2024-01-09", "open": 105.50, "high": 106.00, "low": 102.00, "close": 102.50},
        ],
        
        "swing_high_index": 4,
        "swing_high_price": 108.50,
        
        "swing_low_index": 2,
        "swing_low_price": 104.00,
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # 
    # 📝 PARA ADICIONAR MAIS CENÁRIOS DE SWING:
    # 
    # 1. Copie um cenário acima
    # 2. Cole aqui
    # 3. Edite as velas (candles)
    # 4. Defina swing_high_index e swing_high_price
    # 5. Defina swing_low_index e swing_low_price
    #
    # ══════════════════════════════════════════════════════════════════════════
]


# ══════════════════════════════════════════════════════════════════════════════
#
#                    💧 EXERCÍCIOS DE LIQUIDITY (NÍVEL 3)
#
#                    BSL = Buy Side Liquidity (stops ACIMA de máximas)
#                    SSL = Sell Side Liquidity (stops ABAIXO de mínimas)
#
# ══════════════════════════════════════════════════════════════════════════════

LIQUIDITY_SCENARIOS = [
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 1 - Buy Side Liquidity (BSL)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "BSL",
        "description": "Stop losses dos vendedores estão ACIMA das máximas iguais",
        
        # PERGUNTA CUSTOMIZADA
        "question": "",  # Ex: "Onde está a Buy Side Liquidity?"
        
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 102.00, "low": 99.50, "close": 101.50},
            {"time": "2024-01-02", "open": 101.50, "high": 103.50, "low": 101.00, "close": 103.00},
            # Velas 2, 3, 4 têm máximas iguais (105.00) = EQUAL HIGHS
            {"time": "2024-01-03", "open": 103.00, "high": 105.00, "low": 102.50, "close": 104.50},
            {"time": "2024-01-04", "open": 104.50, "high": 105.00, "low": 103.00, "close": 103.50},
            {"time": "2024-01-05", "open": 103.50, "high": 104.80, "low": 102.50, "close": 104.00},
            # Vela 5 = SWEEP (quebra a liquidez)
            {"time": "2024-01-08", "open": 104.00, "high": 107.00, "low": 103.50, "close": 106.50},
        ],
        
        # RESPOSTA CORRETA
        "liquidity_type": "buy_side",  # buy_side ou sell_side
        "liquidity_level": 105.00,     # Preço onde está a liquidez
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 2 - Sell Side Liquidity (SSL)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "SSL",
        "description": "Stop losses dos compradores estão ABAIXO das mínimas iguais",
        
        "question": "",
        
        "candles": [
            {"time": "2024-01-01", "open": 105.00, "high": 106.00, "low": 103.50, "close": 104.00},
            {"time": "2024-01-02", "open": 104.00, "high": 105.00, "low": 102.00, "close": 102.50},
            # Velas 2, 3, 4 têm mínimas iguais (100.00) = EQUAL LOWS
            {"time": "2024-01-03", "open": 102.50, "high": 103.50, "low": 100.00, "close": 100.50},
            {"time": "2024-01-04", "open": 100.50, "high": 102.00, "low": 100.00, "close": 101.50},
            {"time": "2024-01-05", "open": 101.50, "high": 102.50, "low": 100.20, "close": 101.00},
            # Vela 5 = SWEEP (quebra a liquidez)
            {"time": "2024-01-08", "open": 101.00, "high": 101.50, "low": 98.00, "close": 98.50},
        ],
        
        "liquidity_type": "sell_side",
        "liquidity_level": 100.00,
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#
#                    💥 EXERCÍCIOS DE BOS (NÍVEL 4)
#
#                    BOS = Break of Structure
#                    Confirmação de que a tendência continua
#
#                    Bullish BOS = Quebra ACIMA da última máxima
#                    Bearish BOS = Quebra ABAIXO da última mínima
#
# ══════════════════════════════════════════════════════════════════════════════

BOS_SCENARIOS = [
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 1 - Bullish BOS
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Bullish BOS",
        "description": "Preço quebra ACIMA da máxima anterior = tendência de alta continua",
        
        "question": "",  # Ex: "Onde ocorreu o Break of Structure?"
        
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 102.00, "low": 99.50, "close": 101.50},
            # Vela 1 = última máxima importante (104.00)
            {"time": "2024-01-02", "open": 101.50, "high": 104.00, "low": 101.00, "close": 103.50},
            {"time": "2024-01-03", "open": 103.50, "high": 104.00, "low": 101.00, "close": 101.50},
            {"time": "2024-01-04", "open": 101.50, "high": 102.50, "low": 100.50, "close": 102.00},
            # Vela 4 = BOS! (quebra acima de 104.00)
            {"time": "2024-01-05", "open": 102.00, "high": 105.50, "low": 101.80, "close": 105.00},
        ],
        
        # RESPOSTA CORRETA
        "bos_type": "bullish",       # bullish ou bearish
        "structure_level": 104.00,   # Nível que foi quebrado
        "bos_candle_index": 4,       # Qual vela fez o BOS
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 2 - Bearish BOS
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Bearish BOS",
        "description": "Preço quebra ABAIXO da mínima anterior = tendência de baixa continua",
        
        "question": "",
        
        "candles": [
            {"time": "2024-01-01", "open": 105.00, "high": 106.00, "low": 104.00, "close": 104.50},
            # Vela 1 = última mínima importante (102.00)
            {"time": "2024-01-02", "open": 104.50, "high": 105.50, "low": 102.00, "close": 102.50},
            {"time": "2024-01-03", "open": 102.50, "high": 104.50, "low": 102.00, "close": 104.00},
            {"time": "2024-01-04", "open": 104.00, "high": 105.00, "low": 103.00, "close": 103.50},
            # Vela 4 = BOS! (quebra abaixo de 102.00)
            {"time": "2024-01-05", "open": 103.50, "high": 104.00, "low": 100.50, "close": 101.00},
        ],
        
        "bos_type": "bearish",
        "structure_level": 102.00,
        "bos_candle_index": 4,
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#
#                    🔄 EXERCÍCIOS DE CHoCH (NÍVEL 5)
#
#                    CHoCH = Change of Character
#                    PRIMEIRO sinal de que a tendência pode reverter
#
#                    Bullish CHoCH = Em downtrend, quebra a última Lower High
#                    Bearish CHoCH = Em uptrend, quebra a última Higher Low
#
# ══════════════════════════════════════════════════════════════════════════════

CHOCH_SCENARIOS = [
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 1 - Bullish CHoCH (fim do downtrend)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Bullish CHoCH",
        "description": "Downtrend acabando - preço quebra a última Lower High",
        
        "question": "",
        
        "candles": [
            # Downtrend: Lower Highs e Lower Lows
            {"time": "2024-01-01", "open": 105.00, "high": 106.00, "low": 104.00, "close": 104.50},
            {"time": "2024-01-02", "open": 104.50, "high": 105.00, "low": 102.00, "close": 102.50},
            {"time": "2024-01-03", "open": 102.50, "high": 103.50, "low": 100.00, "close": 100.50},
            # Vela 3 = última Lower High (103.00)
            {"time": "2024-01-04", "open": 100.50, "high": 103.00, "low": 100.00, "close": 102.50},
            # Vela 4 = CHoCH! (quebra acima de 103.00)
            {"time": "2024-01-05", "open": 102.50, "high": 104.50, "low": 102.00, "close": 104.00},
        ],
        
        "choch_type": "bullish",
        "structure_level": 103.00,   # Nível da última Lower High
        "choch_candle_index": 4,
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 2 - Bearish CHoCH (fim do uptrend)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Bearish CHoCH",
        "description": "Uptrend acabando - preço quebra a última Higher Low",
        
        "question": "",
        
        "candles": [
            # Uptrend: Higher Highs e Higher Lows
            {"time": "2024-01-01", "open": 100.00, "high": 102.00, "low": 99.50, "close": 101.50},
            {"time": "2024-01-02", "open": 101.50, "high": 104.00, "low": 101.00, "close": 103.50},
            {"time": "2024-01-03", "open": 103.50, "high": 106.00, "low": 103.00, "close": 105.50},
            # Vela 3 = última Higher Low (103.50)
            {"time": "2024-01-04", "open": 105.50, "high": 106.00, "low": 103.50, "close": 104.00},
            # Vela 4 = CHoCH! (quebra abaixo de 103.50)
            {"time": "2024-01-05", "open": 104.00, "high": 104.50, "low": 102.50, "close": 103.00},
        ],
        
        "choch_type": "bearish",
        "structure_level": 103.50,   # Nível da última Higher Low
        "choch_candle_index": 4,
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#
#                    📦 EXERCÍCIOS DE ORDER BLOCK (NÍVEL 6)
#
#                    Order Block = Última vela oposta antes de um movimento forte
#                    É onde as instituições entraram com força
#
#                    Bullish OB = Última vela VERMELHA antes de forte alta
#                    Bearish OB = Última vela VERDE antes de forte queda
#
# ══════════════════════════════════════════════════════════════════════════════

ORDER_BLOCK_SCENARIOS = [
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 1 - Bullish Order Block
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Bullish OB",
        "description": "Última vela VERMELHA antes do movimento forte de ALTA",
        
        "question": "",  # Ex: "Onde está o Order Block?"
        
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 101.00, "low": 99.00, "close": 100.50},
            # Vela 1 = ORDER BLOCK (última vermelha antes da alta)
            {"time": "2024-01-02", "open": 100.50, "high": 101.50, "low": 99.50, "close": 99.80},
            # Vela 2 = DISPLACEMENT (movimento forte que confirma o OB)
            {"time": "2024-01-03", "open": 99.80, "high": 104.00, "low": 99.50, "close": 103.50},
            {"time": "2024-01-04", "open": 103.50, "high": 106.00, "low": 103.00, "close": 105.50},
            {"time": "2024-01-05", "open": 105.50, "high": 108.00, "low": 105.00, "close": 107.50},
        ],
        
        "ob_type": "bullish",
        "ob_candle_index": 1,   # Qual vela é o OB (índice começa em 0)
        "ob_high": 101.50,      # Máxima da zona do OB
        "ob_low": 99.50,        # Mínima da zona do OB
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 2 - Bearish Order Block
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Bearish OB",
        "description": "Última vela VERDE antes do movimento forte de QUEDA",
        
        "question": "",
        
        "candles": [
            {"time": "2024-01-01", "open": 105.00, "high": 106.00, "low": 104.00, "close": 104.50},
            # Vela 1 = ORDER BLOCK (última verde antes da queda)
            {"time": "2024-01-02", "open": 104.50, "high": 106.50, "low": 104.00, "close": 106.00},
            # Vela 2 = DISPLACEMENT (movimento forte que confirma o OB)
            {"time": "2024-01-03", "open": 106.00, "high": 106.50, "low": 102.00, "close": 102.50},
            {"time": "2024-01-04", "open": 102.50, "high": 103.00, "low": 100.00, "close": 100.50},
            {"time": "2024-01-05", "open": 100.50, "high": 101.00, "low": 98.00, "close": 98.50},
        ],
        
        "ob_type": "bearish",
        "ob_candle_index": 1,
        "ob_high": 106.50,
        "ob_low": 104.00,
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#
#                    📊 EXERCÍCIOS DE FVG (NÍVEL 7)
#
#                    FVG = Fair Value Gap (Imbalance)
#                    Gap de preço entre vela 1 e vela 3
#                    Preço tende a voltar para "preencher" esse gap
#
#                    Bullish FVG = Gap para CIMA (high da vela 1 < low da vela 3)
#                    Bearish FVG = Gap para BAIXO (low da vela 1 > high da vela 3)
#
# ══════════════════════════════════════════════════════════════════════════════

FVG_SCENARIOS = [
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 1 - Bullish FVG
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Bullish FVG",
        "description": "Gap entre HIGH da vela 1 e LOW da vela 3",
        
        "question": "",  # Ex: "Onde está o Fair Value Gap?"
        
        "candles": [
            # Vela 0 (vela 1 do FVG) - HIGH = 101.50
            {"time": "2024-01-01", "open": 100.00, "high": 101.50, "low": 99.50, "close": 101.00},
            # Vela 1 (vela do meio - cria o gap)
            {"time": "2024-01-02", "open": 101.00, "high": 105.00, "low": 100.80, "close": 104.80},
            # Vela 2 (vela 3 do FVG) - LOW = 103.50
            {"time": "2024-01-03", "open": 104.80, "high": 107.00, "low": 103.50, "close": 106.50},
        ],
        
        # FVG está entre 101.50 (high vela 1) e 103.50 (low vela 3)
        "fvg_type": "bullish",
        "fvg_high": 103.50,   # Topo do FVG (low da vela 3)
        "fvg_low": 101.50,    # Fundo do FVG (high da vela 1)
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 2 - Bearish FVG
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Bearish FVG",
        "description": "Gap entre LOW da vela 1 e HIGH da vela 3",
        
        "question": "",
        
        "candles": [
            # Vela 0 (vela 1 do FVG) - LOW = 105.00
            {"time": "2024-01-01", "open": 106.00, "high": 107.00, "low": 105.00, "close": 105.50},
            # Vela 1 (vela do meio - cria o gap)
            {"time": "2024-01-02", "open": 105.50, "high": 106.00, "low": 101.00, "close": 101.50},
            # Vela 2 (vela 3 do FVG) - HIGH = 103.00
            {"time": "2024-01-03", "open": 101.50, "high": 103.00, "low": 100.00, "close": 100.50},
        ],
        
        # FVG está entre 103.00 (high vela 3) e 105.00 (low vela 1)
        "fvg_type": "bearish",
        "fvg_high": 105.00,   # Topo do FVG (low da vela 1)
        "fvg_low": 103.00,    # Fundo do FVG (high da vela 3)
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#
#                    💰 EXERCÍCIOS DE PREMIUM/DISCOUNT (NÍVEL 8)
#
#                    Equilibrium = 50% entre Swing High e Swing Low
#                    Premium Zone = ACIMA de 50% (caro para comprar)
#                    Discount Zone = ABAIXO de 50% (barato para comprar)
#
#                    Smart Money compra no Discount, vende no Premium
#
# ══════════════════════════════════════════════════════════════════════════════

PREMIUM_DISCOUNT_SCENARIOS = [
    
    # ══════════════════════════════════════════════════════════════════════════
    # CENÁRIO 1
    # ══════════════════════════════════════════════════════════════════════════
    {
        "name": "Premium/Discount",
        
        "question_premium": "",   # Ex: "Clique na Premium Zone"
        "question_discount": "",  # Ex: "Clique na Discount Zone"
        "question_equilibrium": "",  # Ex: "Onde está o Equilibrium (50%)?"
        
        "candles": [
            {"time": "2024-01-01", "open": 100.00, "high": 101.50, "low": 99.50, "close": 101.00},
            {"time": "2024-01-02", "open": 101.00, "high": 103.00, "low": 100.50, "close": 102.50},
            # Vela 2 = Swing High (105.00)
            {"time": "2024-01-03", "open": 102.50, "high": 105.00, "low": 102.00, "close": 104.50},
            {"time": "2024-01-04", "open": 104.50, "high": 105.00, "low": 102.00, "close": 102.50},
            # Vela 4 = Swing Low (100.00)
            {"time": "2024-01-05", "open": 102.50, "high": 103.00, "low": 100.00, "close": 100.50},
        ],
        
        # CÁLCULO:
        # Swing High = 105.00
        # Swing Low = 100.00
        # Equilibrium = (105 + 100) / 2 = 102.50
        
        "swing_high": 105.00,
        "swing_low": 100.00,
        "equilibrium": 102.50,    # 50% = ponto médio
        
        # Premium = acima de 102.50
        # Discount = abaixo de 102.50
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#
#                         🔧 DICAS RÁPIDAS
#
# ══════════════════════════════════════════════════════════════════════════════
#
# 1. PARA ADICIONAR MAIS EXERCÍCIOS:
#    - Copie um bloco existente
#    - Cole no final da lista (antes do ])
#    - Edite os valores
#
# 2. CAMPOS OBRIGATÓRIOS NAS VELAS:
#    - time: "2024-01-XX" (mude XX para dias diferentes)
#    - open, high, low, close: números decimais
#
# 3. VALIDAÇÃO:
#    - high deve ser >= open, close, low
#    - low deve ser <= open, close, high
#
# 4. PERGUNTAS CUSTOMIZADAS:
#    - Deixe "" para usar a pergunta padrão do sistema
#    - Ou escreva sua própria pergunta
#
# 5. APÓS EDITAR:
#    curl -X DELETE https://SEU-APP/api/interactive/exercises/cache
#    sudo supervisorctl restart backend
#
# ══════════════════════════════════════════════════════════════════════════════
