# 🚀 TransparentML v1.1 - Quick Start

## ¡UN SOLO COMANDO para Empezar!

```bash
make start-all-ml
```

**Eso es todo.** Todo está containerizado y automatizado. ✨

---

## 🎯 Lo Que Obtienes

Después de `make start-all-ml`, tendrás corriendo:

✅ **6 Servicios en Docker:**
1. 📈 Linear Regression API (puerto 8001)
2. 🌈 PCA Analysis API (puerto 8002)
3. 🔍 URL Diagnostics + Dashboard (puerto 8003)
4. 🎯 KNN Classifier API (puerto 8004)
5. 💾 Vector Memory / ChromaDB (puerto 8005)
6. 🤖 Ollama AI Local (puerto 11434)

✅ **Características AI:**
- 🧠 **Metacognición** - AI que explica su razonamiento
- 💾 **Vector Memory** - Aprende de cada interacción
- 🤖 **Ollama** - AI 100% local y gratuito (llama3.2)
- 📊 **Persistencia** - Tus datos se guardan localmente

---

## 📋 Pre-requisitos

Solo necesitas:
- Docker (>= 20.10)
- Docker Compose (>= 2.0)
- Make

**NO necesitas:**
- ❌ Python
- ❌ Node.js
- ❌ Ollama instalado localmente
- ❌ API keys

---

## 🚀 Inicio Rápido

### 1. Iniciar Todo

```bash
cd TransparentML
make start-all-ml
```

Primera vez: **5-10 minutos** (descarga modelo AI ~2GB)
Siguientes veces: **30 segundos**

Verás:
```
══════════════════════════════════════════════════════════════
  🚀 TRANSPARENTML v1.1 - FULLY CONTAINERIZED
══════════════════════════════════════════════════════════════

🎯 MAIN DASHBOARD (START HERE):
   http://localhost:8003/static/dashboard.html

📊 ML SERVICE APIS:
   📈 Linear Regression:    http://localhost:8001/docs
   🌈 PCA Analysis:         http://localhost:8002/docs
   🔍 URL Diagnostics:      http://localhost:8003/docs
   🎯 KNN Classifier:       http://localhost:8004/docs
   💾 Vector Memory:        http://localhost:8005/docs
   🤖 Ollama AI:            http://localhost:11434/api/tags

🧠 AI FEATURES:
   ✅ Metacognition Mode (AI explains its reasoning)
   ✅ Vector Memory (learns from every interaction)
   ✅ Ollama AI (100% local & free)
   ✅ Persistent storage (ChromaDB + Ollama models)

══════════════════════════════════════════════════════════════
💡 USEFUL COMMANDS:
   make logs-all-ml       - View logs from all services
   make stop-all-ml       - Stop all services
   make health-all-ml     - Check health of all services
   make init-ollama       - Re-download AI models
   make ollama-models     - List installed AI models

✅ Ready! Open the dashboard and start analyzing with AI! 🧠✨
```

### 2. Abrir Dashboard

```bash
open http://localhost:8003/static/dashboard.html
```

---

## 🧠 Usar Metacognición (La Mejor Parte)

### Paso 1: Ejecutar un Análisis

En el dashboard:
1. **Select model**: Linear Regression
2. **Click**: "🎯 Train Model"
3. Espera 5 segundos
4. Ve resultados (R², RMSE, etc.)

### Paso 2: Preguntarle al AI

En el chatbot (abajo derecha):

**Pregunta:** `¿Por qué mi R² es 0.72?`

**AI responde con Metacognición ON:**

```
📊 Answer:
Your R² of 0.72 means your model explains 72% of variance.
It's moderately good, but has room for improvement.

🧠 My Reasoning:
Step 1: R² measures explained variance (72% in your case)
Step 2: I searched my memory - found 3 past linear reg analyses
Step 3: Your 0.72 is average compared to your history
Step 4: Academic benchmark is 0.8+ for "good" R²

💾 Past Experience:
- Analysis #1: R² 0.89 with 200 samples
- Analysis #2: R² 0.65 with noise=15.0
- Your current: R² 0.72 with noise=10.0

⚡ Confidence: 90%
Very confident because:
- I have strong statistical knowledge
- I've seen 3 of your past analyses
- Linear regression patterns are well-understood

🎯 What I'm unsure about:
- Your specific dataset characteristics
- Whether features are properly scaled
- If there are outliers affecting fit

💡 How to improve to 0.8+:
1. Try feature engineering (polynomial, interactions)
2. Remove outliers (check for data quality)
3. Consider non-linear models if relationships aren't linear
4. Ensure proper feature scaling

If you share your dataset details, I can give
more specific recommendations.
```

### Paso 3: Toggle Metacognición

