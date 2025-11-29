# 🌐 Dashboard Guide - TransparentML

## Quick Start

### 1. Start the Platform

```bash
# From project root
make start-all-ml
```

### 2. Access Dashboard

Open: **http://localhost:8003/static/dashboard.html**

---

## 🎯 Dashboard Layout

### Main Areas

```
┌──────────────────────────────────────────────────────┐
│  Header: Model Selection + Clear All                │
├─────────────┬────────────────────────┬───────────────┤
│  LEFT       │      CENTER            │    RIGHT      │
│  Sidebar    │      Content           │   Sidebar     │
│             │                        │               │
│ • Config    │ • Statistics (4 cards) │ • Results     │
│ • Settings  │ • Progress Bar         │ • Recomm.     │
│ • Status    │ • Charts (interactive) │               │
│             │ • Real-time Logs       │               │
│             │ • Log Analytics        │               │
└─────────────┴────────────────────────┴───────────────┘
                                        
                        ┌──────────────────┐
                        │  🤖 AI Chatbot   │  ← Floating
                        │  (Bottom Right)  │
                        └──────────────────┘
```

---

## 🤖 AI Chatbot Features

### Location
**Fixed position at bottom-right corner** - Always accessible!

### How It Works

1. **Run any ML analysis** (Linear Reg, PCA, URL Diag, or KNN)
2. **Chatbot automatically activates** and shows available context
3. **Ask questions** about your results
4. **Get AI-powered explanations** based on your actual data

### Example Questions

```
✅ "Explain my R² score"
✅ "What does 72% variance mean?"
✅ "Why is my URL health score 65?"
✅ "What's the difference between training and test accuracy?"
✅ "Should I use more neighbors in KNN?"
✅ "How can I improve my model?"
```

### Controls

- **▼ Button**: Minimize/Expand chatbot
- **Drag-friendly**: Chatbot stays in corner, doesn't block content
- **Context-aware**: Automatically knows which analyses you've run

---

## 📊 Using Each ML Model

### 1. URL Diagnostics

**Steps:**
1. Select "URL Health Diagnostics" from dropdown
2. Enter a URL (e.g., `https://google.com`)
3. Choose analysis type (Comprehensive recommended)
4. Click "🚀 Analyze"

**Results:**
- Health Score (0-100)
- Letter Grade (A-F)
- Load time, SSL status
- Prioritized recommendations

**Ask AI:**
- "Why is my score low?"
- "What should I fix first?"
- "Explain the health metrics"

---

### 2. Linear Regression

**Steps:**
1. Select "Linear Regression" from dropdown
2. Click "🎯 Train Model" (uses demo data)

**Results:**
- R² Score
- RMSE, MAE
- Model coefficients (slope, intercept)

**Ask AI:**
- "Is my R² score good?"
- "Explain the RMSE value"
- "What do the coefficients mean?"

---

### 3. PCA Analysis

**Steps:**
1. Select "PCA Analysis" from dropdown
2. Click "🌟 Run PCA" (uses Iris dataset)

**Results:**
- Variance explained per component
- Total variance captured
- Component loadings

**Ask AI:**
- "How much information was preserved?"
- "What does PC1 represent?"
- "Should I use more components?"

---

### 4. K-Nearest Neighbors

**Steps:**
1. Select "K-Nearest Neighbors" from dropdown
2. Choose dataset (Iris or Random)
3. Set K neighbors (default: 5)
4. Click "🎯 Run KNN"

**Results:**
- Classification accuracy
- Per-class metrics
- Confusion matrix data

**Ask AI:**
- "Is my accuracy good?"
- "What's the best K value?"
- "Which classes are confused?"

---

## 🎨 Interactive Features

### Real-Time Logs
- **Auto-scroll**: New logs appear at bottom
- **Pause button**: Freeze log stream
- **Clear button**: Remove all logs
- **Export button**: Download logs as .txt
- **Filters**: Toggle Info/Warning/Error visibility

### Charts
- **Bar Chart**: Default view
- **Line Chart**: Trend visualization
- **Radar Chart**: Multi-dimensional comparison
- **Scatter Plot**: Relationship visualization

### Statistics Cards
- **Health Score**: Main metric (0-100 or accuracy %)
- **Processing Time**: Analysis duration
- **Data Points**: Sample count
- **Accuracy**: Model performance metric

---

## 🔧 Chatbot Configuration

### Setup Groq API (Free)

1. **Get API Key**:
   - Go to https://console.groq.com
   - Sign up (free)
   - Create API key

2. **Configure Dashboard**:
   ```bash
   # Edit file
   nano url-diagnostics/static/js/dashboard-integrated.js
   
   # Line 17: Replace 'YOUR_GROQ_API_KEY_HERE' with your key
   apiKey: 'gsk_abcd1234...'
   ```

3. **Restart Services**:
   ```bash
   make restart-all-ml
   ```

### Without API Key
Chatbot will still show context but use fallback responses.

---

## 💡 Tips & Tricks

### Performance
- **Run one analysis at a time** for best results
- **Clear logs** periodically to keep UI responsive
- **Export logs** before clearing for record-keeping

### Chatbot
- **Be specific** in questions
- **Reference your results** (e.g., "my R² score")
- **Ask follow-ups** - chat history is maintained
- **Minimize when not needed** to save screen space

### Visualizations
- **Switch chart types** to find best representation
- **Hover over bars/points** for exact values (Chart.js feature)
- **Export charts** via browser screenshot

---

## 🐛 Troubleshooting

### Chatbot Not Responding
1. Check if analysis completed successfully
2. Verify Groq API key is set correctly
3. Check browser console for errors (F12)

### Services Not Starting
```bash
# Check service health
make health-all-ml

# View logs
make logs-all-ml

# Restart all
make restart-all-ml
```

### Dashboard Not Loading
1. Ensure port 8003 is not in use
2. Check Docker containers are running: `docker ps`
3. Verify network: `docker network ls | grep transparentml`

---

## 📈 Advanced Usage

### Multiple Analyses
Run different models sequentially - chatbot remembers all results!

**Example workflow:**
1. Analyze URL → Get health score
2. Run KNN → Get accuracy
3. Ask: "Compare my URL score vs KNN accuracy"

### Context Accumulation
Chatbot builds context as you work:

```
After URL Analysis:
  → Context: URL health = 72

After Linear Regression:
  → Context: URL health = 72, R² = 0.89

Ask: "Which result is better?"
```

---

## 🎓 Learning Resources

### Understanding Metrics

| Metric | Good Range | What It Means |
|--------|------------|---------------|
| **R² Score** | > 0.8 | Model explains 80%+ of variance |
| **RMSE** | Lower is better | Average prediction error |
| **Accuracy** | > 0.9 | 90%+ correct predictions |
| **Variance Explained** | > 0.7 | Captures 70%+ of information |

### Model Selection Guide

- **Linear Regression**: Continuous predictions, trend analysis
- **PCA**: Dimensionality reduction, feature extraction
- **URL Diagnostics**: Website health, SEO, security analysis
- **KNN**: Classification, pattern recognition

---

## 🚀 Next Steps

1. **Explore all models** - Try each one with different parameters
2. **Use chatbot actively** - Ask questions to deepen understanding
3. **Export results** - Save logs and charts for reports
4. **Compare models** - Run multiple analyses and compare

---

## 📞 Support

- **Documentation**: See `ARCHITECTURE.txt` for technical details
- **API Docs**: Access FastAPI docs at each service's `/docs` endpoint
- **Issues**: Check browser console (F12) for error messages

---

**Happy Analyzing! 🎉**

*TransparentML Team*
