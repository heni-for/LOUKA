# 🎤 Enhanced Luca - Tunisian Derja Setup Guide

## 🚀 What's New - "Siri in Derja"

Your Luca voice assistant now supports **Tunisian Derja** with advanced features:

### ✨ **New Features**
- **🧠 Natural Language Understanding (NLU)** for Tunisian Derja
- **🎯 Smart Intent Recognition** with context awareness
- **💾 Memory & Context Management** for conversation flow
- **🗣️ Enhanced TTS** with Tunisian pronunciation
- **🔄 Command-to-Action Mapping** with state management
- **🌍 Multi-language Support** (English, Arabic, Tunisian)
- **📱 Enhanced GUI** with modern interface

---

## 🛠️ **Installation & Setup**

### **1. Install Enhanced Dependencies**

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install enhanced dependencies
pip install -r requirements.txt

# Install additional AI/ML libraries
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers accelerate
pip install coqui-tts
pip install elevenlabs
```

### **2. Download Speech Models**

```powershell
# Download Vosk models for multi-language support
python -c "
import os
import urllib.request
import zipfile

# English model
if not os.path.exists('vosk-model-en-us-0.22'):
    print('Downloading English model...')
    urllib.request.urlretrieve('https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip', 'vosk-model-en-us-0.22.zip')
    with zipfile.ZipFile('vosk-model-en-us-0.22.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    os.remove('vosk-model-en-us-0.22.zip')

# Arabic model
if not os.path.exists('vosk-model-ar-0.22'):
    print('Downloading Arabic model...')
    urllib.request.urlretrieve('https://alphacephei.com/vosk/models/vosk-model-ar-0.22.zip', 'vosk-model-ar-0.22.zip')
    with zipfile.ZipFile('vosk-model-ar-0.22.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    os.remove('vosk-model-ar-0.22.zip')
"
```

### **3. Configure API Keys**

Create a `.env` file with your API keys:

```env
# Required for AI features
GEMINI_API_KEY=your_gemini_api_key_here

# Optional for enhanced features
OPENWEATHER_API_KEY=your_openweather_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Gmail API (for email features)
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json

# Voice settings
DEFAULT_LANGUAGE=en
TTS_ENGINE=pyttsx3
```

---

## 🎯 **Usage Modes**

### **1. Enhanced GUI Mode (Recommended)**

```powershell
python run_enhanced_luca.py gui
```

**Features:**
- Modern dark-themed interface
- Multi-language support (EN/AR/TN)
- Real-time conversation display
- Push-to-talk (Hold 'L')
- Voice and text input
- Context management
- Quick command buttons

### **2. Voice-Only Mode**

```powershell
# English
python run_enhanced_luca.py voice --language en

# Arabic
python run_enhanced_luca.py voice --language ar

# Tunisian
python run_enhanced_luca.py voice --language tn
```

### **3. Testing Mode**

```powershell
# Test all components
python run_enhanced_luca.py test --test-component all

# Test specific components
python run_enhanced_luca.py test --test-component nlu
python run_enhanced_luca.py test --test-component voice
python run_enhanced_luca.py test --test-component memory
python run_enhanced_luca.py test --test-component tts

# Show intent examples
python run_enhanced_luca.py examples
```

---

## 🗣️ **Tunisian Derja Commands**

### **📧 Email Commands**

| Derja Command | English | Action |
|---------------|---------|--------|
| `أعطيني الإيميلات` | Give me emails | Fetch inbox |
| `أعطيني لي 3ندي فيل إيميل` | Give me what I have in email | Fetch inbox |
| `أقرا الإيميل` | Read email | Read current email |
| `حضرلي رد` | Prepare reply | Draft response |
| `أبعت الرد` | Send reply | Send drafted response |
| `نظم الإيميلات` | Organize emails | Sort inbox |

### **🕐 Time & Weather**

| Derja Command | English | Action |
|---------------|---------|--------|
| `شنادي الوقت` | What time is it | Get current time |
| `شنادي الطقس` | What's the weather | Get weather |
| `شنادي الطقس في تونس` | Weather in Tunis | Get weather for city |

### **😄 Entertainment**

| Derja Command | English | Action |
|---------------|---------|--------|
| `أعطني نكتة` | Give me a joke | Tell joke |
| `أحسب لي 2 زائد 2` | Calculate 2 plus 2 | Math calculation |
| `أعطني اقتباس` | Give me a quote | Motivational quote |

### **❓ Help & Greetings**

| Derja Command | English | Action |
|---------------|---------|--------|
| `أهلا وينك` | Hello, how are you | Greeting |
| `أعطني` | Give me | Help request |
| `شنادي نعمل` | What can we do | Show capabilities |
| `باي باي` | Bye bye | Goodbye |

---

## 🧠 **Smart Features**

### **1. Context Awareness**
- Remembers conversation history
- Tracks email context
- Maintains draft state
- Learns user preferences

### **2. Intent Recognition**
- Understands natural Derja speech
- Handles pronunciation variations
- Extracts entities (numbers, names, cities)
- Falls back to AI interpretation

### **3. Memory Management**
- Stores conversation history
- Remembers email interactions
- Tracks user preferences
- Persistent context across sessions

### **4. Enhanced TTS**
- Tunisian pronunciation optimization
- Emotional tone support
- AI-enhanced speech
- Interruptible speech

---

## 🔧 **Advanced Configuration**

### **Voice Recognition Settings**

```python
# In assistant/config.py
VOSK_MODEL_PATH = "vosk-model-en-us-0.22"
ARABIC_MODEL_PATH = "vosk-model-ar-0.22"
TUNISIAN_MODEL_PATH = "vosk-model-ar-0.22"  # Uses Arabic model

# Voice activity detection
VAD_AGGRESSIVENESS = 2  # 0-3, higher = more aggressive
NOISE_THRESHOLD = 0.01  # Lower = more sensitive
SILENCE_TIMEOUT = 3.0   # Seconds of silence before timeout
```

### **TTS Settings**

```python
# In assistant/derja_tts.py
DEFAULT_RATE = 180      # Words per minute
DEFAULT_VOLUME = 0.9    # 0.0 to 1.0
EMOTION_TONES = {
    "happy": {"rate": +20, "volume": +0.1},
    "sad": {"rate": -20, "volume": -0.1},
    "excited": {"rate": +30, "volume": +0.2}
}
```

### **Memory Settings**

```python
# In assistant/memory_manager.py
MAX_SHORT_TERM_MEMORY = 50    # Recent items to keep
MEMORY_CLEANUP_DAYS = 30      # Auto-cleanup old memories
CONTEXT_PERSISTENCE = True    # Save context between sessions
```

---

## 🎨 **Customization**

### **1. Add New Derja Commands**

Edit `assistant/derja_nlu.py`:

```python
# Add new intent patterns
"new_intent": [
    r"pattern1.*derja",
    r"pattern2.*derja",
    # Add more patterns
]
```

### **2. Add New Actions**

Edit `assistant/action_mapper.py`:

```python
def _handle_new_intent(self, intent: Intent) -> str:
    """Handle new intent."""
    # Your implementation
    return "Response in Derja"
```

### **3. Customize TTS Voice**

```python
# In assistant/derja_tts.py
def _find_best_voice(self, voices):
    # Add your voice preferences
    voice_preferences = [
        'your_preferred_voice',
        'arabic', 'tunisian'
    ]
```

---

## 🐛 **Troubleshooting**

### **Common Issues**

1. **Voice Recognition Not Working**
   ```powershell
   # Test microphone
   python -c "import sounddevice as sd; print(sd.query_devices())"
   
   # Test voice recognition
   python run_enhanced_luca.py test --test-component voice
   ```

2. **Derja Commands Not Recognized**
   ```powershell
   # Test NLU
   python run_enhanced_luca.py test --test-component nlu
   
   # Check intent examples
   python run_enhanced_luca.py examples
   ```

3. **TTS Not Working**
   ```powershell
   # Test TTS
   python run_enhanced_luca.py test --test-component tts
   
   # Check available voices
   python -c "from assistant.derja_tts import derja_tts; print(derja_tts.get_available_voices())"
   ```

4. **Memory Issues**
   ```powershell
   # Test memory system
   python run_enhanced_luca.py test --test-component memory
   
   # Clear old memories
   python -c "from assistant.memory_manager import get_memory_manager; get_memory_manager().clear_old_memories(7)"
   ```

### **Performance Optimization**

1. **Reduce Memory Usage**
   ```python
   # In assistant/memory_manager.py
   MAX_SHORT_TERM_MEMORY = 25  # Reduce from 50
   ```

2. **Faster Voice Recognition**
   ```python
   # In assistant/enhanced_voice.py
   VAD_AGGRESSIVENESS = 3  # More aggressive filtering
   NOISE_THRESHOLD = 0.02  # Higher threshold
   ```

3. **Optimize TTS**
   ```python
   # In assistant/derja_tts.py
   DEFAULT_RATE = 200  # Faster speech
   ```

---

## 📚 **API Reference**

### **Derja NLU**

```python
from assistant.derja_nlu import detect_derja_intent

intent = detect_derja_intent("أعطيني الإيميلات")
print(intent.intent)        # "fetch_email"
print(intent.confidence)    # 0.95
print(intent.entities)      # {}
```

### **Action Mapper**

```python
from assistant.action_mapper import execute_derja_action

response = execute_derja_action(intent)
print(response)  # "لقيت 5 إيميلات في الإنبوكس"
```

### **Memory Manager**

```python
from assistant.memory_manager import get_memory_manager

memory = get_memory_manager()
memory.add_conversation_memory("أعطيني الإيميلات", "لقيت 5 إيميلات")
recent = memory.get_recent_conversations(5)
```

### **Derja TTS**

```python
from assistant.derja_tts import speak_derja, speak_derja_with_emotion

speak_derja("أهلا وسهلا!")
speak_derja_with_emotion("تم بنجاح!", "happy")
```

---

## 🎉 **Ready to Use!**

Your enhanced Luca voice assistant is now ready with full Tunisian Derja support! 

**Quick Start:**
```powershell
python run_enhanced_luca.py gui
```

**Try these Derja commands:**
- "أهلا وينك" - Greeting
- "أعطيني الإيميلات" - Get emails
- "حضرلي رد" - Prepare reply
- "أبعت الرد" - Send reply
- "شنادي الوقت" - What time is it

Enjoy your **Siri in Derja** experience! 🎤✨
