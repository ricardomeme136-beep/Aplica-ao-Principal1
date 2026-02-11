# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                    🎓 TRADELINGO QUIZ EXERCISES CONFIG                       ║
# ║                                                                              ║
# ║  COMO USAR:                                                                  ║
# ║  1. Encontre a CATEGORIA (CANDLESTICKS, MARKET_STRUCTURE, etc)               ║
# ║  2. Encontre o LEVEL (1-10)                                                  ║
# ║  3. Encontre o EXERCÍCIO (1-10)                                              ║
# ║  4. Edite e salve                                                            ║
# ║  5. Reinicie: sudo supervisorctl restart backend                             ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                         🕯️ CANDLESTICKS                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

CANDLESTICKS = {
    
    # ╔═════════════════════════════════════════════════════════════════════════╗
    # ║                           LEVEL 1                                       ║
    # ╚═════════════════════════════════════════════════════════════════════════╝
    1: [
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 1
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que uma vela verde/branca indica?",
            "image": "https://www.purple-trading.com/getmedia/1c5d4ca8-9a0f-40d7-961a-d575b7b8d0eb/candles-2-EN.png",
            "options": ["Preço subiu (fechou acima da abertura)", "Preço caiu", "Mercado fechado", "Sem movimento"],
            "correct": 0,
            "explanation": "Correto! Vela verde = preço subiu 📈",
            "hint": "Velas verdes mostram que compradores dominaram"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 2
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que uma vela vermelha/preta indica?",
            "image": "https://i.imgur.com/QBcvXjW.gif",
            "options": ["Preço subiu", "Preço caiu (fechou abaixo da abertura)", "Indecisão", "Gap"],
            "correct": 1,
            "explanation": "Exato! Vela vermelha = preço caiu 📉",
            "hint": "Velas vermelhas mostram que vendedores dominaram"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 3
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é o 'corpo' de uma vela?",
            "image": "https://i.imgur.com/cC4iWtq.gif",
            "options": ["O pavio superior", "A parte grossa entre abertura e fechamento", "O pavio inferior", "A sombra"],
            "correct": 1,
            "explanation": "Isso! O corpo mostra a diferença entre abertura e fechamento",
            "hint": "O corpo é a parte mais larga/grossa da vela"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 4
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que um corpo grande na vela indica?",
            "image": "https://cdn.pixabay.com/photo/2016/11/27/21/42/stock-1863880_1280.jpg",
            "options": ["Indecisão", "Movimento forte/momentum", "Mercado parado", "Reversão"],
            "correct": 1,
            "explanation": "Perfeito! Corpo grande = movimento forte 💪",
            "hint": "Quanto maior o corpo, mais forte o movimento"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 5
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que o pavio superior (sombra superior) mostra?",
            "image": "https://cdn.pixabay.com/photo/2021/01/25/12/43/bitcoin-5948838_1280.jpg",
            "options": ["Preço máximo atingido antes de cair", "Preço mínimo", "Preço de abertura", "Volume"],
            "correct": 0,
            "explanation": "Correto! Pavio superior = rejeição das máximas",
            "hint": "O pavio mostra até onde o preço foi antes de voltar"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 6
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que o pavio inferior (sombra inferior) mostra?",
            "image": "https://cdn.pixabay.com/photo/2018/02/04/09/09/bitcoin-3129440_1280.jpg",
            "options": ["Preço máximo", "Preço mínimo atingido antes de subir", "Fechamento", "Abertura"],
            "correct": 1,
            "explanation": "Exato! Pavio inferior = rejeição das mínimas",
            "hint": "Mostra que compradores entraram nas mínimas"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 7
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é uma vela Doji?",
            "image": "https://cdn.pixabay.com/photo/2017/03/17/10/29/chart-2151021_1280.png",
            "options": ["Vela muito grande", "Vela com abertura e fechamento quase iguais", "Vela sem pavios", "Vela gap"],
            "correct": 1,
            "explanation": "Isso! Doji = indecisão no mercado ⚖️",
            "hint": "Doji parece uma cruz ou sinal de mais"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 8
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "Uma vela sem pavios (marubozu) indica:",
            "image": "https://cdn.pixabay.com/photo/2018/08/08/10/19/chart-3592236_1280.jpg",
            "options": ["Indecisão", "Momentum muito forte em uma direção", "Reversão", "Mercado fechado"],
            "correct": 1,
            "explanation": "Perfeito! Sem pavios = controle total de um lado 🚀",
            "hint": "Marubozu mostra domínio completo de compradores ou vendedores"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 9
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "Um timeframe diário (D1) significa que cada vela representa:",
            "image": "https://cdn.pixabay.com/photo/2016/09/04/14/47/chart-1644118_1280.png",
            "options": ["1 minuto", "1 hora", "1 dia (24 horas)", "1 semana"],
            "correct": 2,
            "explanation": "Correto! D1 = cada vela é 1 dia completo",
            "hint": "D = Day (dia) e 1 = uma unidade"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 10
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "Por que as velas são úteis para traders?",
            "image": "https://cdn.pixabay.com/photo/2021/02/14/18/28/stock-6014940_1280.png",
            "options": ["São bonitas", "Mostram sentimento e momentum do mercado", "Preveem o futuro", "Mostram apenas volume"],
            "correct": 1,
            "explanation": "Exato! Velas contam a história da batalha compradores vs vendedores 📊",
            "hint": "Velas mostram quem está ganhando: compradores ou vendedores"
        },
    ],

    # ╔═════════════════════════════════════════════════════════════════════════╗
    # ║                           LEVEL 2                                       ║
    # ╚═════════════════════════════════════════════════════════════════════════╝
    2: [
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 2 - EXERCÍCIO 1
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é um Hammer (Martelo)?",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            "options": ["Vela grande verde", "Vela com corpo pequeno em cima e pavio longo embaixo", "Vela doji", "Vela sem pavios"],
            "correct": 1,
            "explanation": "Correto! Hammer = sinal de reversão bullish 🔨",
            "hint": "Parece um martelo com cabo longo para baixo"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 2 - EXERCÍCIO 2
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "Onde o Hammer aparece com mais força?",
            "image": "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
            "options": ["No topo após alta", "No fundo após queda", "No meio da tendência", "Qualquer lugar"],
            "correct": 1,
            "explanation": "Isso! Hammer em suporte após queda = forte sinal de reversão",
            "hint": "O hammer mostra que compradores defenderam o preço nas mínimas"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 2 - EXERCÍCIO 3
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é um Shooting Star (Estrela Cadente)?",
            "image": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
            "options": ["Vela verde grande", "Vela com corpo pequeno embaixo e pavio longo em cima", "Vela doji", "Vela marubozu"],
            "correct": 1,
            "explanation": "Correto! Shooting star = sinal de reversão bearish ⭐",
            "hint": "Parece uma estrela caindo, com 'cauda' para cima"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 2 - EXERCÍCIO 4
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O Shooting Star aparece onde?",
            "image": "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?w=800",
            "options": ["No fundo após queda", "No topo após alta", "No meio do range", "Qualquer lugar"],
            "correct": 1,
            "explanation": "Exato! Shooting star em resistência = possível reversão para baixo",
            "hint": "Mostra que compradores tentaram mas foram rejeitados"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 2 - EXERCÍCIO 5
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é Bullish Engulfing (Engolfo de Alta)?",
            "image": "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=800",
            "options": ["Vela pequena", "Vela verde grande que 'engole' a vela vermelha anterior", "Vela doji", "Duas velas iguais"],
            "correct": 1,
            "explanation": "Perfeito! Engulfing bullish = compradores dominaram completamente 🐂",
            "hint": "A vela verde cobre totalmente o corpo da vela vermelha anterior"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 2 - EXERCÍCIO 6
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é Bearish Engulfing (Engolfo de Baixa)?",
            "image": "https://images.unsplash.com/photo-1560221328-12fe60f83ab8?w=800",
            "options": ["Vela verde grande", "Vela vermelha grande que 'engole' a vela verde anterior", "Hammer", "Doji"],
            "correct": 1,
            "explanation": "Isso! Engulfing bearish = vendedores dominaram 🐻",
            "hint": "A vela vermelha cobre totalmente o corpo da vela verde anterior"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 2 - EXERCÍCIO 7
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "Um Pin Bar com pavio longo para baixo indica:",
            "image": "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800",
            "options": ["Vendedores dominaram", "Compradores defenderam - possível alta", "Indecisão", "Nada"],
            "correct": 1,
            "explanation": "Correto! Pavio longo para baixo = rejeição de preços baixos 📈",
            "hint": "Os compradores não deixaram o preço ficar lá embaixo"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 2 - EXERCÍCIO 8
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "Um Pin Bar com pavio longo para cima indica:",
            "image": "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=800",
            "options": ["Compradores dominaram", "Vendedores defenderam - possível queda", "Continuação da alta", "Gap"],
            "correct": 1,
            "explanation": "Exato! Pavio longo para cima = rejeição de preços altos 📉",
            "hint": "Os vendedores não deixaram o preço subir mais"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 2 - EXERCÍCIO 9
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "Morning Star (Estrela da Manhã) é formado por:",
            "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
            "options": ["1 vela", "3 velas: vermelha grande, pequena, verde grande", "2 velas", "4 velas"],
            "correct": 1,
            "explanation": "Perfeito! Morning star = padrão de reversão bullish de 3 velas 🌟",
            "hint": "Mostra transição de venda para indecisão para compra"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 2 - EXERCÍCIO 10
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "Evening Star (Estrela da Noite) indica:",
            "image": "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800",
            "options": ["Continuação da alta", "Reversão bearish (possível queda)", "Indecisão eterna", "Nada"],
            "correct": 1,
            "explanation": "Correto! Evening star = sinal de reversão para baixo 🌙",
            "hint": "Oposto do morning star - aparece no topo"
        },
    ],

    # ╔═════════════════════════════════════════════════════════════════════════╗
    # ║                           LEVEL 3                                       ║
    # ╚═════════════════════════════════════════════════════════════════════════╝
    3: [
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 3 - EXERCÍCIO 1
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "Sua pergunta aqui?",
            "image": "https://sua-imagem.com",
            "options": ["Opção A", "Opção B", "Opção C", "Opção D"],
            "correct": 0,
            "explanation": "Explicação",
            "hint": "Dica"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 3 - EXERCÍCIO 2
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "Sua pergunta aqui?",
            "image": "https://sua-imagem.com",
            "options": ["Opção A", "Opção B", "Opção C", "Opção D"],
            "correct": 0,
            "explanation": "Explicação",
            "hint": "Dica"
        },
        # Adicione LEVEL 3 - EXERCÍCIO 3 até 10...
    ],
    
    # Adicione LEVEL 4 até 10 seguindo o mesmo padrão...
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                       📈 MARKET STRUCTURE                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

