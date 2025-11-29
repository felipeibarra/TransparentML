# 🧠 Metacognition Integration Guide - TransparentML v1.1

## ¡Sistema Completo Integrado! ✅

El dashboard de TransparentML ahora incluye **sistema de metacognición completo** con vector memory persistente y AI que puede reflexionar sobre su propio pensamiento.

---

## 🚀 Inicio Rápido

### 1. Iniciar Todos los Servicios

```bash
cd /Users/felipeibarra_m2_max/GITHUB-FELIPE/TransparentML

# Opción 1: Usar Makefile (recomendado)
make start-all-ml

# Opción 2: Docker Compose directo
docker-compose -f docker-compose.all.yml up --build
```

Esto iniciará **5 servicios**:
- 🔍 **URL Diagnostics** → http://localhost:8003 (Dashboard Central)
- 📈 **Linear Regression** → http://localhost:8001
- 🌈 **PCA** → http://localhost:8002
- 🎯 **KNN** → http://localhost:8004
- 💾 **Vector Memory** → http://localhost:8005

### 2. Iniciar Ollama (AI Local)

```bash
# Si no está instalado
brew install ollama

# Descargar modelo (solo primera vez)
ollama pull llama3.2

# Iniciar servicio (en otra terminal)
ollama serve
```

### 3. Abrir Dashboard

```
http://localhost:8003/static/dashboard.html
```

---

## 🧠 Características del Sistema de Metacognición

### 1. **Toggle de Metacognición**

En el panel del chatbot verás:

```
┌─────────────────────────────────────────┐
│ 🤖 AI Assistant                         │
│ [🧠 Metacognition: ON]  [▼]             │
└─────────────────────────────────────────┘
```

**Click en el botón para activar/desactivar:**

- ✅ **ON** (Activo): AI muestra razonamiento completo, niveles de confianza, gaps de conocimiento
- ⚪ **OFF** (Desactivado): Respuestas concisas y directas

---

### 2. **Respuestas Metacognitivas**

Cuando está **activado**, el AI responde con:

#### Ejemplo de Pregunta Simple:

**Usuario:** "¿Es bueno mi R² de 0.72?"

**Respuesta Metacognitiva:**

```
📊 Answer: Your R² of 0.72 is moderately good.

🧠 My Reasoning:
- R² measures how well your model explains variance
- I searched my memory and found 23 past R² analyses
- Your 0.72 falls in the middle-good range
- Academic benchmark is 0.8+, so you're close

⚡ Confidence: 85%
- High confidence because I have strong statistical knowledge
- I've seen 23 similar cases in your history

🎯 What I'm unsure about:
- Your specific domain (social science vs physics matters)
- Whether you've tried feature engineering
- Your dataset size and characteristics

💡 How I can improve:
- If you tell me your field, I can give domain-specific advice
- Share dataset details for more targeted recommendations
```

---

### 3. **Niveles de Detalle Configurables**

Puedes ajustar el nivel en `dashboard-integrated.js`:

```javascript
AI_CONFIG.metacognition = {
    enabled: true,
    detailLevel: 'standard'  // 'minimal', 'standard', 'detailed'
}
```

**Minimal:** Respuesta breve + confianza
**Standard:** Razonamiento + confianza + gaps
**Detailed:** Todo lo anterior + experiencia pasada + mejoras

---

## 💾 Vector Memory - Aprendizaje Persistente

### ¿Cómo Funciona?

El sistema **automáticamente** almacena:

1. **Resultados de ML** → Cada vez que ejecutas un análisis
2. **Conversaciones** → Cada pregunta y respuesta del chatbot

Estos datos se guardan en **ChromaDB** con persistencia local.

### Búsqueda Automática

Antes de responder, el AI:

1. 🔍 **Busca** en memoria análisis similares
2. 📊 **Recupera** conversaciones relevantes
3. 🧠 **Integra** esta información en su respuesta

### Ver Estadísticas de Memoria

