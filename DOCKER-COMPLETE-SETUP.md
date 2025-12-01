# 🐳 TransparentML - Complete Docker Setup

## Sistema 100% Containerizado con Metacognición AI

Todo el ecosistema TransparentML ahora corre en Docker, incluyendo **Ollama AI** para metacognición local y gratuita.

---

## 🚀 Inicio Rápido (Un Solo Comando)

```bash
make start-all-ml
```

Esto iniciará **TODOS** los servicios en contenedores Docker:

✅ **6 Servicios Corriendo:**
1. 📈 **Linear Regression** (puerto 8001)
2. 🌈 **PCA Analysis** (puerto 8002)
3. 🔍 **URL Diagnostics** (puerto 8003) - Dashboard Central
4. 🎯 **KNN Classifier** (puerto 8004)
5. 💾 **Vector Memory** (puerto 8005) - ChromaDB persistente
6. 🤖 **Ollama AI** (puerto 11434) - AI local para metacognición

---

## 📋 Pre-requisitos

Solo necesitas:

- **Docker** (versión 20.10+)
- **Docker Compose** (versión 2.0+)
- **Make** (para comandos simplificados)

**NO necesitas instalar:**
- ❌ Python
- ❌ Pip
- ❌ Node.js
- ❌ Ollama (se ejecuta en Docker)

---

## 🎯 Setup Inicial

### 1. Clonar Repositorio

```bash
git clone https://github.com/your-org/TransparentML.git
cd TransparentML
```

### 2. Crear Red Docker

```bash
docker network create transparentml-network
```

### 3. Iniciar Todo

```bash
make start-all-ml
```

Esto hará:
- ✅ Build de todas las imágenes Docker
- ✅ Inicio de todos los servicios
- ✅ Creación de volúmenes persistentes
- ✅ Descarga automática del modelo AI (llama3.2, ~2GB)

**Tiempo estimado primera vez:** 5-10 minutos (dependiendo de internet)

---

## 🌐 Acceso al Dashboard

Una vez iniciado, abre tu navegador en:

```
http://localhost:8003/static/dashboard.html
```

Verás:

```
┌─────────────────────────────────────────────────┐
│ 🔬 TransparentML - Central Dashboard           │
│                                                 │
│ Select ML Model: [Linear Regression ▼]         │
│                                                 │
│ [Configuration Panel]                           │
│                                                 │
│ [📊 Statistics] [📉 Visualizations]             │
│                                                 │
│ [📋 Real-time Logs] [📈 Log Timeline]           │
│                                                 │
│ [💡 Recommendations] [🎯 Results]               │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 🤖 AI Assistant                                 │
│ [🧠 Metacognition: ON]  [▼]                     │
├─────────────────────────────────────────────────┤
│                                                 │
│ Chat messages with AI...                        │
│                                                 │
├─────────────────────────────────────────────────┤
│ [Type your question...]         [📨]            │
├─────────────────────────────────────────────────┤
│ Powered by Ollama (Docker) • Local & Free      │
│ 💾 Memory: 0 ML | 0 Chats                       │
└─────────────────────────────────────────────────┘
```

---

## 🧠 Sistema de Metacognición

### ¿Qué es Metacognición?

El AI puede **pensar sobre su propio pensamiento**:

- 🤔 **Explica su razonamiento** paso a paso
- ⚡ **Muestra niveles de confianza** (0-100%)
- 🎯 **Identifica gaps de conocimiento**
- 💡 **Sugiere mejoras** a sus propias respuestas
- 📊 **Aprende de interacciones pasadas**

### Activar/Desactivar Metacognición

Click en el botón `🧠 Metacognition: ON/OFF` en el chatbot.

**Con Metacognición ON:**
```
Usuario: "¿Es bueno mi R² de 0.72?"

AI: 📊 Answer: Your R² of 0.72 is moderately good.

🧠 My Reasoning:
- R² measures variance explained (72% in your case)
- I searched my memory and found 15 past analyses
- Your 0.72 is above your average of 0.68
- Academic benchmark is 0.8+

⚡ Confidence: 85%
- High because I have statistical knowledge
- I've seen 15 similar cases in your history

🎯 What I'm unsure about:
- Your specific domain (affects interpretation)
- Dataset size and characteristics

💡 To improve R² to 0.8+:
1. Try feature engineering
2. Check for outliers
3. Consider non-linear models
```

**Con Metacognición OFF:**
```
Usuario: "¿Es bueno mi R² de 0.72?"

AI: 0.72 is moderately good. For best results, 
    try feature engineering or check for outliers.
```

---

## 📊 Arquitectura Docker

