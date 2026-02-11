// ╔══════════════════════════════════════════════════════════════════════════════╗
// ║                                                                              ║
// ║              🎯 NOVO SISTEMA DE APRENDIZAGEM - TradeLingo 2.0               ║
// ║                                                                              ║
// ║  Baseado em: Decisões → Padrões → Competências                              ║
// ║  Ciclo: Problema → Conceito → Visual → Decisão → Feedback                   ║
// ║                                                                              ║
// ╚══════════════════════════════════════════════════════════════════════════════╝

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { toast } from 'sonner';

const API = process.env.REACT_APP_BACKEND_URL + '/api';

// ==================== ONBOARDING - PRIMEIRA DECISÃO ====================

export const OnboardingFlow = ({ onComplete, user }) => {
  const [step, setStep] = useState(0);
  const [userChoice, setUserChoice] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);

  // Gráfico simplificado para onboarding
  const SimpleChart = ({ trend }) => {
    const canvasRef = useRef(null);
    
    useEffect(() => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      const width = canvas.width;
      const height = canvas.height;
      
      // Background
      ctx.fillStyle = '#0A0A0A';
      ctx.fillRect(0, 0, width, height);
      
      // Generate simple candles
      let price = 100;
      const candles = [];
      
      for (let i = 0; i < 15; i++) {
        const trendBias = trend === 'up' ? 0.6 : trend === 'down' ? -0.6 : 0;
        const change = (Math.random() - 0.5 + trendBias) * 3;
        const open = price;
        const close = price + change;
        const high = Math.max(open, close) + Math.random() * 1.5;
        const low = Math.min(open, close) - Math.random() * 1.5;
        candles.push({ open, high, low, close });
        price = close;
      }
      
      // Draw candles
      const candleWidth = width / 20;
      const minPrice = Math.min(...candles.flatMap(c => [c.low])) - 2;
      const maxPrice = Math.max(...candles.flatMap(c => [c.high])) + 2;
      const priceRange = maxPrice - minPrice;
      
      const priceToY = (p) => height - ((p - minPrice) / priceRange) * height * 0.8 - height * 0.1;
      
      candles.forEach((candle, i) => {
        const x = (i + 3) * candleWidth;
        const isBullish = candle.close > candle.open;
        
        // Wick
        ctx.strokeStyle = isBullish ? '#58CC02' : '#FF4444';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x, priceToY(candle.high));
        ctx.lineTo(x, priceToY(candle.low));
        ctx.stroke();
        
        // Body
        ctx.fillStyle = isBullish ? '#58CC02' : '#FF4444';
        const bodyTop = priceToY(Math.max(candle.open, candle.close));
        const bodyHeight = Math.abs(priceToY(candle.open) - priceToY(candle.close)) || 2;
        ctx.fillRect(x - candleWidth/3, bodyTop, candleWidth/1.5, bodyHeight);
      });
      
      // Question mark overlay for mystery
      if (step === 0) {
        ctx.fillStyle = 'rgba(0,0,0,0.3)';
        ctx.fillRect(width * 0.7, 0, width * 0.3, height);
        ctx.fillStyle = '#9333EA';
        ctx.font = 'bold 48px Arial';
        ctx.fillText('?', width * 0.82, height * 0.55);
      }
      
    }, [trend, step]);
    
    return (
      <canvas 
        ref={canvasRef} 
        width={350} 
        height={200} 
        className="rounded-xl border border-gray-800"
      />
    );
  };

  const steps = [
    // Step 0: Primeira decisão
    {
      type: 'decision',
      content: (
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-2">
            Vamos começar.
          </h2>
          <p className="text-gray-400 mb-6">
            Olha para este gráfico. O que farias?
          </p>
          
          <div className="flex justify-center mb-6">
            <SimpleChart trend="up" />
          </div>
          
          <div className="flex gap-3 justify-center">
            <button
              onClick={() => { setUserChoice('buy'); setShowFeedback(true); }}
              className="px-8 py-4 bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl transition-all transform hover:scale-105"
            >
              🟢 Comprar
            </button>
            <button
              onClick={() => { setUserChoice('wait'); setShowFeedback(true); }}
              className="px-8 py-4 bg-gray-600 hover:bg-gray-700 text-white font-bold rounded-xl transition-all transform hover:scale-105"
            >
              ⏳ Esperar
            </button>
            <button
              onClick={() => { setUserChoice('sell'); setShowFeedback(true); }}
              className="px-8 py-4 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl transition-all transform hover:scale-105"
            >
              🔴 Vender
            </button>
          </div>
          
          {showFeedback && (
            <div className="mt-6 p-4 bg-purple-500/20 border border-purple-500/50 rounded-xl animate-fade-in">
              <p className="text-purple-400 font-semibold text-lg">
                ✨ Acabaste de tomar uma decisão de trader.
              </p>
              <p className="text-gray-400 text-sm mt-2">
                {userChoice === 'buy' && "Viste tendência de alta e quiseste entrar. Boa intuição!"}
                {userChoice === 'wait' && "Preferiste esperar por mais confirmação. Paciência é uma qualidade."}
                {userChoice === 'sell' && "Pensaste em ir contra a tendência. Às vezes funciona!"}
              </p>
              <button
                onClick={() => setStep(1)}
                className="mt-4 px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg"
              >
                Continuar →
              </button>
            </div>
          )}
        </div>
      )
    },
    // Step 1: Explicar o que aconteceu
    {
      type: 'concept',
      content: (
        <div className="text-center">
          <div className="text-5xl mb-4">🎯</div>
          <h2 className="text-2xl font-bold text-white mb-4">
            O trading é isto.
          </h2>
          <p className="text-gray-300 text-lg mb-6 max-w-md mx-auto">
            <span className="text-purple-400 font-semibold">Decisões</span> baseadas em 
            <span className="text-green-400 font-semibold"> padrões</span>, sob 
            <span className="text-orange-400 font-semibold"> incerteza</span>.
          </p>
          
          <div className="bg-[#1A1A1A] rounded-xl p-6 max-w-sm mx-auto mb-6">
            <div className="space-y-3 text-left">
              <div className="flex items-center gap-3">
                <span className="text-2xl">📊</span>
                <span className="text-gray-300">Observar padrões</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-2xl">🧠</span>
                <span className="text-gray-300">Tomar decisões</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-2xl">⚡</span>
                <span className="text-gray-300">Gerir risco</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-2xl">🔄</span>
                <span className="text-gray-300">Repetir com disciplina</span>
              </div>
            </div>
          </div>
          
          <button
            onClick={() => setStep(2)}
            className="px-8 py-3 bg-[#58CC02] hover:bg-[#4CAD02] text-white font-bold rounded-xl"
          >
            Entendi! →
          </button>
        </div>
      )
    },
    // Step 2: O que vais aprender
    {
      type: 'roadmap',
      content: (
        <div className="text-center">
          <div className="text-5xl mb-4">🗺️</div>
          <h2 className="text-2xl font-bold text-white mb-2">
            O teu percurso
          </h2>
          <p className="text-gray-400 mb-6">
            Vais dominar estas competências, passo a passo.
          </p>
          
          <div className="space-y-3 max-w-sm mx-auto mb-6">
            {[
              { level: 1, name: 'Identificar Direção', icon: '📈', color: 'green' },
              { level: 2, name: 'Ler Estrutura', icon: '🏗️', color: 'blue' },
              { level: 3, name: 'Encontrar Zonas', icon: '🎯', color: 'purple' },
              { level: 4, name: 'Timing de Entradas', icon: '⏱️', color: 'orange' },
              { level: 5, name: 'Gerir Risco', icon: '🛡️', color: 'red' },
              { level: 6, name: 'Controlo Emocional', icon: '🧘', color: 'pink' },
            ].map((item, i) => (
              <div 
                key={i}
                className={`flex items-center gap-4 p-3 rounded-xl ${
                  i === 0 ? 'bg-green-500/20 border border-green-500/50' : 'bg-[#1A1A1A] opacity-60'
                }`}
              >
                <span className="text-2xl">{item.icon}</span>
                <div className="text-left flex-1">
                  <div className="text-white font-medium">{item.name}</div>
                  <div className="text-xs text-gray-500">Nível {item.level}</div>
                </div>
                {i === 0 && <span className="text-green-400 text-sm">Começa aqui</span>}
                {i > 0 && <span className="text-gray-600">🔒</span>}
              </div>
            ))}
          </div>
          
          <button
            onClick={() => setStep(3)}
            className="px-8 py-3 bg-[#58CC02] hover:bg-[#4CAD02] text-white font-bold rounded-xl"
          >
            Começar! →
          </button>
        </div>
      )
    },
    // Step 3: Âncora de memória
    {
      type: 'memory',
      content: (
        <div className="text-center">
          <div className="text-5xl mb-4">💡</div>
          <h2 className="text-xl font-bold text-white mb-6">
            Primeira regra para nunca esqueceres:
          </h2>
          
          <div className="bg-gradient-to-r from-purple-500/20 to-blue-500/20 border border-purple-500/50 rounded-2xl p-8 max-w-md mx-auto mb-6">
            <p className="text-2xl font-bold text-white">
              "Sem confirmação,<br/>não há trade."
            </p>
          </div>
          
          <p className="text-gray-400 text-sm mb-6 max-w-sm mx-auto">
            Vais ouvir isto muitas vezes. É o que separa traders lucrativos dos que perdem.
          </p>
          
          <button
            onClick={onComplete}
            className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold rounded-xl"
          >
            🚀 Vamos começar!
          </button>
        </div>
      )
    }
  ];

  return (
    <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center p-4">
      <div className="w-full max-w-lg">
        {/* Skip button */}
        <div className="flex justify-end mb-4">
          <button
            onClick={onComplete}
            className="text-gray-500 hover:text-gray-300 text-sm px-4 py-2"
            data-testid="skip-onboarding-btn"
          >
            Pular →
          </button>
        </div>
        
        {/* Progress dots */}
        <div className="flex justify-center gap-2 mb-8">
          {steps.map((_, i) => (
            <div 
              key={i}
              className={`w-2 h-2 rounded-full transition-all ${
                i === step ? 'bg-purple-500 w-6' : i < step ? 'bg-purple-500' : 'bg-gray-700'
              }`}
            />
          ))}
        </div>
        
        {steps[step].content}
      </div>
    </div>
  );
};