En el footer del chatbot verás:

```
💾 Memory: 15 ML | 42 Chats
```

- **15 ML**: 15 análisis ML almacenados
- **42 Chats**: 42 conversaciones guardadas

---

## 🎯 Flujo de Trabajo Completo

### Paso 1: Ejecutar un Análisis

1. Selecciona un modelo (Linear Regression, PCA, URL Diagnostics, KNN)
2. Configura parámetros
3. Click en **"Analyze"** o **"Train Model"**

**Automático:**
- ✅ Resultados se muestran en dashboard
- ✅ Se guardan en vector memory
- ✅ Chatbot se activa con contexto

### Paso 2: Interactuar con el AI

**Preguntas que puedes hacer:**

```
"¿Por qué mi accuracy es 0.85?"
"¿Cómo puedo mejorar mi modelo?"
"Explica qué significa la varianza del 72% en PCA"
"Compara mis últimos 3 análisis"
"¿Qué patrón ves en mis resultados?"
```

### Paso 3: Observar el Razonamiento

Con **Metacognition ON**, verás:

- 🧠 **Proceso de pensamiento** paso a paso
- ⚡ **Nivel de confianza** (0-100%)
- 📊 **Datos utilizados** de memoria
- 🎯 **Gaps de conocimiento** identificados
- 💡 **Sugerencias** para mejorar respuestas

### Paso 4: Aprendizaje Continuo

El AI aprende de cada interacción:

```
Primera vez:
Usuario: "¿Por qué mi KNN es lento?"
AI: "Podría ser el tamaño del dataset [Confianza: 60%]"

Después de 10 análisis:
Usuario: "¿Por qué mi KNN es lento?"
AI: "Basado en tus 10 análisis anteriores, veo que usas k=15 
     con 10,000 muestras. En tus casos pasados, reducir k 
     a 7 mejoró velocidad en 40% [Confianza: 90%]"
```

---

## ⚙️ Configuración Avanzada

### Editar `dashboard-integrated.js`

```javascript
// API Endpoints
const API_ENDPOINTS = {
    linearRegression: 'http://localhost:8001',
    pca: 'http://localhost:8002',
    urlDiagnostics: 'http://localhost:8003',
    knn: 'http://localhost:8004',
    vectorMemory: 'http://localhost:8005'  // Vector Memory
};

// AI Configuration
const AI_CONFIG = {
    provider: 'ollama',  // 'ollama', 'groq', 'lmstudio', 'openai'
    
    // 🧠 Metacognition Settings
    metacognition: {
        enabled: true,              // Enable/disable metacognition
        showConfidence: true,       // Show confidence scores
        showReasoning: true,        // Display reasoning chains
        showKnowledgeGaps: true,    // Highlight what AI doesn't know
        showCorrections: true,      // Show self-corrections
        confidenceThreshold: 70,    // Warn if below this %
        detailLevel: 'standard'     // 'minimal', 'standard', 'detailed'
    },
    
    // 💾 Vector Memory Settings
    vectorMemory: {
        enabled: true,              // Store analyses and conversations
        autoStore: true,            // Auto-save ML results
        searchBeforeRespond: true,  // Search memory before responding
        maxSearchResults: 5         // Number of past results to consider
    },
    
    // Ollama (Local AI - Free)
    ollama: {
        apiUrl: 'http://localhost:11434/api/chat',
        model: 'llama3.2'
    }
};
```

### Cambiar Provider de AI

```javascript
// Opciones:
AI_CONFIG.provider = 'ollama';     // Local, gratis (recomendado)
AI_CONFIG.provider = 'groq';       // Cloud, gratis (rápido)
AI_CONFIG.provider = 'lmstudio';   // Local, gratis
AI_CONFIG.provider = 'openai';     // Cloud, pagado (GPT)
```

### Ajustar Nivel de Detalle

