#!/usr/bin/env python3
"""
Multi-language voice recognition using multiple Vosk models
Supports English, Arabic, and Tunisian Arabic
"""

import os
import json
import queue
import threading
import time
import sounddevice as sd
import vosk
import numpy as np
from typing import Dict, List, Optional, Tuple
from .config import VOSK_MODEL_PATH, ARABIC_MODEL_PATH, TUNISIAN_MODEL_PATH
from .tts import speak
from .intent_library import detect_intent

# Model configurations
MODEL_CONFIGS = {
    'en': {
        'name': 'English',
        'path': VOSK_MODEL_PATH,  # Default English model
        'wake_phrases': ["luca", "hey luca", "ok luca", "okay luca", "hi luca"],
        'command_keywords': ["inbox", "list", "read", "organize", "organise", "draft", "cancel", "stop", "help", "chat", "ask", "question", "tell", "explain", "what", "how", "why", "when", "where", "who"]
    },
    'ar': {
        'name': 'Arabic',
        'path': ARABIC_MODEL_PATH,
        'wake_phrases': ["لوكا", "مرحبا لوكا", "أهلا لوكا", "يا لوكا"],
        'command_keywords': ["صندوق", "قائمة", "اقرأ", "تنظيم", "مسودة", "إلغاء", "توقف", "مساعدة", "محادثة", "سؤال", "أخبر", "اشرح", "ماذا", "كيف", "لماذا", "متى", "أين", "من"]
    },
    'tn': {
        'name': 'Tunisian Arabic',
        'path': TUNISIAN_MODEL_PATH,
        'wake_phrases': ["لوكا", "أهلا لوكا", "مرحبا لوكا", "يا لوكا", "luca", "hey luca", "salut luca", "bonjour luca"],
        'command_keywords': ["صندوق", "قائمة", "اقرأ", "تنظيم", "مسودة", "إلغاء", "توقف", "مساعدة", "محادثة", "سؤال", "أخبر", "اشرح", "ماذا", "كيف", "لماذا", "متى", "أين", "من", "inbox", "read", "draft", "help", "boite", "lire", "aide"]
    }
}

# Audio settings
SAMPLE_RATE = 16000
FRAME_MS = 30
BYTES_PER_SAMPLE = 2
CHANNELS = 1
VAD_AGGRESSIVENESS = 2

# Noise filtering settings - Optimized for Siri-like experience
MIN_UTTERANCE_LENGTH = 2  # Minimum characters for valid command
NOISE_THRESHOLD = 0.01    # Balanced sensitivity
SILENCE_TIMEOUT = 1.5     # Faster response - wait for user to finish speaking
MIN_WAKE_LENGTH = 2       # Minimum wake word length
WAKE_WORD_CONFIDENCE = 0.7  # Confidence threshold for wake word detection

