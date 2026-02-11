# 📁 TradeLingo Image Guide
# ================================

## How to Add Your Own Images

### 1. Put images in this folder:
```
/app/backend/static/images/
```

### 2. Organize by category (recommended):
```
/app/backend/static/images/
├── candlesticks/
│   ├── bullish-1.png
│   ├── bearish-1.png
│   └── doji-1.png
├── market-structure/
│   ├── hh-hl-1.png
│   └── lh-ll-1.png
├── order-blocks/
│   ├── bullish-ob-1.png
│   └── bearish-ob-1.png
└── fvg/
    ├── bullish-fvg-1.png
    └── bearish-fvg-1.png
```

### 3. Reference in exercises using:
```
/api/static/images/candlesticks/bullish-1.png
/api/static/images/order-blocks/bullish-ob-1.png
```

### 4. Update curriculum.py CHART_IMAGES:
```python
CHART_IMAGES = {
    "candlesticks": [
        "/api/static/images/candlesticks/bullish-1.png",
        "/api/static/images/candlesticks/bearish-1.png",
        # ... 10 images per level
    ],
}
```

## Quick Test
Your images are accessible at:
- Local: http://localhost:8001/api/static/images/YOUR-IMAGE.png
- Preview: {REACT_APP_BACKEND_URL}/api/static/images/YOUR-IMAGE.png

## Supported Formats
- PNG (recommended for charts)
- JPG/JPEG
- GIF
- WebP
