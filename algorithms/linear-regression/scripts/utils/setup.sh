#!/bin/bash
###############################################################################
# Script de Setup Automático - Tarea 1 Regresión Lineal
# 
# Este script configura el entorno completo del proyecto:
#   - Verifica prerequisitos
#   - Crea entorno virtual Python
#   - Instala dependencias
#   - Configura estructura de directorios
#   - Ejecuta entrenamiento inicial
#   - Limpieza completa del proyecto
#
# Uso: 
#   ./setup.sh                    # Setup completo con entrenamiento
#   ./setup.sh --skip-training    # Setup sin entrenamiento
#   ./setup.sh --clean            # Limpieza completa del proyecto
#   ./setup.sh --clean --force    # Limpieza sin confirmación
###############################################################################

set -e  # Exit on error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Variables
PROJECT_DIR=$(cd "$(dirname "$0")" && pwd)
SKIP_TRAINING=false
CLEAN_MODE=false
FORCE_CLEAN=false

# Parsear argumentos
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --skip-training) SKIP_TRAINING=true ;;
        --clean) CLEAN_MODE=true ;;
        --force) FORCE_CLEAN=true ;;
        --help) 
            echo "Uso: ./setup.sh [opciones]"
            echo ""
            echo "Opciones:"
            echo "  (sin opciones)      Setup completo con entrenamiento"
            echo "  --skip-training     Setup sin ejecutar entrenamiento"
            echo "  --clean             Limpieza completa del proyecto"
            echo "  --force             Limpieza sin confirmación (úsalo con --clean)"
            echo "  --help              Mostrar esta ayuda"
            echo ""
            echo "Ejemplos:"
            echo "  ./setup.sh                    # Setup normal"
            echo "  ./setup.sh --skip-training    # Setup rápido"
            echo "  ./setup.sh --clean            # Limpiar todo"
            echo "  ./setup.sh --clean --force    # Limpiar sin preguntar"
            exit 0
            ;;
        *) echo "Unknown parameter: $1. Use --help for usage."; exit 1 ;;
    esac
    shift
done

