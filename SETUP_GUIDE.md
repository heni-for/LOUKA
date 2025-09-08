# Luca AI Voice Assistant - Setup Guide

## 🚀 Quick Start

### 1. **Automatic Microphone Detection** ✅
Luca now automatically detects and uses the best available microphone! No manual configuration needed.

### 2. **Launch Options**

#### **Option A: GUI (Recommended)**
```bash
python run_luca_gui.py
```
- Modern graphical interface
- Voice and text input
- Real-time conversation display
- Quick command buttons

#### **Option B: Command Line**
```bash
python -m assistant.voice
```
- Push-to-talk voice interface
- Press Enter to speak
- Ctrl+C to quit

### 3. **Setup Requirements**

#### **Required:**
- Python 3.8+ with virtual environment activated
- Vosk model downloaded (already done: `vosk-model-en-us-0.22`)

#### **Optional:**
- OpenAI API key for AI chat features
- Microsoft Outlook for email management

### 4. **Configuration (Optional)**

Create a `.env` file in the project root for advanced features:

```env
# OpenAI API Key (for AI chat)
OPENAI_API_KEY=your_api_key_here

# Vosk Model Path (auto-detected)
VOSK_MODEL_PATH=C:\Users\Heni2\luca\vosk-model-en-us-0.22

# Default AI Model
DEFAULT_MODEL=gpt-3.5-turbo
```

### 5. **Features**

#### **Voice Commands:**
- **Email:** "inbox", "organize", "read", "draft"
- **General:** "help", "clear conversation"
- **AI Chat:** Ask anything!

#### **GUI Features:**
- 🎤 Voice input with push-to-talk
- 💬 Text input
- 📧 Quick email commands
- 🗑️ Clear conversation
- 📱 Real-time conversation display

### 6. **Troubleshooting**

#### **Microphone Issues:**
- Luca automatically selects the best microphone
- Check Windows audio settings if no microphone detected
- Ensure microphone permissions are enabled

#### **AI Chat Not Working:**
- Add your OpenAI API key to `.env` file
- Without API key, only email commands work

#### **Voice Recognition Issues:**
- Speak clearly and wait for "Listening..." prompt
- Use push-to-talk (press Enter) for better control
- Check microphone levels in Windows settings

### 7. **Current Status** ✅

- ✅ **Automatic microphone detection** - Working
- ✅ **Voice recognition** - Working  
- ✅ **GUI interface** - Working
- ✅ **Email commands** - Working (requires Outlook)
- ⚠️ **AI chat** - Requires OpenAI API key

## 🎯 Ready to Use!

Your Luca AI Voice Assistant is ready! The automatic microphone detection means you can just run it and start talking. No configuration needed!

**Start with:** `python run_luca_gui.py` for the best experience.
