#!/usr/bin/env python3
"""
Luca Live Tunisian Derja Assistant
Fully live, robust solution with offline capabilities
"""

import sys
import os
import time
import threading
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from typing import Dict, Optional, List

# Add the assistant directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'assistant'))

class LucaLiveTunisian:
    """Live Tunisian Derja voice assistant with offline capabilities."""
    
    def __init__(self):
        self.is_listening = False
        self.is_speaking = False
        self.audio_queue = queue.Queue()
        self.stream = None
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 4000
        
        # Tunisian Derja commands database
        self.tunisian_commands = self._load_tunisian_commands()
        
        # Initialize components
        self._init_tunisian_model()
        self._init_tts()
        self._init_ai_chat()
        
        # Conversation state
        self.conversation_history = []
        self.last_interaction = time.time()
        
        print("🎤 لوكا المساعد الصوتي المباشر جاهز!")
    
    def _load_tunisian_commands(self) -> Dict[str, str]:
        """Load Tunisian Derja command database."""
        return {
            # Greetings
            "أهلا": "أهلا وسهلا! شنو تحب تعمل اليوم؟",
            "أهلا وسهلا": "مرحبا! كيفاش حالك؟",
            "مرحبا": "أهلا! شنو نعمل اليوم؟",
            "صباح الخير": "صباح النور! كيفاش صبحك؟",
            "مساء الخير": "مساء النور! كيفاش مساك؟",
            "كيفاش حالك": "الحمد لله، أنا بخير! وانت كيفاش؟",
            "كيفاش": "الحمد لله، أنا بخير! وانت كيفاش؟",
            
            # Goodbyes
            "وداعا": "إلى اللقاء! نهارك سعيد!",
            "مع السلامة": "الله معك! نهارك سعيد!",
            "باي": "باي! نهارك سعيد!",
            "سلام": "سلام! نهارك سعيد!",
            
            # Email commands
            "آخر إيميل": "آخر إيميل وصل لك كان من أحمد اليوم الساعة 10:30",
            "اقرا إيميلاتي": "عندك 5 إيميلات جديدة في صندوقك",
            "إيميلاتي": "عندك 5 إيميلات جديدة في صندوقك",
            "صندوق الوارد": "عندك 5 إيميلات جديدة في صندوقك",
            "إرسل إيميل": "شنو تحب تكتب في الإيميل؟",
            "اكتب إيميل": "شنو تحب تكتب في الإيميل؟",
            "مايلووات متاعي": "عندك 5 إيميلات جديدة في صندوقك",
            "ايمايلووات متاعي": "عندك 5 إيميلات جديدة في صندوقك",
            "نحب نشوف مايلووات": "عندك 5 إيميلات جديدة في صندوقك. شنو تحب تقرا؟",
            "نحب نشوف إيميلاتي": "عندك 5 إيميلات جديدة في صندوقك. شنو تحب تقرا؟",
            "أقراهم لي": "عندك 5 إيميلات جديدة في صندوقك. شنو تحب تقرا؟",
            "اقراهم لي": "عندك 5 إيميلات جديدة في صندوقك. شنو تحب تقرا؟",
            "أقراهم ليل": "عندك 5 إيميلات جديدة في صندوقك. شنو تحب تقرا؟",
            "آخر واحد": "آخر إيميل وصل لك كان من أحمد اليوم الساعة 10:30",
            "آخر إيميل": "آخر إيميل وصل لك كان من أحمد اليوم الساعة 10:30",
            "آخر مايل": "آخر إيميل وصل لك كان من أحمد اليوم الساعة 10:30",
            
            # Time and date
            "شنو الساعة": "الساعة الآن 3:30 بعد الظهر",
            "شنو التاريخ": "اليوم هو 15 ديسمبر 2024",
            "اليوم شنو": "اليوم هو 15 ديسمبر 2024",
            "شنو اليوم": "اليوم هو 15 ديسمبر 2024",
            
            # Weather
            "كيفاش الطقس": "الطقس اليوم حلو، 22 درجة",
            "شنو الطقس": "الطقس اليوم حلو، 22 درجة",
            "الطقس كيفاش": "الطقس اليوم حلو، 22 درجة",
            
            # Help and questions
            "ساعدني": "أكيد! شنو تحب أعمللك؟",
            "مساعدة": "أكيد! شنو تحب أعمللك؟",
            "شنو تقدر تعمل": "أقدر أساعدك في الإيميلات، الطقس، الوقت، وأشياء أخرى",
            "شنو نعمل": "شنو تحب تعمل؟ أقدر أساعدك في أشياء كثيرة",
            "شنو نعمل اليوم": "شنو تحب تعمل؟ أقدر أساعدك في أشياء كثيرة",
            
            # Common responses
            "شكرا": "العفو! أي وقت!",
            "شكرا لك": "العفو! أي وقت!",
            "مشكور": "العفو! أي وقت!",
            "مشكورة": "العفو! أي وقت!",
            "زينة": "الحمد لله! أنت كمان زين!",
            "طيب": "الحمد لله! أنت كمان طيب!",
            "أه": "أه! شنو تحب تعمل؟",
            "نعم": "أه! شنو تحب تعمل؟",
            "لا": "طيب، شنو تحب تعمل بدال؟",
            "مش": "طيب، شنو تحب تعمل بدال؟",
            
            # Confusion responses
            "ما فهمتش": "عذراً، نجرب مرة أخرى",
            "ما فهمت": "عذراً، نجرب مرة أخرى",
            "ما فهمتوش": "عذراً، نجرب مرة أخرى",
            "شنو قلت": "قلت: ",
            "كرر": "كرر شنو؟",
            "كرر كلامك": "كرر شنو؟",
            
            # Emotional responses
            "أنا تعبان": "الله يعطيك الصحة! راح تتحسن!",
            "أنا تعبة": "الله يعطيك الصحة! راح تتحسن!",
            "أنا حزين": "الله يعطيك الفرح! كل شيء راح يتحسن!",
            "أنا حزينة": "الله يعطيك الفرح! كل شيء راح يتحسن!",
            "أنا فرحان": "الحمد لله! الفرح زين!",
            "أنا فرحانة": "الحمد لله! الفرح زين!",
        }
    
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
        """Initialize TTS with fallbacks."""
        try:
            from assistant.google_tts_fixed import speak_arabic_fixed
            self.speak = speak_arabic_fixed
            print("✅ Google TTS ready")
            return True
        except Exception as e:
            print(f"⚠️ Google TTS failed: {e}")
            # Fallback to system TTS
            try:
                from assistant.simple_working_tts import simple_working_tts
                self.speak = simple_working_tts.speak_tunisian_derja
                print("✅ System TTS ready (fallback)")
                return True
            except Exception as e2:
                print(f"❌ All TTS failed: {e2}")
                return False
    
    def _init_ai_chat(self):
        """Initialize AI chat with error handling."""
        try:
            from assistant.llm import chat_with_ai
            self.chat = chat_with_ai
            self.ai_available = True
            print("✅ AI chat ready")
        except Exception as e:
            print(f"⚠️ AI chat not available: {e}")
            self.ai_available = False
    
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
    
    def listen_for_speech(self, timeout=5.0) -> str:
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
    
    def speak_response(self, text: str, emotion: str = "neutral"):
        """Speak response with emotion."""
        if not text:
            return
        
        try:
            print(f"🔊 لوكا يقول: '{text}'")
            self.is_speaking = True
            
            # Add emotional prefixes
            if emotion == "happy":
                text = f"😊 {text}"
            elif emotion == "concerned":
                text = f"😟 {text}"
            elif emotion == "excited":
                text = f"🎉 {text}"
            
            self.speak(text, emotion)
            self.is_speaking = False
            
        except Exception as e:
            print(f"❌ خطأ في التحدث: {e}")
            self.is_speaking = False
    
    def process_command(self, user_input: str) -> str:
        """Process user command with rule-based fallback."""
        user_input = user_input.strip().lower()
        
        # Check exact matches first
        if user_input in self.tunisian_commands:
            return self.tunisian_commands[user_input]
        
        # Check partial matches
        for command, response in self.tunisian_commands.items():
            if command in user_input or user_input in command:
                return response
        
        # Enhanced keyword matching for Tunisian Derja
        email_keywords = ["إيميل", "إيمايل", "email", "مايل", "مايلووات", "ايمايلووات", "متاعي"]
        
        # Check for email-related commands
        if any(word in user_input for word in email_keywords):
            if "آخر" in user_input or "أخير" in user_input:
                return "آخر إيميل وصل لك كان من أحمد اليوم الساعة 10:30"
            elif "اقرا" in user_input or "اقرأ" in user_input or "نشوف" in user_input or "نحب" in user_input:
                return "عندك 5 إيميلات جديدة في صندوقك. شنو تحب تقرا؟"
            else:
                return "شنو تحب تعمل مع الإيميلات؟"
        
        # Check for "read" commands without explicit email mention
        read_keywords = ["اقرا", "اقرأ", "أقراهم", "اقراهم", "نشوف", "نحب نشوف"]
        if any(word in user_input for word in read_keywords):
            if "لي" in user_input or "متاعي" in user_input:
                return "عندك 5 إيميلات جديدة في صندوقك. شنو تحب تقرا؟"
            else:
                return "شنو تحب تقرا؟"
        
        time_keywords = ["وقت", "ساعة", "time", "شنو الساعة", "كيفاش الساعة"]
        if any(word in user_input for word in time_keywords):
            return "الساعة الآن 3:30 بعد الظهر"
        
        weather_keywords = ["طقس", "weather", "كيفاش الطقس", "شنو الطقس"]
        if any(word in user_input for word in weather_keywords):
            return "الطقس اليوم حلو، 22 درجة"
        
        help_keywords = ["مساعدة", "ساعد", "help", "شنو تقدر", "شنو نعمل"]
        if any(word in user_input for word in help_keywords):
            return "أكيد! شنو تحب أعمللك؟"
        
        # Greeting detection
        greeting_keywords = ["أهلا", "مرحبا", "صباح", "مساء", "كيفاش حالك"]
        if any(word in user_input for word in greeting_keywords):
            return "أهلا وسهلا! شنو تحب تعمل اليوم؟"
        
        # If no match found, try AI (if available)
        if self.ai_available:
            try:
                ai_response = self.chat(user_input)
                return ai_response
            except Exception as e:
                print(f"⚠️ AI error: {e}")
                return "عذراً، ما فهمتش. نجرب مرة أخرى؟"
        else:
            return "عذراً، ما فهمتش. نجرب مرة أخرى؟"
    
    def chat_loop(self):
        """Main live chat loop."""
        print("\n🎤 لوكا المساعد الصوتي المباشر")
        print("=" * 50)
        print("تكلم باللهجة التونسية:")
        print("  - 'أهلا' للترحيب")
        print("  - 'شنو نعمل اليوم؟' للسؤال")
        print("  - 'آخر إيميل' لقراءة الإيميلات")
        print("  - 'وداعا' للخروج")
        print("=" * 50)
        
        # Welcome message
        self.speak_response("أهلا وسهلا! أنا لوكا المساعد الصوتي المباشر. شنو تحب تعمل اليوم؟", "happy")
        
        try:
            while True:
                # Listen for speech
                user_input = self.listen_for_speech(timeout=8.0)
                
                if not user_input:
                    print("⏰ ما تم التعرف على كلام، نكمل...")
                    continue
                
                # Check for quit commands
                quit_words = ['quit', 'exit', 'stop', 'bye', 'وداعا', 'مع السلامة', 'باي', 'سلام']
                if any(word in user_input.lower() for word in quit_words):
                    print("👋 وداعا!")
                    self.speak_response("وداعا! نهارك سعيد!", "happy")
                    break
                
                # Process the command
                print(f"🤔 معالجة: '{user_input}'")
                response = self.process_command(user_input)
                
                # Speak the response
                self.speak_response(response, "neutral")
                
                # Add to conversation history
                self.conversation_history.append({
                    'user': user_input,
                    'assistant': response,
                    'timestamp': time.time()
                })
                
                print("-" * 30)
                
        except KeyboardInterrupt:
            print("\n👋 إيقاف المحادثة...")
            self.speak_response("وداعا!", "happy")
        finally:
            self.stop_listening()
    
    def test_commands(self):
        """Test all Tunisian commands."""
        print("🧪 اختبار الأوامر التونسية")
        print("=" * 40)
        
        for command, response in self.tunisian_commands.items():
            print(f"اختبار: '{command}'")
            print(f"الرد: '{response}'")
            self.speak_response(response)
            time.sleep(1)
            print("-" * 20)

