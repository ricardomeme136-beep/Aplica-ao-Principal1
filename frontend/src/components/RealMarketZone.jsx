import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { toast } from 'sonner';

const API = process.env.REACT_APP_BACKEND_URL + '/api';

// ==================== EMOTION SELECTOR ====================
const EmotionSelector = ({ value, onChange, label }) => {
  const emotions = [
    { id: 'neutral', emoji: '😐', label: 'Neutral' },
    { id: 'anxious', emoji: '😬', label: 'Anxious' },
    { id: 'frustrated', emoji: '😡', label: 'Frustrated' },
    { id: 'confident', emoji: '😎', label: 'Confident' },
  ];

  return (
    <div className="mb-4">
      <label className="block text-sm text-gray-400 mb-2">{label}</label>
      <div className="grid grid-cols-4 gap-2">
        {emotions.map((emotion) => (
          <button
            key={emotion.id}
            type="button"
            onClick={() => onChange(emotion.id)}
            className={`p-3 rounded-lg border-2 transition-all flex flex-col items-center ${
              value === emotion.id
                ? 'border-[#58CC02] bg-[#58CC02]/20'
                : 'border-gray-700 hover:border-gray-500'
            }`}
          >
            <span className="text-2xl mb-1">{emotion.emoji}</span>
            <span className="text-xs text-gray-300">{emotion.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

// ==================== VIOLATION SELECTOR ====================
const ViolationSelector = ({ violations, onChange }) => {
  const violationTypes = [
    { id: 'moved_stop', label: 'Moved stop loss' },
    { id: 'entry_outside_plan', label: 'Entry outside the plan' },
    { id: 'overtrading', label: 'Overtrading' },
    { id: 'fomo', label: 'FOMO' },
    { id: 'other', label: 'Other' },
  ];

  const toggleViolation = (id) => {
    if (violations.includes(id)) {
      onChange(violations.filter(v => v !== id));
    } else {
      onChange([...violations, id]);
    }
  };

  return (
    <div className="space-y-2">
      {violationTypes.map((v) => (
        <button
          key={v.id}
          type="button"
          onClick={() => toggleViolation(v.id)}
          className={`w-full p-2 rounded-lg border text-left text-sm transition-all ${
            violations.includes(v.id)
              ? 'border-red-500 bg-red-500/20 text-red-300'
              : 'border-gray-700 text-gray-400 hover:border-gray-500'
          }`}
        >
          <span className="mr-2">{violations.includes(v.id) ? '☑' : '☐'}</span>
          {v.label}
        </button>
      ))}
    </div>
  );
};

// ==================== CANDLESTICK CHART ====================
const CandlestickChart = ({ candles, orbRange, activeTrade, onCandleClick, onPriceSelect }) => {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 400 });
  const [selectedCandle, setSelectedCandle] = useState(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });
  const [chartParams, setChartParams] = useState(null);

  useEffect(() => {
    if (containerRef.current) {
      const { width } = containerRef.current.getBoundingClientRect();
      setDimensions({ width: Math.max(width - 20, 400), height: 350 });
    }
  }, []);

  useEffect(() => {
    if (!canvasRef.current || candles.length === 0) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const { width, height } = dimensions;

    // Clear
    ctx.fillStyle = '#0A0A0A';
    ctx.fillRect(0, 0, width, height);

    // Calculate price range
    const prices = candles.flatMap(c => [c.high, c.low]);
    const minPrice = Math.min(...prices) * 0.999;
    const maxPrice = Math.max(...prices) * 1.001;
    const priceRange = maxPrice - minPrice;

    // Candle dimensions
    const padding = 50;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    const candleWidth = Math.max(3, Math.min(15, chartWidth / candles.length - 2));
    const candleSpacing = chartWidth / candles.length;

    // Store chart params for click detection
    setChartParams({ padding, chartWidth, chartHeight, candleSpacing, candleWidth, minPrice, maxPrice, priceRange });

    // Helper functions
    const priceToY = (price) => padding + (1 - (price - minPrice) / priceRange) * chartHeight;
    const indexToX = (index) => padding + index * candleSpacing + candleSpacing / 2;

    // Draw grid
    ctx.strokeStyle = '#1A1A1A';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
      const y = padding + (chartHeight / 5) * i;
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(width - padding, y);
      ctx.stroke();

      // Price labels
      const price = maxPrice - (priceRange / 5) * i;
      ctx.fillStyle = '#666';
      ctx.font = '10px Arial';
      ctx.fillText(price.toFixed(4), 5, y + 3);
    }

    // Draw ORB range
    if (orbRange) {
      const orbHighY = priceToY(orbRange.high);
      const orbLowY = priceToY(orbRange.low);

      ctx.fillStyle = 'rgba(88, 204, 2, 0.1)';
      ctx.fillRect(padding, orbHighY, chartWidth, orbLowY - orbHighY);

      ctx.setLineDash([5, 5]);
      ctx.strokeStyle = '#58CC02';
      ctx.lineWidth = 2;

      ctx.beginPath();
      ctx.moveTo(padding, orbHighY);
      ctx.lineTo(width - padding, orbHighY);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(padding, orbLowY);
      ctx.lineTo(width - padding, orbLowY);
      ctx.stroke();

      ctx.setLineDash([]);

      // Labels
      ctx.fillStyle = '#58CC02';
      ctx.font = 'bold 10px Arial';
      ctx.fillText(`ORB High: ${orbRange.high.toFixed(4)}`, width - padding - 100, orbHighY - 5);
      ctx.fillText(`ORB Low: ${orbRange.low.toFixed(4)}`, width - padding - 100, orbLowY + 12);
    }

    // Draw candles
    candles.forEach((candle, index) => {
      const x = indexToX(index);
      const openY = priceToY(candle.open);
      const closeY = priceToY(candle.close);
      const highY = priceToY(candle.high);
      const lowY = priceToY(candle.low);

      const isBullish = candle.close > candle.open;
      const bodyColor = isBullish ? '#58CC02' : '#FF4444';
      const wickColor = isBullish ? '#58CC02' : '#FF4444';

      // Highlight selected candle
      if (selectedCandle && selectedCandle.index === index) {
        ctx.fillStyle = 'rgba(147, 51, 234, 0.3)';
        ctx.fillRect(x - candleSpacing / 2, padding, candleSpacing, chartHeight);
      }

      // Draw wick
      ctx.strokeStyle = wickColor;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(x, highY);
      ctx.lineTo(x, lowY);
      ctx.stroke();

      // Draw body
      ctx.fillStyle = bodyColor;
      const bodyTop = Math.min(openY, closeY);
      const bodyHeight = Math.max(1, Math.abs(closeY - openY));
      ctx.fillRect(x - candleWidth / 2, bodyTop, candleWidth, bodyHeight);
    });

    // Draw active trade lines
    if (activeTrade) {
      const entryY = priceToY(activeTrade.entry_price);
      const stopY = priceToY(activeTrade.stop_loss);

      // Entry line
      ctx.strokeStyle = '#00D4FF';
      ctx.lineWidth = 2;
      ctx.setLineDash([3, 3]);
      ctx.beginPath();
      ctx.moveTo(padding, entryY);
      ctx.lineTo(width - padding, entryY);
      ctx.stroke();

      // Stop loss line
      ctx.strokeStyle = '#FF4444';
      ctx.beginPath();
      ctx.moveTo(padding, stopY);
      ctx.lineTo(width - padding, stopY);
      ctx.stroke();

      // Take profit line
      if (activeTrade.take_profit) {
        const tpY = priceToY(activeTrade.take_profit);
        ctx.strokeStyle = '#58CC02';
        ctx.beginPath();
        ctx.moveTo(padding, tpY);
        ctx.lineTo(width - padding, tpY);
        ctx.stroke();
      }

      ctx.setLineDash([]);
    }

  }, [candles, orbRange, activeTrade, dimensions, selectedCandle]);

  const handleCanvasClick = (e) => {
    if (!chartParams || !candles.length) return;

    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const { padding, candleSpacing } = chartParams;

    // Check if click is within chart area
    if (x < padding || x > dimensions.width - padding) return;

    // Find which candle was clicked
    const candleIndex = Math.floor((x - padding) / candleSpacing);
    if (candleIndex >= 0 && candleIndex < candles.length) {
      const candle = candles[candleIndex];
      setSelectedCandle({ ...candle, index: candleIndex });
      setTooltipPos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
    }
  };

  const handlePriceCopy = (price, label) => {
    navigator.clipboard.writeText(price.toString());
    toast.success(`${label}: ${price.toFixed(4)} copied!`);
    if (onPriceSelect) {
      onPriceSelect(price, label);
    }
  };

  const closeTooltip = () => {
    setSelectedCandle(null);
  };

  return (
    <div ref={containerRef} className="w-full relative">
      <canvas
        ref={canvasRef}
        width={dimensions.width}
        height={dimensions.height}
        className="bg-[#0A0A0A] rounded-lg cursor-crosshair"
        onClick={handleCanvasClick}
      />
      
      {/* Click hint */}
      <div className="absolute top-2 right-2 text-xs text-gray-500 bg-[#1A1A1A]/80 px-2 py-1 rounded">
        Click candle to copy price
      </div>

      {/* Candle Price Tooltip */}
      {selectedCandle && (
        <div 
          className="absolute z-20 bg-[#1A1A1A] border border-purple-500/50 rounded-lg shadow-xl p-3 min-w-[180px]"
          style={{
            left: Math.min(tooltipPos.x, dimensions.width - 200),
            top: Math.max(10, tooltipPos.y - 160),
          }}
        >
          <div className="flex justify-between items-center mb-2">
            <span className="text-white font-semibold text-sm">Candle #{selectedCandle.index + 1}</span>
            <button onClick={closeTooltip} className="text-gray-400 hover:text-white">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div className="space-y-1">
            <button 
              onClick={() => handlePriceCopy(selectedCandle.high, 'High')}
              className="w-full flex justify-between items-center p-2 rounded hover:bg-purple-500/20 transition-colors group"
            >
              <span className="text-green-400 text-xs">High</span>
              <span className="text-white font-mono text-sm group-hover:text-purple-400">
                {selectedCandle.high.toFixed(4)}
              </span>
            </button>
            
            <button 
              onClick={() => handlePriceCopy(selectedCandle.low, 'Low')}
              className="w-full flex justify-between items-center p-2 rounded hover:bg-purple-500/20 transition-colors group"
            >
              <span className="text-red-400 text-xs">Low</span>
              <span className="text-white font-mono text-sm group-hover:text-purple-400">
                {selectedCandle.low.toFixed(4)}
              </span>
            </button>
            
            <button 
              onClick={() => handlePriceCopy(selectedCandle.open, 'Open')}
              className="w-full flex justify-between items-center p-2 rounded hover:bg-purple-500/20 transition-colors group"
            >
              <span className="text-gray-400 text-xs">Open</span>
              <span className="text-white font-mono text-sm group-hover:text-purple-400">
                {selectedCandle.open.toFixed(4)}
              </span>
            </button>
            
            <button 
              onClick={() => handlePriceCopy(selectedCandle.close, 'Close')}
              className="w-full flex justify-between items-center p-2 rounded hover:bg-purple-500/20 transition-colors group"
            >
              <span className="text-blue-400 text-xs">Close</span>
              <span className="text-white font-mono text-sm group-hover:text-purple-400">
                {selectedCandle.close.toFixed(4)}
              </span>
            </button>
          </div>
          
          <div className="mt-2 pt-2 border-t border-gray-700 text-xs text-gray-500 text-center">
            Click price to copy
          </div>
        </div>
      )}
    </div>
  );
};

// ==================== TRADE EVALUATION MODAL ====================
const TradeEvaluationModal = ({ trade, currentPrice, onComplete, onCancel }) => {
  const [emotionBefore, setEmotionBefore] = useState('');
  const [emotionAfter, setEmotionAfter] = useState('');
  const [hasViolation, setHasViolation] = useState(false);
  const [violations, setViolations] = useState([]);

  const handleSubmit = () => {
    if (!emotionBefore || !emotionAfter) {
      toast.error('Please select emotions before and after the trade');
      return;
    }

    onComplete({
      emotion_before: emotionBefore,
      emotion_after: emotionAfter,
      rule_violation: hasViolation,
      violation_types: hasViolation ? violations : [],
      exit_price: currentPrice
    });
  };

  const result = trade.direction === 'BUY' 
    ? currentPrice - trade.entry_price 
    : trade.entry_price - currentPrice;
  const isProfit = result > 0;

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="bg-[#1A1A1A] rounded-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <h2 className="text-xl font-bold text-white mb-2">📝 Trade Evaluation</h2>
          <p className="text-gray-400 text-sm mb-6">
            Complete this evaluation before continuing
          </p>

          {/* Trade Summary */}
          <div className={`p-4 rounded-xl mb-6 ${isProfit ? 'bg-green-900/30' : 'bg-red-900/30'}`}>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Result</span>
              <span className={`font-bold ${isProfit ? 'text-green-400' : 'text-red-400'}`}>
                {isProfit ? '+' : ''}{result.toFixed(4)}
              </span>
            </div>
            <div className="flex justify-between items-center mt-2">
              <span className="text-gray-400">Direction</span>
              <span className={`font-bold ${trade.direction === 'BUY' ? 'text-green-400' : 'text-red-400'}`}>
                {trade.direction}
              </span>
            </div>
          </div>

          {/* Emotion Before */}
          <EmotionSelector
            value={emotionBefore}
            onChange={setEmotionBefore}
            label="😊 How did you feel BEFORE the trade?"
          />

          {/* Emotion After */}
          <EmotionSelector
            value={emotionAfter}
            onChange={setEmotionAfter}
            label="😊 How do you feel AFTER the trade?"
          />

          {/* Rule Compliance */}
          <div className="mb-4">
            <label className="block text-sm text-gray-400 mb-2">
              ⚖️ Did you violate any rule?
            </label>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => { setHasViolation(false); setViolations([]); }}
                className={`flex-1 p-3 rounded-lg border-2 transition-all ${
                  !hasViolation
                    ? 'border-green-500 bg-green-500/20 text-green-400'
                    : 'border-gray-700 text-gray-400'
                }`}
              >
                ✓ No
              </button>
              <button
                type="button"
                onClick={() => setHasViolation(true)}
                className={`flex-1 p-3 rounded-lg border-2 transition-all ${
                  hasViolation
                    ? 'border-red-500 bg-red-500/20 text-red-400'
                    : 'border-gray-700 text-gray-400'
                }`}
              >
                ✗ Yes
              </button>
            </div>
          </div>

          {/* Violation Types */}
          {hasViolation && (
            <div className="mb-6">
              <label className="block text-sm text-gray-400 mb-2">
                Select violation type(s):
              </label>
              <ViolationSelector violations={violations} onChange={setViolations} />
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3">
            <button
              onClick={onCancel}
              className="flex-1 py-3 bg-gray-700 text-white rounded-xl hover:bg-gray-600 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleSubmit}
              className="flex-1 py-3 bg-[#58CC02] text-white font-bold rounded-xl hover:bg-[#4CAD02] transition-colors"
            >
              Complete →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// ==================== DISCIPLINE DASHBOARD ====================
const DisciplineDashboard = ({ userId, onClose }) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchData();
  }, [userId]);

  const fetchData = async () => {
    try {
      const [scoreRes, historyRes] = await Promise.all([
        axios.get(`${API}/real-market/discipline-score/${userId}`),
        axios.get(`${API}/real-market/history/${userId}?limit=20`)
      ]);
      setData(scoreRes.data);
      setHistory(historyRes.data);
    } catch (error) {
      toast.error('Failed to load discipline data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#58CC02]"></div>
      </div>
    );
  }

  const score = data?.score || {};
  const insights = data?.insights || [];

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="bg-[#1A1A1A] rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-white">📊 Discipline Dashboard</h2>
            <button onClick={onClose} className="text-gray-400 hover:text-white">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Score Cards */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-[#0A0A0A] p-4 rounded-xl">
              <div className="text-3xl font-bold text-[#58CC02]">{score.discipline_score || 0}</div>
              <div className="text-sm text-gray-400">Discipline Score</div>
            </div>
            <div className="bg-[#0A0A0A] p-4 rounded-xl">
              <div className="text-3xl font-bold text-[#FF9600]">{score.emotional_consistency_score || 0}%</div>
              <div className="text-sm text-gray-400">Emotional Consistency</div>
            </div>
            <div className="bg-[#0A0A0A] p-4 rounded-xl">
              <div className="text-3xl font-bold text-white">{score.total_trades || 0}</div>
              <div className="text-sm text-gray-400">Total Trades</div>
            </div>
            <div className="bg-[#0A0A0A] p-4 rounded-xl">
              <div className="text-3xl font-bold text-green-400">{score.stop_usage_rate || 0}%</div>
              <div className="text-sm text-gray-400">Stop Loss Usage</div>
            </div>
          </div>

          {/* Insights */}
          <div className="mb-6">
            <h3 className="text-white font-semibold mb-3">💡 Insights</h3>
            <div className="space-y-2">
              {insights.map((insight, index) => (
                <div key={index} className="bg-[#0A0A0A] p-3 rounded-lg text-sm text-gray-300">
                  {insight}
                </div>
              ))}
            </div>
          </div>

          {/* Recent Trades */}
          {history.length > 0 && (
            <div>
              <h3 className="text-white font-semibold mb-3">📈 Recent Trades</h3>
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {history.slice(0, 10).map((trade, index) => (
                  <div key={index} className="bg-[#0A0A0A] p-3 rounded-lg flex items-center justify-between">
                    <div>
                      <span className="text-white font-medium">{trade.asset}</span>
                      <span className={`ml-2 text-sm ${trade.direction === 'BUY' ? 'text-green-400' : 'text-red-400'}`}>
                        {trade.direction}
                      </span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className={`text-sm ${trade.result_in_r >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {trade.result_in_r >= 0 ? '+' : ''}{trade.result_in_r}R
                      </span>
                      {trade.rule_violation && (
                        <span className="text-xs bg-red-500/20 text-red-400 px-2 py-1 rounded">
                          Violation
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ==================== MAIN REAL MARKET COMPONENT ====================
const RealMarketZone = ({ user, onBack }) => {
  const [view, setView] = useState('intro'); // 'intro', 'replay', 'dashboard'
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState('EURUSD');
  const [assets, setAssets] = useState([]);
  
  // Trade state
  const [orbMarking, setOrbMarking] = useState(false);
  const [orbHigh, setOrbHigh] = useState('');
  const [orbLow, setOrbLow] = useState('');
  const [tradeDirection, setTradeDirection] = useState('BUY');
  const [entryPrice, setEntryPrice] = useState('');
  const [stopLoss, setStopLoss] = useState('');
  const [takeProfit, setTakeProfit] = useState('');
  const [selectedTimeframe, setSelectedTimeframe] = useState('15m');
  
  // Evaluation modal
  const [showEvaluation, setShowEvaluation] = useState(false);
  const [pendingClose, setPendingClose] = useState(null);

  const timeframes = [
    { id: '1m', label: '1m', minutes: 1 },
    { id: '5m', label: '5m', minutes: 5 },
    { id: '15m', label: '15m', minutes: 15 },
  ];

  useEffect(() => {
    fetchAssets();
  }, []);

  const fetchAssets = async () => {
    try {
      const res = await axios.get(`${API}/real-market/assets`);
      setAssets(res.data);
    } catch (error) {
      console.error('Failed to fetch assets');
    }
  };

  const startSession = async (timeframe = selectedTimeframe) => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/real-market/start-session`, {
        user_id: user.id,
        asset: selectedAsset,
        timeframe: timeframe
      });
      setSession(res.data);
      setSelectedTimeframe(timeframe);
      setView('replay');
      toast.success('Session started! Mark your ORB range.');
    } catch (error) {
      toast.error('Failed to start session');
    } finally {
      setLoading(false);
    }
  };

  const switchTimeframe = async (newTimeframe) => {
    if (!session || newTimeframe === selectedTimeframe) return;
    
    // Preserve current state
    const preservedOrbRange = session.orb_range;
    const preservedTrade = session.active_trade;
    const preservedOrbHigh = orbHigh;
    const preservedOrbLow = orbLow;
    const preservedEntry = entryPrice;
    const preservedStop = stopLoss;
    const preservedTP = takeProfit;
    
    setLoading(true);
    try {
      const res = await axios.post(`${API}/real-market/start-session`, {
        user_id: user.id,
        asset: session.asset,
        timeframe: newTimeframe
      });
      
      // Update session with new candles but restore preserved state
      setSession({
        ...res.data,
        orb_range: preservedOrbRange,
        active_trade: preservedTrade,
        trades_completed: session.trades_completed
      });
      
      // Restore input values
      setOrbHigh(preservedOrbHigh);
      setOrbLow(preservedOrbLow);
      setEntryPrice(preservedEntry);
      setStopLoss(preservedStop);
      setTakeProfit(preservedTP);
      setSelectedTimeframe(newTimeframe);
      
      toast.success(`Switched to ${newTimeframe} timeframe`);
    } catch (error) {
      toast.error('Failed to switch timeframe');
    } finally {
      setLoading(false);
    }
  };

  const advanceCandle = async () => {
    if (!session) return;
    
    try {
      const res = await axios.post(`${API}/real-market/advance-candle?session_id=${session.session_id}`);
      
      if (res.data.finished) {
        toast.info('Session complete!');
        return;
      }
      
      // Update candles
      setSession(prev => ({
        ...prev,
        candles: [...prev.candles, res.data.new_candle],
        current_index: res.data.current_index
      }));
      
      // Check if trade was closed
      if (res.data.trade_closed && session.active_trade) {
        setPendingClose({
          ...session.active_trade,
          exit_price: res.data.trade_closed.exit_price,
          exit_reason: res.data.trade_closed.reason
        });
        setShowEvaluation(true);
      }
    } catch (error) {
      toast.error('Failed to advance candle');
    }
  };

  const markORB = async () => {
    if (!orbHigh || !orbLow) {
      toast.error('Please enter both ORB High and Low');
      return;
    }
    
    try {
      const res = await axios.post(`${API}/real-market/mark-orb`, {
        session_id: session.session_id,
        high: parseFloat(orbHigh),
        low: parseFloat(orbLow)
      });
      
      setSession(prev => ({
        ...prev,
        orb_range: res.data.orb_range
      }));
      setOrbMarking(false);
      toast.success('ORB range marked!');
    } catch (error) {
      toast.error('Failed to mark ORB');
    }
  };

  const enterTrade = async () => {
    if (!session?.orb_range) {
      toast.error('Mark ORB range first');
      return;
    }
    
    if (!entryPrice || !stopLoss) {
      toast.error('Entry price and Stop Loss are required');
      return;
    }
    
    try {
      const res = await axios.post(`${API}/real-market/enter-trade`, {
        session_id: session.session_id,
        direction: tradeDirection,
        entry_price: parseFloat(entryPrice),
        stop_loss: parseFloat(stopLoss),
        take_profit: takeProfit ? parseFloat(takeProfit) : null
      });
      
      setSession(prev => ({
        ...prev,
        active_trade: res.data.trade
      }));
      
      if (res.data.has_violations) {
        toast.warning(`⚠️ Rule violations detected: ${res.data.violations.join(', ')}`);
      } else {
        toast.success('Trade entered!');
      }
      
      // Clear form
      setEntryPrice('');
      setStopLoss('');
      setTakeProfit('');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to enter trade');
    }
  };

  const closeTradeManually = () => {
    if (!session?.active_trade) return;
    
    const currentPrice = session.candles[session.candles.length - 1]?.close;
    setPendingClose({
      ...session.active_trade,
      exit_price: currentPrice
    });
    setShowEvaluation(true);
  };

  const completeEvaluation = async (evalData) => {
    try {
      await axios.post(`${API}/real-market/close-trade`, {
        session_id: session.session_id,
        ...evalData
      });
      
      setSession(prev => ({
        ...prev,
        active_trade: null,
        trades_completed: prev.trades_completed + 1
      }));
      
      setShowEvaluation(false);
      setPendingClose(null);
      toast.success('Trade recorded! Continue or view dashboard.');
    } catch (error) {
      toast.error('Failed to record trade');
    }
  };

  const getCurrentPrice = () => {
    if (!session?.candles?.length) return 0;
    return session.candles[session.candles.length - 1].close;
  };

  // ==================== INTRO VIEW ====================
  if (view === 'intro') {
    return (
      <div className="min-h-screen bg-[#0A0A0A] pb-24" data-testid="backtest-intro">
        {/* Header */}
        <div className="bg-[#1A1A1A] p-4 sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-xl flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Backtest</h1>
              <p className="text-sm text-gray-400">Discipline Zone</p>
            </div>
          </div>
        </div>

        <div className="p-4">
        {/* Info Card */}
        <div className="bg-gradient-to-br from-[#1A1A1A] to-[#252525] rounded-2xl p-6 mb-6 border border-purple-500/30">
          <div className="text-4xl mb-4">📈</div>
          <h2 className="text-white font-bold text-lg mb-2">ORB Execution Training</h2>
          <p className="text-gray-400 text-sm mb-4">
            Train real execution, discipline, and emotional control in a realistic market environment.
          </p>
          
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2 text-gray-300">
              <span className="text-[#58CC02]">✓</span>
              <span>Candle-by-candle market replay</span>
            </div>
            <div className="flex items-center gap-2 text-gray-300">
              <span className="text-[#58CC02]">✓</span>
              <span>Mark ORB range manually</span>
            </div>
            <div className="flex items-center gap-2 text-gray-300">
              <span className="text-[#58CC02]">✓</span>
              <span>Define Stop Loss before entry</span>
            </div>
            <div className="flex items-center gap-2 text-gray-300">
              <span className="text-[#58CC02]">✓</span>
              <span>Track emotions and rule compliance</span>
            </div>
          </div>
          
          <div className="mt-4 p-3 bg-[#FF9600]/10 border border-[#FF9600]/30 rounded-lg">
            <p className="text-[#FF9600] text-xs">
              💡 Profit is not the main metric. <strong>DISCIPLINE</strong> is.
            </p>
          </div>
        </div>

        {/* Asset Selection */}
        <div className="mb-6">
          <label className="block text-white font-semibold mb-3">Select Asset</label>
          <div className="grid grid-cols-2 gap-2">
            {assets.map((asset) => (
              <button
                key={asset.id}
                onClick={() => setSelectedAsset(asset.id)}
                className={`p-3 rounded-lg border-2 text-left transition-all ${
                  selectedAsset === asset.id
                    ? 'border-[#58CC02] bg-[#58CC02]/10'
                    : 'border-gray-700 hover:border-gray-500'
                }`}
              >
                <div className="text-white font-medium">{asset.name}</div>
                <div className="text-xs text-gray-400">{asset.type}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-3">
          <button
            onClick={() => startSession()}
            disabled={loading}
            className="w-full py-4 bg-[#58CC02] text-white font-bold rounded-xl hover:bg-[#4CAD02] transition-colors disabled:opacity-50"
            data-testid="start-session-btn"
          >
            {loading ? 'Starting...' : 'Start Session →'}
          </button>
          
          <button
            onClick={() => setView('dashboard')}
            className="w-full py-4 bg-[#1A1A1A] text-white font-medium rounded-xl border border-gray-700 hover:border-purple-500 transition-colors"
            data-testid="view-dashboard-btn"
          >
            📊 View Discipline Dashboard
          </button>
        </div>
        </div>
      </div>
    );
  }

  // ==================== REPLAY VIEW ====================
  if (view === 'replay' && session) {
    return (
      <div className="min-h-screen bg-[#0A0A0A] pb-24" data-testid="backtest-replay">
        {/* Header */}
        <div className="bg-[#1A1A1A] p-4 sticky top-0 z-10">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <button onClick={() => setView('intro')} className="text-white">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <div>
                <h1 className="text-white font-bold">{session.asset}</h1>
                <p className="text-xs text-gray-400">Candle {session.current_index}/{session.total_candles}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs bg-purple-500/20 text-purple-400 px-2 py-1 rounded">
                Trades: {session.trades_completed || 0}
              </span>
            </div>
          </div>
          
          {/* Timeframe Selector */}
          <div className="flex items-center justify-center gap-1 bg-[#0A0A0A] rounded-lg p-1">
            {timeframes.map((tf) => (
              <button
                key={tf.id}
                onClick={() => switchTimeframe(tf.id)}
                disabled={loading}
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all ${
                  selectedTimeframe === tf.id
                    ? 'bg-purple-600 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-[#1A1A1A]'
                } ${loading ? 'opacity-50' : ''}`}
                data-testid={`timeframe-${tf.id}`}
              >
                {tf.label}
              </button>
            ))}
          </div>
        </div>

        {/* Chart */}
        <div className="p-4">
          <CandlestickChart
            candles={session.candles}
            orbRange={session.orb_range}
            activeTrade={session.active_trade}
            onPriceSelect={(price, label) => {
              // Auto-fill High or Low based on label
              if (label === 'High') {
                setOrbHigh(price.toString());
              } else if (label === 'Low') {
                setOrbLow(price.toString());
              }
            }}
          />
          
          {/* Current Price */}
          <div className="mt-2 text-center">
            <span className="text-gray-400 text-sm">Current: </span>
            <span className="text-white font-bold">{getCurrentPrice().toFixed(4)}</span>
          </div>
        </div>

        {/* Control Panel */}
        <div className="p-4 space-y-4">
          {/* Advance Candle */}
          <button
            onClick={advanceCandle}
            className="w-full py-3 bg-[#2A2A2A] text-white font-medium rounded-xl hover:bg-[#3A3A3A] transition-colors flex items-center justify-center gap-2"
            data-testid="advance-candle-btn"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
            Next Candle
          </button>

          {/* ORB Marking - Enhanced with Copy/Paste */}
          {!session.orb_range && (
            <div className="bg-[#1A1A1A] rounded-xl p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-white font-semibold">📏 Set Price Levels</h3>
                <span className="text-xs text-gray-500">Paste values directly</span>
              </div>
              
              {/* High Price Input */}
              <div className="mb-3">
                <label className="flex items-center justify-between text-xs mb-1">
                  <span className="text-green-400 font-medium">High Price</span>
                  <button
                    type="button"
                    onClick={async () => {
                      try {
                        const text = await navigator.clipboard.readText();
                        const num = parseFloat(text.replace(/[^0-9.-]/g, ''));
                        if (!isNaN(num)) setOrbHigh(num.toString());
                      } catch (e) {
                        toast.error('Could not read clipboard');
                      }
                    }}
                    className="text-gray-400 hover:text-white flex items-center gap-1"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    Paste
                  </button>
                </label>
                <input
                  type="text"
                  inputMode="decimal"
                  value={orbHigh}
                  onChange={(e) => setOrbHigh(e.target.value.replace(/[^0-9.-]/g, ''))}
                  onPaste={(e) => {
                    e.preventDefault();
                    const text = e.clipboardData.getData('text');
                    const num = parseFloat(text.replace(/[^0-9.-]/g, ''));
                    if (!isNaN(num)) setOrbHigh(num.toString());
                  }}
                  className="w-full bg-[#0A0A0A] border-2 border-green-500/30 focus:border-green-500 rounded-lg px-4 py-3 text-white text-lg font-mono focus:outline-none transition-colors"
                  placeholder="e.g. 1.0850"
                  data-testid="high-price-input"
                />
              </div>
              
              {/* Low Price Input */}
              <div className="mb-4">
                <label className="flex items-center justify-between text-xs mb-1">
                  <span className="text-red-400 font-medium">Low Price</span>
                  <button
                    type="button"
                    onClick={async () => {
                      try {
                        const text = await navigator.clipboard.readText();
                        const num = parseFloat(text.replace(/[^0-9.-]/g, ''));
                        if (!isNaN(num)) setOrbLow(num.toString());
                      } catch (e) {
                        toast.error('Could not read clipboard');
                      }
                    }}
                    className="text-gray-400 hover:text-white flex items-center gap-1"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    Paste
                  </button>
                </label>
                <input
                  type="text"
                  inputMode="decimal"
                  value={orbLow}
                  onChange={(e) => setOrbLow(e.target.value.replace(/[^0-9.-]/g, ''))}
                  onPaste={(e) => {
                    e.preventDefault();
                    const text = e.clipboardData.getData('text');
                    const num = parseFloat(text.replace(/[^0-9.-]/g, ''));
                    if (!isNaN(num)) setOrbLow(num.toString());
                  }}
                  className="w-full bg-[#0A0A0A] border-2 border-red-500/30 focus:border-red-500 rounded-lg px-4 py-3 text-white text-lg font-mono focus:outline-none transition-colors"
                  placeholder="e.g. 1.0750"
                  data-testid="low-price-input"
                />
              </div>
              
              {/* Range Preview */}
              {orbHigh && orbLow && parseFloat(orbHigh) > parseFloat(orbLow) && (
                <div className="bg-[#0A0A0A] rounded-lg p-3 mb-4">
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-400">Range Size:</span>
                    <span className="text-purple-400 font-mono">
                      {(parseFloat(orbHigh) - parseFloat(orbLow)).toFixed(4)}
                    </span>
                  </div>
                </div>
              )}
              
              <button
                onClick={markORB}
                disabled={!orbHigh || !orbLow || parseFloat(orbHigh) <= parseFloat(orbLow)}
                className="w-full py-3 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Plot Levels on Chart
              </button>
            </div>
          )}

          {/* Trade Entry */}
          {session.orb_range && !session.active_trade && (
            <div className="bg-[#1A1A1A] rounded-xl p-4">
              <h3 className="text-white font-semibold mb-3">🎯 Enter Trade</h3>
              
              {/* Direction */}
              <div className="flex gap-2 mb-3">
                <button
                  onClick={() => setTradeDirection('BUY')}
                  className={`flex-1 py-2 rounded-lg font-medium transition-all ${
                    tradeDirection === 'BUY'
                      ? 'bg-green-500 text-white'
                      : 'bg-[#2A2A2A] text-gray-400'
                  }`}
                >
                  BUY ↑
                </button>
                <button
                  onClick={() => setTradeDirection('SELL')}
                  className={`flex-1 py-2 rounded-lg font-medium transition-all ${
                    tradeDirection === 'SELL'
                      ? 'bg-red-500 text-white'
                      : 'bg-[#2A2A2A] text-gray-400'
                  }`}
                >
                  SELL ↓
                </button>
              </div>

              {/* Prices */}
              <div className="space-y-3 mb-3">
                <div>
                  <label className="text-xs text-gray-400">Entry Price</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={entryPrice}
                    onChange={(e) => setEntryPrice(e.target.value)}
                    className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-3 py-2 text-white text-sm"
                    placeholder={getCurrentPrice().toFixed(4)}
                  />
                </div>
                <div>
                  <label className="text-xs text-red-400">Stop Loss (Required)</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={stopLoss}
                    onChange={(e) => setStopLoss(e.target.value)}
                    className="w-full bg-[#0A0A0A] border border-red-700 rounded-lg px-3 py-2 text-white text-sm"
                    placeholder="Stop loss price"
                  />
                </div>
                <div>
                  <label className="text-xs text-gray-400">Take Profit (Optional)</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={takeProfit}
                    onChange={(e) => setTakeProfit(e.target.value)}
                    className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-3 py-2 text-white text-sm"
                    placeholder="Take profit price"
                  />
                </div>
              </div>

              <button
                onClick={enterTrade}
                className="w-full py-3 bg-[#58CC02] text-white font-bold rounded-lg"
              >
                Enter Trade
              </button>
            </div>
          )}

          {/* Active Trade */}
          {session.active_trade && (
            <div className="bg-[#1A1A1A] rounded-xl p-4">
              <h3 className="text-white font-semibold mb-3">📊 Active Trade</h3>
              <div className="space-y-2 text-sm mb-4">
                <div className="flex justify-between">
                  <span className="text-gray-400">Direction</span>
                  <span className={session.active_trade.direction === 'BUY' ? 'text-green-400' : 'text-red-400'}>
                    {session.active_trade.direction}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Entry</span>
                  <span className="text-white">{session.active_trade.entry_price}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Stop Loss</span>
                  <span className="text-red-400">{session.active_trade.stop_loss}</span>
                </div>
                {session.active_trade.take_profit && (
                  <div className="flex justify-between">
                    <span className="text-gray-400">Take Profit</span>
                    <span className="text-green-400">{session.active_trade.take_profit}</span>
                  </div>
                )}
              </div>
              
              <button
                onClick={closeTradeManually}
                className="w-full py-2 bg-[#FF9600] text-white font-medium rounded-lg"
              >
                Close Trade Manually
              </button>
            </div>
          )}
        </div>

        {/* Evaluation Modal */}
        {showEvaluation && pendingClose && (
          <TradeEvaluationModal
            trade={pendingClose}
            currentPrice={pendingClose.exit_price}
            onComplete={completeEvaluation}
            onCancel={() => {
              setShowEvaluation(false);
              setPendingClose(null);
            }}
          />
        )}
      </div>
    );
  }

  // ==================== DASHBOARD VIEW ====================
  if (view === 'dashboard') {
    return (
      <DisciplineDashboard
        userId={user.id}
        onClose={() => setView('intro')}
      />
    );
  }

  return null;
};

export default RealMarketZone;
