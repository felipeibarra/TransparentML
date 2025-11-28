# 🔥 Guía: Reset Completo del Proyecto

## 📋 ¿Qué es el Reset Completo?

`make reset-all` es una **super función** que borra TODO el proyecto y lo reinstala desde cero, dejándolo en un estado completamente limpio como si acabaras de clonarlo por primera vez.

---

## ⚠️ ADVERTENCIA

Esta operación es **DESTRUCTIVA** y **NO SE PUEDE DESHACER**.

Borrará:
- ❌ Todos los contenedores Docker
- ❌ Todas las imágenes Docker del proyecto
- ❌ Todos los volúmenes Docker
- ❌ Todo el cache de Docker
- ❌ Todos los resultados generados (`results/`)
- ❌ Todos los modelos entrenados (`models/`)
- ❌ Todos los datos procesados (`data/processed/`, `data/splits/`)
- ❌ Todo el cache de Python (`__pycache__`, `*.pyc`)
- ❌ Archivos temporales

**⚠️ SOLO USA ESTO SI:**
- Tienes problemas graves que no se solucionan de otra forma
- Quieres empezar completamente desde cero
- Estás seguro de que no necesitas ningún resultado actual

---

## 🎯 Casos de Uso

### Cuándo usar `reset-all`:

1. **Problemas de build que no se solucionan**
   ```
   Error: conflicting dependencies
   Error: cache corrupted
   ```

2. **Imágenes Docker corruptas**
   ```
   Error: layer does not exist
   Error: failed to extract layer
   ```

3. **Quieres empezar desde cero**
   ```
   Experimentaste mucho y quieres estado limpio
   ```

4. **Después de cambios mayores**
   ```
   Cambiaste requirements.txt significativamente
   Actualizaste versiones base de Python/librerías
   ```

5. **Espacio en disco lleno**
   ```
   Docker usa mucho espacio
   Quieres limpiar todo y empezar fresco
   ```

### Cuándo NO usar `reset-all`:

1. ❌ Tienes modelos entrenados que necesitas
2. ❌ Solo quieres limpiar resultados (usa `make clean-results`)
3. ❌ Solo quieres rebuild (usa `make build`)
4. ❌ Problemas menores que se pueden solucionar de otra forma

---

## 🚀 Uso

### Opción 1: Con Confirmación (RECOMENDADO)

```bash
make reset-all
```

Esto te pedirá confirmación:
```
⚠️  ═══════════════════════════════════════════════════════════════
⚠️  🔥 RESET COMPLETO DEL PROYECTO 🔥
⚠️  ═══════════════════════════════════════════════════════════════

Esto borrará y reinstalará TODO:
  ❌ Contenedores Docker (todos)
  ❌ Imágenes Docker del proyecto
  ...

⚠️  ADVERTENCIA: Esta operación NO se puede deshacer

¿Estás SEGURO de continuar? Escribe 'SI' para confirmar:
```

**Debes escribir exactamente `SI` (mayúsculas) para confirmar.**

### Opción 2: Sin Confirmación (PELIGROSO)

```bash
make reset-all-force
```

⚠️ **USA CON EXTREMO CUIDADO** - Ejecuta inmediatamente sin preguntar.

Solo úsalo en scripts automatizados donde estés 100% seguro.

---

## 📊 Proceso de Reset

El reset sigue estos 10 pasos:

```
[1/10] Deteniendo contenedores...
[2/10] Eliminando contenedores, volúmenes y redes...
[3/10] Eliminando imágenes del proyecto...
[4/10] Limpiando cache de Docker...
[5/10] Limpiando sistema Docker...
[6/10] Eliminando resultados generados...
[7/10] Eliminando datos procesados...
[8/10] Limpiando cache de Python...
[9/10] Construyendo imágenes desde cero (sin cache)...
[10/10] Iniciando servicios...
```

**Tiempo estimado:** 5-15 minutos (dependiendo de tu conexión y hardware)

---

## 🔍 Qué se Preserva

El reset **NO BORRA**:

✅ Código fuente (`src/`, `scripts/`)
✅ Datos raw originales (`data/raw/`)
✅ Documentación (`docs/`)
✅ Tests (`tests/`)
✅ Configuración (`.gitignore`, `requirements.txt`, etc.)
✅ Dataset original (`kddcup.data_10_percent`)

**Es decir, solo borra outputs generados y cache, NO tu código.**

---

## 📝 Después del Reset

Una vez completado el reset, verás:

```
════════════════════════════════════════════════════════════════════
✅ ¡RESET COMPLETO FINALIZADO!
════════════════════════════════════════════════════════════════════

📋 Estado:
  ✅ Todas las imágenes Docker reconstruidas desde cero
  ✅ Servicios iniciados y funcionando
  ✅ Sistema completamente limpio

🎯 Próximos pasos:
  1. Verifica servicios:  make ps
  2. Ver logs:            make logs
  3. Entrenar modelo:     make train
  4. Verificar API:       make api-health

📍 URLs:
  API:     http://localhost:8000/docs
  Jupyter: http://localhost:8888

💡 Tip: Ejecuta 'make train' para entrenar tu primer modelo
```

