# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║              📚 CATEGORY LESSONS - CURSOS COMPLETOS                          ║
# ║                                                                              ║
# ║  Cada categoria tem um "livro" com várias páginas que o usuário lê          ║
# ║  ANTES de começar os exercícios                                              ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝


# ══════════════════════════════════════════════════════════════════════════════
#
#                         🕯️ CANDLESTICKS - CURSO COMPLETO
#
# ══════════════════════════════════════════════════════════════════════════════

CANDLESTICKS_LESSON = {
    "category_id": "candlesticks",
    "title": "Candlesticks - O Guia Completo",
    "description": "Aprenda a ler velas japonesas como um profissional",
    "total_pages": 10,
    "estimated_time": "25 min",
    
    "pages": [
        # ══════════════════════════════════════════════════════════════════════
        # PÁGINA 1 - Introdução
        # ══════════════════════════════════════════════════════════════════════
        {
            "page": 1,
            "title": "O que são Candlesticks?",
            "subtitle": "A origem das velas japonesas",
            
            "content": """
As velas japonesas (candlesticks) foram inventadas no Japão no século XVIII por Munehisa Homma, um comerciante de arroz que se tornou lendário por sua capacidade de prever movimentos de preço.

Hoje, são a forma mais popular de visualizar preços no mundo do trading. Por quê? Porque cada vela conta uma **história visual** da batalha entre compradores e vendedores.

## Por que aprender Candlesticks?

• **Linguagem universal**: Usadas em todos os mercados (ações, forex, crypto)
• **Informação rica**: Mostram 4 preços em uma única figura
• **Padrões previsíveis**: Certos padrões se repetem e indicam movimentos futuros
• **Fácil visualização**: Mais intuitivo que gráficos de linha ou barras
            """,
            
            "image": "https://www.investopedia.com/thmb/G8GjR5c_1j-A_W_p-JHVxJqE1QE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/CandlestickFINAL-9fb5ac2f0a7f4e9783a0d0dc1b3ce642.png",
            
            "tip": "Cada vela representa um período de tempo (1 minuto, 1 hora, 1 dia, etc.)"
        },
        
        # ══════════════════════════════════════════════════════════════════════
        # PÁGINA 2 - Anatomia da Vela
        # ══════════════════════════════════════════════════════════════════════
        {
            "page": 2,
            "title": "Anatomia de uma Vela",
            "subtitle": "Os 4 componentes essenciais",
            
            "content": """
Cada vela mostra **4 preços** importantes de um período:

## OPEN (Abertura)
O preço quando o período **começou**. É onde a vela "nasce".

## HIGH (Máxima)
O preço **mais alto** atingido durante o período. Forma o topo do pavio superior.

## LOW (Mínima)
O preço **mais baixo** atingido durante o período. Forma a base do pavio inferior.

## CLOSE (Fechamento)
O preço quando o período **terminou**. É onde a vela "morre".

## O Corpo e os Pavios

• **Corpo**: A parte grossa da vela, entre Open e Close
• **Pavio Superior**: Linha fina acima do corpo (até o High)
• **Pavio Inferior**: Linha fina abaixo do corpo (até o Low)
            """,
            
            "image": "https://www.babypips.com/images/2016/05/candlestick-anatomy.png",
            
            "tip": "Memorize: OHLC = Open, High, Low, Close"
        },
        
        # ══════════════════════════════════════════════════════════════════════
        # PÁGINA 3 - Velas Bullish vs Bearish
        # ══════════════════════════════════════════════════════════════════════
        {
            "page": 3,
            "title": "Verde vs Vermelha",
            "subtitle": "Quem ganhou a batalha?",
            
            "content": """
A COR da vela mostra quem venceu naquele período: compradores ou vendedores.

## 🟢 Vela VERDE (Bullish/Alta)

**Close > Open** = O preço SUBIU

• Compradores dominaram
• O corpo mostra o quanto subiu
• Quanto maior o corpo, mais forte a vitória dos compradores

## 🔴 Vela VERMELHA (Bearish/Baixa)

**Close < Open** = O preço CAIU

• Vendedores dominaram
• O corpo mostra o quanto caiu
• Quanto maior o corpo, mais forte a vitória dos vendedores

## A Batalha

Pense assim: cada vela é uma **batalha** entre dois exércitos:
- Exército Verde (Compradores/Bulls) quer preço SUBIR
- Exército Vermelho (Vendedores/Bears) quer preço CAIR

A cor da vela mostra quem ganhou essa batalha específica.
            """,
            
            "image": "https://www.investopedia.com/thmb/gHjvEJLPMJ8k0LbFMq6uMx_WJaY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/CandlestickPatterns1-d6fc3b453f1b4c57bdd6c6c2c5f67d60.png",
            
            "tip": "Algumas plataformas usam branco/preto em vez de verde/vermelho"
        },
        
        # ══════════════════════════════════════════════════════════════════════
        # PÁGINA 4 - O que o Corpo Revela
        # ══════════════════════════════════════════════════════════════════════
        {
            "page": 4,
            "title": "O Tamanho do Corpo",
            "subtitle": "Força e momentum",
            
            "content": """
O **tamanho do corpo** revela a FORÇA do movimento:

## Corpo GRANDE

• Movimento forte e decisivo
• Um lado dominou completamente
• Alta convicção dos traders
• Geralmente indica continuação

## Corpo PEQUENO

• Movimento fraco, indeciso
• Nem compradores nem vendedores dominaram
• Baixa convicção
• Pode indicar reversão ou pausa

## Corpo INEXISTENTE (Doji)

• Open = Close (ou muito próximos)
• Indecisão total
• Mercado "travado"
• Frequentemente precede reversões

## Na Prática

Imagine o corpo como o "placar" da partida:
- Corpo grande = Goleada (5x0)
- Corpo pequeno = Empate técnico (1x1)
- Doji = Empate sem gols (0x0)
            """,
            
            "image": "https://www.investopedia.com/thmb/8gx8-Lz-6uO2oPyQzO4d7HS4UGM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/dotdash_Final_Market_Trends_Aug_2020-01-75bf0f1b1dc84b76921c5f6a06b9b29c.jpg",
            
            "tip": "Corpo grande + direção clara = sinal forte"
        },
        
        # ══════════════════════════════════════════════════════════════════════
        # PÁGINA 5 - O que os Pavios Revelam
        # ══════════════════════════════════════════════════════════════════════
        {
            "page": 5,
            "title": "Os Pavios (Sombras)",
            "subtitle": "Rejeição de preço",
            
            "content": """
Os pavios mostram **REJEIÇÃO** - preços que foram testados mas não aceitos.

## Pavio Superior LONGO

• Preço subiu mas foi REJEITADO
• Vendedores entraram nas máximas
• Sinal de que compradores perderam força
• Potencial reversão para baixo

## Pavio Inferior LONGO

• Preço caiu mas foi REJEITADO
• Compradores entraram nas mínimas
• Sinal de que vendedores perderam força
• Potencial reversão para cima

## Sem Pavios (Marubozu)

• Sem rejeição
• Um lado controlou TODO o período
• Sinal de força extrema
• Geralmente indica continuação forte

## A Analogia

Pense nos pavios como "tentativas fracassadas":
- Pavio superior = "Tentaram subir, mas não conseguiram manter"
- Pavio inferior = "Tentaram derrubar, mas não conseguiram manter"
            """,
            
            "image": "https://a.c-dn.net/c/content/dam/publicsites/igcom/uk/images/ContentImage/Candlestick_wicks.png",
            
            "tip": "Pavios longos em níveis importantes (suporte/resistência) são muito significativos"
        },
        
        # ══════════════════════════════════════════════════════════════════════
        # PÁGINA 6 - Padrões de 1 Vela
        # ══════════════════════════════════════════════════════════════════════
        {
            "page": 6,
            "title": "Padrões de Uma Vela",
            "subtitle": "Doji, Hammer, Shooting Star",
            
            "content": """
Algumas velas sozinhas já indicam possíveis reversões:

## ✝️ DOJI

• Corpo mínimo (open ≈ close)
• Forma de cruz ou "+"
• Indica: INDECISÃO
• Após tendência forte = possível reversão

## 🔨 HAMMER (Martelo)

• Corpo pequeno no TOPO
• Pavio inferior LONGO (2-3x o corpo)
• Pavio superior pequeno/inexistente
• Indica: Reversão para ALTA
• Deve aparecer após QUEDA

## ⭐ SHOOTING STAR (Estrela Cadente)

• Corpo pequeno na BASE
• Pavio superior LONGO (2-3x o corpo)
• Pavio inferior pequeno/inexistente
• Indica: Reversão para BAIXA
• Deve aparecer após ALTA

## ⬛ MARUBOZU

• Vela SEM pavios (ou quase)
• Indica: FORÇA extrema na direção
• Verde = Bulls dominaram 100%
• Vermelho = Bears dominaram 100%
            """,
            
            "image": "https://www.investopedia.com/thmb/gHjvEJLPMJ8k0LbFMq6uMx_WJaY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/CandlestickPatterns1-d6fc3b453f1b4c57bdd6c6c2c5f67d60.png",
            
            "tip": "O CONTEXTO é crucial - um hammer só funciona se aparecer após uma queda"
        },
        
        # ══════════════════════════════════════════════════════════════════════
        # PÁGINA 7 - Padrões de 2 Velas
        # ══════════════════════════════════════════════════════════════════════
        {
            "page": 7,
            "title": "Padrões de Duas Velas",
            "subtitle": "Engulfing e outros",
            
            "content": """
Alguns padrões precisam de 2 velas para se formar:

## 🐂 BULLISH ENGULFING (Engolfo de Alta)

1. Vela 1: Vermelha (qualquer tamanho)
2. Vela 2: Verde GRANDE que "engole" o corpo da vela 1

• Indica: Reversão para ALTA
• Quanto maior a vela 2, mais forte o sinal
• Deve aparecer após queda

## 🐻 BEARISH ENGULFING (Engolfo de Baixa)

1. Vela 1: Verde (qualquer tamanho)
2. Vela 2: Vermelha GRANDE que "engole" o corpo da vela 1

• Indica: Reversão para BAIXA
• Quanto maior a vela 2, mais forte o sinal
• Deve aparecer após alta

## 🌓 TWEEZER TOP / BOTTOM

• Duas velas com máximas iguais (top) ou mínimas iguais (bottom)
• Indica que um nível foi testado duas vezes e rejeitado
• Sinal de reversão

## 📍 PIERCING LINE / DARK CLOUD

• Vela 2 abre com gap e fecha além de 50% da vela 1
• Sinal de reversão forte
            """,
            
            "image": "https://www.investopedia.com/thmb/8gx8-Lz-6uO2oPyQzO4d7HS4UGM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/dotdash_Final_Market_Trends_Aug_2020-01-75bf0f1b1dc84b76921c5f6a06b9b29c.jpg",
            
            "tip": "Engulfing é um dos padrões mais confiáveis - preste atenção nele!"
        },
        
        # ══════════════════════════════════════════════════════════════════════
        # PÁGINA 8 - Padrões de 3 Velas
        # ══════════════════════════════════════════════════════════════════════
        {
            "page": 8,
            "title": "Padrões de Três Velas",
            "subtitle": "Morning Star, Evening Star",
            
            "content": """
Os padrões de 3 velas são os mais confiáveis para reversões:

## 🌅 MORNING STAR (Estrela da Manhã)

Padrão de reversão para ALTA:

1. **Vela 1**: Vermelha grande (tendência de baixa)
2. **Vela 2**: Corpo pequeno (indecisão) - a "estrela"
3. **Vela 3**: Verde grande (reversão confirmada)

• Aparece no FUNDO após queda
• Mostra transição de venda → indecisão → compra

## 🌆 EVENING STAR (Estrela da Noite)

Padrão de reversão para BAIXA:

1. **Vela 1**: Verde grande (tendência de alta)
2. **Vela 2**: Corpo pequeno (indecisão) - a "estrela"
3. **Vela 3**: Vermelha grande (reversão confirmada)

• Aparece no TOPO após alta
• Mostra transição de compra → indecisão → venda

## 🪖 THREE SOLDIERS / THREE CROWS

• **3 White Soldiers**: 3 velas verdes consecutivas, cada uma fechando mais alto
• **3 Black Crows**: 3 velas vermelhas consecutivas, cada uma fechando mais baixo
• Indicam tendência forte na direção
            """,
            
            "image": "https://www.investopedia.com/thmb/gHjvEJLPMJ8k0LbFMq6uMx_WJaY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/CandlestickPatterns1-d6fc3b453f1b4c57bdd6c6c2c5f67d60.png",
            
            "tip": "Morning/Evening Star são padrões de alta probabilidade quando aparecem em níveis chave"
        },
        
        # ══════════════════════════════════════════════════════════════════════
        # PÁGINA 9 - Timeframes
        # ══════════════════════════════════════════════════════════════════════
        {
            "page": 9,
            "title": "Timeframes",
            "subtitle": "Cada vela = um período",
            
            "content": """
O TIMEFRAME define quanto tempo cada vela representa:

## Timeframes Comuns

• **M1** (1 minuto): Cada vela = 1 minuto
• **M5** (5 minutos): Cada vela = 5 minutos
• **M15** (15 minutos): Cada vela = 15 minutos
• **H1** (1 hora): Cada vela = 1 hora
• **H4** (4 horas): Cada vela = 4 horas
• **D1** (Diário): Cada vela = 1 dia
• **W1** (Semanal): Cada vela = 1 semana

## Qual usar?

• **Scalping**: M1, M5 (operações de segundos/minutos)
• **Day Trading**: M15, H1 (operações de horas)
• **Swing Trading**: H4, D1 (operações de dias/semanas)
• **Position Trading**: W1, MN (operações de semanas/meses)

## Regra de Ouro

**Timeframes maiores são mais confiáveis**

• Um padrão no D1 é mais significativo que no M5
• Sempre olhe o "big picture" em timeframes maiores
• Use timeframes menores para entrada precisa
            """,
            
            "image": "https://cdn.pixabay.com/photo/2016/11/27/21/42/stock-1863880_1280.jpg",
            
            "tip": "Comece analisando timeframes maiores (D1, H4) e depois vá para menores"
        },
        
        # ══════════════════════════════════════════════════════════════════════
        # PÁGINA 10 - Resumo e Próximos Passos
        # ══════════════════════════════════════════════════════════════════════
        {
            "page": 10,
            "title": "Resumo e Próximos Passos",
            "subtitle": "Você está pronto!",
            
            "content": """
## 📝 O que você aprendeu:

✅ **Anatomia**: OHLC (Open, High, Low, Close)
✅ **Cores**: Verde = alta, Vermelha = baixa
✅ **Corpo**: Tamanho indica força do movimento
✅ **Pavios**: Indicam rejeição de preço
✅ **Padrões de 1 vela**: Doji, Hammer, Shooting Star
✅ **Padrões de 2 velas**: Engulfing
✅ **Padrões de 3 velas**: Morning/Evening Star
✅ **Timeframes**: Cada vela = um período de tempo

## 🎯 Dicas Finais

1. **Contexto é TUDO** - Um hammer só funciona se aparecer no lugar certo
2. **Confirme sempre** - Espere a próxima vela confirmar o padrão
3. **Timeframe importa** - Padrões em D1 > padrões em M5
4. **Pratique muito** - A leitura de velas vem com experiência

## 🚀 Agora é hora de PRATICAR!

Nos exercícios a seguir, você vai:
- Identificar Open, High, Low, Close
- Reconhecer padrões de velas
- Testar seu conhecimento com quizzes interativos

Boa sorte! 💪
            """,
            
            "image": "https://cdn.pixabay.com/photo/2021/02/14/18/28/stock-6014940_1280.png",
            
            "tip": "Volte a esta lição sempre que precisar revisar os conceitos!"
        },
    ]
}