Click en **`🧠 Metacognition: ON`** para apagarlo.

**Con OFF:**
```
AI: 0.72 is moderately good. Try feature engineering
    or check for outliers to improve.
```

---

## 🛠️ Comandos del Makefile

### Gestión de Servicios

```bash
# Iniciar todo (con Ollama auto-init)
make start-all-ml

# Detener todo
make stop-all-ml

# Reiniciar todo
make restart-all-ml

# Ver logs en tiempo real
make logs-all-ml

# Health check completo
make health-all-ml
```

### Gestión de Ollama AI

```bash
# Inicializar/descargar modelos
make init-ollama

# Ver modelos instalados
make ollama-models

# Descargar modelo adicional
make ollama-pull MODEL=mistral
make ollama-pull MODEL=phi3
make ollama-pull MODEL=codellama

# Remover modelo
make ollama-remove MODEL=llama3.2

# Ver logs de Ollama
make ollama-logs
```

---

## 📊 Ejemplo Completo de Uso

```bash
# 1. START
make start-all-ml

# 2. OPEN DASHBOARD
open http://localhost:8003/static/dashboard.html

# 3. RUN KNN ANALYSIS
#    - Dashboard → Select "KNN Classifier"
#    - Dataset: Iris
#    - K Neighbors: 5
#    - Click "🎯 Run KNN"
#    - Results appear in ~5 seconds

# 4. ASK AI ABOUT RESULTS
#    - Chatbot (bottom right)
#    - Type: "Why is my accuracy 85%?"
#    - Press Enter or click 📨

# 5. SEE METACOGNITION
#    AI explains:
#    - Its reasoning process
#    - Confidence level
#    - What it's unsure about
#    - How to improve

# 6. RUN MORE ANALYSES
#    - Try Linear Regression
#    - Try PCA
#    - Ask: "Compare my last 3 analyses"
#    - AI uses Vector Memory to compare!

# 7. STOP WHEN DONE
make stop-all-ml
```

---

## 🔍 Verificación Post-Inicio

Después de `make start-all-ml`, verifica:

```bash
# 1. Contenedores corriendo (deberías ver 6)
docker ps | grep transparentml

# 2. Ollama tiene modelos
make ollama-models
# Output debe mostrar: llama3.2

# 3. Vector Memory funciona
curl http://localhost:8005/health
# Output: {"status":"healthy",...}

# 4. Dashboard accesible
curl -s http://localhost:8003/static/dashboard.html | head -5
# Debe mostrar HTML

# 5. Ver stats de memoria
curl http://localhost:8005/api/v1/stats
# Output: {"total_ml_results":0,"total_conversations":0}
```

Si todo funciona ✅, ¡estás listo!

---

## 🐛 Troubleshooting

### Problema: "Chatbot no responde"

**Causa:** Ollama no tiene modelos descargados

**Solución:**
```bash
make init-ollama
```

Espera 2-5 minutos (descarga ~2GB).

---

### Problema: "Puerto 8003 ya está en uso"

**Solución:**
```bash
# Encuentra qué usa el puerto
lsof -i :8003

# Mata el proceso
kill -9 <PID>

# Reinicia
make restart-all-ml
```

---

### Problema: "Vector Memory no guarda datos"

**Verificar:**
```bash
# Ver logs
docker logs transparentml-vector-memory

# Verificar volumen
docker volume ls | grep vector

# Restart servicio
docker restart transparentml-vector-memory
```

---

### Reset Completo (Si nada funciona)

```bash
make stop-all-ml
docker-compose -f docker-compose.all.yml down -v
docker volume rm transparentml-vector-data transparentml-ollama-data
docker network create transparentml-network
make start-all-ml
```

---

## 📚 Documentación Completa

Para más detalles:

- **DOCKER-COMPLETE-SETUP.md** - Setup Docker completo
- **METACOGNITION-INTEGRATION-GUIDE.md** - Guía de metacognición
- **METACOGNITION-SYSTEM.md** - Teoría de metacognición
- **VECTOR-MEMORY-GUIDE.md** - Sistema de memoria vectorial

---

## 🎉 ¡Eso es Todo!

Con un solo comando tienes:

✅ **6 servicios ML** corriendo en Docker
✅ **AI metacognitivo** local y gratuito  
✅ **Vector memory** que aprende de ti
✅ **Dashboard centralizado** con todo integrado
✅ **Zero instalaciones** locales (solo Docker)

**Comando mágico:**
```bash
make start-all-ml
```

**Dashboard:**
```
http://localhost:8003/static/dashboard.html
```

**¡Empieza a analizar con IA que piensa sobre cómo piensa! 🧠✨**

---

*TransparentML v1.1 - Explainable AI, Fully Dockerized*
