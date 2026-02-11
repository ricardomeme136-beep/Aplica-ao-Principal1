# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║              📚 LESSON INTRODUCTIONS - APRENDA ANTES DE PRATICAR             ║
# ║                                                                              ║
# ║  Este arquivo contém as introduções/lições que aparecem ANTES dos quizzes   ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝


# ══════════════════════════════════════════════════════════════════════════════
#
#                         🕯️ CANDLESTICKS - INTRODUÇÕES
#
# ══════════════════════════════════════════════════════════════════════════════

CANDLESTICKS_INTRO = {
    
    # ══════════════════════════════════════════════════════════════════════════
    # LEVEL 1 - Introdução
    # ══════════════════════════════════════════════════════════════════════════
    1: {
        "title": "O que são Candlesticks?",
        "subtitle": "A linguagem visual do mercado",
        "duration": "5 min",  # Tempo estimado de leitura
        
        "content": """
As velas japonesas (candlesticks) são a forma mais popular de visualizar movimentos de preço no trading. Cada vela conta uma história sobre a batalha entre compradores e vendedores.

## 📊 Anatomia de uma Vela

Cada vela tem 4 componentes principais:

• **Open (Abertura)**: Preço quando o período começou
• **High (Máxima)**: Preço mais alto atingido
• **Low (Mínima)**: Preço mais baixo atingido  
• **Close (Fechamento)**: Preço quando o período terminou

## 🟢 Vela Verde (Bullish)
Quando o preço **FECHOU ACIMA** da abertura = compradores ganharam
- O corpo mostra o quanto subiu
- Sinal de força compradora

## 🔴 Vela Vermelha (Bearish)
Quando o preço **FECHOU ABAIXO** da abertura = vendedores ganharam
- O corpo mostra o quanto caiu
- Sinal de força vendedora

## 📏 O que os Pavios Mostram

Os pavios (ou sombras) mostram **rejeição de preço**:
- **Pavio superior longo**: Preço subiu mas foi rejeitado (vendedores entraram)
- **Pavio inferior longo**: Preço caiu mas foi rejeitado (compradores entraram)
        """,
        
        "key_points": [
            "Velas verdes = preço subiu (compradores dominaram)",
            "Velas vermelhas = preço caiu (vendedores dominaram)",
            "Corpo grande = movimento forte",
            "Pavios longos = rejeição de preço"
        ],
        
        "image": "https://www.investopedia.com/thmb/G8GjR5c_1j-A_W_p-JHVxJqE1QE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/CandlestickFINAL-9fb5ac2f0a7f4e9783a0d0dc1b3ce642.png"
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # LEVEL 2 - Introdução
    # ══════════════════════════════════════════════════════════════════════════
    2: {
        "title": "Padrões de Velas",
        "subtitle": "Reconhecendo sinais de reversão",
        "duration": "7 min",
        
        "content": """
Agora que você entende a anatomia das velas, vamos aprender os **padrões mais importantes** que sinalizam possíveis reversões.

## 🔨 Hammer (Martelo)

O Hammer é um padrão de **reversão bullish** que aparece após uma queda:
- Corpo pequeno no **topo** da vela
- Pavio inferior **longo** (2-3x o tamanho do corpo)
- Pavio superior pequeno ou inexistente
- Mostra que compradores **rejeitaram** preços baixos

**Onde procurar**: Em suportes, após tendência de baixa

## ⭐ Shooting Star (Estrela Cadente)

O oposto do Hammer - sinal de **reversão bearish** que aparece após alta:
- Corpo pequeno na **base** da vela
- Pavio superior **longo**
- Mostra que vendedores **rejeitaram** preços altos

**Onde procurar**: Em resistências, após tendência de alta

## 🐂 Engulfing Patterns

### Bullish Engulfing (Engolfo de Alta)
- Vela verde que **engole completamente** a vela vermelha anterior
- Sinal forte de reversão para alta

### Bearish Engulfing (Engolfo de Baixa)  
- Vela vermelha que **engole completamente** a vela verde anterior
- Sinal forte de reversão para baixa

## 🌟 Morning Star / Evening Star

Padrões de 3 velas que sinalizam reversões importantes:

### Morning Star (Estrela da Manhã)
1. Vela vermelha grande
2. Vela pequena (indecisão)
3. Vela verde grande

### Evening Star (Estrela da Noite)
1. Vela verde grande
2. Vela pequena (indecisão)
3. Vela vermelha grande
        """,
        
        "key_points": [
            "Hammer no fundo = possível reversão para alta",
            "Shooting Star no topo = possível reversão para baixa",
            "Engulfing = sinal forte de mudança de controle",
            "Contexto é tudo - procure padrões em níveis importantes"
        ],
        
        "image": "https://www.investopedia.com/thmb/gHjvEJLPMJ8k0LbFMq6uMx_WJaY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/CandlestickPatterns1-d6fc3b453f1b4c57bdd6c6c2c5f67d60.png"
    },
    
    # Adicione LEVEL 3-10...
}


# ══════════════════════════════════════════════════════════════════════════════
#
#                         📈 MARKET STRUCTURE - INTRODUÇÕES
#
# ══════════════════════════════════════════════════════════════════════════════

MARKET_STRUCTURE_INTRO = {
    
    # ══════════════════════════════════════════════════════════════════════════
    # LEVEL 1 - Introdução
    # ══════════════════════════════════════════════════════════════════════════
    1: {
        "title": "Estrutura de Mercado",
        "subtitle": "Entendendo como o preço se move",
        "duration": "6 min",
        
        "content": """
A estrutura de mercado é o **esqueleto** do movimento de preços. Entender isso é fundamental para qualquer trader.

## 📈 Tendência de Alta (Uptrend)

Em uma tendência de alta, o preço faz:
- **Higher Highs (HH)**: Cada máxima é MAIS ALTA que a anterior
- **Higher Lows (HL)**: Cada mínima é MAIS ALTA que a anterior

```
        HH
       /  \\
      /    \\
    HH      HL
   /  \\    /
  /    \\  /
HL      HH
```

## 📉 Tendência de Baixa (Downtrend)

Em uma tendência de baixa, o preço faz:
- **Lower Highs (LH)**: Cada máxima é MAIS BAIXA que a anterior
- **Lower Lows (LL)**: Cada mínima é MAIS BAIXA que a anterior

```
LH
  \\
   \\
    LH
      \\
       \\
        LL
```

## ↔️ Consolidação (Range)

Quando o preço não está em tendência:
- Máximas e mínimas relativamente iguais
- Preço "preso" entre suporte e resistência
- Geralmente precede um movimento forte

## 🎯 Swing Points

- **Swing High**: Ponto mais alto antes de uma queda
- **Swing Low**: Ponto mais baixo antes de uma alta

Identificar esses pontos é crucial para encontrar entradas e saídas.
        """,
        
        "key_points": [
            "Uptrend = Higher Highs + Higher Lows",
            "Downtrend = Lower Highs + Lower Lows",
            "Swing High = máxima antes de cair",
            "Swing Low = mínima antes de subir"
        ],
        
        "image": "https://www.investopedia.com/thmb/8gx8-Lz-6uO2oPyQzO4d7HS4UGM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/dotdash_Final_Market_Trends_Aug_2020-01-75bf0f1b1dc84b76921c5f6a06b9b29c.jpg"
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#
#                         💧 LIQUIDITY - INTRODUÇÕES
#
# ══════════════════════════════════════════════════════════════════════════════

LIQUIDITY_INTRO = {
    
    # ══════════════════════════════════════════════════════════════════════════
    # LEVEL 1 - Introdução
    # ══════════════════════════════════════════════════════════════════════════
    1: {
        "title": "Liquidez no Trading",
        "subtitle": "Onde o Smart Money busca ordens",
        "duration": "8 min",
        
        "content": """
Liquidez é onde existem **ordens pendentes** no mercado. Instituições (Smart Money) precisam de liquidez para entrar e sair de posições grandes.

## 💰 O que é Liquidez?

Liquidez = **Stop losses** e **ordens pendentes** de outros traders

Quando você coloca um stop loss, você está criando uma ordem que será executada se o preço chegar lá. Instituições sabem onde essas ordens estão!

## 📍 Buy Side Liquidity (BSL)

**Stop losses de VENDEDORES** ficam **ACIMA** de máximas:
- Quando vemos várias máximas iguais (equal highs)
- Instituições frequentemente "varrem" essa liquidez antes de cair

```
Stop losses aqui -----> 🎯 BSL
                        ═══════
    /\\      /\\      /\\
   /  \\    /  \\    /  \\
  /    \\  /    \\  /    \\
```

## 📍 Sell Side Liquidity (SSL)

**Stop losses de COMPRADORES** ficam **ABAIXO** de mínimas:
- Quando vemos várias mínimas iguais (equal lows)
- Instituições frequentemente "varrem" essa liquidez antes de subir

```
  \\    /  \\    /  \\    /
   \\  /    \\  /    \\  /
    \\/      \\/      \\/
                        ═══════
Stop losses aqui -----> 🎯 SSL
```

## 🎯 Liquidity Sweep

Quando o preço **quebra** um nível de liquidez e **volta rapidamente**:
- É um sinal de que instituições pegaram as ordens
- Frequentemente precede um movimento forte na direção oposta
        """,
        
        "key_points": [
            "BSL = stops acima de máximas (alvos para quedas)",
            "SSL = stops abaixo de mínimas (alvos para altas)",
            "Equal highs/lows = zonas de liquidez óbvias",
            "Sweep = instituições coletando stops antes de reverter"
        ],
        
        "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800"
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#
#                         💥 BOS - INTRODUÇÕES
#
# ══════════════════════════════════════════════════════════════════════════════

BOS_INTRO = {
    
    # ══════════════════════════════════════════════════════════════════════════
    # LEVEL 1 - Introdução
    # ══════════════════════════════════════════════════════════════════════════
    1: {
        "title": "Break of Structure (BOS)",
        "subtitle": "Confirmando a continuação da tendência",
        "duration": "5 min",
        
        "content": """
BOS (Break of Structure) é quando o preço **quebra** uma máxima ou mínima importante, **confirmando** que a tendência continua.

## 📈 Bullish BOS

Em uma tendência de ALTA, um Bullish BOS acontece quando:
- Preço faz um **Higher Low** (HL)
- Depois **QUEBRA ACIMA** da última máxima (HH)
- Isso CONFIRMA que a tendência de alta continua

```
                    BOS! ↑
                      │
            HH ──────┼────→ Novo HH
           /  \\      │
          /    \\     │
         /      HL   │
        /            │
    HH              
   /
  /
HL
```

## 📉 Bearish BOS

Em uma tendência de BAIXA, um Bearish BOS acontece quando:
- Preço faz um **Lower High** (LH)
- Depois **QUEBRA ABAIXO** da última mínima (LL)
- Isso CONFIRMA que a tendência de baixa continua

```
LH
  \\
   \\
    LH
      \\
       LL ──────────→ Novo LL
             │
         BOS! ↓
```

## ⚠️ Importante

- BOS **confirma** a tendência, não prevê reversão
- Procure entradas após o BOS, em pullbacks
- Combine com outras confluências (OB, FVG, etc.)
        """,
        
        "key_points": [
            "Bullish BOS = quebra acima da última máxima",
            "Bearish BOS = quebra abaixo da última mínima",
            "BOS confirma que a tendência continua",
            "Use BOS para entradas a favor da tendência"
        ],
        
        "image": "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800"
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#
#                         🔄 CHoCH - INTRODUÇÕES
#
# ══════════════════════════════════════════════════════════════════════════════

CHOCH_INTRO = {
    
    # ══════════════════════════════════════════════════════════════════════════
    # LEVEL 1 - Introdução
    # ══════════════════════════════════════════════════════════════════════════
    1: {
        "title": "Change of Character (CHoCH)",
        "subtitle": "O primeiro sinal de reversão",
        "duration": "6 min",
        
        "content": """
CHoCH (Change of Character) é o **PRIMEIRO** sinal de que a tendência pode estar mudando. É a primeira quebra de estrutura **CONTRA** a tendência atual.

## 🔄 Diferença entre BOS e CHoCH

- **BOS** = Quebra **A FAVOR** da tendência (continuação)
- **CHoCH** = Quebra **CONTRA** a tendência (possível reversão)

## 📈 Bullish CHoCH (Fim do Downtrend)

Quando estamos em TENDÊNCIA DE BAIXA e:
- Preço vinha fazendo Lower Highs e Lower Lows
- De repente **QUEBRA ACIMA** da última Lower High
- Isso é o CHoCH - primeiro sinal de reversão para alta!

```
LH
  \\
   LH ─────────────────→ CHoCH! (quebra acima)
     \\               ↗
      LL            /
        \\         /
         LL ────→
```

## 📉 Bearish CHoCH (Fim do Uptrend)

Quando estamos em TENDÊNCIA DE ALTA e:
- Preço vinha fazendo Higher Highs e Higher Lows
- De repente **QUEBRA ABAIXO** da última Higher Low
- Isso é o CHoCH - primeiro sinal de reversão para baixa!

```
            HH
           /
          /
    HH ─────────────────→ CHoCH! (quebra abaixo)
   /                    ↘
  /                      \\
HL                        ↓
```

## ⚠️ CHoCH ≠ Reversão Confirmada

CHoCH é apenas o **primeiro sinal**. Para confirmar:
1. Espere um BOS na nova direção
2. Procure outras confluências (OB, liquidez)
3. Não entre imediatamente no CHoCH
        """,
        
        "key_points": [
            "CHoCH = primeira quebra CONTRA a tendência",
            "BOS = quebra A FAVOR da tendência",
            "Bullish CHoCH = quebra acima da última LH no downtrend",
            "Bearish CHoCH = quebra abaixo da última HL no uptrend"
        ],
        
        "image": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800"
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#
#                         📦 ORDER BLOCKS - INTRODUÇÕES
#
# ══════════════════════════════════════════════════════════════════════════════

ORDER_BLOCKS_INTRO = {
    
    # ══════════════════════════════════════════════════════════════════════════
    # LEVEL 1 - Introdução
    # ══════════════════════════════════════════════════════════════════════════
    1: {
        "title": "Order Blocks (OB)",
        "subtitle": "A pegada do Smart Money",
        "duration": "8 min",
        
        "content": """
Order Blocks são zonas onde **instituições** (Smart Money) entraram com ordens grandes. O preço frequentemente **retorna** a essas zonas.

## 📦 O que é um Order Block?

É a **última vela de cor oposta** antes de um movimento forte (displacement):
- **Bullish OB**: Última vela **VERMELHA** antes de forte alta
- **Bearish OB**: Última vela **VERDE** antes de forte queda

## 🟢 Bullish Order Block

```
     Displacement (forte alta)
           ↗ ↗ ↗
          /
         /
    [OB] ← Última vela vermelha
    ────
```

Como identificar:
1. Procure um movimento forte para CIMA
2. A última vela VERMELHA antes desse movimento = Bullish OB
3. Quando o preço voltar a essa zona, é oportunidade de COMPRA

## 🔴 Bearish Order Block

```
    [OB] ← Última vela verde
    ────
         \\
          \\
           ↘ ↘ ↘
     Displacement (forte queda)
```

Como identificar:
1. Procure um movimento forte para BAIXO
2. A última vela VERDE antes desse movimento = Bearish OB
3. Quando o preço voltar a essa zona, é oportunidade de VENDA

## 🎯 Por que Order Blocks funcionam?

Instituições não conseguem executar todas as ordens de uma vez. Quando o preço retorna ao OB:
- Eles têm mais ordens para executar
- O preço tende a reagir novamente na mesma direção

## ⚡ Displacement

É o movimento forte que **valida** o Order Block:
- Deve ser uma vela grande
- Idealmente cria um FVG (gap)
- Sem displacement, não há OB válido
        """,
        
        "key_points": [
            "Bullish OB = última vela vermelha antes de alta forte",
            "Bearish OB = última vela verde antes de queda forte",
            "Preço tende a retornar ao OB antes de continuar",
            "Displacement valida o OB - sem ele, não há OB"
        ],
        
        "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800"
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#
#                         📊 FVG - INTRODUÇÕES
#
# ══════════════════════════════════════════════════════════════════════════════

FVG_INTRO = {
    
    # ══════════════════════════════════════════════════════════════════════════
    # LEVEL 1 - Introdução
    # ══════════════════════════════════════════════════════════════════════════
    1: {
        "title": "Fair Value Gap (FVG)",
        "subtitle": "Desequilíbrios que o preço preenche",
        "duration": "7 min",
        
        "content": """
FVG (Fair Value Gap) é um **gap de preço** entre 3 velas consecutivas. É causado por movimento tão rápido que deixa um "vazio" no preço.

## 📊 O que é FVG?

Quando o preço se move muito rápido:
- A vela do MEIO é muito grande
- Cria um GAP entre a vela 1 e a vela 3
- Esse gap = Fair Value Gap

## 🟢 Bullish FVG (Imbalance para cima)

```
        Vela 3
       ┌─────┐
       │     │  LOW da vela 3
       └─────┘
         ↑
       [FVG] ← Gap entre high da vela 1 e low da vela 3
         ↑
       ┌─────┐  HIGH da vela 1
       │     │
       │     │  Vela 2 (grande)
       │     │
       └─────┘
       ┌─────┐
       │     │  Vela 1
       └─────┘
```

**FVG = área entre HIGH da vela 1 e LOW da vela 3**

## 🔴 Bearish FVG (Imbalance para baixo)

O oposto - gap criado em movimento de queda forte.

**FVG = área entre LOW da vela 1 e HIGH da vela 3**

## 🎯 Por que FVG é importante?

1. **Preço tende a PREENCHER o gap** antes de continuar
2. FVG = zona de entrada de alta probabilidade
3. Smart Money usa FVG como ponto de entrada

## 💡 Como usar FVG

1. Identifique o FVG após movimento forte
2. Espere o preço **retornar** ao FVG
3. Entre na direção do movimento original
4. Stop abaixo/acima do FVG completo
        """,
        
        "key_points": [
            "FVG = gap entre 3 velas (high vela 1 vs low vela 3)",
            "Causado por movimento muito rápido",
            "Preço tende a voltar e preencher o gap",
            "Use FVG como zona de entrada"
        ],
        
        "image": "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800"
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#
#                    MAPA DE INTRODUÇÕES POR CATEGORIA
#
# ══════════════════════════════════════════════════════════════════════════════

LESSON_INTROS = {
    "candlesticks": CANDLESTICKS_INTRO,
    "market-structure": MARKET_STRUCTURE_INTRO,
    "liquidity": LIQUIDITY_INTRO,
    "bos": BOS_INTRO,
    "choch": CHOCH_INTRO,
    "order-blocks": ORDER_BLOCKS_INTRO,
    "fvg": FVG_INTRO,
}


# ══════════════════════════════════════════════════════════════════════════════
#
#                    FUNÇÃO PARA OBTER INTRODUÇÃO
#
# ══════════════════════════════════════════════════════════════════════════════

def get_lesson_intro(category_id: str, level: int) -> dict:
    """
    Retorna a introdução/lição para uma categoria e level.
    Se não existir, retorna uma introdução padrão.
    """
    category_intros = LESSON_INTROS.get(category_id, {})
    intro = category_intros.get(level, None)
    
    if intro:
        return {
            "has_intro": True,
            "title": intro.get("title", ""),
            "subtitle": intro.get("subtitle", ""),
            "duration": intro.get("duration", "5 min"),
            "content": intro.get("content", ""),
            "key_points": intro.get("key_points", []),
            "image": intro.get("image", ""),
            "category_id": category_id,
            "level": level
        }
    else:
        return {
            "has_intro": False,
            "category_id": category_id,
            "level": level
        }
