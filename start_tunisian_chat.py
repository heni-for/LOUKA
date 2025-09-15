#!/usr/bin/env python3
"""
Start Tunisian Derja Voice Chat
Simple interactive chat using the correct Tunisian model
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

class TunisianChat:
    """Simple Tunisian Derja voice chat."""
    
    def __init__(self):
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.stream = None
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 4000
        
        # Initialize components
        self._init_tunisian_model()
        self._init_tts()
        self._init_ai_chat()
    
    def _init_tunisian_model(self):
        """Initialize Tunisian Derja model."""
        self.model_path = "vosk-model-ar-tn-0.1-linto"
        
        if not os.path.exists(self.model_path):
            print(f"❌ Tunisian model not found at {self.model_path}")
            return False
        
        try:
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            print("✅ Tunisian Derja model loaded!")
            return True
        except Exception as e:
            print(f"❌ Failed to load Tunisian model: {e}")
            return False
    
    def _init_tts(self):
        """Initialize TTS."""
        try:
            from assistant.google_tts_fixed import speak_arabic_fixed
            self.speak = speak_arabic_fixed
            print("✅ TTS ready")
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
        """Listen for Tunisian Derja speech."""
        if not self.is_listening:
            self.start_listening()
        
        print("🎤 تكلم باللهجة التونسية...")
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
                            print(f"🎯 قلت: '{text}'")
                            return text
                    
                    partial = json.loads(self.recognizer.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text and len(partial_text) > 2:
                        print(f"📝 جزئي: '{partial_text}'")
                
                if time.time() - last_activity > 2.0:
                    print("⏰ انتهى وقت الصمت")
                    break
                
                time.sleep(0.1)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ خطأ في الاستماع: {e}")
                break
        
        return ""
    
    def speak_response(self, text):
        """Speak the response."""
        try:
            print(f"🔊 لوكا يقول: '{text}'")
            self.speak(text)
        except Exception as e:
            print(f"❌ خطأ في التحدث: {e}")
    
    def chat_loop(self):
        """Main chat loop."""
        print("\n🎤 مرحبا! أنا لوكا المساعد الصوتي")
        print("=" * 50)
        print("تكلم باللهجة التونسية:")
        print("  - 'أهلا وسهلا' للترحيب")
        print("  - 'شنو نعمل اليوم؟' للسؤال")
        print("  - 'وداعا' للخروج")
        print("=" * 50)
        
        # Welcome message
        self.speak_response("أهلا وسهلا! أنا لوكا المساعد الصوتي. شنو نعمل اليوم؟")
        
        try:
            while True:
                # Listen for speech
                user_input = self.listen_for_speech(timeout=8.0)
                
                if not user_input:
                    print("⏰ ما تم التعرف على كلام، نكمل...")
                    continue
                
                # Check for quit commands
                if any(word in user_input.lower() for word in ['quit', 'exit', 'stop', 'bye', 'وداعا', 'مع السلامة']):
                    print("👋 وداعا!")
                    self.speak_response("وداعا! كان من دواعي سروري مساعدتك")
                    break
                
                # Process the input
                print(f"🤔 معالجة: '{user_input}'")
                
                # Get AI response
                try:
                    ai_response = self.chat(user_input)
                    print(f"🧠 رد الذكاء الاصطناعي: '{ai_response}'")
                    
                    # Speak the response
                    self.speak_response(ai_response)
                    
                except Exception as e:
                    error_msg = f"عذراً، حدث خطأ: {str(e)}"
                    print(f"❌ خطأ: {e}")
                    self.speak_response(error_msg)
                
                print("-" * 30)
                
        except KeyboardInterrupt:
            print("\n👋 إيقاف المحادثة...")
            self.speak_response("وداعا!")
        finally:
            self.stop_listening()

def main():
    """Main function."""
    print("🎤 لوكا - المحادثة الصوتية باللهجة التونسية")
    print("=" * 50)
    
    # Check if Tunisian model exists
    if not os.path.exists("vosk-model-ar-tn-0.1-linto"):
        print("❌ نموذج اللهجة التونسية غير موجود!")
        return
    
    # Initialize chat
    chat = TunisianChat()
    
    if not hasattr(chat, 'model'):
        print("❌ فشل في تهيئة النظام")
        return
    
    # Start chat
    chat.chat_loop()

if __name__ == "__main__":
    main()