```javascript
// Respuestas minimalistas
AI_CONFIG.metacognition.detailLevel = 'minimal';

// Respuestas estándar (recomendado)
AI_CONFIG.metacognition.detailLevel = 'standard';

// Respuestas muy detalladas
AI_CONFIG.metacognition.detailLevel = 'detailed';
```

---

## 📊 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                  DASHBOARD CENTRAL                      │
│             http://localhost:8003                       │
│                                                         │
│  ┌───────────────────────────────────────────┐         │
│  │     🧠 AI CHATBOT (Metacognition)        │         │
│  │  ┌─────────────────────────────────────┐ │         │
│  │  │ [🧠 Metacognition: ON] [▼]          │ │         │
│  │  └─────────────────────────────────────┘ │         │
│  │                                           │         │
│  │  User: "¿Es bueno mi R² de 0.72?"        │         │
│  │                                           │         │
│  │  ┌─── METACOGNITIVE PROCESSING ────┐    │         │
│  │  │ 1. Search Vector Memory          │    │         │
│  │  │ 2. Build Reasoning Chain         │    │         │
│  │  │ 3. Assess Confidence             │    │         │
│  │  │ 4. Identify Gaps                 │    │         │
│  │  └──────────────────────────────────┘    │         │
│  │                                           │         │
│  │  AI: "📊 Your R² is moderately good...   │         │
│  │       🧠 My reasoning: [...]              │         │
│  │       ⚡ Confidence: 85%                  │         │
│  │       🎯 What I'm unsure about: [...]"   │         │
│  │                                           │         │
│  │  💾 Memory: 15 ML | 42 Chats             │         │
│  └───────────────────────────────────────────┘         │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌────────────────┐    ┌────────────────┐
│  OLLAMA (AI)   │    │ VECTOR MEMORY  │
│  localhost:    │    │  localhost:    │
│     11434      │    │     8005       │
│                │    │                │
│  • llama3.2    │    │  • ChromaDB    │
│  • Local       │    │  • Persistent  │
│  • Free        │    │  • Semantic    │
│  • Private     │    │    Search      │
└────────────────┘    └────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  DOCKER VOLUME   │
                    │ transparentml-   │
                    │  vector-data     │
                    └──────────────────┘

ADEMÁS:
├─ Linear Regression API (8001)
├─ PCA API (8002)
├─ URL Diagnostics API (8003)
└─ KNN API (8004)
```

---

## 🔍 Ejemplos de Uso

### Ejemplo 1: Análisis de R²

**Ejecutar:**
1. Select: Linear Regression
2. Click: "🎯 Train Model"

**Resultado:**
```
✅ Model trained! R² = 0.7234

Chatbot:
📊 New analysis results available! 
   Linear Regression (R²: 0.723)
```

**Pregunta:**
```
User: "¿Por qué mi R² es 0.72 y no más alto?"
```

**Respuesta Metacognitiva:**

```
📊 Answer:
Your R² of 0.72 means your model explains 72% of variance. 
It's not higher because there's likely non-linear relationships 
or noise in the data.

🧠 My Reasoning:
Step 1: R² = 0.72 means 72% variance explained
Step 2: I searched my memory - you have 8 past Linear Reg analyses
Step 3: Your average R² is 0.68, so 0.72 is ABOVE your normal
Step 4: Typical "good" R² is 0.8+, but domain matters

💾 Past Experience:
- Analysis #3 (2 days ago): R² 0.89 with 200 samples
- Analysis #7 (today): R² 0.65 with noise=15.0
- Your current: R² 0.72 with noise=10.0

⚡ Confidence: 90%
I'm very confident because:
- I have strong statistical knowledge
- I've seen 8 of your past analyses
- Linear regression patterns are well-understood

🎯 What I'm unsure about:
- Your actual dataset characteristics
- Whether features are properly scaled
- If there are outliers affecting fit
- Your domain (social science vs physics)

