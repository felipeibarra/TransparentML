#!/bin/bash

# Script para migrar mejoras de TAREA_1 a TAREA_2
# Adapta configuraciones para PCA en lugar de Regresión Lineal

set -e

TAREA1="/Users/felipeibarra_m2_max/MASTER-IA-CS/master-ai-cs/MODULO2-MACHINE-LEARNING/TAREA_1"
TAREA2="/Users/felipeibarra_m2_max/MASTER-IA-CS/master-ai-cs/MODULO2-MACHINE-LEARNING/TAREA_2"

echo "🔄 Migrando mejoras de TAREA_1 a TAREA_2..."
echo ""

# 1. Copiar Makefile y adaptarlo
echo "[1/5] Copiando Makefile..."
cp "$TAREA1/Makefile" "$TAREA2/Makefile"
# Adaptar nombres de servicios
sed -i '' 's/training-service/pca-analysis/g' "$TAREA2/Makefile"
sed -i '' 's/prediction-api/pca-api/g' "$TAREA2/Makefile"
sed -i '' 's/Regresión Lineal/PCA/g' "$TAREA2/Makefile"
sed -i '' 's/tarea_1/tarea_2/g' "$TAREA2/Makefile"
echo "✅ Makefile adaptado"

# 2. Copiar QUICK_REFERENCE.md
echo "[2/5] Copiando QUICK_REFERENCE.md..."
cp "$TAREA1/QUICK_REFERENCE.md" "$TAREA2/QUICK_REFERENCE.md"
sed -i '' 's/Regresión Lineal/PCA - Reducción de Dimensionalidad/g' "$TAREA2/QUICK_REFERENCE.md"
sed -i '' 's/training-service/pca-analysis/g' "$TAREA2/QUICK_REFERENCE.md"
sed -i '' 's/shell-training/shell-pca/g' "$TAREA2/QUICK_REFERENCE.md"
echo "✅ QUICK_REFERENCE.md adaptado"

# 3. Copiar PROJECT_ORGANIZATION.md
echo "[3/5] Copiando PROJECT_ORGANIZATION.md..."
cp "$TAREA1/PROJECT_ORGANIZATION.md" "$TAREA2/PROJECT_ORGANIZATION.md"
sed -i '' 's/Regresión Lineal/PCA/g' "$TAREA2/PROJECT_ORGANIZATION.md"
sed -i '' 's/training-service/pca-analysis/g' "$TAREA2/PROJECT_ORGANIZATION.md"
sed -i '' 's/prediction-api/pca-api/g' "$TAREA2/PROJECT_ORGANIZATION.md"
sed -i '' 's/KDD Cup 1999/Iris Dataset/g' "$TAREA2/PROJECT_ORGANIZATION.md"
sed -i '' 's/kddcup.data_10_percent/iris.csv/g' "$TAREA2/PROJECT_ORGANIZATION.md"
echo "✅ PROJECT_ORGANIZATION.md adaptado"

# 4. Copiar guías de Docker
echo "[4/5] Copiando guías de Docker..."
cp "$TAREA1/docs/guides/DOCKER_WORKFLOW.md" "$TAREA2/docs/guides/"
cp "$TAREA1/docs/guides/CONTAINER_SETUP.md" "$TAREA2/docs/guides/"
cp "$TAREA1/docs/guides/ARCHITECTURE.md" "$TAREA2/docs/guides/"
cp "$TAREA1/docs/guides/RESET_GUIDE.md" "$TAREA2/docs/guides/"

# Adaptar contenido
for file in "$TAREA2/docs/guides"/*.md; do
    sed -i '' 's/Regresión Lineal/PCA/g' "$file"
    sed -i '' 's/training-service/pca-analysis/g' "$file"
    sed -i '' 's/prediction-api/pca-api/g' "$file"
    sed -i '' 's/tarea_1/tarea_2/g' "$file"
    sed -i '' 's/TAREA_1/TAREA_2/g' "$file"
done
echo "✅ Guías adaptadas"

# 5. Copiar READMEs de carpetas (si no existen)
echo "[5/5] Copiando READMEs de carpetas..."

# data/README.md
if [ ! -f "$TAREA2/data/README.md" ]; then
    cp "$TAREA1/data/README.md" "$TAREA2/data/README.md"
    sed -i '' 's/KDD Cup 1999/Iris Dataset/g' "$TAREA2/data/README.md"
    sed -i '' 's/~494,021 registros/150 registros/g' "$TAREA2/data/README.md"
    sed -i '' 's/41 variables/4 features/g' "$TAREA2/data/README.md"
fi

# results/README.md
if [ ! -f "$TAREA2/results/README.md" ]; then
    cp "$TAREA1/results/README.md" "$TAREA2/results/README.md"
    sed -i '' 's/Regresión/PCA/g' "$TAREA2/results/README.md"
fi

# notebooks/README.md
if [ ! -f "$TAREA2/notebooks/README.md" ]; then
    cp "$TAREA1/notebooks/README.md" "$TAREA2/notebooks/README.md"
fi

# tests/README.md
if [ ! -f "$TAREA2/tests/README.md" ]; then
    cp "$TAREA1/tests/README.md" "$TAREA2/tests/README.md"
    sed -i '' 's/training-service/pca-analysis/g' "$TAREA2/tests/README.md"
fi

echo "✅ READMEs copiados"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ ¡Migración completada!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📝 Archivos migrados:"
echo "  ✅ Makefile (con reset-all)"
echo "  ✅ QUICK_REFERENCE.md"
echo "  ✅ PROJECT_ORGANIZATION.md"
echo "  ✅ docs/guides/ (4 guías)"
echo "  ✅ READMEs de carpetas"
echo ""
echo "🎯 Siguiente paso:"
echo "  1. Revisar Makefile y adaptarlo si es necesario"
echo "  2. Crear docker-compose.yml (ver ejemplo en TAREA_1)"
echo "  3. Crear Dockerfiles para cada servicio"
echo "  4. Actualizar README.md principal"
echo ""
echo "💡 Para empezar:"
echo "  cd $TAREA2"
echo "  cat QUICK_REFERENCE.md"
echo ""