```
┌────────────────────────────────────────────────────────┐
│              TRANSPARENTML DOCKER NETWORK              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │ Linear Regression│  │   PCA Analysis   │          │
│  │   Port: 8001     │  │   Port: 8002     │          │
│  │   Container      │  │   Container      │          │
│  └──────────────────┘  └──────────────────┘          │
│                                                        │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │ URL Diagnostics  │  │  KNN Classifier  │          │
│  │   Port: 8003     │  │   Port: 8004     │          │
│  │ (Dashboard)      │  │   Container      │          │
│  └──────────────────┘  └──────────────────┘          │
│                                                        │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │  Vector Memory   │  │   Ollama AI      │          │
│  │   Port: 8005     │  │   Port: 11434    │          │
│  │   + ChromaDB     │  │   + llama3.2     │          │
│  └──────────────────┘  └──────────────────┘          │
│          │                      │                      │
│          ▼                      ▼                      │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │  Docker Volume   │  │  Docker Volume   │          │
│  │  vector_data     │  │  ollama_data     │          │
│  │  (Persistent)    │  │  (Models: 2GB)   │          │
│  └──────────────────┘  └──────────────────┘          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 🛠️ Comandos Disponibles

### Gestión General

```bash
# Iniciar todo
make start-all-ml

# Detener todo
make stop-all-ml

# Reiniciar todo
make restart-all-ml

# Ver logs de todos los servicios
make logs-all-ml

# Ver estado de contenedores
docker-compose -f docker-compose.all.yml ps
```

### Health Checks

```bash
# Verificar salud de todos los servicios
make health-all-ml

# Verificar servicio específico
curl http://localhost:8001/health  # Linear Regression
curl http://localhost:8002/health  # PCA
curl http://localhost:8003/health  # URL Diagnostics
curl http://localhost:8004/health  # KNN
curl http://localhost:8005/health  # Vector Memory
curl http://localhost:11434/api/tags  # Ollama AI
```

### Gestión de Ollama AI

```bash
# Inicializar Ollama (descargar modelos)
make init-ollama

# Ver modelos disponibles
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

### Gestión de Vector Memory

```bash
# Ver stats de memoria
curl http://localhost:8005/api/v1/stats

# Buscar análisis ML pasados
curl -X POST http://localhost:8005/api/v1/search/ml \
  -H "Content-Type: application/json" \
  -d '{"query": "linear regression", "n_results": 5}'

# Buscar conversaciones pasadas
curl -X POST http://localhost:8005/api/v1/search/conversations \
  -H "Content-Type: application/json" \
  -d '{"query": "R squared", "n_results": 5}'

# Reset memoria (cuidado!)
curl -X DELETE http://localhost:8005/api/v1/reset
```

---

## 🔧 Configuración Avanzada

### Cambiar Modelo de AI

Edita `url-diagnostics/static/js/dashboard-integrated.js`:

```javascript
const AI_CONFIG = {
    provider: 'ollama',
    ollama: {
        apiUrl: 'http://localhost:11434/api/chat',
        model: 'llama3.2'  // Cambiar aquí: mistral, phi3, etc.
    }
};
```

Luego reinicia:
```bash
make restart-all-ml
```

### Ajustar Nivel de Metacognición

En `dashboard-integrated.js`:

```javascript
AI_CONFIG.metacognition = {
    enabled: true,
    detailLevel: 'standard'  // 'minimal', 'standard', 'detailed'
};
```

**Niveles:**
- `minimal`: Respuesta + confianza
- `standard`: Respuesta + razonamiento + confianza + gaps
- `detailed`: Todo lo anterior + experiencia + sugerencias

### Desactivar Vector Memory

```javascript
AI_CONFIG.vectorMemory = {
    enabled: false,  // Cambiar a false
    autoStore: false
};
```

---

## 📦 Volúmenes Docker

Los datos persisten en volúmenes Docker:

```bash
# Ver volúmenes
docker volume ls | grep transparentml

# Salida:
# transparentml-vector-data    # ChromaDB (conversaciones + análisis)
# transparentml-ollama-data    # Modelos AI (llama3.2, etc.)
```

### Backup de Datos

```bash
# Backup vector memory
docker run --rm -v transparentml-vector-data:/data \
  -v $(pwd):/backup alpine \
  tar czf /backup/vector-memory-backup.tar.gz -C /data .

# Backup ollama models
docker run --rm -v transparentml-ollama-data:/data \
  -v $(pwd):/backup alpine \
  tar czf /backup/ollama-models-backup.tar.gz -C /data .
```

### Restore de Datos