// ==================== LIÇÃO COM CICLO DE 5 PASSOS ====================

export const LessonCycle = ({ lesson, onComplete, user }) => {
  const [phase, setPhase] = useState(0); // 0: Problem, 1: Concept, 2: Visual, 3: Decision, 4: Feedback
  const [userAnswer, setUserAnswer] = useState(null);
  const [isCorrect, setIsCorrect] = useState(null);

  const phases = ['problem', 'concept', 'visual', 'decision', 'feedback'];

  const handleDecision = (answer) => {
    setUserAnswer(answer);
    setIsCorrect(answer === lesson.correctAnswer);
    setPhase(4); // Go to feedback
  };

  const handleComplete = () => {
    onComplete({
      lessonId: lesson.id,
      correct: isCorrect,
      answer: userAnswer,
      timeSpent: 120 // TODO: track actual time
    });
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A] p-4 pb-24">
      {/* Progress bar */}
      <div className="mb-6">
        <div className="flex justify-between text-xs text-gray-500 mb-2">
          <span>{lesson.category}</span>
          <span>{phase + 1}/5</span>
        </div>
        <div className="h-1 bg-[#2A2A2A] rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-purple-500 to-blue-500 transition-all duration-500"
            style={{ width: `${((phase + 1) / 5) * 100}%` }}
          />
        </div>
      </div>

      {/* Phase 0: Problem */}
      {phase === 0 && (
        <div className="text-center py-8 animate-fade-in">
          <div className="text-4xl mb-4">🤔</div>
          <h2 className="text-xl font-bold text-white mb-4">Problema</h2>
          <div className="bg-[#1A1A1A] rounded-xl p-6 max-w-md mx-auto">
            <p className="text-gray-300 text-lg">{lesson.problem}</p>
          </div>
          <button
            onClick={() => setPhase(1)}
            className="mt-8 px-8 py-3 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl"
          >
            Mostrar solução →
          </button>
        </div>
      )}

      {/* Phase 1: Concept */}
      {phase === 1 && (
        <div className="text-center py-8 animate-fade-in">
          <div className="text-4xl mb-4">💡</div>
          <h2 className="text-xl font-bold text-white mb-4">Conceito</h2>
          <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 border border-green-500/30 rounded-xl p-6 max-w-md mx-auto">
            <p className="text-white text-lg font-medium">{lesson.concept}</p>
          </div>
          
          {/* Memory anchor */}
          {lesson.memoryAnchor && (
            <div className="mt-4 bg-purple-500/10 border border-purple-500/30 rounded-lg p-4 max-w-md mx-auto">
              <p className="text-purple-400 text-sm font-medium">
                📌 "{lesson.memoryAnchor}"
              </p>
            </div>
          )}
          
          <button
            onClick={() => setPhase(2)}
            className="mt-8 px-8 py-3 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl"
          >
            Ver exemplo →
          </button>
        </div>
      )}

      {/* Phase 2: Visual */}
      {phase === 2 && (
        <div className="text-center py-8 animate-fade-in">
          <div className="text-4xl mb-4">📊</div>
          <h2 className="text-xl font-bold text-white mb-4">Exemplo Visual</h2>
          
          {/* Chart visualization */}
          <div className="bg-[#1A1A1A] rounded-xl p-4 max-w-md mx-auto mb-4">
            <InteractiveChartExample scenario={lesson.scenario} />
          </div>
          
          <p className="text-gray-400 text-sm max-w-md mx-auto mb-6">
            {lesson.visualExplanation}
          </p>
          
          <button
            onClick={() => setPhase(3)}
            className="px-8 py-3 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl"
          >
            Testar agora →
          </button>
        </div>
      )}

      {/* Phase 3: Decision */}
      {phase === 3 && (
        <div className="text-center py-8 animate-fade-in">
          <div className="text-4xl mb-4">🎯</div>
          <h2 className="text-xl font-bold text-white mb-4">A tua vez</h2>
          
          <div className="bg-[#1A1A1A] rounded-xl p-4 max-w-md mx-auto mb-6">
            <InteractiveChartExample scenario={lesson.testScenario} hideAnswer />
          </div>
          
          <p className="text-gray-300 mb-6">{lesson.question}</p>
          
          <div className="flex flex-wrap gap-3 justify-center">
            {lesson.options.map((option, i) => (
              <button
                key={i}
                onClick={() => handleDecision(option.value)}
                className={`px-6 py-3 rounded-xl font-medium transition-all transform hover:scale-105 ${
                  option.color === 'green' ? 'bg-green-600 hover:bg-green-700 text-white' :
                  option.color === 'red' ? 'bg-red-600 hover:bg-red-700 text-white' :
                  option.color === 'yellow' ? 'bg-yellow-600 hover:bg-yellow-700 text-white' :
                  'bg-gray-600 hover:bg-gray-700 text-white'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Phase 4: Feedback */}
      {phase === 4 && (
        <div className="text-center py-8 animate-fade-in">
          <div className={`text-6xl mb-4 ${isCorrect ? 'animate-bounce' : 'animate-shake'}`}>
            {isCorrect ? '✅' : '❌'}
          </div>
          <h2 className={`text-2xl font-bold mb-4 ${isCorrect ? 'text-green-400' : 'text-red-400'}`}>
            {isCorrect ? 'Correto!' : 'Não foi desta vez'}
          </h2>
          
          <div className={`rounded-xl p-6 max-w-md mx-auto mb-6 ${
            isCorrect ? 'bg-green-500/10 border border-green-500/30' : 'bg-red-500/10 border border-red-500/30'
          }`}>
            <p className="text-gray-300">{lesson.feedback[userAnswer] || lesson.feedback.default}</p>
          </div>

          {/* Points earned */}
          <div className="flex justify-center gap-4 mb-6">
            {isCorrect && (
              <>
                <div className="bg-[#1A1A1A] rounded-lg px-4 py-2">
                  <span className="text-green-400 font-bold">+10</span>
                  <span className="text-gray-500 text-sm ml-1">Precisão</span>
                </div>
                {userAnswer === 'wait' && (
                  <div className="bg-[#1A1A1A] rounded-lg px-4 py-2">
                    <span className="text-blue-400 font-bold">+5</span>
                    <span className="text-gray-500 text-sm ml-1">Paciência</span>
                  </div>
                )}
              </>
            )}
          </div>
          
          <button
            onClick={handleComplete}
            className="px-8 py-3 bg-[#58CC02] hover:bg-[#4CAD02] text-white font-bold rounded-xl"
          >
            Continuar →
          </button>
        </div>
      )}
    </div>
  );
};

// ==================== GRÁFICO INTERATIVO ====================

const InteractiveChartExample = ({ scenario, hideAnswer, onDecision }) => {
  const canvasRef = useRef(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Background
    ctx.fillStyle = '#0A0A0A';
    ctx.fillRect(0, 0, width, height);
    
    // Draw based on scenario
    const scenarios = {
      uptrend: { trend: 1, volatility: 0.5 },
      downtrend: { trend: -1, volatility: 0.5 },
      consolidation: { trend: 0, volatility: 0.3 },
      breakout: { trend: 0.8, volatility: 0.8 },
      fakeout: { trend: 0.3, volatility: 1 },
    };
    
    const config = scenarios[scenario] || scenarios.uptrend;
    
    let price = 100;
    const candles = [];
    
    for (let i = 0; i < 20; i++) {
      const change = (Math.random() - 0.5 + config.trend * 0.3) * config.volatility * 3;
      const open = price;
      const close = price + change;
      const high = Math.max(open, close) + Math.random() * config.volatility;
      const low = Math.min(open, close) - Math.random() * config.volatility;
      candles.push({ open, high, low, close });
      price = close;
    }
    
    // Calculate scale
    const minPrice = Math.min(...candles.flatMap(c => [c.low])) - 1;
    const maxPrice = Math.max(...candles.flatMap(c => [c.high])) + 1;
    const priceRange = maxPrice - minPrice;
    const candleWidth = width / 25;
    
    const priceToY = (p) => height - ((p - minPrice) / priceRange) * height * 0.85 - height * 0.075;
    
    // Draw candles
    candles.forEach((candle, i) => {
      const x = (i + 2.5) * candleWidth;
      const isBullish = candle.close > candle.open;
      
      ctx.strokeStyle = isBullish ? '#58CC02' : '#FF4444';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(x, priceToY(candle.high));
      ctx.lineTo(x, priceToY(candle.low));
      ctx.stroke();
      
      ctx.fillStyle = isBullish ? '#58CC02' : '#FF4444';
      const bodyTop = priceToY(Math.max(candle.open, candle.close));
      const bodyHeight = Math.abs(priceToY(candle.open) - priceToY(candle.close)) || 2;
      ctx.fillRect(x - candleWidth/3, bodyTop, candleWidth/1.5, bodyHeight);
    });
    
    // Hide future if needed
    if (hideAnswer) {
      ctx.fillStyle = 'rgba(10,10,10,0.9)';
      ctx.fillRect(width * 0.75, 0, width * 0.25, height);
      ctx.fillStyle = '#9333EA';
      ctx.font = 'bold 24px Arial';
      ctx.fillText('?', width * 0.85, height * 0.5);
    }
    
  }, [scenario, hideAnswer]);
  
  return (
    <canvas 
      ref={canvasRef} 
      width={320} 
      height={180} 
      className="rounded-lg w-full"
    />
  );
};

// ==================== SISTEMA DE PONTUAÇÃO ====================

export const ScoreDisplay = ({ scores }) => {
  return (
    <div className="grid grid-cols-3 gap-3">
      <div className="bg-[#1A1A1A] rounded-xl p-3 text-center">
        <div className="text-2xl font-bold text-green-400">{scores.precision || 0}</div>
        <div className="text-xs text-gray-500">Precisão</div>
        <div className="text-[10px] text-gray-600 mt-1">Decisões certas</div>
      </div>
      <div className="bg-[#1A1A1A] rounded-xl p-3 text-center">
        <div className="text-2xl font-bold text-blue-400">{scores.patience || 0}</div>
        <div className="text-xs text-gray-500">Paciência</div>
        <div className="text-[10px] text-gray-600 mt-1">Saber esperar</div>
      </div>
      <div className="bg-[#1A1A1A] rounded-xl p-3 text-center">
        <div className="text-2xl font-bold text-purple-400">{scores.discipline || 0}</div>
        <div className="text-xs text-gray-500">Disciplina</div>
        <div className="text-[10px] text-gray-600 mt-1">Seguir regras</div>
      </div>
    </div>
  );
};

// ==================== MAPA DE COMPETÊNCIAS ====================

export const SkillMap = ({ skills, currentLevel, onSelectSkill }) => {
  const skillLevels = [
    { id: 'direction', level: 1, name: 'Identificar Direção', icon: '📈', lessons: 6, description: 'Saber se o mercado está a subir ou descer' },
    { id: 'structure', level: 2, name: 'Ler Estrutura', icon: '🏗️', lessons: 6, description: 'Entender máximos e mínimos' },
    { id: 'zones', level: 3, name: 'Encontrar Zonas', icon: '🎯', lessons: 6, description: 'Identificar suporte e resistência' },
    { id: 'timing', level: 4, name: 'Timing de Entradas', icon: '⏱️', lessons: 6, description: 'Saber quando entrar' },
    { id: 'risk', level: 5, name: 'Gerir Risco', icon: '🛡️', lessons: 6, description: 'Proteger o capital' },
    { id: 'emotion', level: 6, name: 'Controlo Emocional', icon: '🧘', lessons: 6, description: 'Manter a calma' },
  ];

  return (
    <div className="space-y-3">
      <h3 className="text-white font-bold text-lg mb-4">🗺️ Mapa de Competências</h3>
      {skillLevels.map((skill, i) => {
        const isUnlocked = skill.level <= currentLevel;
        const isCurrent = skill.level === currentLevel;
        const progress = skills[skill.id]?.progress || 0;
        
        return (
          <button
            key={skill.id}
            onClick={() => isUnlocked && onSelectSkill(skill)}
            disabled={!isUnlocked}
            className={`w-full flex items-center gap-4 p-4 rounded-xl transition-all ${
              isCurrent ? 'bg-purple-500/20 border-2 border-purple-500' :
              isUnlocked ? 'bg-[#1A1A1A] hover:bg-[#252525] border-2 border-transparent' :
              'bg-[#1A1A1A] opacity-50 cursor-not-allowed border-2 border-transparent'
            }`}
          >
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-2xl ${
              isCurrent ? 'bg-purple-500/30' : 'bg-[#2A2A2A]'
            }`}>
              {skill.icon}
            </div>
            
            <div className="flex-1 text-left">
              <div className="flex items-center gap-2">
                <span className="text-white font-medium">{skill.name}</span>
                {isCurrent && (
                  <span className="text-xs bg-purple-500 text-white px-2 py-0.5 rounded">ATUAL</span>
                )}
              </div>
              <div className="text-xs text-gray-500 mt-1">{skill.description}</div>
              
              {isUnlocked && (
                <div className="mt-2">
                  <div className="h-1 bg-[#2A2A2A] rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-[#58CC02]"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                  <div className="text-xs text-gray-600 mt-1">{progress}% completo</div>
                </div>
              )}
            </div>
            
            {!isUnlocked && (
              <span className="text-gray-600 text-xl">🔒</span>
            )}
          </button>
        );
      })}
    </div>
  );
};

