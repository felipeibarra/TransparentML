# 🚀 TransparentML Quick Start Guide

Get up and running with URL Diagnostics in **under 2 minutes**!

---

## 📋 Prerequisites

- ✅ Docker Desktop installed and running
- ✅ Port 8003 available
- ✅ Internet connection

---

## ⚡ Option 1: One-Command Start (Recommended)

### Using Make (Easiest)

```bash
make start-complete
```

This will:
1. Create the Docker network
2. Build the service
3. Start the container
4. Display all endpoints and instructions

### Using Shell Script

```bash
./start-url-diagnostics.sh
```

The script will automatically:
- Check Docker status
- Build and start the service
- Open your browser to the interface

---

## ⚡ Option 2: Manual Start

### Step 1: Create Network

```bash
docker network create transparentml-network
```

### Step 2: Build & Start

```bash
cd url-diagnostics
docker-compose up -d
```

### Step 3: Open Browser

Visit: **http://localhost:8003/static/index.html**

---

## 🎯 Using the Interface

### 1️⃣ Enter a URL

Type any website URL in the input field:
```
https://www.google.com
https://www.github.com
https://www.amazon.com
```

### 2️⃣ Select Analysis Type

Choose from:
- **Comprehensive** (recommended) - Full analysis with all metrics
- **Quick** - Fast scan of essential metrics
- **Security** - Focus on security headers and SSL

### 3️⃣ Click "Analyze URL"

Watch the magic happen:
- ⏳ Real-time progress bar
- 📋 Live log streaming
- 🤖 ML analysis in action

### 4️⃣ View Results

Get comprehensive insights:
- 📊 **Health Score** (0-100) with letter grade
- ⚡ **Performance Metrics** (load time, page size)
- 🔒 **Security Analysis** (SSL, headers)
- 📱 **Mobile Compatibility**
- 📈 **Interactive Charts**
- 💡 **Actionable Recommendations** (prioritized)

### 5️⃣ Analyze Another URL

Click the **"🔄 Analyze Another URL"** button at the bottom to:
- Reset the interface
- Start a new analysis
- Keep your workflow smooth

---

## 📍 All Available Endpoints

### 🎛️ Central Dashboard (NEW - All Models)
```
http://localhost:8003/static/dashboard.html
```
👆 **Start here!** - Unified interface with all ML models

### 📊 URL Analysis Interface (Simple)
```
http://localhost:8003/static/index.html
```
Focused on URL health diagnostics only

### API Documentation
```
http://localhost:8003/docs
```
Interactive Swagger UI

### Health Check
```
http://localhost:8003/health
```
Service status

### API Endpoints

**Async Analysis:**
```bash
curl -X POST http://localhost:8003/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com", "analysis_type": "comprehensive"}'
```

**Sync Analysis:**
```bash
curl -X POST http://localhost:8003/api/v1/analyze/sync \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

---

## 🔧 Useful Commands

### View Logs
```bash
make logs-url-diagnostics

# OR
docker-compose -f url-diagnostics/docker-compose.yml logs -f
```

### Stop Service
```bash
make stop-complete

# OR
cd url-diagnostics && docker-compose down
```

### Restart Service
```bash
make restart-complete

# OR
./start-url-diagnostics.sh
```

### Enter Container
```bash
make shell-url-diagnostics

# OR
docker exec -it transparentml-url-diagnostics /bin/bash
```

### Check Status
```bash
make status