class MultiLanguageVoiceRecognizer:
    """Multi-language voice recognition using multiple Vosk models."""
    
    def __init__(self):
        self.models = {}
        self.recognizers = {}
        self.current_language = 'en'  # Default to English
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.is_running = False
        self.microphone_index = None
        self.vad = None
        
        # Initialize VAD if available
        try:
            import webrtcvad
            self.vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)
            self.has_vad = True
        except ImportError:
            self.has_vad = False
            print("⚠️ WebRTC VAD not available. Install with: pip install webrtcvad")
        
        # Load available models
        self._load_models()
    
    def _load_models(self):
        """Load all available Vosk models."""
        for lang_code, config in MODEL_CONFIGS.items():
            model_path = config['path']
            if os.path.exists(model_path):
                try:
                    print(f"Loading {config['name']} model from {model_path}")
                    self.models[lang_code] = vosk.Model(model_path)
                    self.recognizers[lang_code] = vosk.KaldiRecognizer(
                        self.models[lang_code], SAMPLE_RATE
                    )
                    print(f"✅ {config['name']} model loaded successfully")
                except Exception as e:
                    print(f"❌ Failed to load {config['name']} model: {e}")
            else:
                print(f"⚠️ {config['name']} model not found at {model_path}")
    
    def set_language(self, language: str):
        """Set the current recognition language."""
        if language in self.recognizers:
            self.current_language = language
            print(f"🌍 Switched to {MODEL_CONFIGS[language]['name']}")
        else:
            print(f"❌ Language '{language}' not available")
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages."""
        return list(self.recognizers.keys())
    
    def find_best_microphone(self) -> Optional[int]:
        """Find the best available microphone."""
        try:
            devices = sd.query_devices()
            input_devices = []
            
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    input_devices.append((i, device))
            
            if not input_devices:
                print("❌ No input devices found")
                return None
            
            # Try to find a working microphone (prefer devices 0, 1, 4, 5)
            preferred_devices = [0, 1, 4, 5]  # Known working devices from test
            
            for device_index in preferred_devices:
                if device_index < len(devices) and devices[device_index]['max_input_channels'] > 0:
                    try:
                        # Test if device is accessible
                        test_stream = sd.InputStream(
                            device=device_index,
                            channels=1,
                            samplerate=SAMPLE_RATE,
                            blocksize=1024
                        )
                        test_stream.close()
                        
                        print(f"🎤 Auto-selected microphone: {devices[device_index]['name']} (Device {device_index})")
                        print(f"  Channels: {devices[device_index]['max_input_channels']}, Default: {devices[device_index].get('is_default', False)}")
                        return device_index
                        
                    except Exception as e:
                        print(f"⚠️ Device {device_index} not accessible: {e}")
                        continue
            
            # If preferred devices don't work, try others
            for device_index, device_info in input_devices:
                if device_index not in preferred_devices:
                    try:
                        # Test if device is accessible
                        test_stream = sd.InputStream(
                            device=device_index,
                            channels=1,
                            samplerate=SAMPLE_RATE,
                            blocksize=1024
                        )
                        test_stream.close()
                        
                        print(f"🎤 Auto-selected microphone: {device_info['name']} (Device {device_index})")
                        print(f"  Channels: {device_info['max_input_channels']}, Default: {device_info.get('is_default', False)}")
                        return device_index
                        
                    except Exception as e:
                        print(f"⚠️ Device {device_index} not accessible: {e}")
                        continue
            
            # If no device works, try default
            try:
                default_device = sd.default.device[0]
                print(f"🎤 Using default microphone: Device {default_device}")
                return default_device
            except:
                print("❌ No accessible microphones found")
                return None
            
        except Exception as e:
            print(f"❌ Error detecting microphone: {e}")
            return None
    
    def _audio_callback(self, indata, frames, time, status):
        """Audio input callback."""
        if status:
            print(f"Audio status: {status}")
        
        if self.is_listening:
            # Calculate volume level for debugging
            volume = np.linalg.norm(indata) * 10
            if volume > 0.1:  # Only show when there's significant audio
                print(f"🔊 Volume: {volume:.2f}")
            
            # Convert to int16
            audio_data = (indata * 32767).astype(np.int16)
            self.audio_queue.put(audio_data.tobytes())
    
    def _detect_wake_word(self, text: str) -> bool:
        """Detect if the text contains a wake word for current language."""
        config = MODEL_CONFIGS[self.current_language]
        text_lower = text.lower().strip()
        
        # Enhanced wake word detection with fuzzy matching
        for phrase in config['wake_phrases']:
            phrase_lower = phrase.lower()
            
            # Exact match
            if phrase_lower in text_lower:
                print(f"🔔 Wake word '{phrase}' detected in '{text_lower}'")
                return True
            
            # Fuzzy match for common variations
            if self._fuzzy_wake_match(text_lower, phrase_lower):
                print(f"🔔 Wake word '{phrase}' detected (fuzzy) in '{text_lower}'")
                return True
                
        return False
    
    def _fuzzy_wake_match(self, text: str, phrase: str) -> bool:
        """Fuzzy matching for wake words to handle pronunciation variations."""
        # Remove common filler words
        text_clean = text.replace("um", "").replace("uh", "").replace("ah", "").strip()
        
        # Check if phrase words are present in order
        phrase_words = phrase.split()
        text_words = text_clean.split()
        
        if len(phrase_words) == 1:
            # Single word - check if it's at the start or contains the word
            return phrase_words[0] in text_clean
        else:
            # Multi-word phrase - check if all words are present in order
            phrase_idx = 0
            for word in text_words:
                if phrase_idx < len(phrase_words) and phrase_words[phrase_idx] in word:
                    phrase_idx += 1
                    if phrase_idx == len(phrase_words):
                        return True
        return False
    
    def _extract_command(self, text: str) -> Optional[str]:
        """Extract command from text for current language."""
        config = MODEL_CONFIGS[self.current_language]
        text_lower = text.lower().strip()
        
        # First, try to recognize intent from the full text (including wake words)
        command_intent = self._recognize_intent(text, config)
        if command_intent:
            return command_intent
        
        # Remove wake words and try again
        for phrase in config['wake_phrases']:
            text_lower = text_lower.replace(phrase.lower(), '').strip()
        
        # Enhanced command extraction with intent recognition
        command_intent = self._recognize_intent(text_lower, config)
        if command_intent:
            return command_intent
        
        # Check for direct command keywords
        for keyword in config['command_keywords']:
            if keyword.lower() in text_lower:
                return keyword
        
        # If no specific keyword found, check if it's a meaningful command
        if len(text_lower) >= MIN_UTTERANCE_LENGTH:
            # Check if it contains question words or action words
            question_words = ['what', 'how', 'when', 'where', 'why', 'who', 'which', 'can', 'could', 'would', 'should', 'will', 'do', 'does', 'did', 'is', 'are', 'was', 'were']
            action_words = ['open', 'close', 'start', 'stop', 'play', 'show', 'tell', 'give', 'help', 'check', 'read', 'write', 'send', 'create', 'delete', 'find', 'search']
            
            if any(word in text_lower for word in question_words + action_words):
                return text_lower
            else:
                return None
        
        # If only wake word detected, return a greeting
        if any(phrase in text.lower() for phrase in config['wake_phrases']):
            return "greeting"
        
        return None
    
    def _recognize_intent(self, text: str, config: dict) -> Optional[str]:
        """Recognize user intent from natural language using comprehensive library."""
        # Use the comprehensive intent library
        intent_match = detect_intent(text, self.current_language)
        if intent_match:
            return intent_match.intent
        
        # Fallback to basic pattern matching for edge cases
        text_lower = text.lower().strip()
        
        # Email-related intents (fallback)
        if any(word in text_lower for word in ['email', 'mail', 'message', 'inbox', 'بريد', 'رسالة']):
            if any(word in text_lower for word in ['read', 'show', 'check', 'اقرأ', 'أظهر']):
                return 'email_inbox'
            elif any(word in text_lower for word in ['organize', 'sort', 'arrange', 'تنظيم', 'ترتيب']):
                return 'organize_emails'
            elif any(word in text_lower for word in ['draft', 'write', 'compose', 'مسودة', 'اكتب']):
                return 'email_compose'
            elif any(word in text_lower for word in ['list', 'show', 'display', 'قائمة', 'أظهر']):
                return 'email_inbox'
        
        # Question intents (fallback)
        elif text_lower.startswith(('what', 'how', 'why', 'when', 'where', 'who', 'ماذا', 'كيف', 'لماذا', 'متى', 'أين', 'من')):
            return 'question'
        
        return None
    
    def _process_audio_chunk(self, audio_data: bytes) -> Optional[str]:
        """Process a chunk of audio data."""
        if self.current_language not in self.recognizers:
            return None
        
        recognizer = self.recognizers[self.current_language]
        
        if recognizer.AcceptWaveform(audio_data):
            result = json.loads(recognizer.Result())
            return result.get('text', '').strip()
        else:
            result = json.loads(recognizer.PartialResult())
            return result.get('partial', '').strip()
    
    def listen_for_command(self, timeout: float = 10.0) -> Optional[str]:
        """Listen for a voice command."""
        if not self.recognizers:
            print("❌ No models loaded")
            return None
        
        if self.current_language not in self.recognizers:
            print(f"❌ Current language '{self.current_language}' not available")
            return None
        
        # Find microphone
        if self.microphone_index is None:
            self.microphone_index = self.find_best_microphone()
            if self.microphone_index is None:
                return None
        
        print(f"🎧 Listening for commands in {MODEL_CONFIGS[self.current_language]['name']}...")
        print("💡 Say a wake word followed by a command (e.g., 'Hey Luca, read my emails')")
        
        self.is_listening = True
        self.is_running = True
        
        try:
            # Start audio stream with error handling
            stream = sd.InputStream(
                device=self.microphone_index,
                channels=CHANNELS,
                samplerate=SAMPLE_RATE,
                callback=self._audio_callback,
                blocksize=int(SAMPLE_RATE * FRAME_MS / 1000)
            )
            
            with stream:
                start_time = time.time()
                last_audio_time = start_time
                utterance_buffer = ""
                wake_word_detected = False
                
                while self.is_running and (time.time() - start_time) < timeout:
                    try:
                        # Get audio data
                        audio_data = self.audio_queue.get(timeout=0.1)
                        
                        # Process audio
                        text = self._process_audio_chunk(audio_data)
                        
                        if text:
                            last_audio_time = time.time()
                            utterance_buffer += text + " "
                            
                            # Show what was heard in real-time
                            print(f"👂 Heard: {text}")
                            
                            # Check for wake word
                            if self._detect_wake_word(utterance_buffer):
                                print(f"🔔 Wake word detected: {utterance_buffer.strip()}")
                                wake_word_detected = True
                                
                                # Extract command
                                command = self._extract_command(utterance_buffer)
                                if command and len(command.strip()) > 2:  # Ensure we have a real command
                                    print(f"📝 Command: {command}")
                                    return command
                                
                                # If just wake word, continue listening for more
                                if wake_word_detected and len(utterance_buffer.strip()) < 10:
                                    print("🔔 Wake word detected, waiting for command...")
                                    # Continue listening for more input
                                    continue
                                
                                # If wake word detected but no clear command, return the wake word
                                if wake_word_detected and len(utterance_buffer.strip()) >= 10:
                                    print(f"📝 Command: {utterance_buffer.strip()}")
                                    return utterance_buffer.strip()
                            
                            # Don't process commands while still speaking - wait for silence
                            # This will be handled in the silence timeout section
                        
                        # Check for silence timeout after wake word
                        if wake_word_detected and time.time() - last_audio_time > SILENCE_TIMEOUT:
                            if utterance_buffer.strip():
                                print(f"⏰ Silence timeout, processing: {utterance_buffer.strip()}")
                                command = self._extract_command(utterance_buffer)
                                if command:
                                    return command
                            utterance_buffer = ""
                            wake_word_detected = False
                        
                        # Check for general silence timeout - process commands when user stops speaking
                        elif not wake_word_detected and time.time() - last_audio_time > SILENCE_TIMEOUT:
                            if utterance_buffer.strip():
                                print(f"⏰ Silence timeout, processing: {utterance_buffer.strip()}")
                                command = self._extract_command(utterance_buffer)
                                if command and command not in ["greeting", "question"]:
                                    print(f"📝 Command extracted: {command}")
                                    return command
                                else:
                                    # If no clear command detected, return "don't understand"
                                    print("❌ No clear command detected, returning dont_understand")
                                    return "dont_understand"
                            utterance_buffer = ""
                    
                    except queue.Empty:
                        continue
                    except KeyboardInterrupt:
                        break
                
                print("⏰ Listening timeout")
                return None
                
        except Exception as e:
            print(f"❌ Error during listening: {e}")
            return None
        finally:
            self.is_listening = False
            self.is_running = False
    
    def stop_listening(self):
        """Stop the listening process."""
        self.is_running = False
        self.is_listening = False

def test_multilang_voice():
    """Test the multi-language voice recognition."""
    recognizer = MultiLanguageVoiceRecognizer()
    
    print("🎤 Multi-Language Voice Recognition Test")
    print("=" * 50)
    
    # Show available languages
    available = recognizer.get_available_languages()
    print(f"Available languages: {available}")
    
    if not available:
        print("❌ No models available. Please download Vosk models.")
        return
    
    # Test each language
    for lang in available:
        print(f"\n🌍 Testing {MODEL_CONFIGS[lang]['name']}...")
        recognizer.set_language(lang)
        
        command = recognizer.listen_for_command(timeout=5.0)
        if command:
            print(f"✅ Recognized: {command}")
        else:
            print("❌ No command recognized")

if __name__ == "__main__":
    test_multilang_voice()