```bash
# Restore vector memory
docker run --rm -v transparentml-vector-data:/data \
  -v $(pwd):/backup alpine \
  tar xzf /backup/vector-memory-backup.tar.gz -C /data

# Restore ollama models
docker run --rm -v transparentml-ollama-data:/data \
  -v $(pwd):/backup alpine \
  tar xzf /backup/ollama-models-backup.tar.gz -C /data
```

---

## 🐛 Troubleshooting

### Problema: Ollama no descarga modelos

```bash
# Verificar que Ollama esté corriendo
docker ps | grep ollama

# Logs de Ollama
make ollama-logs

# Descargar manualmente
make init-ollama
```

### Problema: Chatbot no responde

**Verificar:**
1. Ollama está corriendo: `docker ps | grep ollama`
2. Modelo está descargado: `make ollama-models`
3. Dashboard puede conectar: `curl http://localhost:11434/api/tags`

**Solución:**
```bash
# Reiniciar Ollama
docker restart transparentml-ollama

# Esperar 10 segundos
sleep 10

# Verificar modelos
make ollama-models

# Si no hay modelos, descargar
make init-ollama
```

### Problema: Vector Memory no guarda datos

```bash
# Check servicio
curl http://localhost:8005/health

# Ver logs
docker logs transparentml-vector-memory

# Verificar volumen existe
docker volume ls | grep vector-data

# Restart servicio
docker restart transparentml-vector-memory
```

### Problema: Puertos en uso

```bash
# Encontrar qué usa el puerto
lsof -i :8003

# Matar proceso
kill -9 <PID>

# O cambiar puerto en docker-compose.all.yml
ports:
  - "9003:8003"  # Puerto externo cambiado a 9003
```

### Reset Completo

Si nada funciona:

```bash
# Detener todo
make stop-all-ml

# Remover contenedores
docker-compose -f docker-compose.all.yml down -v

# Remover volúmenes
docker volume rm transparentml-vector-data
docker volume rm transparentml-ollama-data

# Rebuild y restart
docker network create transparentml-network
make start-all-ml
```

---

## 🔐 Seguridad

### Datos 100% Locales

✅ **TODO corre en tu máquina:**
- Ollama AI: 100% local, sin internet
- Vector Memory: ChromaDB local
- Todos los ML algorithms: locales

❌ **NADA se envía a la nube:**
- Tus conversaciones se quedan en tu máquina
- Tus datos ML no salen de localhost
- No se necesita API key (excepto si usas Groq/OpenAI)

### Cambiar a Proveedor Cloud (Opcional)

Si prefieres usar AI en la nube:

```javascript
// En dashboard-integrated.js
AI_CONFIG.provider = 'groq';  // o 'openai'
AI_CONFIG.groq.apiKey = 'tu-api-key-aquí';
```

---

## 📊 Monitoreo

### Ver Recursos Docker

```bash
# CPU y memoria de contenedores
docker stats

# Ver uso de volúmenes
docker system df -v
```

### Logs en Tiempo Real

```bash
# Todos los servicios
make logs-all-ml

# Servicio específico
docker logs -f transparentml-url-diagnostics
docker logs -f transparentml-ollama
docker logs -f transparentml-vector-memory
```

---

## 🚀 Performance

### Recursos Recomendados

**Mínimo:**
- RAM: 8GB
- CPU: 4 cores
- Disk: 10GB libre

**Recomendado:**
- RAM: 16GB+
- CPU: 8+ cores
- Disk: 20GB+ libre
- SSD para mejor velocidad

### Ollama con GPU (Opcional)

Para acelerar AI responses con GPU NVIDIA:

Edita `docker-compose.all.yml`:

```yaml
ollama:
  image: ollama/ollama:latest
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

Requiere:
- NVIDIA GPU
- nvidia-docker2 instalado

---

## 📚 Documentación Adicional

- **METACOGNITION-SYSTEM.md** - Teoría de metacognición
- **METACOGNITION-INTEGRATION-GUIDE.md** - Guía de uso completa
- **VECTOR-MEMORY-GUIDE.md** - ChromaDB y vector search
- **ARCHITECTURE.txt** - Arquitectura detallada
- **README-COMPLETE.md** - Documentación general

---

## 🎉 Todo Listo!

Ahora tienes un sistema **100% containerizado** con:

✅ **6 servicios ML** en Docker
✅ **AI local gratuito** (Ollama)
✅ **Metacognición** activada
✅ **Vector memory** persistente
✅ **Dashboard centralizado**
✅ **Zero dependencias** locales

**Comando para iniciar todo:**
```bash
make start-all-ml
```

**Abrir dashboard:**
```
http://localhost:8003/static/dashboard.html
```

**¡Empieza a analizar con IA metacognitiva! 🧠✨**

---

*TransparentML Team - Explainable AI in Docker*
