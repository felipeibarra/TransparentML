#!/bin/bash

# Script de limpieza del proyecto
# Limpia archivos temporales, caches, y artefactos antiguos

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "════════════════════════════════════════════════════════"
echo "   LIMPIEZA DEL PROYECTO - TAREA 1 ML"
echo "════════════════════════════════════════════════════════"
echo -e "${NC}\n"

# Función de confirmación
confirm() {
    read -p "$1 (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    fi
    return 1
}

# Contador de archivos eliminados
deleted_count=0

echo -e "${YELLOW}Opciones de limpieza:${NC}"
echo "1) Limpieza básica (caches, __pycache__)"
echo "2) Limpieza de resultados antiguos (mantener últimos 5)"
echo "3) Limpieza de modelos antiguos (mantener últimos 3)"
echo "4) Limpieza completa (TODO excepto raw data)"
echo "5) Limpieza de Docker (contenedores e imágenes)"
echo "6) Limpieza del venv local"
echo "7) Generar PDF de entrega (ENTREGA_FINAL.md -> ENTREGA_TAREA1.pdf)"
echo ""
read -p "Selecciona opción [1-7]: " option

case $option in
    1)
        echo -e "\n${YELLOW}🧹 Limpieza básica...${NC}\n"
        
        # Python caches
        echo "Eliminando __pycache__..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete
        find . -type f -name "*.pyo" -delete
        find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
        
        # pytest cache
        echo "Eliminando .pytest_cache..."
        find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
        
        # mypy cache
        echo "Eliminando .mypy_cache..."
        find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
        
        # Jupyter checkpoints
        echo "Eliminando .ipynb_checkpoints..."
        find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
        
        # macOS
        echo "Eliminando .DS_Store..."
        find . -name ".DS_Store" -delete 2>/dev/null || true
        
        echo -e "${GREEN}✓ Limpieza básica completada${NC}"
        ;;
    
    2)
        echo -e "\n${YELLOW}🧹 Limpiando resultados antiguos...${NC}\n"
        
        # Mantener últimos 5 archivos de métricas
        if [ -d "results/metrics" ]; then
            cd results/metrics
            ls -t *.json 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true
            cd ../..
            echo "✓ Métricas antiguas eliminadas (manteniendo últimas 5)"
        fi
        
        # Mantener últimas 5 figuras
        if [ -d "results/figures" ]; then
            cd results/figures
            ls -t *.png 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true
            cd ../..
            echo "✓ Figuras antiguas eliminadas (manteniendo últimas 5)"
        fi
        
        echo -e "${GREEN}✓ Resultados antiguos limpiados${NC}"
        ;;
    
    3)
        echo -e "\n${YELLOW}🧹 Limpiando modelos antiguos...${NC}\n"
        
        if [ -d "models" ]; then
            cd models
            ls -t *.joblib 2>/dev/null | tail -n +4 | xargs rm -f 2>/dev/null || true
            cd ..
            echo "✓ Modelos antiguos eliminados (manteniendo últimos 3)"
        fi
        
        echo -e "${GREEN}✓ Modelos antiguos limpiados${NC}"
        ;;
    
    4)
        if confirm "${RED}⚠️  LIMPIEZA COMPLETA - Esto eliminará todos los resultados, modelos procesados y caches. ¿Continuar?${NC}"; then
            echo -e "\n${YELLOW}🧹 Limpieza completa...${NC}\n"
            
            # Limpieza básica
            find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
            find . -type f -name "*.pyc" -delete
            find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
            find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
            find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
            find . -name ".DS_Store" -delete 2>/dev/null || true
            
            # Limpiar processed data (mantener raw)
            rm -rf data/processed/* 2>/dev/null || true
            rm -rf data/splits/* 2>/dev/null || true
            echo "✓ Datos procesados eliminados"
            
            # Limpiar todos los resultados
            rm -rf results/figures/* 2>/dev/null || true
            rm -rf results/metrics/* 2>/dev/null || true
            echo "✓ Resultados eliminados"
            
            # Limpiar todos los modelos
            rm -rf models/*.joblib 2>/dev/null || true
            echo "✓ Modelos eliminados"
            
            echo -e "${GREEN}✓ Limpieza completa terminada${NC}"
        else
            echo -e "${YELLOW}Limpieza cancelada${NC}"
        fi
        ;;
    
    5)
        echo -e "\n${YELLOW}🐳 Limpieza de Docker...${NC}\n"
        
        if confirm "¿Detener y eliminar todos los contenedores del proyecto?"; then
            docker-compose down 2>/dev/null || true
            echo "✓ Contenedores detenidos"
        fi
        
        if confirm "¿Eliminar imágenes del proyecto?"; then
            docker-compose down --rmi all 2>/dev/null || true
            echo "✓ Imágenes eliminadas"
        fi
        
        if confirm "¿Eliminar volúmenes (BORRA DATOS PERSISTENTES)?"; then
            docker-compose down -v 2>/dev/null || true
            echo "✓ Volúmenes eliminados"
        fi
        
        if confirm "¿Ejecutar limpieza general de Docker (system prune)?"; then
            docker system prune -f
            echo "✓ Sistema Docker limpiado"
        fi
        
        echo -e "${GREEN}✓ Limpieza de Docker completada${NC}"
        ;;
    
    6)
        if confirm "${RED}⚠️  Esto eliminará el entorno virtual local (venv/). ¿Continuar?${NC}"; then
            echo -e "\n${YELLOW}🧹 Eliminando venv...${NC}\n"
            
            if [ -d "venv" ]; then
                rm -rf venv
                echo "✓ Entorno virtual eliminado"
            else
                echo "ℹ No se encontró venv/"
            fi
            
            echo -e "${GREEN}✓ venv limpiado${NC}"
        else
            echo -e "${YELLOW}Limpieza cancelada${NC}"
        fi
        ;;
    
    7)
        echo -e "\n${YELLOW}📄 Generando PDF de entrega...${NC}\n"
        
        # Verificar que existe ENTREGA_FINAL.md
        if [ ! -f "ENTREGA_FINAL.md" ]; then
            echo -e "${RED}✗ Error: No se encontró ENTREGA_FINAL.md${NC}"
            exit 1
        fi
        
        # Verificar que pandoc está instalado
        if ! command -v pandoc &> /dev/null; then
            echo -e "${RED}✗ Error: pandoc no está instalado${NC}"
            echo -e "${YELLOW}Instalar con: brew install pandoc${NC}"
            exit 1
        fi
        
        # Verificar que xelatex está disponible
        if ! command -v xelatex &> /dev/null; then
            echo -e "${YELLOW}⚠️  Advertencia: xelatex no está instalado${NC}"
            echo -e "${YELLOW}Instalar con: brew install --cask mactex${NC}"
            echo -e "${YELLOW}Intentando con motor PDF por defecto...${NC}\n"
            
            # Intentar sin especificar motor
            pandoc ENTREGA_FINAL.md -o ENTREGA_TAREA1.pdf --toc -V geometry:margin=1in
        else
            # Generar PDF con xelatex
            pandoc ENTREGA_FINAL.md -o ENTREGA_TAREA1.pdf \
              --pdf-engine=xelatex \
              --toc \
              -V geometry:margin=1in
        fi
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ PDF generado exitosamente: ENTREGA_TAREA1.pdf${NC}"
            
            # Mostrar información del archivo
            if [ -f "ENTREGA_TAREA1.pdf" ]; then
                file_size=$(du -h ENTREGA_TAREA1.pdf | cut -f1)
                echo -e "${BLUE}  Tamaño: $file_size${NC}"
                
                # Abrir PDF si está en macOS
                if confirm "¿Abrir el PDF generado?"; then
                    open ENTREGA_TAREA1.pdf
                fi
            fi
        else
            echo -e "${RED}✗ Error al generar PDF${NC}"
            exit 1
        fi
        ;;
    
    *)
        echo -e "${RED}Opción inválida${NC}"
        exit 1
        ;;
esac

echo -e "\n${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✨ Limpieza completada exitosamente${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}\n"

# Mostrar espacio liberado
echo -e "${YELLOW}💡 Tip: Para ver espacio en disco:${NC}"
echo "   du -sh data/ models/ results/"
echo ""
