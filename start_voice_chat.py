#!/usr/bin/env python3
"""
Start Voice Chat with Luca
Simple interactive voice chat session
"""

import sys
import os
import time
import threading
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Add the assistant directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'assistant'))

class LucaVoiceChat:
    """Simple voice chat with Luca."""
    
    def __init__(self):
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.stream = None
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 4000
        
        # Initialize components
        self._init_speech_recognition()
        self._init_tts()
        self._init_ai_chat()
    
    def _init_speech_recognition(self):
        """Initialize speech recognition."""
        self.model_path = "vosk-model-en-us-0.22"
        if not os.path.exists(self.model_path):
            print(f"❌ Vosk model not found at {self.model_path}")
            return False
        
        try:
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            print("✅ Speech recognition ready")
            return True
        except Exception as e:
            print(f"❌ Speech recognition failed: {e}")
            return False
    
    def _init_tts(self):
        """Initialize text-to-speech."""
        try:
            from assistant.google_tts_fixed import speak_arabic_fixed
            self.speak = speak_arabic_fixed
            print("✅ Text-to-speech ready")
            return True
        except Exception as e:
            print(f"❌ TTS failed: {e}")
            return False
    
    def _init_ai_chat(self):
        """Initialize AI chat."""
        try:
            from assistant.llm import chat_with_ai
            self.chat = chat_with_ai
            print("✅ AI chat ready")
            return True
        except Exception as e:
            print(f"❌ AI chat failed: {e}")
            return False
    
    def audio_callback(self, indata, frames, time, status):
        """Audio input callback."""
        self.audio_queue.put(bytes(indata))
    
    def start_listening(self):
        """Start listening for speech."""
        try:
            self.stream = sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            )
            self.stream.start()
            self.is_listening = True
        except Exception as e:
            print(f"❌ Failed to start listening: {e}")
    
    def stop_listening(self):
        """Stop listening for speech."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.is_listening = False
    
    def listen_for_speech(self, timeout=5.0):
        """Listen for speech and return recognized text."""
        if not self.is_listening:
            self.start_listening()
        
        print("🎤 Speak now...")
        start_time = time.time()
        last_activity = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if not self.audio_queue.empty():
                    data = self.audio_queue.get_nowait()
                    last_activity = time.time()
                    
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        text = result.get("text", "").strip()
                        
                        if text and len(text) > 2:
                            print(f"🎯 You said: '{text}'")
                            return text
                    
                    partial = json.loads(self.recognizer.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text and len(partial_text) > 2:
                        print(f"📝 Partial: '{partial_text}'")
                
                if time.time() - last_activity > 2.0:
                    print("⏰ Silence timeout")
                    break
                
                time.sleep(0.1)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Listening error: {e}")
                break
        
        return ""
    
    def speak_response(self, text):
        """Speak the response."""
        try:
            print(f"🔊 Luca says: '{text}'")
            self.speak(text)
        except Exception as e:
            print(f"❌ Speaking error: {e}")
    
    def chat_loop(self):
        """Main chat loop."""
        print("\n🎤 Starting Voice Chat with Luca!")
        print("=" * 50)
        print("Commands:")
        print("  - Say anything to chat")
        print("  - Say 'quit' or 'bye' to exit")
        print("  - Press Ctrl+C to stop")
        print("=" * 50)
        
        # Welcome message
        self.speak_response("مرحبا! أنا لوكا المساعد الصوتي. كيف يمكنني مساعدتك؟")
        
        try:
            while True:
                # Listen for speech
                user_input = self.listen_for_speech(timeout=8.0)
                
                if not user_input:
                    print("⏰ No speech detected, continuing...")
                    continue
                
                # Check for quit commands
                if any(word in user_input.lower() for word in ['quit', 'exit', 'stop', 'bye', 'goodbye']):
                    print("👋 Goodbye!")
                    self.speak_response("وداعا! كان من دواعي سروري مساعدتك")
                    break
                
                # Process the input
                print(f"🤔 Processing: '{user_input}'")
                
                # Get AI response
                try:
                    ai_response = self.chat(user_input)
                    print(f"🧠 AI Response: '{ai_response}'")
                    
                    # Speak the response
                    self.speak_response(ai_response)
                    
                except Exception as e:
                    error_msg = f"عذراً، حدث خطأ: {str(e)}"
                    print(f"❌ Error: {e}")
                    self.speak_response(error_msg)
                
                print("-" * 30)
                
        except KeyboardInterrupt:
            print("\n👋 Stopping voice chat...")
            self.speak_response("وداعا!")
        finally:
            self.stop_listening()

def main():
    """Main function."""
    print("🎤 Luca Voice Chat")
    print("=" * 30)
    
    # Check if required models exist
    if not os.path.exists("vosk-model-en-us-0.22"):
        print("❌ Vosk model not found!")
        print("Please download the model:")
        print("1. Go to https://alphacephei.com/vosk/models")
        print("2. Download vosk-model-en-us-0.22")
        print("3. Extract it to the current directory")
        return
    
    # Initialize chat
    chat = LucaVoiceChat()
    
    if not hasattr(chat, 'model'):
        print("❌ Failed to initialize voice system")
        return
    
    # Start chat
    chat.chat_loop()

if __name__ == "__main__":
    main()