💡 How I can improve:
To get R² > 0.8, try:
1. Feature engineering (polynomial features, interactions)
2. Remove outliers (check for data quality issues)
3. Try non-linear models (KNN, neural networks)
4. Ensure proper feature scaling

If you share your dataset details, I can give 
more specific recommendations.
```

---

### Ejemplo 2: Comparación de Modelos

**Después de ejecutar PCA y KNN:**

**Pregunta:**
```
User: "Compara mis últimos análisis"
```

**Respuesta:**

```
📊 Answer:
You've run 3 analyses recently:
1. Linear Regression: R² 0.72 (moderate fit)
2. PCA: 72% variance in PC1 (strong first component)
3. KNN: 85% accuracy (good classification)

🧠 My Reasoning:
I searched memory and found these 3 analyses from the last hour:

Analysis 1 - Linear Regression:
- Moderate fit suggests linear relationships exist
- Could be improved with feature engineering

Analysis 2 - PCA:
- 72% variance in PC1 is excellent
- Indicates one dominant pattern in your data
- Suggests dimensionality reduction will work well

Analysis 3 - KNN:
- 85% accuracy is good for classification
- Better than Linear Reg's 72% for your data
- Suggests non-linear decision boundaries

💾 Past Experience:
All three analyses used the Iris dataset:
- Your Linear Reg: R² 0.72
- Your PCA: PC1 72%, PC2 28%
- Your KNN: 85% accuracy with k=5

⚡ Confidence: 95%
Very confident because:
- All three are on the same dataset (Iris)
- I can directly compare results
- Patterns are clear

🎯 What I'm unsure about:
- Which metric matters most to you
- Your end goal (prediction vs interpretation)
- Production constraints (speed, interpretability)

💡 Recommendation:
For Iris dataset:
1. Use KNN for BEST ACCURACY (85%)
2. Use Linear Reg for INTERPRETABILITY
3. Use PCA for VISUALIZATION (2D plots)

KNN wins for prediction, but if you need to 
explain decisions to stakeholders, Linear Reg 
is more interpretable despite lower accuracy.
```

---

### Ejemplo 3: Debugging

**Pregunta:**
```
User: "¿Por qué mi KNN solo tiene 75% accuracy?"
```

**Respuesta:**

```
📊 Answer:
75% accuracy with KNN can be caused by:
1. Suboptimal k value
2. Unscaled features
3. Class imbalance
4. Too few training samples

🧠 My Reasoning:
Let me analyze your specific case...

Step 1: Check your parameters
- Your k = 5 (default)
- Dataset: Iris (balanced, 150 samples)
- Test split: 30%

Step 2: Search memory for similar cases
Found 4 past KNN analyses:
- k=3: 82% accuracy
- k=5: 75% accuracy (YOUR CURRENT)
- k=7: 78% accuracy
- k=10: 73% accuracy

Step 3: Identify pattern
Your k=5 is giving 75%, but k=3 gave 82%.
For Iris dataset, lower k values perform better.

💾 Past Experience:
In your analysis history:
- Best KNN: 87% with k=3, scaled features
- Worst KNN: 72% with k=10, unscaled
- Current: 75% with k=5

⚡ Confidence: 88%
High confidence because:
- I have your past KNN results to compare
- Iris dataset is well-studied
- Pattern is clear: lower k works better here

🎯 What I'm unsure about:
- Whether you scaled features
- If there are preprocessing steps I'm not seeing
- Your tolerance for overfitting

💡 Actionable Recommendations:
To improve from 75% to 85%+:

1. CHANGE K VALUE (highest impact):
   Try k=3 (based on your past success)

2. SCALE FEATURES:
   from sklearn.preprocessing import StandardScaler
   scaler = StandardScaler()
   X_scaled = scaler.fit_transform(X)

3. TRY DIFFERENT DISTANCE METRICS:
   Try manhattan distance instead of euclidean

4. CROSS-VALIDATION:
   Your 75% might be test set dependent
   Use 5-fold CV to get stable estimate

