#!/usr/bin/env python3
"""
Tunisian Derja Voice Chat
Uses the correct Tunisian Arabic Vosk model for speech recognition
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

class TunisianVoiceChat:
    """Tunisian Derja voice chat with proper model."""
    
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
        """Initialize Tunisian Derja speech recognition."""
        # Use the Tunisian model
        self.model_path = "vosk-model-ar-tn-0.1-linto"
        
        if not os.path.exists(self.model_path):
            print(f"❌ Tunisian model not found at {self.model_path}")
            print("Please ensure the model is downloaded and extracted")
            return False
        
        try:
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            print(f"✅ Tunisian Derja model loaded: {self.model_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to load Tunisian model: {e}")
            return False
    
    def _init_tts(self):
        """Initialize text-to-speech."""
        try:
            from assistant.google_tts_fixed import speak_arabic_fixed
            self.speak = speak_arabic_fixed
            print("✅ Tunisian TTS ready")
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
            print("🎤 Listening for Tunisian Derja...")
        except Exception as e:
            print(f"❌ Failed to start listening: {e}")
    
    def stop_listening(self):
        """Stop listening for speech."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.is_listening = False
            print("🔇 Listening stopped")
    
    def listen_for_speech(self, timeout=5.0):
        """Listen for Tunisian Derja speech and return recognized text."""
        if not self.is_listening:
            self.start_listening()
        
        print("🎤 تكلم الآن باللهجة التونسية...")
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
                            print(f"🎯 تم التعرف على: '{text}'")
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
    
    def speak_response(self, text, emotion="neutral"):
        """Speak the response in Tunisian Derja."""
        try:
            print(f"🔊 لوكا يقول: '{text}'")
            self.speak(text, emotion)
        except Exception as e:
            print(f"❌ خطأ في التحدث: {e}")
    
    def chat_loop(self):
        """Main Tunisian Derja chat loop."""
        print("\n🎤 بدء المحادثة الصوتية مع لوكا باللهجة التونسية!")
        print("=" * 60)
        print("الأوامر:")
        print("  - تكلم باللهجة التونسية")
        print("  - قل 'وداعا' أو 'مع السلامة' للخروج")
        print("  - اضغط Ctrl+C للتوقف")
        print("=" * 60)
        
        # Welcome message in Tunisian Derja
        self.speak_response("أهلا وسهلا! أنا لوكا المساعد الصوتي. شنو نعمل اليوم؟", "happy")
        
        try:
            while True:
                # Listen for Tunisian Derja speech
                user_input = self.listen_for_speech(timeout=8.0)
                
                if not user_input:
                    print("⏰ ما تم التعرف على كلام، نكمل...")
                    continue
                
                # Check for quit commands in Tunisian
                quit_words = ['quit', 'exit', 'stop', 'bye', 'وداعا', 'مع السلامة', 'باي', 'سلام']
                if any(word in user_input.lower() for word in quit_words):
                    print("👋 وداعا!")
                    self.speak_response("وداعا! كان من دواعي سروري مساعدتك", "calm")
                    break
                
                # Process the input
                print(f"🤔 معالجة: '{user_input}'")
                
                # Get AI response
                try:
                    ai_response = self.chat(user_input)
                    print(f"🧠 رد الذكاء الاصطناعي: '{ai_response}'")
                    
                    # Speak the response
                    self.speak_response(ai_response, "neutral")
                    
                except Exception as e:
                    error_msg = f"عذراً، حدث خطأ: {str(e)}"
                    print(f"❌ خطأ: {e}")
                    self.speak_response(error_msg, "concerned")
                
                print("-" * 30)
                
        except KeyboardInterrupt:
            print("\n👋 إيقاف المحادثة الصوتية...")
            self.speak_response("وداعا!")
        finally:
            self.stop_listening()
    
    def test_tunisian_recognition(self):
        """Test Tunisian Derja recognition only."""
        print("🧪 اختبار التعرف على اللهجة التونسية")
        print("-" * 40)
        
        self.start_listening()
        
        try:
            for i in range(3):
                print(f"اختبار {i+1}/3: تكلم باللهجة التونسية...")
                text = self.listen_for_speech(timeout=5.0)
                
                if text:
                    print(f"✅ تم التعرف على: '{text}'")
                else:
                    print("❌ لم يتم التعرف على كلام")
                
                time.sleep(1)
                
        finally:
            self.stop_listening()
    
    def test_tunisian_phrases(self):
        """Test specific Tunisian Derja phrases."""
        print("🧪 اختبار العبارات التونسية")
        print("-" * 30)
        
        test_phrases = [
            "أهلا وسهلا",
            "شنو نعمل اليوم؟",
            "كيف حالك؟",
            "شكرا لك",
            "وداعا"
        ]
        
        for phrase in test_phrases:
            print(f"اختبار: '{phrase}'")
            self.speak_response(phrase)
            time.sleep(2)

def main():
    """Main function."""
    print("🎤 لوكا - المحادثة الصوتية باللهجة التونسية")
    print("=" * 50)
    
    # Check if Tunisian model exists
    if not os.path.exists("vosk-model-ar-tn-0.1-linto"):
        print("❌ نموذج اللهجة التونسية غير موجود!")
        print("يرجى تحميل النموذج:")
        print("1. اذهب إلى https://alphacephei.com/vosk/models")
        print("2. حمل vosk-model-ar-tn-0.1-linto")
        print("3. استخرج الملفات في المجلد الحالي")
        return
    
    # Initialize chat
    chat = TunisianVoiceChat()
    
    if not hasattr(chat, 'model'):
        print("❌ فشل في تهيئة نظام الصوت")
        return
    
    print("\nاختر وضع الاختبار:")
    print("1. محادثة صوتية كاملة (تفاعلية)")
    print("2. اختبار التعرف على الصوت فقط")
    print("3. اختبار العبارات التونسية")
    print("4. جميع الاختبارات")
    
    try:
        choice = input("\nأدخل الاختيار (1-4): ").strip()
        
        if choice == "1":
            chat.chat_loop()
        elif choice == "2":
            chat.test_tunisian_recognition()
        elif choice == "3":
            chat.test_tunisian_phrases()
        elif choice == "4":
            chat.test_tunisian_phrases()
            print()
            chat.test_tunisian_recognition()
            print()
            chat.chat_loop()
        else:
            print("اختيار غير صحيح، تشغيل المحادثة الصوتية...")
            chat.chat_loop()
            
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")

if __name__ == "__main__":
    main()
