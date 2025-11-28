FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y actualizar pip
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear carpeta de resultados
RUN mkdir -p results

# Variables de entorno para el servicio
ENV RESULTS_PATH=/app/results

# Exponer puerto
EXPOSE 8080

# Punto de entrada del microservicio PCA
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8080"]