Based on your past analyses, these changes 
should get you to 82-87% accuracy.
```

---

## 🎛️ Controles del Dashboard

### Panel de Chatbot

```
┌─────────────────────────────────────────┐
│ 🤖 AI Assistant                         │
│ [🧠 Metacognition: ON]  [▼]             │
├─────────────────────────────────────────┤
│                                         │
│ [Chat messages...]                      │
│                                         │
├─────────────────────────────────────────┤
│ [Type your question...]    [📨]         │
├─────────────────────────────────────────┤
│ Powered by Ollama • Context-aware       │
│ 💾 Memory: 15 ML | 42 Chats             │
└─────────────────────────────────────────┘
```

### Botones:

- **🧠 Metacognition: ON/OFF** → Toggle de metacognición
- **▼** → Minimizar/Expandir chatbot
- **📨** → Enviar mensaje

---

## 🐛 Troubleshooting

### Problema: Chatbot no responde

**Solución:**
```bash
# Verificar Ollama está corriendo
ollama list

# Si no está corriendo, iniciar
ollama serve

# En otra terminal
ollama run llama3.2
```

### Problema: Vector Memory no guarda datos

**Check:**
```bash
# Verificar servicio está corriendo
curl http://localhost:8005/health

# Ver stats
curl http://localhost:8005/api/v1/stats

# Debería responder:
# {"total_ml_results": X, "total_conversations": Y}
```

**Si falla:**
```bash
# Restart servicios
docker-compose -f docker-compose.all.yml restart vector-memory
```

### Problema: Metacognición no se muestra

**Verificar en navegador (F12 Console):**
```javascript
// Check estado
state.metacognitionEnabled
// Debería ser: true

// Check config
AI_CONFIG.metacognition.enabled
// Debería ser: true
```

**Si es false:**
```javascript
// Activar manualmente
state.metacognitionEnabled = true;

// O click en botón "🧠 Metacognition: OFF"
```

### Problema: Memory stats siempre en 0

**Debug:**
```bash
# Check vector memory logs
docker-compose -f docker-compose.all.yml logs vector-memory

# Test manualmente
curl -X POST http://localhost:8005/api/v1/memory/ml-result \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm_type": "test",
    "results": {"metric": 0.5},
    "metadata": {}
  }'

# Check stats
curl http://localhost:8005/api/v1/stats
```

---

## 📈 Mejoras Futuras

### v1.2 (Próximamente)

- [ ] **Uncertainty Quantification**: Confianza con intervalos (85% ± 10%)
- [ ] **Alternative Reasoning Paths**: Mostrar múltiples caminos de razonamiento
- [ ] **Meta-Learning**: AI ajusta confianza basado en precisión histórica
- [ ] **Collaborative Refinement**: Feedback loop usuario-AI
- [ ] **Visualización de Reasoning**: Grafos de pensamiento
- [ ] **Export de Conversaciones**: Download chat history
- [ ] **Comparación Multi-modelo**: Compare 4 algoritmos automáticamente

---

## 📚 Documentación Adicional

- **METACOGNITION-SYSTEM.md** → Teoría y filosofía de metacognición
- **VECTOR-MEMORY-GUIDE.md** → Guía completa de vector memory
- **OLLAMA-SETUP.md** → Setup detallado de Ollama
- **ARCHITECTURE.txt** → Arquitectura completa del sistema
- **README-COMPLETE.md** → Documentación general del proyecto

---

## 🎉 ¡Disfruta de TransparentML v1.1!

Ahora tienes un AI que:

✅ **Explica su razonamiento** paso a paso
✅ **Evalúa su propia confianza** con honestidad
✅ **Identifica gaps de conocimiento** para mejorar
✅ **Aprende de cada interacción** con memoria persistente
✅ **Se autocorrige** basándose en feedback
✅ **Es transparente** sobre sus limitaciones

**El AI que piensa sobre cómo piensa.** 🧠✨

---

*TransparentML Team - Building Explainable AI*
