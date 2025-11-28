# 🚀 Quick Reference - Todo en Contenedores

## ⚠️ REGLA DE ORO
**NUNCA ejecutes Python directamente en tu Mac. Siempre usa `make` o `docker-compose exec`**

---

## 🎯 Comandos Esenciales

```bash
# Ver ayuda completa
make help

# Setup inicial
make build && make up

# Entrenar modelo (EN CONTENEDOR)
make train

# Ejecutar tests (EN CONTENEDOR)
make test

# Ver estado
make ps

# Ver logs
make logs
```

---

## 📋 Flujo Típico de Trabajo

```bash
# 1. Iniciar servicios (una vez)
make up

# 2. Desarrollar: edita código en tu Mac
#    Los cambios se sincronizan automáticamente

# 3. Entrenar/probar (EN CONTENEDOR)
make train
make test

# 4. Detener al finalizar
make down
```

---

## 💻 Debugging

```bash
# Acceder a shell del contenedor
make shell-pca

# Dentro del contenedor puedes ejecutar:
python scripts/train.py
pytest tests/ -v
python -c "import sys; print(sys.version)"

# Salir del contenedor
exit
```

---

## 🔧 Comandos Completos

### Gestión
- `make build` - Construir imágenes
- `make up` - Iniciar servicios
- `make down` - Detener servicios
- `make ps` - Ver estado
- `make logs` - Ver logs
- `make restart` - Reiniciar servicios

### Desarrollo
- `make train` - Entrenar modelo
- `make test` - Ejecutar tests
- `make lint` - Verificar código
- `make format` - Formatear código

### Shell
- `make shell-pca` - Shell en training
- `make shell-api` - Shell en API
- `make shell-jupyter` - Shell en Jupyter

### API
- `make api-health` - Salud de API
- `make api-info` - Info del modelo
- `make api-reload` - Recargar modelo

### Limpieza
- `make clean-results` - Limpiar resultados
- `make clean-docker` - Limpiar Docker
- `make reset-all` - 🔥 BORRAR TODO y reinstalar (con confirmación)

---

## ❌ NO HACER vs ✅ HACER

| ❌ NO (en Mac) | ✅ SÍ (en contenedor) |
|---------------|---------------------|
| `python scripts/train.py` | `make train` |
| `pytest tests/` | `make test` |
| `black src/` | `make format` |
| `pip install numpy` | Editar `requirements.txt` + `make build` |

---

## 📂 Dónde están las cosas

```
./src/           → Código (edita en Mac, ejecuta en contenedor)
./scripts/       → Scripts (edita en Mac, ejecuta en contenedor)
./results/       → Resultados (generados en contenedor, visibles en Mac)
./models/        → Modelos (generados en contenedor, visibles en Mac)
./data/          → Datos (compartidos entre Mac y contenedor)
```

---

## 🆘 Problemas Comunes

**"Container not running"**
```bash
make up
```

**"Port already in use"**
```bash
make down
# Luego editar puertos en docker-compose.yml si persiste
```

**"Changes not working"**
```bash
make restart
# O reconstruir: make build
```

**"Need fresh start"**
```bash
make clean-docker && make build && make up
```

**"Nuclear option - RESET TODO"**
```bash
make reset-all  # Borra TODO y reinstala desde cero
# Ver docs/guides/RESET_GUIDE.md para detalles
```

---

## 📞 Más Info

- Detalles completos: `DOCKER_WORKFLOW.md`
- Arquitectura: `DOCKER_GUIDE.md`
- API: `API_EXAMPLES.md`
- Ayuda: `make help`