// ==================== CARTÕES DESLIZÁVEIS ====================

export const SwipeCards = ({ cards, onComplete }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [swipeDirection, setSwipeDirection] = useState(null);

  const currentCard = cards[currentIndex];

  const handleSwipe = (direction) => {
    setSwipeDirection(direction);
    setTimeout(() => {
      if (currentIndex < cards.length - 1) {
        setCurrentIndex(prev => prev + 1);
        setSwipeDirection(null);
      } else {
        onComplete();
      }
    }, 300);
  };

  if (!currentCard) return null;

  return (
    <div className="relative h-[400px] w-full max-w-sm mx-auto">
      <div 
        className={`absolute inset-0 bg-gradient-to-br from-[#1A1A1A] to-[#252525] rounded-2xl p-6 transition-all duration-300 ${
          swipeDirection === 'left' ? '-translate-x-full opacity-0 rotate-[-20deg]' :
          swipeDirection === 'right' ? 'translate-x-full opacity-0 rotate-[20deg]' : ''
        }`}
      >
        <div className="text-center h-full flex flex-col">
          <div className="text-4xl mb-4">{currentCard.icon}</div>
          <h3 className="text-xl font-bold text-white mb-4">{currentCard.title}</h3>
          <p className="text-gray-300 flex-1">{currentCard.content}</p>
          
          {currentCard.type === 'memory' && (
            <div className="bg-purple-500/20 border border-purple-500/50 rounded-lg p-4 mt-4">
              <p className="text-purple-400 font-medium">📌 {currentCard.anchor}</p>
            </div>
          )}
          
          <div className="flex gap-4 mt-6">
            <button
              onClick={() => handleSwipe('left')}
              className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-xl"
            >
              ← Anterior
            </button>
            <button
              onClick={() => handleSwipe('right')}
              className="flex-1 py-3 bg-[#58CC02] hover:bg-[#4CAD02] text-white rounded-xl"
            >
              Próximo →
            </button>
          </div>
        </div>
      </div>
      
      {/* Progress */}
      <div className="absolute -bottom-8 left-0 right-0 flex justify-center gap-1">
        {cards.map((_, i) => (
          <div 
            key={i}
            className={`w-2 h-2 rounded-full ${i === currentIndex ? 'bg-purple-500' : 'bg-gray-700'}`}
          />
        ))}
      </div>
    </div>
  );
};