# ══════════════════════════════════════════════════════════════════════════════
#
#                         📈 MARKET STRUCTURE - CURSO COMPLETO
#
# ══════════════════════════════════════════════════════════════════════════════

MARKET_STRUCTURE_LESSON = {
    "category_id": "market-structure",
    "title": "Estrutura de Mercado",
    "description": "Entenda como o preço se move",
    "total_pages": 10,
    "estimated_time": "30 min",
    
    "pages": [
        {
            "page": 1,
            "title": "O que é Estrutura de Mercado?",
            "subtitle": "O esqueleto do movimento de preços",
            
            "content": """
Estrutura de Mercado é o "esqueleto" do movimento de preços. É como o preço se organiza em tendências e reversões.

## Por que é importante?

• Identifica a DIREÇÃO do mercado
• Mostra pontos de ENTRADA de baixo risco
• Revela quando a tendência pode MUDAR
• É a base de todas as estratégias profissionais

## Os 3 Estados do Mercado

1. **UPTREND** (Tendência de Alta)
2. **DOWNTREND** (Tendência de Baixa)
3. **RANGE** (Consolidação/Lateral)

Sua principal tarefa como trader é identificar em qual estado o mercado está.
            """,
            
            "image": "https://www.investopedia.com/thmb/8gx8-Lz-6uO2oPyQzO4d7HS4UGM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/dotdash_Final_Market_Trends_Aug_2020-01-75bf0f1b1dc84b76921c5f6a06b9b29c.jpg",
            
            "tip": "Trade with the trend, not against it (Opere a favor da tendência)"
        },
        {
            "page": 2,
            "title": "Swing Points",
            "subtitle": "Swing High e Swing Low",
            
            "content": """
Swing Points são os pontos de "virada" no preço:

## Swing High (Topo)

• O ponto MAIS ALTO antes do preço cair
• É onde compradores perderam e vendedores ganharam
• Funciona como RESISTÊNCIA

## Swing Low (Fundo)

• O ponto MAIS BAIXO antes do preço subir
• É onde vendedores perderam e compradores ganharam
• Funciona como SUPORTE

## Como Identificar

Um Swing High válido:
- Tem velas mais baixas dos dois lados
- O ponto mais alto em uma "onda"

Um Swing Low válido:
- Tem velas mais altas dos dois lados
- O ponto mais baixo em uma "onda"
            """,
            
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            
            "tip": "Marque os swing points no gráfico - eles são sua referência principal"
        },
        # Adicione páginas 3-10 para Market Structure...
        {
            "page": 3,
            "title": "Higher Highs & Higher Lows",
            "subtitle": "A marca registrada do uptrend",
            "content": """
Em uma tendência de ALTA, o preço faz:

## Higher High (HH)

Cada MÁXIMA é mais alta que a anterior.

## Higher Low (HL)

Cada MÍNIMA é mais alta que a anterior.

## Visualização

```
            HH
           /
         HH
        /
      HL
     /
   HH
  /
HL
```

Se você ver HH + HL = UPTREND confirmado!
            """,
            "image": "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
            "tip": "Em uptrend, compre nos Higher Lows"
        },
        {
            "page": 4,
            "title": "Lower Highs & Lower Lows",
            "subtitle": "A marca registrada do downtrend",
            "content": """
Em uma tendência de BAIXA, o preço faz:

## Lower High (LH)

Cada MÁXIMA é mais baixa que a anterior.

## Lower Low (LL)

Cada MÍNIMA é mais baixa que a anterior.

## Visualização

```
LH
  \\
   LH
     \\
      LL
        \\
         LH
           \\
            LL
```

Se você ver LH + LL = DOWNTREND confirmado!
            """,
            "image": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
            "tip": "Em downtrend, venda nos Lower Highs"
        },
        {
            "page": 5,
            "title": "Break of Structure (BOS)",
            "subtitle": "Confirmação de continuação",
            "content": """
BOS acontece quando o preço QUEBRA uma estrutura importante:

## Bullish BOS

- Preço quebra ACIMA da última máxima
- Confirma que o UPTREND continua

## Bearish BOS

- Preço quebra ABAIXO da última mínima
- Confirma que o DOWNTREND continua

## Importância

BOS é sua CONFIRMAÇÃO de que a tendência está intacta.
Sem BOS = tendência enfraquecendo.
            """,
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            "tip": "BOS confirma; CHoCH reverte"
        },
        {
            "page": 6,
            "title": "Change of Character (CHoCH)",
            "subtitle": "O primeiro sinal de reversão",
            "content": """
CHoCH é a PRIMEIRA quebra CONTRA a tendência:

## Bullish CHoCH (em downtrend)

- Preço quebra ACIMA da última Lower High
- Primeiro sinal de que o downtrend pode estar acabando

## Bearish CHoCH (em uptrend)

- Preço quebra ABAIXO da última Higher Low
- Primeiro sinal de que o uptrend pode estar acabando

## BOS vs CHoCH

- BOS = a FAVOR da tendência (continuação)
- CHoCH = CONTRA a tendência (possível reversão)
            """,
            "image": "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
            "tip": "CHoCH é alerta, não confirmação. Espere mais sinais."
        },
        {
            "page": 7,
            "title": "Range / Consolidação",
            "subtitle": "Quando o mercado descansa",
            "content": """
Range é quando o preço fica "preso" entre dois níveis:

## Características

- Máximas aproximadamente iguais (resistência)
- Mínimas aproximadamente iguais (suporte)
- Sem HH/HL ou LH/LL claros

## O que fazer no range?

1. **Opção 1**: Comprar no suporte, vender na resistência
2. **Opção 2**: Esperar o breakout (rompimento)

## Breakout

Quando o preço SAIR do range com força:
- Para CIMA = provável alta
- Para BAIXO = provável queda
            """,
            "image": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
            "tip": "Ranges frequentemente precedem movimentos explosivos"
        },
        {
            "page": 8,
            "title": "Multi-Timeframe Analysis",
            "subtitle": "O big picture",
            "content": """
Sempre analise MÚLTIPLOS timeframes:

## Timeframe Maior (HTF)

- Mostra a tendência PRINCIPAL
- D1, H4
- Define a DIREÇÃO geral

## Timeframe Menor (LTF)

- Mostra detalhes da estrutura
- H1, M15
- Define ENTRADAS precisas

## Regra de Ouro

O timeframe MAIOR manda:
- Se HTF é uptrend → só busque COMPRAS no LTF
- Se HTF é downtrend → só busque VENDAS no LTF
            """,
            "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            "tip": "Sempre comece pelo timeframe maior"
        },
        {
            "page": 9,
            "title": "Erros Comuns",
            "subtitle": "O que evitar",
            "content": """
Evite estes erros de iniciante:

## 1. Ignorar a tendência maior

Não compre em downtrend só porque viu um padrão bullish.

## 2. Forçar estrutura

Nem todo movimento é HH/HL ou LH/LL. Às vezes é range.

## 3. Não esperar confirmação

Um possível CHoCH não é CHoCH até quebrar de verdade.

## 4. Timeframe muito baixo

M1 e M5 têm muito "ruído". Use pelo menos M15/H1.

## 5. Não marcar swing points

Sem referência, você fica perdido. SEMPRE marque.
            """,
            "image": "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800",
            "tip": "Paciência é a maior virtude de um trader"
        },
        {
            "page": 10,
            "title": "Resumo Final",
            "subtitle": "Você está pronto!",
            "content": """
## O que você aprendeu:

✅ Swing High e Swing Low
✅ Higher Highs & Higher Lows (Uptrend)
✅ Lower Highs & Lower Lows (Downtrend)
✅ Break of Structure (BOS)
✅ Change of Character (CHoCH)
✅ Range / Consolidação
✅ Multi-Timeframe Analysis

## Checklist antes de operar:

1. Qual a tendência no HTF?
2. Onde estão os swing points?
3. Houve BOS ou CHoCH recente?
4. O preço está em range?

Agora pratique identificando estrutura nos exercícios! 💪
            """,
            "image": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800",
            "tip": "Estrutura é a BASE. Domine isso primeiro!"
        },
    ]
}


