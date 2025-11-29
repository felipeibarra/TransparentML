# 🦙 Ollama Setup Guide - Local AI for TransparentML

## Why Ollama?

✅ **100% Free** - No API keys, no costs  
✅ **100% Local** - Data never leaves your machine  
✅ **100% Private** - Complete privacy  
✅ **Fast** - Runs on your Mac's GPU  
✅ **Easy** - One command to install

---

## Installation (macOS)

### 1. Install Ollama

```bash
# Download and install from official site
# Go to: https://ollama.ai
# Or use Homebrew:
brew install ollama
```

### 2. Start Ollama Server

```bash
# Start Ollama service (runs in background)
ollama serve
```

### 3. Download a Model

Choose one of these models:

```bash
# Recommended: Llama 3.2 (3B) - Fast & Good
ollama pull llama3.2

# Alternative: Mistral (7B) - Better but slower
ollama pull mistral

# Tiny: Llama 3.2 1B - Very fast, less accurate
ollama pull llama3.2:1b

# Code-focused: CodeLlama
ollama pull codellama
```

### 4. Test It

```bash
# Test the model
ollama run llama3.2

# Type a question, press Ctrl+D to exit
>>> Hello!
Hello! How can I help you today?
>>> /bye
```

---

## Configuration in TransparentML

### Edit Dashboard JavaScript

```bash
# Open the config file
nano url-diagnostics/static/js/dashboard-integrated.js
```

### Set Provider to Ollama (Line 16)

```javascript
const AI_CONFIG = {
    provider: 'ollama',  // ✅ Already set by default!
    
    ollama: {
        apiUrl: 'http://localhost:11434/api/chat',
        model: 'llama3.2',  // Match the model you downloaded
    },
    // ... other providers
};
```

### Change Model (Optional)

If you downloaded a different model:

```javascript
ollama: {
    apiUrl: 'http://localhost:11434/api/chat',
    model: 'mistral',  // or 'codellama', 'llama3.2:1b', etc.
}
```

---

## Available Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **llama3.2** | 3GB | ⚡⚡⚡ | ⭐⭐⭐ | General use (Recommended) |
| **llama3.2:1b** | 1GB | ⚡⚡⚡⚡ | ⭐⭐ | Very fast responses |
| **mistral** | 4GB | ⚡⚡ | ⭐⭐⭐⭐ | Better reasoning |
| **codellama** | 4GB | ⚡⚡ | ⭐⭐⭐ | Code & technical |
| **llama3.1:8b** | 5GB | ⚡ | ⭐⭐⭐⭐ | Best quality |

---

## Usage

### 1. Start Services

```bash
# Terminal 1: Start Ollama (if not already running)
ollama serve

# Terminal 2: Start TransparentML
make start-all-ml
```

### 2. Use Dashboard

1. Open http://localhost:8003/static/dashboard.html
2. Run any ML analysis
3. Chatbot activates automatically
4. Ask questions - AI responds using local model!

### 3. Example Questions

```
✅ "Explain my R² score of 0.89"
✅ "Why is my URL health score 65?"
✅ "What does 72% variance mean in PCA?"
✅ "How can I improve KNN accuracy?"
✅ "Compare my Linear Regression vs KNN results"
```

---

## Troubleshooting

### Error: "Ollama not running"

```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama if not running
ollama serve

# Or restart
pkill ollama
ollama serve
```

### Error: "Model not available"

```bash
# List downloaded models
ollama list

# Download the model you need
ollama pull llama3.2
```

### Chatbot Not Responding

1. Check Ollama is running: `ollama list`
2. Verify model name matches config
3. Check browser console (F12) for errors
4. Restart Ollama: `pkill ollama && ollama serve`

### Slow Responses

```bash
# Use a smaller/faster model
ollama pull llama3.2:1b

# Update config to use smaller model
# In dashboard-integrated.js line 21:
model: 'llama3.2:1b'
```

---

## Advanced Configuration

### Run Ollama on Startup (macOS)

```bash
# Create Launch Agent
mkdir -p ~/Library/LaunchAgents

cat > ~/Library/LaunchAgents/com.ollama.serve.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ollama.serve</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/ollama</string>
        <string>serve</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load it
launchctl load ~/Library/LaunchAgents/com.ollama.serve.plist
```

### Custom System Prompt

Edit `dashboard-integrated.js` line 616:

```javascript
const systemMessage = `You are an expert ML engineer specializing in TransparentML...`;
```

---

## Performance Tips

### 1. GPU Acceleration

Ollama automatically uses your Mac's GPU (M1/M2/M3).

### 2. Memory Usage

- Llama 3.2 3B: ~4GB RAM
- Mistral 7B: ~8GB RAM
- Close other apps for better performance

### 3. Speed Optimization

```bash
# Use quantized models (smaller, faster)
ollama pull llama3.2:1b-q4_0

# Check running models
ollama ps
```

---

## Comparison: Ollama vs Other Providers

| Feature | Ollama | Groq | OpenAI |
|---------|--------|------|--------|
| **Cost** | Free | Free (limited) | Paid |
| **Privacy** | 100% Local | Cloud | Cloud |
| **Speed** | Fast | Very Fast | Fast |
| **Setup** | Easy | API Key | API Key |
| **Internet** | Not needed | Required | Required |
| **Models** | Many open-source | Llama, Mixtral | GPT-3.5/4 |

---

## Next Steps

1. ✅ Install Ollama
2. ✅ Download a model
3. ✅ Test with TransparentML
4. 🔜 Set up vector database for memory (see VECTOR-DB-SETUP.md)

---

## Resources

- **Ollama Website**: https://ollama.ai
- **Model Library**: https://ollama.ai/library
- **GitHub**: https://github.com/ollama/ollama
- **Discord**: https://discord.gg/ollama

---

## Support

If you have issues:

1. Check Ollama is running: `ollama list`
2. View Ollama logs: `tail -f ~/.ollama/logs/server.log`
3. Check TransparentML logs: `make logs-all-ml`
4. Open browser console (F12) for errors

---

**Happy chatting with your local AI! 🦙**

*TransparentML Team*