// ==================== DADOS DE LIÇÕES ====================

export const LESSON_DATA = {
  direction: {
    level1: [
      {
        id: 'dir-1',
        category: 'Identificar Direção',
        problem: 'O mercado está a mostrar velas verdes e vermelhas. Como sabes para onde está a ir?',
        concept: 'Uma tendência de alta tem máximos e mínimos cada vez mais altos. Uma tendência de baixa tem máximos e mínimos cada vez mais baixos.',
        memoryAnchor: 'Máximos mais altos = Alta. Mínimos mais baixos = Baixa.',
        scenario: 'uptrend',
        testScenario: 'uptrend',
        visualExplanation: 'Repara como cada pico é mais alto que o anterior, e cada fundo também.',
        question: 'Qual é a direção deste mercado?',
        options: [
          { value: 'up', label: '📈 Alta', color: 'green' },
          { value: 'down', label: '📉 Baixa', color: 'red' },
          { value: 'sideways', label: '↔️ Lateral', color: 'yellow' },
        ],
        correctAnswer: 'up',
        feedback: {
          up: 'Excelente! Os máximos e mínimos estão a subir, é claramente uma tendência de alta.',
          down: 'Olha com mais atenção. Os picos estão cada vez mais altos, não mais baixos.',
          sideways: 'Há movimento claro para cima. Lateral seria se os preços andassem entre dois níveis.',
          default: 'Analisa os máximos e mínimos para identificar a direção.'
        }
      },
      // More lessons...
    ]
  }
};

export default { OnboardingFlow, LessonCycle, ScoreDisplay, SkillMap, SwipeCards, LESSON_DATA };
