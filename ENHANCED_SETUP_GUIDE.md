# 🎤 Luca Enhanced Voice Assistant - Setup Guide

## Overview

Luca is now enhanced with Siri-like capabilities including:
- **Continuous listening** with wake word detection
- **Multi-language support** (English, Arabic, Tunisian)
- **Smart commands** (weather, time, jokes, calculations)
- **Natural conversation** with AI
- **High-quality text-to-speech**
- **Email management** integration

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up API Keys
Create a `.env` file in the project root:
```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (for weather)
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Voice model paths (adjust if needed)
VOSK_MODEL_PATH=vosk-model-en-us-0.22
ARABIC_MODEL_PATH=vosk-model-ar-tn-0.1-linto
TUNISIAN_MODEL_PATH=vosk-model-ar-tn-0.1-linto
```

### 3. Run Luca
```bash
# GUI Mode (Recommended)
python run_enhanced_luca.py

# Continuous Voice Mode (Siri-like)
python run_enhanced_luca.py continuous

# Voice Mode (Push-to-talk)
python run_enhanced_luca.py voice

# Command Line Mode
python run_enhanced_luca.py cli
```

## Voice Commands

### Wake Words
- **English**: "Hey Luca", "Luca", "OK Luca"
- **Arabic**: "لوكا", "مرحبا لوكا", "أهلا لوكا"
- **Tunisian**: "لوكا", "أهلا لوكا", "Hey Luca"

### Smart Commands
- **Weather**: "What's the weather?", "How's the weather in Paris?"
- **Time**: "What time is it?", "Current time"
- **Jokes**: "Tell me a joke", "Make me laugh"
- **Quotes**: "Give me a motivational quote"
- **Math**: "Calculate 2 plus 2", "What's 15 times 8?"
- **Definitions**: "Define artificial intelligence"
- **News**: "What's the latest news?"

### Email Commands
- **Inbox**: "Read my emails", "Show my inbox"
- **Organize**: "Organize my emails", "Sort my messages"
- **Draft**: "Draft an email", "Help me write an email"
- **Read**: "Read my last email"

### General Conversation
- Ask questions: "What is machine learning?"
- Get help: "Help me with Python programming"
- Creative tasks: "Write a poem about AI"
- Planning: "Help me plan my day"

## Features

### 🎯 Enhanced Voice Recognition
- **Fuzzy matching** for wake words
- **Intent recognition** for natural commands
- **Multi-language support** with automatic detection
- **Noise filtering** for better accuracy

### 🧠 Smart AI Responses
- **Siri-like personality** with natural conversation
- **Context awareness** with conversation memory
- **Proactive suggestions** and follow-up questions
- **Emotional intelligence** in responses

### 🎵 High-Quality TTS
- **Natural speech patterns** with appropriate pacing
- **Voice selection** for best quality
- **Multi-language support** for Arabic and English
- **Volume and rate optimization**

### 🌟 Smart Features
- **Weather information** (requires OpenWeatherMap API)
- **Time and date** with friendly formatting
- **Jokes and quotes** for entertainment
- **Math calculations** and definitions
- **News summaries** (requires news API)

## Configuration

### Language Settings
```python
# In assistant/config.py
DEFAULT_LANGUAGE = "en"  # en, ar, tn
```

### Voice Settings
```python
# In assistant/tts.py
RATE = 180  # Speech rate (words per minute)
VOLUME = 0.9  # Volume level (0.0 to 1.0)
```

### Wake Word Sensitivity
```python
# In assistant/multilang_voice.py
WAKE_WORD_CONFIDENCE = 0.7  # Higher = more strict
SILENCE_TIMEOUT = 3.0  # Seconds before timeout
```

## Troubleshooting

### Common Issues

1. **"No microphone found"**
   - Check microphone permissions
   - Try different microphone device index
   - Run: `python test_microphone.py`

2. **"Voice recognition not working"**
   - Check Vosk model paths in `.env`
   - Ensure models are downloaded
   - Try different language settings

3. **"TTS not working"**
   - Check audio output device
   - Try different voice settings
   - Run: `python test_tts.py`

4. **"AI responses not working"**
   - Check Gemini API key in `.env`
   - Verify internet connection
   - Check API quota limits

### Performance Optimization

1. **Reduce latency**:
   - Use faster TTS engines
   - Optimize wake word detection
   - Reduce conversation history length

2. **Improve accuracy**:
   - Use better microphone
   - Adjust noise thresholds
   - Train with your voice

3. **Memory usage**:
   - Limit conversation history
   - Use smaller language models
   - Clear cache regularly

## Advanced Usage

### Custom Commands
Add your own commands in `assistant/smart_features.py`:
```python
def handle_custom_command(text: str) -> str:
    if "my custom command" in text.lower():
        return "Custom response here"
    return None
```

### Custom Wake Words
Modify wake phrases in `assistant/multilang_voice.py`:
```python
MODEL_CONFIGS = {
    'en': {
        'wake_phrases': ["luca", "hey luca", "your custom phrase"],
        # ...
    }
}
```

### Integration with Other Services
- **Calendar**: Add Google Calendar integration
- **Reminders**: Connect to task management apps
- **Smart Home**: Control IoT devices
- **Music**: Integrate with Spotify/Apple Music

## API Keys Setup

### Gemini API (Required)
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Add to `.env`: `GEMINI_API_KEY=your_key_here`

### OpenWeatherMap API (Optional)
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get free API key
3. Add to `.env`: `OPENWEATHER_API_KEY=your_key_here`

## Support

- **Documentation**: Check this guide and code comments
- **Issues**: Report bugs and feature requests
- **Community**: Join discussions and share improvements

## License

This project is open source. Feel free to modify and distribute according to your needs.

---

**Enjoy your enhanced Luca voice assistant! 🎤✨**