### Pasos recomendados post-reset:

```bash
# 1. Verificar que servicios están corriendo
make ps

# 2. Ver logs para asegurarte que todo está bien
make logs

# 3. Entrenar modelo
make train

# 4. Verificar API
make api-health
open http://localhost:8000/docs
```

---

## 🛠️ Alternativas Menos Destructivas

Antes de usar `reset-all`, considera estas alternativas:

### Limpiar solo resultados
```bash
make clean-results
```
Elimina solo `results/` y `models/`, mantiene Docker intacto.

### Limpiar solo Docker
```bash
make clean-docker
```
Elimina contenedores y volúmenes, pero no resultados locales.

### Rebuild sin cache
```bash
make down
docker-compose build --no-cache
make up
```
Reconstruye imágenes sin cache pero no borra todo.

### Restart servicios
```bash
make restart
```
Simplemente reinicia contenedores existentes.

---

## 🔧 Troubleshooting

### "Error: Cannot connect to Docker daemon"
```bash
# Asegúrate que Docker Desktop está corriendo
open -a Docker

# Espera a que inicie completamente
# Luego intenta de nuevo
make reset-all
```

### "Error: Permission denied"
```bash
# En Mac normalmente no necesitas sudo
# Pero si tienes problemas:
sudo make reset-all-force
```

### Reset se quedó a la mitad
```bash
# Si el reset falló a la mitad, puedes:

# 1. Limpiar manualmente Docker
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker system prune -af --volumes

# 2. Intentar reset de nuevo
make reset-all-force
```

### Servicios no inician después del reset
```bash
# Ver qué pasó
make logs

# Verificar que puertos no estén en uso
lsof -i :8000
lsof -i :8888

# Si hay conflicto, matar procesos
kill -9 <PID>

# Reintentar
make down
make up
```

---

## 💾 Backup Antes del Reset

Si tienes resultados importantes, guárdalos antes:

```bash
# Backup de resultados
tar -czf backup_results_$(date +%Y%m%d_%H%M%S).tar.gz results/ models/

# Backup de datos procesados
tar -czf backup_data_$(date +%Y%m%d_%H%M%S).tar.gz data/processed/ data/splits/

# Ahora sí, reset
make reset-all
```

Restaurar después:
```bash
tar -xzf backup_results_XXXXXX.tar.gz
```

---

## 📊 Comparación de Comandos

| Comando | Borra Contenedores | Borra Imágenes | Borra Cache | Borra Resultados | Rebuild | Tiempo |
|---------|-------------------|----------------|-------------|------------------|---------|---------|
| `make down` | ✅ | ❌ | ❌ | ❌ | ❌ | 5s |
| `make restart` | ❌ | ❌ | ❌ | ❌ | ❌ | 10s |
| `make clean-docker` | ✅ | ❌ | ✅ | ❌ | ❌ | 30s |
| `make clean-results` | ❌ | ❌ | ❌ | ✅ | ❌ | 5s |
| `make build` | ❌ | ❌ | ❌ | ❌ | ✅ | 2-5min |
| **`make reset-all`** | ✅ | ✅ | ✅ | ✅ | ✅ | 5-15min |

---

## 🎯 Checklist Pre-Reset

Antes de ejecutar `make reset-all`, verifica:

- [ ] ¿Guardé backup de resultados importantes?
- [ ] ¿Guardé backup de modelos entrenados importantes?
- [ ] ¿Estoy seguro que quiero borrar TODO?
- [ ] ¿Intenté alternativas menos destructivas?
- [ ] ¿Tengo tiempo para esperar 5-15 minutos?
- [ ] ¿Docker Desktop está corriendo?
- [ ] ¿Tengo espacio en disco suficiente? (mínimo 5GB)

Si respondiste SÍ a todo, adelante con el reset.

---

## 📚 Ver También

- **make help** - Todos los comandos disponibles
- **DOCKER_WORKFLOW.md** - Workflows normales de desarrollo
- **QUICK_REFERENCE.md** - Comandos rápidos
- **TROUBLESHOOTING.md** - Guía de solución de problemas

---

## 🆘 Soporte

Si tienes problemas con el reset:

1. Lee esta guía completa
2. Revisa los logs: `make logs`
3. Verifica Docker: `docker ps`, `docker images`
4. Intenta alternativas menos destructivas primero
5. Si nada funciona, usa `reset-all-force` y cruza dedos 🤞

---

**⚠️ Recuerda: `make reset-all` es tu último recurso, no tu primera opción.**