# OR
docker ps | grep transparentml
```

---

## 💡 Makefile Commands Reference

### Main Commands

| Command | Description |
|---------|-------------|
| `make start-complete` | 🚀 Start everything (RECOMMENDED) |
| `make stop-complete` | ⛔ Stop all services |
| `make restart-complete` | 🔄 Restart all services |

### Service-Specific

| Command | Description |
|---------|-------------|
| `make up-url-diagnostics` | Start URL Diagnostics |
| `make down-url-diagnostics` | Stop URL Diagnostics |
| `make logs-url-diagnostics` | View logs |
| `make shell-url-diagnostics` | Enter container |

### Other Services

| Command | Description |
|---------|-------------|
| `make up-linear-regression` | Start Linear Regression |
| `make up-pca` | Start PCA Analysis |
| `make up-all` | Start core ML services |

### Utilities

| Command | Description |
|---------|-------------|
| `make status` | Show all running services |
| `make help` | Show all available commands |
| `make clean-all` | Clean temporary files |

---

## 🎨 What You'll See

### 1. Health Score Display
- Large circular progress indicator
- Letter grade (A+ to F)
- Color-coded by performance
- Interpretation message

### 2. Metrics Dashboard
- ⚡ Load Time
- 📦 Page Size
- 🔒 SSL Status
- 📱 Mobile Compatibility

### 3. Interactive Charts
- **Bar Chart**: Feature-by-feature analysis
- **Radar Chart**: Category scores (Performance, Security, SEO, Mobile)

### 4. Anomalies Section
- 🔍 Detected issues
- ⚠️ Warning indicators
- ✅ Success confirmations

### 5. Recommendations Panel
- 🔴 **Critical** issues (fix immediately)
- 🟠 **High** priority items
- 🔵 **Medium** improvements
- 🟢 **Low** priority enhancements

Each recommendation includes:
- Current state
- Target state
- Specific action to take

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find what's using port 8003
lsof -i :8003

# Kill the process
kill -9 <PID>

# Or use a different port in docker-compose.yml
```

### Docker Not Running

```bash
# Start Docker Desktop
open -a Docker

# Wait a few seconds, then retry
```

### Service Not Responding

```bash
# Check logs
make logs-url-diagnostics

# Restart service
make restart-complete
```

### Can't Connect to Network

```bash
# Recreate network
docker network rm transparentml-network
docker network create transparentml-network

# Restart service
make restart-complete
```

---

## 📖 Example Analysis Flow

```
1. Open: http://localhost:8003/static/index.html
   
2. Enter: https://www.github.com
   
3. Select: Comprehensive
   
4. Click: "Analyze URL"
   
5. Watch: 
   ✓ Fetching URL metrics...
   ✓ Extracting features...
   ✓ Running ML analysis...
   ✓ Health Score: 89/100 (A-)
   
6. Review:
   - Performance: Good (1.2s load time)
   - Security: Excellent (SSL + headers)
   - SEO: Great (meta tags present)
   - Mobile: Optimized
   
7. Recommendations:
   - Medium: Enable compression (save 30%)
   - Low: Add Schema.org markup
   
8. Click: "🔄 Analyze Another URL"
   
9. Repeat!
```

---

## 🎓 Understanding the Results

### Health Score Ranges

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A+ / A | Excellent |
| 80-89 | A- / B+ | Good |
| 70-79 | B / B- | Fair |
| 60-69 | C+ / C | Needs Work |
| < 60 | C- / D / F | Critical Issues |

### Key Metrics

**Load Time:**
- < 2s: 🟢 Excellent
- 2-3s: 🟡 Good
- 3-5s: 🟠 Needs improvement
- > 5s: 🔴 Poor

**Page Size:**
- < 500KB: 🟢 Excellent
- 500KB-1MB: 🟡 Good
- 1-3MB: 🟠 Heavy
- > 3MB: 🔴 Very heavy

**SSL:**
- ✅ Present & valid: Required
- ❌ Missing: Critical issue

**Mobile:**
- ✅ Viewport meta: Required
- ❌ Missing: High priority fix

---

## 🔐 No Authentication Required

This is a **local development tool**. No user/password needed!

Simply start the service and access:
```
http://localhost:8003/static/index.html
```

---

## 🆘 Need Help?

- **Documentation**: http://localhost:8003/docs
- **README**: `url-diagnostics/README.md`
- **API Reference**: http://localhost:8003/redoc
- **Logs**: `make logs-url-diagnostics`

---

## 🎉 You're Ready!

Now go analyze some URLs and discover insights about any website!

```bash
make start-complete
```

Then open: **http://localhost:8003/static/index.html**

Happy analyzing! 🚀