MARKET_STRUCTURE = {
    # ╔═════════════════════════════════════════════════════════════════════════╗
    # ║                           LEVEL 1                                       ║
    # ╚═════════════════════════════════════════════════════════════════════════╝
    1: [
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 1
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é Higher High (HH)?",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            "options": ["Máxima mais alta que a anterior", "Mínima mais baixa", "Preço lateral", "Gap"],
            "correct": 0,
            "explanation": "Correto! HH = tendência de alta confirmada 📈",
            "hint": "Higher = mais alto, High = máxima"
        },
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 2
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é Lower Low (LL)?",
            "image": "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
            "options": ["Máxima mais alta", "Mínima mais baixa que a anterior", "Preço lateral", "Doji"],
            "correct": 1,
            "explanation": "Exato! LL = tendência de baixa 📉",
            "hint": "Lower = mais baixo, Low = mínima"
        },
        # Adicione LEVEL 1 - EXERCÍCIO 3 até 10...
    ],
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                         💧 LIQUIDITY                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

LIQUIDITY = {
    # ╔═════════════════════════════════════════════════════════════════════════╗
    # ║                           LEVEL 1                                       ║
    # ╚═════════════════════════════════════════════════════════════════════════╝
    1: [
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 1
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é Buy Side Liquidity (BSL)?",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            "options": ["Stop losses acima de máximas", "Stop losses abaixo de mínimas", "Ordens de compra", "Nada"],
            "correct": 0,
            "explanation": "Correto! BSL = stops de vendedores acima de máximas 🎯",
            "hint": "Instituições caçam esses stops antes de reverter"
        },
        # Adicione mais exercícios...
    ],
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                         💥 BOS (Break of Structure)                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