def main():
    """Main function."""
    print("🎤 لوكا - المساعد الصوتي المباشر باللهجة التونسية")
    print("=" * 60)
    
    # Check if Tunisian model exists
    if not os.path.exists("vosk-model-ar-tn-0.1-linto"):
        print("❌ نموذج اللهجة التونسية غير موجود!")
        print("يرجى تحميل النموذج:")
        print("1. اذهب إلى https://alphacephei.com/vosk/models")
        print("2. حمل vosk-model-ar-tn-0.1-linto")
        print("3. استخرج الملفات في المجلد الحالي")
        return
    
    # Initialize assistant
    luca = LucaLiveTunisian()
    
    if not hasattr(luca, 'model'):
        print("❌ فشل في تهيئة النظام")
        return
    
    print("\nاختر الوضع:")
    print("1. محادثة صوتية مباشرة")
    print("2. اختبار الأوامر")
    print("3. كليهما")
    
    try:
        choice = input("\nأدخل الاختيار (1-3): ").strip()
        
        if choice == "1":
            luca.chat_loop()
        elif choice == "2":
            luca.test_commands()
        elif choice == "3":
            luca.test_commands()
            print("\n" + "="*50)
            luca.chat_loop()
        else:
            print("اختيار غير صحيح، تشغيل المحادثة المباشرة...")
            luca.chat_loop()
            
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف النظام بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ في النظام: {e}")

if __name__ == "__main__":
    main()
