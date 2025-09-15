#!/usr/bin/env python3
"""
Enhanced Voice Recognition System for Luca
Integrates Derja NLU with voice recognition
"""

import json
import queue
import sys
import time
import threading
import msvcrt
from typing import Optional, Dict, Any

import sounddevice as sd
from vosk import Model, KaldiRecognizer
try:
    import webrtcvad
    HAS_VAD = True
except Exception:
    HAS_VAD = False
from rich import print

from .derja_nlu import detect_derja_intent, Intent
from .action_mapper import execute_derja_action
from .derja_tts import speak_derja, speak_derja_with_emotion
from .memory_manager import add_conversation_memory, get_memory_manager
from .conversational_personality import get_personality_response, update_conversation_context
from .ai_chatty_brain import chat_naturally, get_context
from .emotional_tts import speak_with_emotion, speak_naturally, speak_conversationally
from .config import VOSK_MODEL_PATH, ARABIC_MODEL_PATH, TUNISIAN_MODEL_PATH

class EnhancedVoiceRecognizer:
    """Enhanced voice recognizer with Derja NLU integration."""
    
    def __init__(self, model_path: str = None, input_device: int = None, language: str = "en"):
        self.model_path = model_path or VOSK_MODEL_PATH
        self.input_device = input_device
        self.language = language
        self.model = None
        self.recognizer = None
        self.stream = None
        self.audio_queue = queue.Queue()
        self.running = False
        self.is_listening = False
        self.memory_manager = get_memory_manager()
        
        # Voice activity detection
        self.vad = webrtcvad.Vad(2) if HAS_VAD else None
        
        # Audio settings
        self.SAMPLE_RATE = 16000
        self.FRAME_MS = 30
        self.BYTES_PER_SAMPLE = 2
        self.CHANNELS = 1
        self.VAD_AGGRESSIVENESS = 2
        
        # Noise filtering
        self.MIN_UTTERANCE_LENGTH = 2
        self.NOISE_THRESHOLD = 0.01
        self.SILENCE_TIMEOUT = 3.0
        
        self._init_model()
        self._init_audio()
    
    def _init_model(self):
        """Initialize speech recognition model."""
        try:
            # Choose model based on language
            if self.language == "ar" or self.language == "tn":
                model_path = ARABIC_MODEL_PATH
            else:
                model_path = self.model_path
            
            self.model = Model(model_path)
            self.recognizer = KaldiRecognizer(self.model, self.SAMPLE_RATE)
            print(f"✅ Loaded {self.language} model: {model_path}")
            
        except Exception as e:
            print(f"❌ Model initialization error: {e}")
            self.model = None
            self.recognizer = None
    
    def _init_audio(self):
        """Initialize audio input."""
        try:
            if self.input_device is not None:
                sd.default.device = (self.input_device, None)
            
            dev_info = sd.query_devices(self.input_device, 'input') if self.input_device is not None else sd.query_devices(kind='input')
            max_in = int(dev_info.get('max_input_channels', 1) or 1)
            self.input_channels = max_in if max_in > 0 else 1
            
            print(f"✅ Audio initialized: {self.input_channels} channels")
            
        except Exception as e:
            print(f"❌ Audio initialization error: {e}")
            self.input_channels = 1
    
    def _audio_callback(self, indata, frames, time_info, status):
        """Audio input callback."""
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(bytes(indata))
    
    def start(self):
        """Start the voice recognizer."""
        if not self.model or not self.recognizer:
            print("❌ Model not initialized")
            return False
        
        try:
            self.running = True
            self.stream = sd.RawInputStream(
                samplerate=self.SAMPLE_RATE,
                blocksize=self._frame_bytes() // (self.BYTES_PER_SAMPLE * self.CHANNELS),
                dtype='int16',
                channels=self.input_channels,
                callback=self._audio_callback
            )
            self.stream.start()
            print("✅ Voice recognizer started")
            return True
            
        except Exception as e:
            print(f"❌ Error starting voice recognizer: {e}")
            return False
    
    def stop(self):
        """Stop the voice recognizer."""
        self.running = False
        self.is_listening = False
        
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
            print("✅ Voice recognizer stopped")
        except Exception as e:
            print(f"❌ Error stopping voice recognizer: {e}")
    
    def _frame_bytes(self, num_ms: int = None) -> int:
        """Calculate bytes per frame."""
        if num_ms is None:
            num_ms = self.FRAME_MS
        return int(self.SAMPLE_RATE * (num_ms / 1000.0)) * self.BYTES_PER_SAMPLE * self.CHANNELS
    
    def _read_frame(self) -> bytes:
        """Read and process audio frame."""
        try:
            data = self.audio_queue.get(timeout=0.1)
        except queue.Empty:
            return b""
        
        # Voice activity detection
        if self.vad and len(data) >= self._frame_bytes():
            if self.vad.is_speech(data[:self._frame_bytes()], self.SAMPLE_RATE):
                return data
            return b""
        
        # Noise filtering
        if len(data) >= self._frame_bytes():
            import numpy as np
            audio_data = np.frombuffer(data, dtype=np.int16)
            mean_squared = np.mean(audio_data**2)
            audio_level = np.sqrt(mean_squared) / 32768.0 if mean_squared > 0 else 0.0
            
            if audio_level < self.NOISE_THRESHOLD:
                return b""
            
            # Check for speech patterns
            audio_variation = np.std(audio_data) / 32768.0
            if audio_variation < 0.005:
                return b""
        
        return data
    
    def listen_for_command(self, timeout: float = 5.0) -> Optional[Intent]:
        """Listen for voice command and return intent."""
        if not self.running:
            print("❌ Voice recognizer not running")
            return None
        
        self.is_listening = True
        start_time = time.time()
        last_activity = time.time()
        speech_detected = False
        
        print(f"🎤 Listening for {self.language} command...")
        
        try:
            while self.running and self.is_listening:
                # Check timeout
                if time.time() - start_time > timeout:
                    print("⏰ Listening timeout")
                    break
                
                # Check silence timeout
                if time.time() - last_activity > self.SILENCE_TIMEOUT:
                    print("🔇 Silence timeout")
                    break
                
                # Read audio frame
                data = self._read_frame()
                if not data:
                    continue
                
                last_activity = time.time()
                
                # Detect speech
                if not speech_detected:
                    import numpy as np
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    mean_squared = np.mean(audio_data**2)
                    audio_level = np.sqrt(mean_squared) / 32768.0 if mean_squared > 0 else 0.0
                    audio_variation = np.std(audio_data) / 32768.0
                    
                    if audio_level > 0.02 and audio_variation > 0.01:
                        speech_detected = True
                        print("🗣️ Speech detected, processing...")
                
                # Process audio
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()
                    
                    if text and len(text) >= self.MIN_UTTERANCE_LENGTH:
                        print(f"🎯 Recognized: '{text}'")
                        
                        # Detect intent
                        intent = detect_derja_intent(text)
                        print(f"🧠 Intent: {intent.intent} (confidence: {intent.confidence:.2f})")
                        
                        self.is_listening = False
                        return intent
                
                # Process partial results
                partial_result = json.loads(self.recognizer.PartialResult())
                partial_text = partial_result.get("partial", "").strip()
                
                if partial_text and len(partial_text) >= 2:
                    print(f"📝 Partial: '{partial_text}'")
        
        except Exception as e:
            print(f"❌ Listening error: {e}")
        
        finally:
            self.is_listening = False
        
        return None
    
    def process_voice_command(self, intent: Intent) -> str:
        """Process voice command and return response."""
        try:
            # Execute action
            response = execute_derja_action(intent)
            
            # Add to memory
            add_conversation_memory(
                intent.original_text,
                response,
                intent.intent
            )
            
            return response
            
        except Exception as e:
            error_msg = f"مش قادر أعالج الأمر. خطأ: {str(e)}"
            print(f"❌ Command processing error: {e}")
            return error_msg
    
    def speak_response(self, response: str, emotion: str = "neutral"):
        """Speak response with appropriate emotion."""
        try:
            # Get conversation context
            context = get_context()
            
            # Determine emotion from response content
            if emotion == "error" or "❌" in response or "خطأ" in response:
                emotion = "concerned"
            elif "✅" in response or "نجح" in response or "زينة" in response:
                emotion = "happy"
            elif "هههه" in response or "نكتة" in response:
                emotion = "playful"
            elif "مهم" in response or "ضروري" in response:
                emotion = "professional"
            elif "تعبان" in response or "مش" in response:
                emotion = "tired"
            
            # Use emotional TTS with context
            speak_naturally(response, context)
                
        except Exception as e:
            print(f"❌ TTS error: {e}")
            speak_derja(response)
    
    def continuous_listen(self, callback=None):
        """Continuously listen for commands."""
        print("🔄 Starting continuous listening mode...")
        print("Press 'q' to quit, 'l' to stop current speech")
        
        try:
            while self.running:
                # Check for keyboard input
                if msvcrt.kbhit():
                    key = msvcrt.getwch()
                    if key == 'q':
                        print("👋 Quitting...")
                        break
                    elif key == 'l':
                        speak_derja("", interrupt=True)  # Stop current speech
                        continue
                
                # Listen for command
                intent = self.listen_for_command(timeout=1.0)
                
                if intent:
                    # Process command
                    response = self.process_voice_command(intent)
                    
                    # Speak response
                    self.speak_response(response)
                    
                    # Call callback if provided
                    if callback:
                        callback(intent, response)
                
                # Brief pause to prevent excessive CPU usage
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user")
        except Exception as e:
            print(f"❌ Continuous listening error: {e}")
        finally:
            self.stop()
    
    def set_language(self, language: str):
        """Set recognition language."""
        if language in ["en", "ar", "tn"]:
            self.language = language
            # Reinitialize model if needed
            self._init_model()
            print(f"✅ Language set to: {language}")
        else:
            print(f"❌ Unsupported language: {language}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        return {
            "running": self.running,
            "listening": self.is_listening,
            "language": self.language,
            "model_loaded": self.model is not None,
            "recognizer_loaded": self.recognizer is not None,
            "vad_available": HAS_VAD,
            "input_channels": self.input_channels
        }