BOS = {
    # ╔═════════════════════════════════════════════════════════════════════════╗
    # ║                           LEVEL 1                                       ║
    # ╚═════════════════════════════════════════════════════════════════════════╝
    1: [
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 1
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é Break of Structure (BOS)?",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            "options": ["Preço lateral", "Preço quebrando máxima/mínima anterior", "Doji", "Gap"],
            "correct": 1,
            "explanation": "Correto! BOS confirma continuação da tendência 💥",
            "hint": "BOS mostra que a tendência continua"
        },
    ],
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                    🔄 CHoCH (Change of Character)                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

CHOCH = {
    # ╔═════════════════════════════════════════════════════════════════════════╗
    # ║                           LEVEL 1                                       ║
    # ╚═════════════════════════════════════════════════════════════════════════╝
    1: [
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 1
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é Change of Character (CHoCH)?",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            "options": ["Continuação", "Primeira quebra de estrutura contra a tendência", "Doji", "Marubozu"],
            "correct": 1,
            "explanation": "Correto! CHoCH = possível reversão de tendência 🔄",
            "hint": "CHoCH é o primeiro sinal de mudança"
        },
    ],
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                         📦 ORDER BLOCKS                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

ORDER_BLOCKS = {
    # ╔═════════════════════════════════════════════════════════════════════════╗
    # ║                           LEVEL 1                                       ║
    # ╚═════════════════════════════════════════════════════════════════════════╝
    1: [
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 1
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é um Order Block (OB)?",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            "options": ["Qualquer vela", "Zona onde instituições entraram com força", "Doji", "Gap"],
            "correct": 1,
            "explanation": "Correto! OB = pegada institucional 📦",
            "hint": "OBs são zonas de entrada de smart money"
        },
    ],
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                      📊 FVG (Fair Value Gap)                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