# ══════════════════════════════════════════════════════════════════════════════
#                         MAPA DE LIÇÕES POR CATEGORIA
# ══════════════════════════════════════════════════════════════════════════════

CATEGORY_LESSONS = {
    "candlesticks": CANDLESTICKS_LESSON,
    "market-structure": MARKET_STRUCTURE_LESSON,
    # Adicione mais categorias aqui...
}


# ══════════════════════════════════════════════════════════════════════════════
#                         FUNÇÕES DE ACESSO
# ══════════════════════════════════════════════════════════════════════════════

def get_category_lesson(category_id: str) -> dict:
    """Retorna a lição completa de uma categoria"""
    lesson = CATEGORY_LESSONS.get(category_id)
    if lesson:
        return {
            "has_lesson": True,
            **lesson
        }
    return {"has_lesson": False, "category_id": category_id}


def get_lesson_page(category_id: str, page_number: int) -> dict:
    """Retorna uma página específica da lição"""
    lesson = CATEGORY_LESSONS.get(category_id)
    if not lesson:
        return {"has_lesson": False, "category_id": category_id}
    
    pages = lesson.get("pages", [])
    page = next((p for p in pages if p["page"] == page_number), None)
    
    if page:
        return {
            "has_lesson": True,
            "category_id": category_id,
            "total_pages": lesson["total_pages"],
            "category_title": lesson["title"],
            **page
        }
    return {"has_lesson": False, "page_not_found": True}