# Banner
clear
echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}   SETUP AUTOMÁTICO - TAREA 1 REGRESIÓN LINEAL${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Proyecto:${NC} Análisis de Regresión Lineal con KDD Cup 1999"
echo -e "${BLUE}Autor:${NC}    Felipe Ibarra"
echo -e "${BLUE}Directorio:${NC} $PROJECT_DIR"
echo ""

# Función para imprimir pasos
print_step() {
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}▶ $1${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Función para imprimir éxito
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Función para imprimir error
print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Función para imprimir warning
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Cambiar al directorio del proyecto
cd "$PROJECT_DIR"

###############################################################################
# MODO LIMPIEZA COMPLETA
###############################################################################
if [ "$CLEAN_MODE" = true ]; then
    clear
    echo -e "${RED}████████████████████████████████████████████████████${NC}"
    echo -e "${RED}   LIMPIEZA COMPLETA DEL PROYECTO${NC}"
    echo -e "${RED}████████████████████████████████████████████████████${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  ADVERTENCIA: Esta acción eliminará:${NC}"
    echo ""
    echo -e "  ${RED}✗${NC} Entorno virtual (venv/)"   
    echo -e "  ${RED}✗${NC} Resultados generados (results/)"   
    echo -e "  ${RED}✗${NC} Archivos Python compilados (__pycache__, *.pyc)"   
    echo -e "  ${RED}✗${NC} Archivos temporales (.DS_Store, *.log)"   
    echo -e "  ${RED}✗${NC} Script de activación (activate.sh)"   
    echo -e "  ${RED}✗${NC} Imágenes y volúmenes de Docker (opcional)"   
    echo ""
    echo -e "  ${GREEN}✓${NC} Se preservará:"   
    echo -e "    - Código fuente (src/, scripts/)"   
    echo -e "    - Dataset (kddcup.data_10_percent)"   
    echo -e "    - Documentación (*.md, docs/)"   
    echo -e "    - Configuración (requirements.txt, Dockerfile, etc.)"   
    echo ""
    
    if [ "$FORCE_CLEAN" = false ]; then
        read -p "¿Estás SEGURO de que deseas continuar? (escribe 'SI' para confirmar): " -r
        echo ""
        if [[ ! $REPLY == "SI" ]]; then
            echo -e "${YELLOW}Limpieza cancelada.${NC}"
            exit 0
        fi
    fi
    
    echo -e "${MAGENTA}Iniciando limpieza completa...${NC}"
    echo ""
    
    # 1. Eliminar entorno virtual
    if [ -d "venv" ]; then
        echo -e "${YELLOW}🗑️  Eliminando entorno virtual...${NC}"
        rm -rf venv
        print_success "Entorno virtual eliminado"
    fi
    
    # 2. Eliminar resultados
    if [ -d "results" ]; then
        echo -e "${YELLOW}🗑️  Eliminando resultados...${NC}"
        rm -rf results/figures/* results/metrics/* results/models/* 2>/dev/null || true
        print_success "Resultados eliminados"
    fi
    
    # 3. Eliminar archivos compilados de Python
    echo -e "${YELLOW}🗑️  Limpiando archivos Python compilados...${NC}"
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    print_success "Archivos Python compilados eliminados"
    
    # 4. Eliminar archivos temporales
    echo -e "${YELLOW}🗑️  Limpiando archivos temporales...${NC}"
    find . -name ".DS_Store" -delete 2>/dev/null || true
    find . -name "*.log" -delete 2>/dev/null || true
    find . -name "*.tmp" -delete 2>/dev/null || true
    find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
    print_success "Archivos temporales eliminados"
    
    # 5. Eliminar script de activación
    if [ -f "activate.sh" ]; then
        rm -f activate.sh
        print_success "Script de activación eliminado"
    fi
    
    # 6. Limpiar Docker (opcional)
    if command -v docker &> /dev/null; then
        echo ""
        read -p "¿Deseas limpiar imágenes y volúmenes de Docker? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}🐳 Limpiando Docker...${NC}"
            
            # Detener contenedores
            docker-compose down 2>/dev/null || true
            print_success "Contenedores detenidos"
            
            # Eliminar volúmenes
            docker-compose down -v 2>/dev/null || true
            print_success "Volúmenes eliminados"
            
            # Eliminar imágenes del proyecto
            docker images | grep tarea1 | awk '{print $3}' | xargs docker rmi -f 2>/dev/null || true
            print_success "Imágenes eliminadas"
            
            # Limpiar sistema Docker (opcional)
            read -p "¿Limpiar imágenes huérfanas de Docker? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                docker image prune -f 2>/dev/null || true
                docker volume prune -f 2>/dev/null || true
                print_success "Sistema Docker limpio"
            fi
        fi
    fi
    
    echo ""
    echo -e "${GREEN}████████████████████████████████████████████████████${NC}"
    echo -e "${GREEN}   LIMPIEZA COMPLETADA EXITOSAMENTE${NC}"
    echo -e "${GREEN}████████████████████████████████████████████████████${NC}"
    echo ""
    echo -e "${CYAN}✅ Proyecto limpio y listo para nuevo setup${NC}"
    echo ""
    echo "Para reinstalar el proyecto, ejecuta:"
    echo -e "  ${CYAN}./setup.sh${NC}"
    echo ""
    
    # Mostrar espacio liberado
    echo -e "${BLUE}📊 Espacio en disco:${NC}"
    du -sh . 2>/dev/null || true
    echo ""
    
    exit 0
fi

###############################################################################
# PASO 1: Verificar Prerequisitos
###############################################################################
print_step "PASO 1: Verificando prerequisitos"

# Verificar macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "Este script está diseñado para macOS"
    exit 1
fi
print_success "Sistema operativo: macOS"

# Verificar Python 3
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado"
    echo ""
    echo "Instala Python 3:"
    echo "  brew install python3"
    echo "  O descarga desde: https://www.python.org/downloads/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
print_success "Python $PYTHON_VERSION instalado"

# Verificar pip
if ! python3 -m pip --version &> /dev/null; then
    print_error "pip no está instalado"
    exit 1
fi
print_success "pip instalado"

# Verificar Docker (opcional)
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    print_success "Docker $DOCKER_VERSION instalado (opcional)"
    DOCKER_AVAILABLE=true
else
    print_warning "Docker no está instalado (opcional)"
    DOCKER_AVAILABLE=false
fi

# Verificar docker-compose (opcional)
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version | awk '{print $4}' | sed 's/,//')
    print_success "Docker Compose $COMPOSE_VERSION instalado (opcional)"
else
    print_warning "Docker Compose no está instalado (opcional)"
fi

echo ""

###############################################################################
# PASO 2: Crear estructura de directorios
###############################################################################
print_step "PASO 2: Creando estructura de directorios"

mkdir -p data/{raw,processed,splits}
mkdir -p notebooks
mkdir -p results/{figures,metrics,models}
mkdir -p tests
mkdir -p docs

print_success "Directorios creados:"
echo "   - data/{raw,processed,splits}"
echo "   - notebooks/"
echo "   - results/{figures,metrics,models}"
echo "   - tests/"
echo "   - docs/"
echo ""

###############################################################################
# PASO 3: Verificar dataset
###############################################################################
print_step "PASO 3: Verificando dataset KDD Cup"

if [ -f "kddcup.data_10_percent" ]; then
    FILE_SIZE=$(du -h kddcup.data_10_percent | awk '{print $1}')
    print_success "Dataset encontrado (${FILE_SIZE})"
else
    print_warning "Dataset KDD Cup no encontrado"
    echo ""
    echo "Por favor, descarga el dataset desde:"
    echo "  http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html"
    echo ""
    echo "Archivo necesario: kddcup.data_10_percent.gz"
    echo "Comando para descomprimir:"
    echo "  gunzip kddcup.data_10_percent.gz"
    echo ""
    read -p "¿Deseas continuar sin el dataset? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo ""

###############################################################################
# PASO 4: Configurar entorno virtual Python
###############################################################################
print_step "PASO 4: Configurando entorno virtual Python"

if [ -d "venv" ]; then
    print_warning "Entorno virtual ya existe"
    read -p "¿Deseas recrearlo? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Eliminando entorno virtual anterior..."
        rm -rf venv
        print_success "Entorno anterior eliminado"
    fi
fi

if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate
print_success "Entorno virtual activado"
echo ""

###############################################################################
# PASO 5: Actualizar pip
###############################################################################
print_step "PASO 5: Actualizando pip"

echo "Actualizando pip a la última versión..."
pip install --upgrade pip -q
PIP_VERSION=$(pip --version | awk '{print $2}')
print_success "pip actualizado a versión $PIP_VERSION"
echo ""

###############################################################################
# PASO 6: Instalar dependencias
###############################################################################
print_step "PASO 6: Instalando dependencias Python"

if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt no encontrado"
    exit 1
fi

echo "Instalando dependencias (esto puede tomar unos minutos)..."
echo ""
pip install -r requirements.txt

print_success "Dependencias instaladas exitosamente"
echo ""

# Verificar instalaciones clave
echo "Verificando instalaciones clave:"
python3 -c "import numpy; print('  ✓ numpy', numpy.__version__)"
python3 -c "import pandas; print('  ✓ pandas', pandas.__version__)"
python3 -c "import sklearn; print('  ✓ scikit-learn', sklearn.__version__)"
python3 -c "import matplotlib; print('  ✓ matplotlib', matplotlib.__version__)"
echo ""

###############################################################################
# PASO 7: Hacer scripts ejecutables
###############################################################################
print_step "PASO 7: Configurando permisos de scripts"

chmod +x scripts/train.py
chmod +x scripts/backup.sh
chmod +x setup.sh

print_success "Permisos configurados:"
echo "   - scripts/train.py"
echo "   - scripts/backup.sh"
echo "   - setup.sh"
echo ""

###############################################################################
# PASO 8: Configurar Docker (opcional)
###############################################################################
if [ "$DOCKER_AVAILABLE" = true ]; then
    print_step "PASO 8: Configurando Docker (opcional)"
    
    read -p "¿Deseas construir la imagen Docker? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Construyendo imagen Docker..."
        docker-compose build
        print_success "Imagen Docker construida"
    else
        print_warning "Construcción de Docker omitida"
    fi
    echo ""
else
    print_warning "PASO 8: Docker no disponible (omitido)"
    echo ""
fi

###############################################################################
# PASO 9: Ejecutar entrenamiento de prueba
###############################################################################
if [ "$SKIP_TRAINING" = false ]; then
    print_step "PASO 9: Ejecutando entrenamiento de prueba"
    
    if [ -f "kddcup.data_10_percent" ]; then
        echo "Iniciando entrenamiento de modelos..."
        echo "Esto tomará aproximadamente 30-60 segundos..."
        echo ""
        
        python scripts/train.py
        
        print_success "Entrenamiento completado"
        echo ""
        
        # Mostrar resultados
        if [ -f "results/metrics/model_comparison.csv" ]; then
            echo "Resultados de modelos:"
            cat results/metrics/model_comparison.csv
            echo ""
        fi
    else
        print_warning "Dataset no disponible, entrenamiento omitido"
        echo ""
    fi
else
    print_warning "PASO 9: Entrenamiento omitido (--skip-training)"
    echo ""
fi

###############################################################################
# PASO 10: Generar PDF de entrega
###############################################################################
print_step "PASO 10: Generar PDF de entrega"

# Verificar si existe ENTREGA_FINAL.md
if [ -f "ENTREGA_FINAL.md" ]; then
    echo "Documento de entrega encontrado: ENTREGA_FINAL.md"
    
    # Verificar si pandoc está instalado
    if command -v pandoc &> /dev/null; then
        print_success "pandoc está instalado"
        
        read -p "¿Deseas generar el PDF de entrega? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Generando PDF: ENTREGA_TAREA1.pdf..."
            
            # Intentar con xelatex si está disponible
            if command -v xelatex &> /dev/null; then
                pandoc ENTREGA_FINAL.md -o ENTREGA_TAREA1.pdf \
                  --pdf-engine=xelatex \
                  --toc \
                  -V geometry:margin=1in
            else
                print_warning "xelatex no disponible, usando motor por defecto"
                pandoc ENTREGA_FINAL.md -o ENTREGA_TAREA1.pdf \
                  --toc \
                  -V geometry:margin=1in
            fi
            
            if [ $? -eq 0 ] && [ -f "ENTREGA_TAREA1.pdf" ]; then
                file_size=$(du -h ENTREGA_TAREA1.pdf | cut -f1)
                print_success "PDF generado exitosamente: ENTREGA_TAREA1.pdf ($file_size)"
                
                read -p "¿Deseas abrir el PDF? (y/n) " -n 1 -r
                echo ""
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    open ENTREGA_TAREA1.pdf
                fi
            else
                print_error "Error al generar PDF"
            fi
        else
            print_warning "Generación de PDF omitida"
        fi
    else
        print_warning "pandoc no está instalado (opcional)"
        echo "Para instalar: brew install pandoc"
    fi
else
    print_warning "ENTREGA_FINAL.md no encontrado"
fi

echo ""

###############################################################################
# PASO 11: Resumen final
###############################################################################
print_step "PASO 11: Resumen de instalación"

echo -e "${GREEN}✅ Setup completado exitosamente!${NC}"
echo ""
echo "📁 Estructura del proyecto:"
tree -L 2 -I 'venv|__pycache__|*.pyc' . 2>/dev/null || ls -R . | head -30
echo ""

echo "🚀 Próximos pasos:"
echo ""
echo "1. Activar entorno virtual:"
echo "   ${CYAN}source venv/bin/activate${NC}"
echo ""
echo "2. Ejecutar entrenamiento:"
echo "   ${CYAN}python scripts/train.py${NC}"
echo ""
echo "3. Ver resultados:"
echo "   ${CYAN}cat results/metrics/model_comparison.csv${NC}"
echo "   ${CYAN}open results/figures/${NC}"
echo ""

if [ "$DOCKER_AVAILABLE" = true ]; then
    echo "4. Usar Docker (opcional):"
    echo "   ${CYAN}docker-compose run --rm ml-task python scripts/train.py${NC}"
    echo "   ${CYAN}docker-compose up jupyter${NC} (http://localhost:8888)"
    echo ""
fi

echo "5. Crear backup:"
echo "   ${CYAN}./scripts/backup.sh${NC}"
echo ""

echo "📚 Documentación:"
echo "   - README.MD           - Documentación principal"
echo "   - RESULTADOS.md       - Análisis de resultados"
echo "   - ENTREGA_FINAL.md    - Resumen ejecutivo"
echo "   - docs/ARQUITECTURA.txt - Arquitectura del sistema"
echo "   - docs/DOCKER_GUIDE.md  - Guía de Docker"
echo ""

echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   ¡Proyecto listo para usar! 🎉${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
echo ""

# Crear archivo de activación rápida
cat > activate.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
echo "✓ Entorno virtual activado"
echo "Ejecuta: python scripts/train.py"
EOF
chmod +x activate.sh

print_success "Script de activación rápida creado: ./activate.sh"
echo ""
