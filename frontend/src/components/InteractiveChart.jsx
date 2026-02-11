import React, { useEffect, useRef, useState, useCallback } from 'react';
import { createChart } from 'lightweight-charts';

/**
 * Interactive TradingView Chart Component
 * Supports: Draw lines (price levels) OR Draw rectangles (zones)
 */
const InteractiveChart = ({ 
  candles, 
  onPriceClick,
  onZoneDrawn,
  onLineDrawn,
  correctAnswer,
  showAnswer,
  targetPart,
  drawMode = 'none',  // 'none', 'line', 'rectangle'
  height = 400 
}) => {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);
  const seriesRef = useRef(null);
  const priceLinesRef = useRef([]);
  const [clickedPrice, setClickedPrice] = useState(null);
  const [containerHeight, setContainerHeight] = useState(400);
  
  // Drawing state
  const [isDrawing, setIsDrawing] = useState(false);
  const [drawStart, setDrawStart] = useState(null);
  const [drawEnd, setDrawEnd] = useState(null);
  const [drawnZone, setDrawnZone] = useState(null);
  const [drawnLine, setDrawnLine] = useState(null);

  // Update container height on resize
  useEffect(() => {
    const updateHeight = () => {
      if (chartContainerRef.current) {
        const newHeight = chartContainerRef.current.clientHeight || 400;
        setContainerHeight(newHeight);
      }
    };
    
    updateHeight();
    window.addEventListener('resize', updateHeight);
    return () => window.removeEventListener('resize', updateHeight);
  }, []);

  // Initialize chart
  useEffect(() => {
    if (!chartContainerRef.current || !candles || candles.length === 0) return;

    if (chartRef.current) {
      chartRef.current.remove();
    }

    const chartHeight = height === '100%' ? containerHeight : height;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: chartHeight,
      layout: {
        background: { type: 'solid', color: '#1A1A1A' },
        textColor: '#d1d5db',
      },
      grid: {
        vertLines: { color: '#2A2A2A' },
        horzLines: { color: '#2A2A2A' },
      },
      localization: {
        locale: 'en-US',
        dateFormat: 'yyyy-MM-dd',
        timeFormatter: () => '',
      },
      crosshair: {
        mode: drawMode !== 'none' ? 0 : 1,
        vertLine: {
          color: '#58CC02',
          width: 1,
          style: 2,
          labelVisible: false,
        },
        horzLine: {
          color: '#58CC02',
          width: 1,
          style: 2,
          labelBackgroundColor: '#58CC02',
        },
      },
      rightPriceScale: {
        borderColor: '#2A2A2A',
        scaleMargins: { top: 0.15, bottom: 0.15 },
      },
      timeScale: {
        borderColor: '#2A2A2A',
        visible: false,
        timeVisible: false,
        secondsVisible: false,
      },
      handleScale: false,
      handleScroll: false,
    });

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#58CC02',
      downColor: '#FF4B4B',
      borderDownColor: '#FF4B4B',
      borderUpColor: '#58CC02',
      wickDownColor: '#FF4B4B',
      wickUpColor: '#58CC02',
    });

    candlestickSeries.setData(candles);
    chart.timeScale().fitContent();

    chartRef.current = chart;
    seriesRef.current = candlestickSeries;
    priceLinesRef.current = [];

    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, [candles, height, drawMode, containerHeight]);

  // Reset drawn items when exercise changes
  useEffect(() => {
    setDrawnLine(null);
    setDrawnZone(null);
    setClickedPrice(null);
    setIsDrawing(false);
    setDrawStart(null);
    setDrawEnd(null);
  }, [candles]);

  // Get price from Y coordinate
  const getPriceFromY = useCallback((clientY) => {
    if (!chartContainerRef.current || !seriesRef.current) return null;
    const rect = chartContainerRef.current.getBoundingClientRect();
    const y = clientY - rect.top;
    return seriesRef.current.coordinateToPrice(y);
  }, []);

  // Drawing handlers for LINE mode
  const handleLineMouseDown = useCallback((event) => {
    if (showAnswer) return;
    event.preventDefault();
    
    const rect = chartContainerRef.current.getBoundingClientRect();
    const y = event.clientY - rect.top;
    const price = getPriceFromY(event.clientY);
    
    setIsDrawing(true);
    setDrawStart({ y, price });
    setDrawEnd({ y, price });
    setDrawnLine(null);
  }, [showAnswer, getPriceFromY]);

  const handleLineMouseMove = useCallback((event) => {
    if (!isDrawing || !drawStart) return;
    event.preventDefault();
    
    const rect = chartContainerRef.current.getBoundingClientRect();
    const y = event.clientY - rect.top;
    const price = getPriceFromY(event.clientY);
    
    setDrawEnd({ y, price });
  }, [isDrawing, drawStart, getPriceFromY]);

  const handleLineMouseUp = useCallback((event) => {
    if (!isDrawing) return;
    event.preventDefault();
    
    const price = getPriceFromY(event.clientY);
    
    if (price !== null) {
      setDrawnLine({ price });
      if (onLineDrawn) onLineDrawn({ price });
      if (onPriceClick) onPriceClick(price);
    }
    
    setIsDrawing(false);
  }, [isDrawing, getPriceFromY, onLineDrawn, onPriceClick]);

  // Drawing handlers for RECTANGLE mode
  const handleRectMouseDown = useCallback((event) => {
    if (showAnswer) return;
    event.preventDefault();
    
    const rect = chartContainerRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const price = getPriceFromY(event.clientY);
    
    setIsDrawing(true);
    setDrawStart({ x, y, price });
    setDrawEnd({ x, y, price });
    setDrawnZone(null);
  }, [showAnswer, getPriceFromY]);

  const handleRectMouseMove = useCallback((event) => {
    if (!isDrawing || !drawStart) return;
    event.preventDefault();
    
    const rect = chartContainerRef.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const price = getPriceFromY(event.clientY);
    
    setDrawEnd({ x, y, price });
  }, [isDrawing, drawStart, getPriceFromY]);

  const handleRectMouseUp = useCallback((event) => {
    if (!isDrawing || !drawStart) return;
    event.preventDefault();
    
    const endPrice = getPriceFromY(event.clientY);
    
    if (drawStart.price !== null && endPrice !== null) {
      const zone = {
        high: Math.max(drawStart.price, endPrice),
        low: Math.min(drawStart.price, endPrice),
      };
      
      setDrawnZone(zone);
      if (onZoneDrawn) onZoneDrawn(zone);
    }
    
    setIsDrawing(false);
  }, [isDrawing, drawStart, getPriceFromY, onZoneDrawn]);

  // Show correct answer
  useEffect(() => {
    if (!seriesRef.current || !showAnswer || !correctAnswer || !candles?.length) return;

    priceLinesRef.current.forEach(line => {
      try { seriesRef.current.removePriceLine(line); } catch (e) {}
    });
    priceLinesRef.current = [];

    // Zone answer (FVG, OB)
    if (correctAnswer.price_high && correctAnswer.price_low) {
      const topLine = seriesRef.current.createPriceLine({
        price: correctAnswer.price_high,
        color: '#58CC02',
        lineWidth: 2,
        lineStyle: 0,
        axisLabelVisible: true,
        title: 'Zone Top',
      });
      priceLinesRef.current.push(topLine);
      
      const bottomLine = seriesRef.current.createPriceLine({
        price: correctAnswer.price_low,
        color: '#58CC02',
        lineWidth: 2,
        lineStyle: 0,
        axisLabelVisible: true,
        title: 'Zone Bottom',
      });
      priceLinesRef.current.push(bottomLine);
    } 
    // Single price answer
    else if (correctAnswer.price) {
      const correctLine = seriesRef.current.createPriceLine({
        price: correctAnswer.price,
        color: '#58CC02',
        lineWidth: 3,
        lineStyle: 0,
        axisLabelVisible: true,
        title: '✓ CORRECT',
      });
      priceLinesRef.current.push(correctLine);

      // Show user's line
      if (drawnLine) {
        const userLine = seriesRef.current.createPriceLine({
          price: drawnLine.price,
          color: '#FBBF24',
          lineWidth: 2,
          lineStyle: 0,
          axisLabelVisible: true,
          title: 'Your Line',
        });
        priceLinesRef.current.push(userLine);
      }
    }

    // Show OHLC for single candle
    if (candles.length === 1 && !correctAnswer.price_high) {
      const candle = candles[0];
      [
        { price: candle.open, color: '#3B82F6', title: 'Open' },
        { price: candle.high, color: '#22C55E', title: 'High' },
        { price: candle.low, color: '#EF4444', title: 'Low' },
        { price: candle.close, color: '#A855F7', title: 'Close' },
      ].forEach(cfg => {
        const line = seriesRef.current.createPriceLine({
          price: cfg.price,
          color: cfg.color,
          lineWidth: 1,
          lineStyle: 2,
          axisLabelVisible: true,
          title: cfg.title,
        });
        priceLinesRef.current.push(line);
      });
    }
  }, [showAnswer, correctAnswer, drawnLine, candles]);

  // Get Y coordinate for price
  const getYForPrice = useCallback((price) => {
    if (!seriesRef.current) return null;
    return seriesRef.current.priceToCoordinate(price);
  }, []);

  // Calculate drawing rectangle
  const getDrawRect = () => {
    if (!drawStart || !drawEnd) return null;
    return {
      left: Math.min(drawStart.x, drawEnd.x),
      top: Math.min(drawStart.y, drawEnd.y),
      width: Math.abs(drawEnd.x - drawStart.x),
      height: Math.abs(drawEnd.y - drawStart.y),
    };
  };

  const drawRect = getDrawRect();
  const currentDrawY = drawEnd?.y;

  return (
    <div className="relative w-full h-full" style={{ minHeight: height === '100%' ? '100%' : height }}>
      {/* Chart container */}
      <div
        ref={chartContainerRef}
        className="w-full h-full overflow-hidden"
        data-testid="interactive-chart"
      />
      
      {/* LINE drawing overlay */}
      {drawMode === 'line' && !showAnswer && (
        <div
          className="absolute inset-0 cursor-crosshair"
          style={{ zIndex: 10 }}
          onMouseDown={handleLineMouseDown}
          onMouseMove={handleLineMouseMove}
          onMouseUp={handleLineMouseUp}
          onMouseLeave={handleLineMouseUp}
        >
          {/* Drawing line preview */}
          {isDrawing && currentDrawY && (
            <div
              className="absolute left-0 right-0 border-t-2 border-dashed border-[#FBBF24] pointer-events-none"
              style={{ top: currentDrawY }}
            >
              <span className="absolute right-2 -top-6 text-xs font-bold text-[#FBBF24] bg-black/80 px-2 py-1 rounded">
                ${drawEnd?.price?.toFixed(2)}
              </span>
            </div>
          )}
          
          {/* Drawn line display */}
          {drawnLine && !isDrawing && (
            <div
              className="absolute left-0 right-0 border-t-3 border-[#FBBF24] pointer-events-none"
              style={{ 
                top: getYForPrice(drawnLine.price),
                borderTopWidth: '3px',
                boxShadow: '0 0 10px rgba(251, 191, 36, 0.5)'
              }}
            >
              <span className="absolute left-2 -top-6 text-xs font-bold text-[#FBBF24] bg-black/80 px-2 py-1 rounded">
                Your Line: ${drawnLine.price.toFixed(2)}
              </span>
            </div>
          )}
        </div>
      )}

      {/* RECTANGLE drawing overlay */}
      {drawMode === 'rectangle' && !showAnswer && (
        <div
          className="absolute inset-0 cursor-crosshair"
          style={{ zIndex: 10 }}
          onMouseDown={handleRectMouseDown}
          onMouseMove={handleRectMouseMove}
          onMouseUp={handleRectMouseUp}
          onMouseLeave={handleRectMouseUp}
        >
          {/* Drawing rectangle preview */}
          {isDrawing && drawRect && (
            <div
              className="absolute border-2 border-[#58CC02] bg-[#58CC02]/30 pointer-events-none"
              style={{
                left: drawRect.left,
                top: drawRect.top,
                width: drawRect.width,
                height: drawRect.height,
              }}
            />
          )}
          
          {/* Drawn zone display */}
          {drawnZone && !isDrawing && (
            <div
              className="absolute left-12 right-12 border-2 border-[#FBBF24] bg-[#FBBF24]/30 pointer-events-none"
              style={{
                top: getYForPrice(drawnZone.high),
                height: Math.abs(
                  (getYForPrice(drawnZone.low) || 0) - 
                  (getYForPrice(drawnZone.high) || 0)
                ),
              }}
            >
              <span className="absolute top-1 left-2 text-xs font-bold text-[#FBBF24] bg-black/80 px-2 py-1 rounded">
                Your Zone: ${drawnZone.low.toFixed(2)} - ${drawnZone.high.toFixed(2)}
              </span>
            </div>
          )}
        </div>
      )}
      
      {/* Instruction overlay */}
      {!showAnswer && !drawnLine && !drawnZone && !isDrawing && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none" style={{ zIndex: 20 }}>
          <div className="bg-black/70 px-6 py-3 rounded-xl border border-[#58CC02]/30">
            <p className="text-white text-sm flex items-center gap-2">
              {drawMode === 'rectangle' ? (
                <>
                  <span className="text-xl">✏️</span>
                  <span>Click and drag to draw the zone</span>
                </>
              ) : drawMode === 'line' ? (
                <>
                  <span className="text-xl">📏</span>
                  <span>Click and drag to draw a line at the price level</span>
                </>
              ) : (
                <>
                  <span className="text-xl">👆</span>
                  <span>Click on the chart to mark your answer</span>
                </>
              )}
            </p>
          </div>
        </div>
      )}

      {/* Drawn line indicator */}
      {drawnLine && !showAnswer && drawMode === 'line' && (
        <div className="absolute top-2 right-2 bg-[#FBBF24] px-4 py-2 rounded-lg shadow-lg" style={{ zIndex: 30 }}>
          <p className="text-black font-bold">Line at: ${drawnLine.price.toFixed(2)}</p>
        </div>
      )}

      {/* Drawn zone indicator */}
      {drawnZone && !showAnswer && drawMode === 'rectangle' && (
        <div className="absolute top-2 right-2 bg-[#58CC02] px-4 py-2 rounded-lg shadow-lg" style={{ zIndex: 30 }}>
          <p className="text-black font-bold text-sm">
            Zone: ${drawnZone.low.toFixed(2)} - ${drawnZone.high.toFixed(2)}
          </p>
        </div>
      )}

      {/* Legend for single candle */}
      {showAnswer && candles?.length === 1 && !correctAnswer?.price_high && (
        <div className="absolute bottom-2 left-2 bg-black/90 px-4 py-3 rounded-lg border border-gray-700" style={{ zIndex: 30 }}>
          <p className="text-xs text-gray-400 mb-2 font-semibold">PRICE LEVELS</p>
          <div className="grid grid-cols-2 gap-x-6 gap-y-1 text-xs">
            <span className="flex items-center gap-2">
              <span className="w-4 h-0.5 bg-blue-500"></span>
              <span className="text-blue-400">Open: ${candles[0].open.toFixed(2)}</span>
            </span>
            <span className="flex items-center gap-2">
              <span className="w-4 h-0.5 bg-green-500"></span>
              <span className="text-green-400">High: ${candles[0].high.toFixed(2)}</span>
            </span>
            <span className="flex items-center gap-2">
              <span className="w-4 h-0.5 bg-red-500"></span>
              <span className="text-red-400">Low: ${candles[0].low.toFixed(2)}</span>
            </span>
            <span className="flex items-center gap-2">
              <span className="w-4 h-0.5 bg-purple-500"></span>
              <span className="text-purple-400">Close: ${candles[0].close.toFixed(2)}</span>
            </span>
          </div>
        </div>
      )}

      {/* FVG zone legend */}
      {showAnswer && correctAnswer?.price_high && (
        <div className="absolute bottom-2 left-2 bg-black/90 px-4 py-3 rounded-lg border border-gray-700" style={{ zIndex: 30 }}>
          <p className="text-xs text-gray-400 mb-2 font-semibold">CORRECT ZONE</p>
          <div className="text-xs space-y-1">
            <span className="flex items-center gap-2">
              <span className="w-4 h-0.5 bg-green-500"></span>
              <span className="text-green-400">Top: ${correctAnswer.price_high.toFixed(2)}</span>
            </span>
            <span className="flex items-center gap-2">
              <span className="w-4 h-0.5 bg-green-500"></span>
              <span className="text-green-400">Bottom: ${correctAnswer.price_low.toFixed(2)}</span>
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default InteractiveChart;
