import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import { toast } from 'sonner';

const API = process.env.REACT_APP_BACKEND_URL + '/api';

// ==================== ADVANCED BACKTEST COMPONENT ====================

const AdvancedBacktest = ({ user, onBack }) => {
  // Chart State
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 500 });
  const [candles, setCandles] = useState([]);
  const [visibleCandles, setVisibleCandles] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playSpeed, setPlaySpeed] = useState(1000);
  
  // Trading State
  const [orders, setOrders] = useState([]);
  const [pendingOrders, setPendingOrders] = useState([]);
  const [positions, setPositions] = useState([]);
  const [balance, setBalance] = useState(10000);
  const [equity, setEquity] = useState(10000);
  const [selectedAsset, setSelectedAsset] = useState('EUR/USD');
  
  // Drawing State
  const [drawingMode, setDrawingMode] = useState(null); // 'line', 'horizontal', 'rectangle', 'fibonacci'
  const [drawings, setDrawings] = useState([]);
  const [tempDrawing, setTempDrawing] = useState(null);
  const [drawStart, setDrawStart] = useState(null);
  
  // Order Panel State
  const [showOrderPanel, setShowOrderPanel] = useState(false);
  const [orderType, setOrderType] = useState('market'); // 'market', 'limit', 'stop'
  const [orderSide, setOrderSide] = useState('buy');
  const [orderPrice, setOrderPrice] = useState('');
  const [orderSize, setOrderSize] = useState(0.1);
  const [stopLoss, setStopLoss] = useState('');
  const [takeProfit, setTakeProfit] = useState('');
  const [showOrderPreview, setShowOrderPreview] = useState(false);
  
  // Chart params for coordinate conversion
  const [chartParams, setChartParams] = useState(null);
  const [hoveredPrice, setHoveredPrice] = useState(null);
  const [crosshair, setCrosshair] = useState({ x: 0, y: 0, visible: false });

  // Assets data
  const assets = [
    { id: 'EUR/USD', name: 'EUR/USD', type: 'forex', pip: 0.0001 },
    { id: 'GBP/USD', name: 'GBP/USD', type: 'forex', pip: 0.0001 },
    { id: 'BTC/USD', name: 'Bitcoin', type: 'crypto', pip: 1 },
    { id: 'XAU/USD', name: 'Gold', type: 'commodity', pip: 0.01 },
    { id: 'SPX500', name: 'S&P 500', type: 'index', pip: 0.1 },
  ];

  // Generate realistic candle data
  const generateCandles = useCallback((asset, count = 500) => {
    const basePrice = {
      'EUR/USD': 1.0850,
      'GBP/USD': 1.2650,
      'BTC/USD': 43500,
      'XAU/USD': 2025,
      'SPX500': 4780,
    }[asset] || 1.0850;

    const volatility = {
      'EUR/USD': 0.0008,
      'GBP/USD': 0.001,
      'BTC/USD': 200,
      'XAU/USD': 5,
      'SPX500': 10,
    }[asset] || 0.001;

    const newCandles = [];
    let price = basePrice;
    let time = new Date();
    time.setHours(time.getHours() - count * 5 / 60);

    for (let i = 0; i < count; i++) {
      const trend = Math.sin(i / 50) * 0.3 + Math.random() * 0.4;
      const change = (Math.random() - 0.5 + trend * 0.1) * volatility;
      
      const open = price;
      const close = price + change;
      const high = Math.max(open, close) + Math.random() * volatility * 0.5;
      const low = Math.min(open, close) - Math.random() * volatility * 0.5;
      
      newCandles.push({
        time: new Date(time),
        open,
        high,
        low,
        close,
        volume: Math.floor(Math.random() * 1000) + 100
      });
      
      price = close;
      time = new Date(time.getTime() + 5 * 60 * 1000); // 5 min candles
    }
    
    return newCandles;
  }, []);

  // Load candles on mount and asset change
  useEffect(() => {
    setLoading(true);
    const newCandles = generateCandles(selectedAsset);
    setCandles(newCandles);
    setCurrentIndex(Math.min(100, newCandles.length - 1));
    setLoading(false);
    setDrawings([]);
    setOrders([]);
    setPendingOrders([]);
    setPositions([]);
  }, [selectedAsset, generateCandles]);

  // Update visible candles when index changes
  useEffect(() => {
    if (candles.length > 0) {
      const start = Math.max(0, currentIndex - 100);
      setVisibleCandles(candles.slice(start, currentIndex + 1));
    }
  }, [candles, currentIndex]);

  // Auto-play functionality
  useEffect(() => {
    let interval;
    if (isPlaying && currentIndex < candles.length - 1) {
      interval = setInterval(() => {
        setCurrentIndex(prev => {
          if (prev >= candles.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, playSpeed);
    }
    return () => clearInterval(interval);
  }, [isPlaying, currentIndex, candles.length, playSpeed]);

  // Check pending orders on each new candle
  useEffect(() => {
    if (visibleCandles.length === 0) return;
    const currentCandle = visibleCandles[visibleCandles.length - 1];
    
    pendingOrders.forEach(order => {
      let triggered = false;
      
      if (order.type === 'limit') {
        if (order.side === 'buy' && currentCandle.low <= order.price) triggered = true;
        if (order.side === 'sell' && currentCandle.high >= order.price) triggered = true;
      } else if (order.type === 'stop') {
        if (order.side === 'buy' && currentCandle.high >= order.price) triggered = true;
        if (order.side === 'sell' && currentCandle.low <= order.price) triggered = true;
      }
      
      if (triggered) {
        executeOrder(order);
        setPendingOrders(prev => prev.filter(o => o.id !== order.id));
      }
    });
    
    // Check stop loss and take profit for positions
    positions.forEach(pos => {
      if (pos.stopLoss && ((pos.side === 'buy' && currentCandle.low <= pos.stopLoss) || 
          (pos.side === 'sell' && currentCandle.high >= pos.stopLoss))) {
        closePosition(pos, pos.stopLoss, 'Stop Loss');
      }
      if (pos.takeProfit && ((pos.side === 'buy' && currentCandle.high >= pos.takeProfit) ||
          (pos.side === 'sell' && currentCandle.low <= pos.takeProfit))) {
        closePosition(pos, pos.takeProfit, 'Take Profit');
      }
    });
  }, [visibleCandles, pendingOrders, positions]);

  // Execute order
  const executeOrder = (order) => {
    const newPosition = {
      id: Date.now(),
      side: order.side,
      size: order.size,
      entryPrice: order.price || visibleCandles[visibleCandles.length - 1]?.close,
      stopLoss: order.stopLoss || null,
      takeProfit: order.takeProfit || null,
      openTime: new Date(),
      pnl: 0
    };
    
    setPositions(prev => [...prev, newPosition]);
    setOrders(prev => [...prev, { ...order, status: 'filled', filledAt: new Date() }]);
    toast.success(`${order.side.toUpperCase()} ${order.size} @ ${newPosition.entryPrice.toFixed(5)}`);
  };

  // Close position
  const closePosition = (position, exitPrice, reason = 'Manual') => {
    const pip = assets.find(a => a.id === selectedAsset)?.pip || 0.0001;
    const pnl = position.side === 'buy' 
      ? (exitPrice - position.entryPrice) / pip * position.size * 10
      : (position.entryPrice - exitPrice) / pip * position.size * 10;
    
    setBalance(prev => prev + pnl);
    setPositions(prev => prev.filter(p => p.id !== position.id));
    toast[pnl >= 0 ? 'success' : 'error'](`${reason}: ${pnl >= 0 ? '+' : ''}${pnl.toFixed(2)} USD`);
  };

  // Place order
  const placeOrder = () => {
    const currentPrice = visibleCandles[visibleCandles.length - 1]?.close;
    
    const newOrder = {
      id: Date.now(),
      type: orderType,
      side: orderSide,
      size: orderSize,
      price: orderType === 'market' ? currentPrice : parseFloat(orderPrice),
      stopLoss: stopLoss ? parseFloat(stopLoss) : null,
      takeProfit: takeProfit ? parseFloat(takeProfit) : null,
      status: 'pending',
      createdAt: new Date()
    };
    
    if (orderType === 'market') {
      executeOrder(newOrder);
    } else {
      setPendingOrders(prev => [...prev, newOrder]);
      toast.info(`${orderType.toUpperCase()} order placed @ ${newOrder.price.toFixed(5)}`);
    }
    
    setShowOrderPanel(false);
    resetOrderForm();
  };

  const resetOrderForm = () => {
    setOrderPrice('');
    setStopLoss('');
    setTakeProfit('');
    setOrderSize(0.1);
  };

  // Navigation controls
  const goBack = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => Math.max(0, prev - 1));
    }
  };

  const goForward = () => {
    if (currentIndex < candles.length - 1) {
      setCurrentIndex(prev => Math.min(candles.length - 1, prev + 1));
    }
  };

  const goToStart = () => setCurrentIndex(0);
  const goToEnd = () => setCurrentIndex(candles.length - 1);

  // Drawing functions
  const startDrawing = (e) => {
    if (!drawingMode || !chartParams) return;
    
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const price = yToPrice(y);
    const candleIndex = xToCandleIndex(x);
    
    setDrawStart({ x, y, price, candleIndex });
  };

  const continueDrawing = (e) => {
    if (!drawStart || !drawingMode) return;
    
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const price = yToPrice(y);
    const candleIndex = xToCandleIndex(x);
    
    setTempDrawing({
      type: drawingMode,
      start: drawStart,
      end: { x, y, price, candleIndex }
    });
  };

  const finishDrawing = (e) => {
    if (!tempDrawing) return;
    
    setDrawings(prev => [...prev, { ...tempDrawing, id: Date.now() }]);
    setTempDrawing(null);
    setDrawStart(null);
  };

  // Price/Coordinate conversion
  const priceToY = (price) => {
    if (!chartParams) return 0;
    const { padding, chartHeight, minPrice, priceRange } = chartParams;
    return padding + (1 - (price - minPrice) / priceRange) * chartHeight;
  };

  const yToPrice = (y) => {
    if (!chartParams) return 0;
    const { padding, chartHeight, minPrice, priceRange } = chartParams;
    return minPrice + (1 - (y - padding) / chartHeight) * priceRange;
  };

  const xToCandleIndex = (x) => {
    if (!chartParams) return 0;
    const { padding, candleSpacing } = chartParams;
    return Math.floor((x - padding) / candleSpacing);
  };

  // Handle mouse move for crosshair
  const handleMouseMove = (e) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    setCrosshair({ x, y, visible: true });
    setHoveredPrice(yToPrice(y));
    
    if (drawStart) {
      continueDrawing(e);
    }
  };

  const handleMouseLeave = () => {
    setCrosshair(prev => ({ ...prev, visible: false }));
    setHoveredPrice(null);
  };

  // Draw chart
  useEffect(() => {
    if (!canvasRef.current || visibleCandles.length === 0) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const { width, height } = dimensions;

    // Clear
    ctx.fillStyle = '#0d1117';
    ctx.fillRect(0, 0, width, height);

    // Calculate price range
    const prices = visibleCandles.flatMap(c => [c.high, c.low]);
    const minPrice = Math.min(...prices) * 0.9995;
    const maxPrice = Math.max(...prices) * 1.0005;
    const priceRange = maxPrice - minPrice;

    // Chart dimensions
    const padding = { top: 20, right: 70, bottom: 40, left: 10 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;
    const candleSpacing = chartWidth / visibleCandles.length;
    const candleWidth = Math.max(2, Math.min(12, candleSpacing - 2));

    // Store params
    setChartParams({ 
      padding: padding.left, 
      chartWidth, 
      chartHeight, 
      candleSpacing, 
      candleWidth, 
      minPrice, 
      maxPrice, 
      priceRange,
      paddingTop: padding.top,
      paddingRight: padding.right
    });

    // Helper functions
    const priceToYLocal = (price) => padding.top + (1 - (price - minPrice) / priceRange) * chartHeight;
    const indexToX = (index) => padding.left + index * candleSpacing + candleSpacing / 2;

    // Draw grid
    ctx.strokeStyle = '#1e2430';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 6; i++) {
      const y = padding.top + (chartHeight / 6) * i;
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();

      // Price labels
      const price = maxPrice - (priceRange / 6) * i;
      ctx.fillStyle = '#6b7280';
      ctx.font = '11px monospace';
      ctx.textAlign = 'left';
      ctx.fillText(price.toFixed(5), width - padding.right + 5, y + 4);
    }

    // Draw candles
    visibleCandles.forEach((candle, index) => {
      const x = indexToX(index);
      const openY = priceToYLocal(candle.open);
      const closeY = priceToYLocal(candle.close);
      const highY = priceToYLocal(candle.high);
      const lowY = priceToYLocal(candle.low);

      const isBullish = candle.close > candle.open;
      const bodyColor = isBullish ? '#22c55e' : '#ef4444';
      const wickColor = bodyColor;

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

    // Draw pending orders
    pendingOrders.forEach(order => {
      const y = priceToYLocal(order.price);
      ctx.strokeStyle = order.side === 'buy' ? '#3b82f6' : '#f97316';
      ctx.setLineDash([4, 4]);
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();
      ctx.setLineDash([]);
      
      // Label
      ctx.fillStyle = order.side === 'buy' ? '#3b82f6' : '#f97316';
      ctx.font = 'bold 10px Arial';
      ctx.fillText(`${order.type.toUpperCase()} ${order.side.toUpperCase()} @ ${order.price.toFixed(5)}`, padding.left + 5, y - 5);
    });

    // Draw positions
    positions.forEach(pos => {
      const entryY = priceToYLocal(pos.entryPrice);
      
      // Entry line
      ctx.strokeStyle = pos.side === 'buy' ? '#22c55e' : '#ef4444';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(padding.left, entryY);
      ctx.lineTo(width - padding.right, entryY);
      ctx.stroke();
      
      // Stop loss
      if (pos.stopLoss) {
        const slY = priceToYLocal(pos.stopLoss);
        ctx.strokeStyle = '#ef4444';
        ctx.setLineDash([3, 3]);
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(padding.left, slY);
        ctx.lineTo(width - padding.right, slY);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#ef4444';
        ctx.fillText(`SL: ${pos.stopLoss.toFixed(5)}`, width - padding.right - 100, slY - 3);
      }
      
      // Take profit
      if (pos.takeProfit) {
        const tpY = priceToYLocal(pos.takeProfit);
        ctx.strokeStyle = '#22c55e';
        ctx.setLineDash([3, 3]);
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(padding.left, tpY);
        ctx.lineTo(width - padding.right, tpY);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#22c55e';
        ctx.fillText(`TP: ${pos.takeProfit.toFixed(5)}`, width - padding.right - 100, tpY - 3);
      }
    });

    // Draw drawings
    [...drawings, tempDrawing].filter(Boolean).forEach(drawing => {
      ctx.strokeStyle = '#a855f7';
      ctx.lineWidth = 2;
      
      if (drawing.type === 'line') {
        ctx.beginPath();
        ctx.moveTo(drawing.start.x, drawing.start.y);
        ctx.lineTo(drawing.end.x, drawing.end.y);
        ctx.stroke();
      } else if (drawing.type === 'horizontal') {
        const y = drawing.start.y;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(width - padding.right, y);
        ctx.stroke();
        ctx.fillStyle = '#a855f7';
        ctx.fillText(yToPrice(y).toFixed(5), width - padding.right + 5, y + 4);
      } else if (drawing.type === 'rectangle') {
        ctx.strokeRect(
          Math.min(drawing.start.x, drawing.end.x),
          Math.min(drawing.start.y, drawing.end.y),
          Math.abs(drawing.end.x - drawing.start.x),
          Math.abs(drawing.end.y - drawing.start.y)
        );
      } else if (drawing.type === 'fibonacci') {
        const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];
        const startY = drawing.start.y;
        const endY = drawing.end.y;
        const range = endY - startY;
        
        levels.forEach((level, i) => {
          const y = startY + range * level;
          ctx.strokeStyle = `rgba(168, 85, 247, ${1 - level * 0.5})`;
          ctx.beginPath();
          ctx.moveTo(padding.left, y);
          ctx.lineTo(width - padding.right, y);
          ctx.stroke();
          ctx.fillStyle = '#a855f7';
          ctx.fillText(`${(level * 100).toFixed(1)}%`, width - padding.right + 5, y + 4);
        });
      }
    });

    // Draw crosshair
    if (crosshair.visible) {
      ctx.strokeStyle = '#4b5563';
      ctx.setLineDash([2, 2]);
      ctx.lineWidth = 1;
      
      // Vertical line
      ctx.beginPath();
      ctx.moveTo(crosshair.x, padding.top);
      ctx.lineTo(crosshair.x, height - padding.bottom);
      ctx.stroke();
      
      // Horizontal line
      ctx.beginPath();
      ctx.moveTo(padding.left, crosshair.y);
      ctx.lineTo(width - padding.right, crosshair.y);
      ctx.stroke();
      
      ctx.setLineDash([]);
      
      // Price label
      if (hoveredPrice) {
        ctx.fillStyle = '#374151';
        ctx.fillRect(width - padding.right, crosshair.y - 10, padding.right, 20);
        ctx.fillStyle = '#ffffff';
        ctx.font = '11px monospace';
        ctx.fillText(hoveredPrice.toFixed(5), width - padding.right + 5, crosshair.y + 4);
      }
    }

    // Draw order preview
    if (showOrderPreview && orderPrice) {
      const previewY = priceToYLocal(parseFloat(orderPrice));
      ctx.strokeStyle = orderSide === 'buy' ? '#3b82f6' : '#f97316';
      ctx.lineWidth = 2;
      ctx.setLineDash([8, 4]);
      ctx.beginPath();
      ctx.moveTo(padding.left, previewY);
      ctx.lineTo(width - padding.right, previewY);
      ctx.stroke();
      ctx.setLineDash([]);
      
      // Preview label
      ctx.fillStyle = orderSide === 'buy' ? '#3b82f6' : '#f97316';
      ctx.font = 'bold 11px Arial';
      ctx.fillText(`Preview: ${orderSide.toUpperCase()} @ ${parseFloat(orderPrice).toFixed(5)}`, padding.left + 5, previewY - 8);
    }

  }, [visibleCandles, dimensions, pendingOrders, positions, drawings, tempDrawing, crosshair, hoveredPrice, showOrderPreview, orderPrice, orderSide]);

  // Update dimensions on resize
  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        const { width } = containerRef.current.getBoundingClientRect();
        setDimensions({ width: Math.max(width - 20, 400), height: 450 });
      }
    };
    
    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  const currentPrice = visibleCandles[visibleCandles.length - 1]?.close || 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0d1117]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0d1117] pb-24" data-testid="advanced-backtest">
      {/* Header */}
      <div className="bg-[#161b22] border-b border-gray-800 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={onBack} className="text-gray-400 hover:text-white" data-testid="backtest-back-btn">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <h1 className="text-lg font-bold text-white">Backtest</h1>
          </div>
          
          {/* Asset Selector */}
          <select
            value={selectedAsset}
            onChange={(e) => setSelectedAsset(e.target.value)}
            className="bg-[#0d1117] border border-gray-700 rounded-lg px-3 py-2 text-white text-sm"
            data-testid="asset-selector"
          >
            {assets.map(asset => (
              <option key={asset.id} value={asset.id}>{asset.name}</option>
            ))}
          </select>
        </div>
        
        {/* Account Info */}
        <div className="flex items-center gap-4 mt-2 text-sm">
          <div className="text-gray-400">
            Balance: <span className="text-white font-semibold">${balance.toFixed(2)}</span>
          </div>
          <div className="text-gray-400">
            Positions: <span className="text-white font-semibold">{positions.length}</span>
          </div>
          <div className="text-gray-400">
            Pending: <span className="text-yellow-400 font-semibold">{pendingOrders.length}</span>
          </div>
        </div>
      </div>

      {/* Toolbar */}
      <div className="bg-[#161b22] border-b border-gray-800 px-4 py-2 flex items-center gap-2 flex-wrap">
        {/* Navigation Controls */}
        <div className="flex items-center gap-1 border-r border-gray-700 pr-3 mr-2">
          <button onClick={goToStart} className="p-2 hover:bg-gray-800 rounded text-gray-400 hover:text-white" title="Go to start">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
            </svg>
          </button>
          <button onClick={goBack} className="p-2 hover:bg-gray-800 rounded text-gray-400 hover:text-white" title="Previous candle" data-testid="go-back-btn">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button 
            onClick={() => setIsPlaying(!isPlaying)} 
            className={`p-2 rounded ${isPlaying ? 'bg-purple-600 text-white' : 'hover:bg-gray-800 text-gray-400 hover:text-white'}`}
            title={isPlaying ? 'Pause' : 'Play'}
            data-testid="play-pause-btn"
          >
            {isPlaying ? (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9v6m4-6v6" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
            )}
          </button>
          <button onClick={goForward} className="p-2 hover:bg-gray-800 rounded text-gray-400 hover:text-white" title="Next candle" data-testid="go-forward-btn">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
          <button onClick={goToEnd} className="p-2 hover:bg-gray-800 rounded text-gray-400 hover:text-white" title="Go to end">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
          </button>
          <select 
            value={playSpeed} 
            onChange={(e) => setPlaySpeed(Number(e.target.value))}
            className="bg-[#0d1117] border border-gray-700 rounded px-2 py-1 text-xs text-white ml-1"
          >
            <option value={2000}>0.5x</option>
            <option value={1000}>1x</option>
            <option value={500}>2x</option>
            <option value={250}>4x</option>
          </select>
        </div>

        {/* Drawing Tools */}
        <div className="flex items-center gap-1 border-r border-gray-700 pr-3 mr-2">
          <button 
            onClick={() => setDrawingMode(drawingMode === 'line' ? null : 'line')}
            className={`p-2 rounded ${drawingMode === 'line' ? 'bg-purple-600 text-white' : 'hover:bg-gray-800 text-gray-400 hover:text-white'}`}
            title="Trend Line"
            data-testid="draw-line-btn"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 20l16-16" />
            </svg>
          </button>
          <button 
            onClick={() => setDrawingMode(drawingMode === 'horizontal' ? null : 'horizontal')}
            className={`p-2 rounded ${drawingMode === 'horizontal' ? 'bg-purple-600 text-white' : 'hover:bg-gray-800 text-gray-400 hover:text-white'}`}
            title="Horizontal Line"
            data-testid="draw-horizontal-btn"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 12h16" />
            </svg>
          </button>
          <button 
            onClick={() => setDrawingMode(drawingMode === 'rectangle' ? null : 'rectangle')}
            className={`p-2 rounded ${drawingMode === 'rectangle' ? 'bg-purple-600 text-white' : 'hover:bg-gray-800 text-gray-400 hover:text-white'}`}
            title="Rectangle"
            data-testid="draw-rect-btn"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <rect x="4" y="6" width="16" height="12" strokeWidth={2} rx="1" />
            </svg>
          </button>
          <button 
            onClick={() => setDrawingMode(drawingMode === 'fibonacci' ? null : 'fibonacci')}
            className={`p-2 rounded ${drawingMode === 'fibonacci' ? 'bg-purple-600 text-white' : 'hover:bg-gray-800 text-gray-400 hover:text-white'}`}
            title="Fibonacci"
            data-testid="draw-fib-btn"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
            </svg>
          </button>
          <button 
            onClick={() => setDrawings([])}
            className="p-2 hover:bg-gray-800 rounded text-gray-400 hover:text-red-400"
            title="Clear drawings"
            data-testid="clear-drawings-btn"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>

        {/* Order Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => { setShowOrderPanel(true); setOrderSide('buy'); }}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-semibold rounded-lg"
            data-testid="buy-btn"
          >
            BUY
          </button>
          <button
            onClick={() => { setShowOrderPanel(true); setOrderSide('sell'); }}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-semibold rounded-lg"
            data-testid="sell-btn"
          >
            SELL
          </button>
        </div>

        {/* Candle info */}
        <div className="ml-auto text-sm text-gray-400">
          Candle {currentIndex + 1} / {candles.length}
        </div>
      </div>

      {/* Chart */}
      <div ref={containerRef} className="relative">
        <canvas
          ref={canvasRef}
          width={dimensions.width}
          height={dimensions.height}
          className="cursor-crosshair"
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          onMouseDown={startDrawing}
          onMouseUp={finishDrawing}
          onClick={(e) => {
            if (!drawingMode && chartParams) {
              const rect = canvasRef.current.getBoundingClientRect();
              const y = e.clientY - rect.top;
              const price = yToPrice(y);
              setOrderPrice(price.toFixed(5));
              setShowOrderPreview(true);
            }
          }}
        />
        
        {/* Current price label */}
        <div className="absolute top-2 left-2 bg-[#161b22]/90 px-3 py-1.5 rounded text-sm">
          <span className="text-gray-400">Price: </span>
          <span className="text-white font-mono">{currentPrice.toFixed(5)}</span>
        </div>
        
        {/* Drawing mode indicator */}
        {drawingMode && (
          <div className="absolute top-2 right-2 bg-purple-600/90 px-3 py-1.5 rounded text-sm text-white">
            Drawing: {drawingMode}
          </div>
        )}
      </div>

      {/* Open Positions */}
      {positions.length > 0 && (
        <div className="px-4 py-3 border-t border-gray-800">
          <h3 className="text-sm font-semibold text-gray-400 mb-2">Open Positions</h3>
          <div className="space-y-2">
            {positions.map(pos => {
              const pip = assets.find(a => a.id === selectedAsset)?.pip || 0.0001;
              const unrealizedPnl = pos.side === 'buy'
                ? (currentPrice - pos.entryPrice) / pip * pos.size * 10
                : (pos.entryPrice - currentPrice) / pip * pos.size * 10;
              
              return (
                <div key={pos.id} className="flex items-center justify-between bg-[#161b22] rounded-lg p-3">
                  <div className="flex items-center gap-3">
                    <span className={`px-2 py-1 rounded text-xs font-bold ${pos.side === 'buy' ? 'bg-green-600/20 text-green-400' : 'bg-red-600/20 text-red-400'}`}>
                      {pos.side.toUpperCase()}
                    </span>
                    <span className="text-white">{pos.size} lots @ {pos.entryPrice.toFixed(5)}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`font-mono ${unrealizedPnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {unrealizedPnl >= 0 ? '+' : ''}{unrealizedPnl.toFixed(2)} USD
                    </span>
                    <button
                      onClick={() => closePosition(pos, currentPrice, 'Manual Close')}
                      className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white text-xs rounded"
                      data-testid={`close-position-${pos.id}`}
                    >
                      Close
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Pending Orders */}
      {pendingOrders.length > 0 && (
        <div className="px-4 py-3 border-t border-gray-800">
          <h3 className="text-sm font-semibold text-gray-400 mb-2">Pending Orders</h3>
          <div className="space-y-2">
            {pendingOrders.map(order => (
              <div key={order.id} className="flex items-center justify-between bg-[#161b22] rounded-lg p-3">
                <div className="flex items-center gap-3">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${order.side === 'buy' ? 'bg-blue-600/20 text-blue-400' : 'bg-orange-600/20 text-orange-400'}`}>
                    {order.type.toUpperCase()} {order.side.toUpperCase()}
                  </span>
                  <span className="text-white">{order.size} lots @ {order.price.toFixed(5)}</span>
                </div>
                <button
                  onClick={() => setPendingOrders(prev => prev.filter(o => o.id !== order.id))}
                  className="px-3 py-1 bg-red-600/20 hover:bg-red-600/40 text-red-400 text-xs rounded"
                >
                  Cancel
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Order Panel Modal */}
      {showOrderPanel && (
        <div className="fixed inset-0 bg-black/70 flex items-end justify-center z-50" onClick={() => setShowOrderPanel(false)}>
          <div 
            className="bg-[#161b22] w-full max-w-lg rounded-t-2xl p-5 animate-slide-up"
            onClick={e => e.stopPropagation()}
            data-testid="order-panel"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-white">
                {orderSide === 'buy' ? '🟢 Buy' : '🔴 Sell'} {selectedAsset}
              </h2>
              <button onClick={() => setShowOrderPanel(false)} className="text-gray-400 hover:text-white">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Order Type Tabs */}
            <div className="flex gap-2 mb-4">
              {['market', 'limit', 'stop'].map(type => (
                <button
                  key={type}
                  onClick={() => setOrderType(type)}
                  className={`flex-1 py-2 rounded-lg text-sm font-semibold transition-colors ${
                    orderType === type 
                      ? 'bg-purple-600 text-white' 
                      : 'bg-[#0d1117] text-gray-400 hover:text-white'
                  }`}
                  data-testid={`order-type-${type}`}
                >
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </button>
              ))}
            </div>

            {/* Order Form */}
            <div className="space-y-4">
              {/* Price (for limit/stop) */}
              {orderType !== 'market' && (
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Price</label>
                  <input
                    type="number"
                    step="0.00001"
                    value={orderPrice}
                    onChange={(e) => { setOrderPrice(e.target.value); setShowOrderPreview(true); }}
                    className="w-full bg-[#0d1117] border border-gray-700 rounded-lg px-4 py-3 text-white"
                    placeholder={currentPrice.toFixed(5)}
                    data-testid="order-price-input"
                  />
                </div>
              )}

              {/* Size */}
              <div>
                <label className="block text-sm text-gray-400 mb-2">Size (lots)</label>
                <div className="flex gap-2">
                  {[0.01, 0.1, 0.5, 1].map(size => (
                    <button
                      key={size}
                      onClick={() => setOrderSize(size)}
                      className={`flex-1 py-2 rounded-lg text-sm ${
                        orderSize === size 
                          ? 'bg-purple-600 text-white' 
                          : 'bg-[#0d1117] text-gray-400 hover:text-white border border-gray-700'
                      }`}
                    >
                      {size}
                    </button>
                  ))}
                </div>
              </div>

              {/* Stop Loss */}
              <div>
                <label className="block text-sm text-gray-400 mb-2">Stop Loss (optional)</label>
                <input
                  type="number"
                  step="0.00001"
                  value={stopLoss}
                  onChange={(e) => setStopLoss(e.target.value)}
                  className="w-full bg-[#0d1117] border border-gray-700 rounded-lg px-4 py-3 text-white"
                  placeholder="Enter stop loss price"
                  data-testid="stop-loss-input"
                />
              </div>

              {/* Take Profit */}
              <div>
                <label className="block text-sm text-gray-400 mb-2">Take Profit (optional)</label>
                <input
                  type="number"
                  step="0.00001"
                  value={takeProfit}
                  onChange={(e) => setTakeProfit(e.target.value)}
                  className="w-full bg-[#0d1117] border border-gray-700 rounded-lg px-4 py-3 text-white"
                  placeholder="Enter take profit price"
                  data-testid="take-profit-input"
                />
              </div>

              {/* Submit Button */}
              <button
                onClick={placeOrder}
                className={`w-full py-4 rounded-xl text-white font-bold text-lg ${
                  orderSide === 'buy' 
                    ? 'bg-green-600 hover:bg-green-700' 
                    : 'bg-red-600 hover:bg-red-700'
                }`}
                data-testid="place-order-btn"
              >
                {orderType === 'market' ? 'Execute' : 'Place'} {orderSide.toUpperCase()} Order
              </button>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes slide-up {
          from { transform: translateY(100%); }
          to { transform: translateY(0); }
        }
        .animate-slide-up {
          animation: slide-up 0.3s ease-out;
        }
      `}</style>
    </div>
  );
};

export default AdvancedBacktest;
