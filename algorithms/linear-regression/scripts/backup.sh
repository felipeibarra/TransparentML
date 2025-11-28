#!/bin/bash
###############################################################################
# Script de Backup Automático - Tarea 1 ML
# 
# Este script crea backups de:
#   - Datos procesados
#   - Resultados y métricas
#   - Modelos entrenados
#   - Código fuente
#
# Uso: ./scripts/backup.sh
###############################################################################

set -e  # Exit on error

# Configuración
BACKUP_BASE_DIR="$HOME/backups/ml_tarea1"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_BASE_DIR/$DATE"
PROJECT_DIR=$(cd "$(dirname "$0")/.." && pwd)

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   BACKUP AUTOMÁTICO - TAREA 1 REGRESIÓN LINEAL${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo ""

# Crear directorio de backup
echo -e "${YELLOW}📁 Creando directorio de backup...${NC}"
mkdir -p "$BACKUP_DIR"
echo -e "${GREEN}✓${NC} Directorio creado: $BACKUP_DIR"
echo ""

# Backup de código fuente
echo -e "${YELLOW}📦 Backing up código fuente...${NC}"
cd "$PROJECT_DIR"
tar czf "$BACKUP_DIR/source_code.tar.gz" \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    src/ scripts/ *.py *.md *.txt Dockerfile docker-compose.yml 2>/dev/null || true
echo -e "${GREEN}✓${NC} Código fuente respaldado"

# Backup de datos
echo -e "${YELLOW}💾 Backing up datos...${NC}"
if [ -d "$PROJECT_DIR/data" ] && [ "$(ls -A $PROJECT_DIR/data 2>/dev/null)" ]; then
    tar czf "$BACKUP_DIR/data.tar.gz" -C "$PROJECT_DIR" data/
    echo -e "${GREEN}✓${NC} Datos respaldados"
else
    echo -e "${YELLOW}⚠${NC}  No hay datos para respaldar"
fi

# Backup de resultados
echo -e "${YELLOW}📊 Backing up resultados...${NC}"
if [ -d "$PROJECT_DIR/results" ] && [ "$(ls -A $PROJECT_DIR/results 2>/dev/null)" ]; then
    tar czf "$BACKUP_DIR/results.tar.gz" -C "$PROJECT_DIR" results/
    echo -e "${GREEN}✓${NC} Resultados respaldados"
else
    echo -e "${YELLOW}⚠${NC}  No hay resultados para respaldar"
fi

# Backup de modelos (extra)
echo -e "${YELLOW}🤖 Backing up modelos...${NC}"
if [ -d "$PROJECT_DIR/results/models" ] && [ "$(ls -A $PROJECT_DIR/results/models 2>/dev/null)" ]; then
    tar czf "$BACKUP_DIR/models.tar.gz" -C "$PROJECT_DIR/results" models/
    echo -e "${GREEN}✓${NC} Modelos respaldados"
else
    echo -e "${YELLOW}⚠${NC}  No hay modelos para respaldar"
fi

# Backup de notebooks (si existen)
echo -e "${YELLOW}📓 Backing up notebooks...${NC}"
if [ -d "$PROJECT_DIR/notebooks" ] && [ "$(ls -A $PROJECT_DIR/notebooks 2>/dev/null)" ]; then
    tar czf "$BACKUP_DIR/notebooks.tar.gz" -C "$PROJECT_DIR" notebooks/
    echo -e "${GREEN}✓${NC} Notebooks respaldados"
else
    echo -e "${YELLOW}⚠${NC}  No hay notebooks para respaldar"
fi

# Crear metadata del backup
echo -e "${YELLOW}📝 Creando metadata...${NC}"
cat > "$BACKUP_DIR/backup_info.txt" << EOF
Backup Information
==================
Date: $(date)
Project: Tarea 1 - Regresión Lineal
Author: Felipe Ibarra
Hostname: $(hostname)
User: $(whoami)
Project Path: $PROJECT_DIR
Backup Path: $BACKUP_DIR

Contents:
---------
EOF

# Listar archivos y tamaños
ls -lh "$BACKUP_DIR" | tail -n +2 >> "$BACKUP_DIR/backup_info.txt"

echo -e "${GREEN}✓${NC} Metadata creada"
echo ""

# Resumen
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   BACKUP COMPLETADO EXITOSAMENTE${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "📍 Ubicación: ${GREEN}$BACKUP_DIR${NC}"
echo ""
echo -e "📦 Archivos creados:"
ls -lh "$BACKUP_DIR" | tail -n +2 | awk '{print "   -", $9, "("$5")"}'
echo ""

# Calcular tamaño total
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | awk '{print $1}')
echo -e "💾 Tamaño total: ${GREEN}$TOTAL_SIZE${NC}"
echo ""

# Limpieza de backups antiguos (mantener últimos 5)
echo -e "${YELLOW}🧹 Limpiando backups antiguos...${NC}"
cd "$BACKUP_BASE_DIR"
BACKUP_COUNT=$(ls -1 | wc -l)
if [ $BACKUP_COUNT -gt 5 ]; then
    ls -1t | tail -n +6 | xargs -I {} rm -rf {}
    DELETED=$((BACKUP_COUNT - 5))
    echo -e "${GREEN}✓${NC} Eliminados $DELETED backups antiguos (manteniendo últimos 5)"
else
    echo -e "${GREEN}✓${NC} No hay backups antiguos para eliminar"
fi
echo ""

echo -e "${GREEN}✅ Proceso completado${NC}"
echo ""
