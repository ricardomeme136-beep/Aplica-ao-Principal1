import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import InteractiveChart from './InteractiveChart';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

/**
 * Interactive Exercise Screen - Full Screen Chart Layout
 * Chart fills all available space, no empty black areas
 */
const InteractiveExerciseScreen = ({ category, level, user, onBack, onComplete }) => {
  const [exercises, setExercises] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [selectedPrice, setSelectedPrice] = useState(null);
  const [drawnZone, setDrawnZone] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [result, setResult] = useState(null);
  const [sessionXP, setSessionXP] = useState(0);
  const [showHint, setShowHint] = useState(false);
  
  // Lesson intro state
  const [lessonIntro, setLessonIntro] = useState(null);
  const [showIntro, setShowIntro] = useState(true);

  useEffect(() => {
    fetchLessonIntro();
    fetchExercises();
  }, [category, level, user]);

  const fetchLessonIntro = async () => {
    try {
      // Map interactive category to regular category for intro
      const categoryMap = {
        'chart_candlesticks': 'candlesticks',
        'chart_swing': 'market-structure',
        'chart_liquidity': 'liquidity',
        'chart_bos': 'bos',
        'chart_choch': 'choch',
        'chart_ob': 'order-blocks',
        'chart_fvg': 'fvg'
      };
      const introCategory = categoryMap[category.id] || category.id;
      
      const response = await axios.get(
        `${API}/curriculum/categories/${introCategory}/levels/${level.level}/intro`
      );
      if (response.data.has_intro) {
        setLessonIntro(response.data);
      } else {
        setShowIntro(false);
      }
    } catch (error) {
      setShowIntro(false);
    }
  };

  const fetchExercises = async () => {
    try {
      const response = await axios.get(
        `${API}/interactive/exercises/${category.id}/level/${level.level}?user_id=${user.id}`
      );
      const exerciseList = response.data;
      const firstIncomplete = exerciseList.findIndex(ex => !ex.is_completed);
      setExercises(exerciseList);
      setCurrentIndex(firstIncomplete >= 0 ? firstIncomplete : 0);
    } catch (error) {
      console.error('Failed to load exercises:', error);
      toast.error('Failed to load exercises');
    } finally {
      setLoading(false);
    }
  };

  const currentExercise = exercises[currentIndex];
  const progress = ((currentIndex + 1) / exercises.length) * 100;
  
  const getDrawMode = () => {
    if (category.id === 'chart_fvg') return 'rectangle';
    if (category.id.startsWith('chart_')) return 'line';
    return 'none';
  };
  const drawModeType = getDrawMode();

  const handlePriceClick = (price) => {
    if (showResult || submitting) return;
    setSelectedPrice(price);
    setDrawnZone(null);
    setShowHint(false);
  };

  const handleZoneDrawn = (zone) => {
    if (showResult || submitting) return;
    setDrawnZone(zone);
    setSelectedPrice(null);
    setShowHint(false);
  };

  const handleLineDrawn = (line) => {
    if (showResult || submitting) return;
    setSelectedPrice(line.price);
    setDrawnZone(null);
    setShowHint(false);
  };

  const handleSubmit = async () => {
    if (drawModeType === 'rectangle' && !drawnZone) return;
    if (drawModeType === 'line' && selectedPrice === null) return;
    if (submitting) return;

    setSubmitting(true);
    try {
      const submitData = {
        user_id: user.id,
        exercise_id: currentExercise.id,
        clicked_time: currentExercise.candles[0]?.time
      };

      if (drawModeType === 'rectangle' && drawnZone) {
        submitData.zone_high = drawnZone.high;
        submitData.zone_low = drawnZone.low;
        submitData.clicked_price = (drawnZone.high + drawnZone.low) / 2;
      } else {
        submitData.clicked_price = selectedPrice;
      }

      const response = await axios.post(`${API}/interactive/exercises/submit`, submitData);
      setResult(response.data);
      setSessionXP(prev => prev + response.data.xp_gained);
      setShowResult(true);
    } catch (error) {
      console.error('Submit error:', error);
      toast.error('Failed to submit answer');
    } finally {
      setSubmitting(false);
    }
  };

  const handleNext = () => {
    if (currentIndex < exercises.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setSelectedPrice(null);
      setDrawnZone(null);
      setShowResult(false);
      setResult(null);
      setShowHint(false);
    } else {
      onComplete(sessionXP);
    }
  };

  const handleRetry = () => {
    setSelectedPrice(null);
    setDrawnZone(null);
    setShowResult(false);
    setResult(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0A0A0A]">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-[#58CC02]"></div>
      </div>
    );
  }

  if (!currentExercise) {
    return (
      <div className="h-screen bg-[#0A0A0A] flex items-center justify-center">
        <div className="text-center">
          <p className="text-white mb-4">No exercises available</p>
          <button onClick={onBack} className="text-[#58CC02]">Go Back</button>
        </div>
      </div>
    );
  }

  const canSubmit = drawModeType === 'rectangle' ? drawnZone !== null : selectedPrice !== null;

  // Show lesson intro first
  if (showIntro && lessonIntro) {
    return (
      <div className="h-screen bg-[#0A0A0A] flex flex-col overflow-hidden" data-testid="lesson-intro-screen">
        {/* Header */}
        <div className="bg-[#1A1A1A] px-4 py-3 flex items-center gap-3 shrink-0">
          <button onClick={onBack} className="text-white hover:text-gray-300">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div className="flex-1">
            <h1 className="text-white font-bold text-lg">{category.name}</h1>
            <p className="text-gray-400 text-xs">Level {level.level} - Interactive</p>
          </div>
          <span className="text-gray-400 text-xs flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {lessonIntro.duration}
          </span>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-4">
          {/* Title Section */}
          <div className="mb-6 text-center">
            <h2 className="text-2xl font-bold text-white mb-2">{lessonIntro.title}</h2>
            <p className="text-[#58CC02] text-sm">{lessonIntro.subtitle}</p>
          </div>

          {/* Image */}
          {lessonIntro.image && (
            <div className="mb-6 rounded-xl overflow-hidden">
              <img 
                src={lessonIntro.image} 
                alt={lessonIntro.title}
                className="w-full h-48 object-cover"
              />
            </div>
          )}

          {/* Content - Markdown style */}
          <div className="bg-[#1A1A1A] rounded-xl p-4 mb-6">
            <div className="prose prose-invert prose-sm max-w-none">
              {lessonIntro.content.split('\n').map((line, index) => {
                if (line.startsWith('## ')) {
                  return <h3 key={index} className="text-[#58CC02] font-bold text-lg mt-4 mb-2">{line.replace('## ', '')}</h3>;
                }
                if (line.startsWith('### ')) {
                  return <h4 key={index} className="text-[#FF9600] font-bold text-base mt-3 mb-1">{line.replace('### ', '')}</h4>;
                }
                if (line.includes('**')) {
                  const parts = line.split(/\*\*(.*?)\*\*/g);
                  return (
                    <p key={index} className="text-gray-300 text-sm mb-2">
                      {parts.map((part, i) => 
                        i % 2 === 1 ? <strong key={i} className="text-white">{part}</strong> : part
                      )}
                    </p>
                  );
                }
                if (line.startsWith('• ') || line.startsWith('- ')) {
                  return (
                    <div key={index} className="flex items-start gap-2 mb-1">
                      <span className="text-[#58CC02] mt-1">•</span>
                      <p className="text-gray-300 text-sm">{line.replace(/^[•-]\s*/, '')}</p>
                    </div>
                  );
                }
                if (line.startsWith('```')) return null;
                if (line.trim()) {
                  return <p key={index} className="text-gray-300 text-sm mb-2">{line}</p>;
                }
                return null;
              })}
            </div>
          </div>

          {/* Key Points */}
          {lessonIntro.key_points && lessonIntro.key_points.length > 0 && (
            <div className="bg-[#1A1A1A] rounded-xl p-4 mb-6 border border-[#58CC02]/30">
              <h4 className="text-[#58CC02] font-bold mb-3 flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Pontos Chave
              </h4>
              <ul className="space-y-2">
                {lessonIntro.key_points.map((point, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="text-[#58CC02] font-bold">{index + 1}.</span>
                    <span className="text-gray-300 text-sm">{point}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Start Button */}
        <div className="p-4 bg-[#1A1A1A] shrink-0">
          <button
            onClick={() => setShowIntro(false)}
            className="w-full py-4 bg-[#58CC02] hover:bg-[#4CAD02] text-white font-bold rounded-xl text-lg transition-all"
            data-testid="start-interactive-btn"
          >
            Começar Exercícios Interativos
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen bg-[#0A0A0A] flex flex-col" data-testid="interactive-exercise-screen">
      {/* Header - Fixed Height */}
      <div className="bg-[#1A1A1A] px-3 py-2 flex items-center gap-2 shrink-0">
        <button onClick={onBack} className="text-white hover:text-gray-300" data-testid="interactive-back-btn">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div className="flex-1">
          <div className="h-1.5 bg-[#2A2A2A] rounded-full overflow-hidden">
            <div className="h-full bg-[#58CC02] transition-all" style={{ width: `${progress}%` }} />
          </div>
        </div>
        <span className="text-white text-xs font-medium">{currentIndex + 1}/{exercises.length}</span>
        <span className="text-[#FF9600] text-xs font-medium">+{sessionXP} XP</span>
      </div>

      {/* Title Bar - Compact */}
      <div className="bg-[#131313] px-3 py-1.5 flex items-center justify-between shrink-0 border-b border-[#2A2A2A]">
        <div className="flex-1 min-w-0">
          <h2 className="text-sm font-bold text-white truncate">{currentExercise.title}</h2>
          <p className="text-gray-400 text-xs truncate">{currentExercise.instruction}</p>
        </div>
        {currentExercise.hints?.length > 0 && !showResult && (
          <button
            onClick={() => setShowHint(!showHint)}
            className="text-[#58CC02] text-xs flex items-center gap-1 hover:underline shrink-0 ml-2"
          >
            💡 {showHint ? 'Hide' : 'Hint'}
          </button>
        )}
      </div>

      {/* Hint Panel - Only shows when active */}
      {showHint && (
        <div className="px-3 py-1.5 bg-[#1A1A1A] border-b border-[#58CC02]/30 shrink-0">
          <div className="text-xs text-gray-300 flex flex-wrap gap-2">
            {currentExercise.hints.map((hint, idx) => (
              <span key={idx} className="flex items-center gap-1">
                <span className="text-[#58CC02]">•</span>
                <span>{hint}</span>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Chart - FILLS ALL REMAINING SPACE */}
      <div className="flex-1 min-h-0">
        <InteractiveChart
          candles={currentExercise.candles}
          onPriceClick={handlePriceClick}
          onZoneDrawn={handleZoneDrawn}
          onLineDrawn={handleLineDrawn}
          correctAnswer={currentExercise.correct_answer}
          showAnswer={showResult}
          targetPart={currentExercise.target_part}
          drawMode={drawModeType}
          height="100%"
        />
      </div>

      {/* Bottom Panel - Fixed at bottom */}
      <div className="bg-[#131313] px-3 py-2 shrink-0 border-t border-[#2A2A2A]">
        {/* Result Display */}
        {showResult && result ? (
          <div className={`p-2 rounded-lg mb-2 ${result.is_correct ? 'bg-[#2D5016]' : 'bg-[#4B1A1A]'}`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {result.is_correct ? (
                  <>
                    <span className="w-5 h-5 bg-[#58CC02] rounded-full flex items-center justify-center">
                      <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                    <span className="text-white font-bold text-xs">Correct!</span>
                    {result.xp_gained > 0 && <span className="text-[#FF9600] text-xs">+{result.xp_gained} XP</span>}
                  </>
                ) : (
                  <>
                    <span className="w-5 h-5 bg-[#FF4B4B] rounded-full flex items-center justify-center">
                      <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </span>
                    <span className="text-white font-bold text-xs">Not quite</span>
                  </>
                )}
              </div>
              <div className="flex gap-3 text-xs">
                <span className="text-gray-400">You: <span className="text-white">
                  {drawnZone ? `$${drawnZone.low.toFixed(0)}-$${drawnZone.high.toFixed(0)}` : `$${result.clicked_price?.toFixed(2)}`}
                </span></span>
                <span className="text-gray-400">Answer: <span className="text-[#58CC02]">
                  {currentExercise.correct_answer.price_high 
                    ? `$${currentExercise.correct_answer.price_low?.toFixed(0)}-$${currentExercise.correct_answer.price_high?.toFixed(0)}`
                    : `$${result.correct_price?.toFixed(2)}`}
                </span></span>
              </div>
            </div>
          </div>
        ) : (
          /* Selection indicator when drawing */
          (selectedPrice !== null || drawnZone) && (
            <div className="flex items-center justify-between p-2 bg-[#2A2A2A] rounded-lg mb-2">
              <div className="flex items-center gap-2">
                <span className="text-gray-400 text-xs">Your answer:</span>
                <span className="text-white font-bold text-sm">
                  {drawnZone ? `$${drawnZone.low.toFixed(2)} - $${drawnZone.high.toFixed(2)}` : `$${selectedPrice?.toFixed(2)}`}
                </span>
              </div>
              <button
                onClick={() => { setSelectedPrice(null); setDrawnZone(null); }}
                className="text-gray-400 hover:text-white text-xs"
              >
                Redraw
              </button>
            </div>
          )
        )}

        {/* Action Buttons */}
        {!showResult ? (
          <button
            onClick={handleSubmit}
            disabled={!canSubmit || submitting}
            className="w-full bg-[#58CC02] hover:bg-[#4CAF00] text-white font-bold py-2.5 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
            data-testid="submit-interactive-btn"
          >
            {submitting ? 'Checking...' : 'Check Answer'}
          </button>
        ) : (
          <div className="flex gap-2">
            {!result?.is_correct && (
              <button
                onClick={handleRetry}
                className="flex-1 bg-[#2A2A2A] hover:bg-[#3A3A3A] text-white font-bold py-2.5 rounded-xl text-sm"
                data-testid="retry-btn"
              >
                Try Again
              </button>
            )}
            <button
              onClick={handleNext}
              className="flex-1 bg-[#58CC02] hover:bg-[#4CAF00] text-white font-bold py-2.5 rounded-xl text-sm"
              data-testid="next-interactive-btn"
            >
              {currentIndex < exercises.length - 1 ? 'Continue' : 'Complete'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default InteractiveExerciseScreen;
