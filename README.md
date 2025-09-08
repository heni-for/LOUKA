# Luca - AI Voice Assistant with Gemini

A powerful Siri-like voice assistant that helps you manage emails, have conversations, and get things done using Google's Gemini AI models.

## ✨ Features

- **🎤 Voice Control**: Push-to-talk voice recognition with automatic microphone detection
- **🔊 Voice Output**: Speaks responses aloud using Windows TTS
- **📧 Email Management**: Inbox, organize, read, and draft emails (Outlook integration)
- **🤖 AI Chat**: General conversations powered by Google Gemini
- **🖥️ Modern GUI**: Beautiful desktop interface with conversation history
- **⚡ Offline Speech**: Uses Vosk for local speech recognition (no internet required)
- **🔧 Auto-Setup**: Automatically detects the best microphone and configures everything

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
# Navigate to project directory
cd C:\Users\Heni2\luca

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install all dependencies
pip install -r requirements.txt
```

### 2. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### 3. Configure API Key

**Option A: Use the setup script (Recommended)**
```powershell
python setup_gemini_key.py
```

**Option B: Manual setup**
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
VOSK_MODEL_PATH=vosk-model-small-en-us-0.15
```

### 4. Download Speech Model (One-time setup)

Download the Vosk speech recognition model:
- Go to [Vosk Models](https://alphacephei.com/vosk/models)
- Download `vosk-model-small-en-us-0.15.zip`
- Extract to project root so you have: `vosk-model-small-en-us-0.15/`

### 5. Launch Luca

**GUI Mode (Recommended):**
```powershell
python run_luca_gui.py
```

**Voice-Only Mode:**
```powershell
python -m assistant.voice
```

## 🎯 How to Use

### Voice Commands
- **Press Enter** to start listening
- **Say "help"** to see available commands
- **Email commands**: "inbox", "organize", "read", "draft"
- **General chat**: Ask questions, get help, brainstorm ideas

### GUI Features
- **Voice Input**: Click microphone button or press Enter
- **Text Input**: Type messages in the text box
- **Conversation History**: See all interactions
- **Voice Output**: Luca speaks all responses aloud

## 🔧 Configuration

### Environment Variables (.env file)
```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
VOSK_MODEL_PATH=vosk-model-small-en-us-0.15
LLM_MODEL=gemini-1.5-flash

# Legacy OpenAI support (optional)
OPENAI_API_KEY=sk-...
```

### Available Models
- `gemini-1.5-flash` (default) - Fast and efficient
- `gemini-1.5-pro` - More capable for complex tasks
- `gemini-1.0-pro` - Stable and reliable

## 🛠️ Troubleshooting

### Voice Recognition Issues
```powershell
# Test microphone detection
python -c "from assistant.voice import find_best_microphone; print(find_best_microphone())"

# Test speech recognition
python test_speech.py
```

### API Key Issues
```powershell
# Test Gemini integration
python test_gemini.py

# Test voice output
python test_voice.py
```

### Common Solutions
- **No microphone detected**: Check Windows audio settings
- **Poor voice recognition**: Speak clearly, reduce background noise
- **API errors**: Verify your Gemini API key is correct
- **Installation issues**: Try `pip install --upgrade pip` first

## 📁 Project Structure

```
luca/
├── assistant/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── llm.py             # Gemini AI integration
│   ├── tts.py             # Text-to-speech
│   ├── voice.py           # Voice recognition
│   ├── gui.py             # Desktop interface
│   └── outlook_local.py   # Email integration
├── run_luca_gui.py        # GUI launcher
├── setup_gemini_key.py    # API key setup
├── test_gemini.py         # Gemini testing
├── test_voice.py          # Voice testing
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 🎉 What's New

- **✅ Migrated to Google Gemini**: More powerful and cost-effective AI
- **✅ Automatic Microphone Detection**: No manual setup required
- **✅ Voice Output Integration**: Luca speaks all responses
- **✅ Modern GUI**: Beautiful desktop interface
- **✅ Push-to-Talk**: Only listens when you want it to
- **✅ Error Handling**: Graceful handling of API issues

## 🔄 Migration from OpenAI

If you were using OpenAI before:
1. Get a Gemini API key (free tier available)
2. Run `python setup_gemini_key.py`
3. Your existing voice commands will work with Gemini!

## 📞 Support

- **Voice Issues**: Check microphone permissions in Windows
- **API Issues**: Verify your Gemini API key
- **Installation**: Ensure Python 3.10+ and virtual environment

## 🗑️ Clean Up

```powershell
# Remove virtual environment
Remove-Item .venv -Recurse -Force

# Remove cached files
Remove-Item assistant\.token_cache.bin -Force -ErrorAction SilentlyContinue
```

---

**Luca** - Your AI Voice Assistant powered by Google Gemini! 🎤🤖✨