#!/bin/bash
# ============================================================================
# TransparentML - Ollama Initialization Script
# ============================================================================
# This script downloads the AI models for Ollama automatically

set -e

echo "🚀 Initializing Ollama AI Service..."

# Wait for Ollama service to be ready
echo "⏳ Waiting for Ollama service to start..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama service is ready!"
        break
    fi
    echo "   Attempt $((attempt + 1))/$max_attempts - waiting..."
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ Ollama service failed to start"
    exit 1
fi

# Pull default model (llama3.2 - lightweight and powerful)
echo ""
echo "📥 Downloading AI model: llama3.2 (2GB)..."
echo "   This may take a few minutes on first run..."

docker exec transparentml-ollama ollama pull llama3.2

echo ""
echo "✅ Model downloaded successfully!"

# Verify model is available
echo ""
echo "🔍 Verifying model installation..."
docker exec transparentml-ollama ollama list

echo ""
echo "🎉 Ollama initialization complete!"
echo ""
echo "Available models:"
echo "  - llama3.2 (default, 2GB) ✅"
echo ""
echo "To download additional models:"
echo "  docker exec transparentml-ollama ollama pull mistral"
echo "  docker exec transparentml-ollama ollama pull phi3"
echo "  docker exec transparentml-ollama ollama pull codellama"
echo ""
echo "Dashboard ready at: http://localhost:8003/static/dashboard.html"