FVG = {
    # ╔═════════════════════════════════════════════════════════════════════════╗
    # ║                           LEVEL 1                                       ║
    # ╚═════════════════════════════════════════════════════════════════════════╝
    1: [
        # ══════════════════════════════════════════════════════════════════════
        # LEVEL 1 - EXERCÍCIO 1
        # ══════════════════════════════════════════════════════════════════════
        {
            "question": "O que é Fair Value Gap (FVG)?",
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            "options": ["Vela normal", "Desequilíbrio de preço entre 3 velas", "Doji", "Marubozu"],
            "correct": 1,
            "explanation": "Correto! FVG = imbalance que preço tende a preencher 📊",
            "hint": "FVG mostra pressa institucional"
        },
    ],
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║               MAPA DE CATEGORIAS (NÃO EDITAR)                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

EXERCISES_BY_CATEGORY = {
    "candlesticks": CANDLESTICKS,
    "market-structure": MARKET_STRUCTURE,
    "liquidity": LIQUIDITY,
    "bos": BOS,
    "choch": CHOCH,
    "order-blocks": ORDER_BLOCKS,
    "fvg": FVG,
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                    FUNÇÃO (NÃO EDITAR)                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def get_exercises(category_id: str, level: int) -> list:
    category_data = EXERCISES_BY_CATEGORY.get(category_id, {})
    exercises = category_data.get(level, [])
    
    formatted = []
    for i, ex in enumerate(exercises):
        formatted.append({
            "id": f"{category_id}-L{level}-E{i+1}",
            "exercise_number": i + 1,
            "category_id": category_id,
            "level": level,
            "title": f"Exercise {i+1}",
            "explanation": ex.get("explanation", ""),
            "question": ex.get("question", ""),
            "answer_type": "multiple_choice",
            "options": ex.get("options", ["A", "B", "C", "D"]),
            "correct_answer": ex.get("correct", 0),
            "feedback_correct": ex.get("explanation", "Correct! 🎯"),
            "feedback_wrong": ex.get("hint", "Try again!"),
            "xp_reward": 5 + (level * 2),
            "image_url": ex.get("image", "")
        })
    
    return formatted