def find_best_microphone() -> Optional[int]:
    """Find the best available microphone."""
    try:
        devices = sd.query_devices()
        input_devices = []
        
        for i, device in enumerate(devices):
            if device.get('max_input_channels', 0) > 0:
                device_info = {
                    'index': i,
                    'name': device.get('name', f'Device {i}'),
                    'channels': device.get('max_input_channels', 0),
                    'is_default': device.get('is_default', False),
                    'hostapi': device.get('hostapi', 0)
                }
                input_devices.append(device_info)
        
        if not input_devices:
            print("❌ No input devices found")
            return None
        
        # Sort by priority
        input_devices.sort(key=lambda x: (
            not x['is_default'],
            -x['channels'],
            x['hostapi']
        ))
        
        best_device = input_devices[0]
        print(f"✅ Auto-selected microphone: {best_device['name']} (Device {best_device['index']})")
        return best_device['index']
        
    except Exception as e:
        print(f"❌ Error detecting microphones: {e}")
        return None


def main():
    """Main function for testing."""
    print("🎤 Enhanced Luca Voice Assistant")
    print("Language options: en, ar, tn")
    
    # Get language preference
    language = input("Enter language (en/ar/tn): ").strip().lower()
    if language not in ["en", "ar", "tn"]:
        language = "en"
    
    # Find microphone
    mic_index = find_best_microphone()
    if mic_index is None:
        print("❌ No suitable microphone found")
        return
    
    # Initialize recognizer
    recognizer = EnhancedVoiceRecognizer(
        input_device=mic_index,
        language=language
    )
    
    if not recognizer.start():
        print("❌ Failed to start voice recognizer")
        return
    
    # Start continuous listening
    recognizer.continuous_listen()


if __name__ == "__main__":
    main()
