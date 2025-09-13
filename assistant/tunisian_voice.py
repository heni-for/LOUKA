#!/usr/bin/env python3
"""
Tunisian Arabic Voice Assistant - Speaks like a Tunisian friend
"""

import threading
import time
import queue
import json
import msvcrt
from typing import Optional, Dict, Any
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from rich import print

from .llm import chat_with_ai
from .tts import speak
from .smart_features import handle_smart_command, is_smart_command

class TunisianVoiceAssistant:
    def __init__(self):
        self.is_running = False
        self.is_listening = False
        self.conversation_history = []
        self.last_interaction = time.time()
        self.sleep_timeout = 30
        
        # Initialize speech recognition with Tunisian model
        self.model_path = "vosk-model-ar-tn-0.1-linto"
        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        
        # Audio settings
        self.sample_rate = 16000
        self.audio_queue = queue.Queue()
        self.stream = None
        
        # Tunisian phrases and responses
        self.tunisian_greetings = [
            "أهلا وسهلا! كيفاش؟",
            "سلام عليكم! شكون؟",
            "أهلا! شنوة الأخبار؟",
            "مرحبا! كيفاش الحال؟"
        ]
        
        self.tunisian_responses = {
            "time": "الساعة {time}",
            "weather": "الطقس اليوم {weather}",
            "email": "شوفت بريدك، عندك {count} رسالة جديدة",
            "help": "أنا هنا باش نخدمك! شنوة تحب؟",
            "joke": "سمع هاذي النكتة: {joke}",
            "goodbye": "باي! نراك باش!",
            "thanks": "العفو! أي وقت تحب!"
        }
        
    def start(self):
        """Start the Tunisian voice assistant."""
        self.is_running = True
        print("🇹🇳 Tunisian Voice Assistant is now active!")
        print("💡 Just start talking naturally - no wake words needed!")
        print("💡 Press 'l' to interrupt speech, Ctrl+C to quit")
        
        # Welcome message in Tunisian
        self.speak_tunisian("أهلا وسهلا! أنا مساعدك الذكي. كيفاش نخدمك؟")
        
        # Start listening
        self.start_listening()
        
        # Main conversation loop
        self.conversation_loop()
    
    def start_listening(self):
        """Start audio input stream."""
        try:
            self.stream = sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            )
            self.stream.start()
            self.is_listening = True
            print("🎧 Listening...")
        except Exception as e:
            print(f"❌ Audio error: {e}")
    
    def audio_callback(self, indata, frames, time, status):
        """Audio input callback."""
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(bytes(indata))
    
    def conversation_loop(self):
        """Main conversation loop."""
        while self.is_running:
            try:
                # Listen for speech
                text = self.listen_for_speech()
                
                if text:
                    self.last_interaction = time.time()
                    self.process_command(text)
                else:
                    # Check if we should go to sleep
                    if time.time() - self.last_interaction > self.sleep_timeout:
                        if self.in_conversation:
                            self.speak_tunisian("أنا هنا إذا احتجت شي!")
                            self.in_conversation = False
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in conversation loop: {e}")
                time.sleep(1)
    
    def listen_for_speech(self, timeout=5.0):
        """Listen for speech with timeout."""
        start_time = time.time()
        audio_buffer = b""
        
        while time.time() - start_time < timeout:
            try:
                # Get audio data
                if not self.audio_queue.empty():
                    data = self.audio_queue.get_nowait()
                    audio_buffer += data
                    
                    # Process when we have enough data
                    if len(audio_buffer) >= 8000:  # 0.5 seconds of audio
                        if self.recognizer.AcceptWaveform(audio_buffer):
                            result = json.loads(self.recognizer.Result())
                            text = result.get("text", "").strip()
                            if text and len(text) > 2:
                                print(f"👂 Heard: {text}")
                                return text
                        audio_buffer = b""
                
                time.sleep(0.1)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Speech recognition error: {e}")
                break
        
        return None
    
    def process_command(self, text: str):
        """Process user command in Tunisian style."""
        text_lower = text.lower().strip()
        
        # Check for conversation enders
        if any(word in text_lower for word in ["goodbye", "bye", "see you", "thanks", "thank you", "باي", "سلام"]):
            self.speak_tunisian("باي! نراك باش!")
            self.in_conversation = False
            return
        
        # Check for smart commands first
        smart_intent = is_smart_command(text)
        if smart_intent:
            self.speak_tunisian("أكيد! نخدمك!")
            response = handle_smart_command(smart_intent, text)
            # Convert response to Tunisian style
            tunisian_response = self.convert_to_tunisian_style(response, smart_intent)
            self.speak_tunisian(tunisian_response)
            self.in_conversation = True
            return
        
        # Natural conversation with AI in Tunisian style
        try:
            self.speak_tunisian("خلاص، نفكر...")
            
            # Add Tunisian context to make responses more natural
            context = """أنت مساعد ذكي يتكلم باللهجة التونسية. رد بطريقة طبيعية ومحلية مثل صديق تونسي. 
            كن ودود ومفيد، واستخدم تعبيرات تونسية مثل "كيفاش"، "شنوة"، "باش"، "أي وقت"."""
            
            response = chat_with_ai(f"{context}\n\nUser: {text}", self.conversation_history)
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": text})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            # Convert to Tunisian style
            tunisian_response = self.convert_to_tunisian_style(response)
            self.speak_tunisian(tunisian_response)
            self.in_conversation = True
            
        except Exception as e:
            self.speak_tunisian("آسف، ما فهمتش. جرب تاني؟")
            print(f"AI Chat error: {e}")
    
    def convert_to_tunisian_style(self, text: str, intent: str = None) -> str:
        """Convert English responses to Tunisian style."""
        # Common translations
        translations = {
            "Hello": "أهلا",
            "Hi": "سلام",
            "Thank you": "شكرا",
            "Yes": "أي",
            "No": "لا",
            "Good": "مزيان",
            "Bad": "مش مزيان",
            "Time": "الوقت",
            "Weather": "الطقس",
            "Email": "البريد",
            "Help": "المساعدة",
            "Sorry": "آسف",
            "Please": "من فضلك",
            "How are you": "كيفاش؟",
            "What": "شنوة",
            "When": "متى",
            "Where": "وين",
            "Why": "علاش",
            "How": "كيفاش",
            "I don't understand": "ما فهمتش",
            "Let me help": "خلاص نخدمك",
            "I'm here": "أنا هنا",
            "Good morning": "صباح الخير",
            "Good evening": "مساء الخير",
            "Good night": "تصبح على خير"
        }
        
        # Convert text
        tunisian_text = text
        for english, tunisian in translations.items():
            tunisian_text = tunisian_text.replace(english, tunisian)
        
        # Add Tunisian expressions
        if "time" in text.lower():
            tunisian_text = f"الساعة {tunisian_text}"
        elif "weather" in text.lower():
            tunisian_text = f"الطقس اليوم {tunisian_text}"
        elif "email" in text.lower():
            tunisian_text = f"شوفت بريدك، {tunisian_text}"
        
        return tunisian_text
    
    def speak_tunisian(self, text: str):
        """Speak text in Tunisian style."""
        print(f"🇹🇳 Assistant: {text}")
        
        # Use enhanced Tunisian TTS
        try:
            from .tts_tunisian import speak_tunisian as tunisian_speak
            tunisian_speak(text)
        except Exception as e:
            print(f"Tunisian TTS error: {e}")
            # Fallback to simple TTS with fresh engine
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.setProperty('rate', 180)
                engine.setProperty('volume', 0.9)
                
                # Try to find an Arabic voice
                try:
                    voices = engine.getProperty('voices')
                    arabic_voice = None
                    
                    # Voice preference order for Arabic
                    voice_preferences = [
                        'arabic', 'ar-', 'ar_', 'tunisian', 'tunisia', 
                        'arab', 'middle east', 'egyptian', 'lebanese'
                    ]
                    
                    for preference in voice_preferences:
                        for v in voices:
                            name = (getattr(v, 'name', '') or '').lower()
                            if preference in name:
                                arabic_voice = v.id
                                break
                        if arabic_voice:
                            break
                    
                    if arabic_voice:
                        engine.setProperty('voice', arabic_voice)
                        print(f"🎤 Using Arabic voice: {arabic_voice}")
                    else:
                        print("⚠️ No Arabic voice found, using default")
                        # Try to use a more natural voice
                        for v in voices:
                            name = (getattr(v, 'name', '') or '').lower()
                            if 'zira' in name or 'david' in name:
                                engine.setProperty('voice', v.id)
                                break
                        
                except Exception as e:
                    print(f"Voice selection error: {e}")
                
                engine.say(text)
                engine.runAndWait()
                
            except Exception as e2:
                print(f"Fallback TTS error: {e2}")
                print(f"🔊 [TTS Failed] {text}")
    
    def stop(self):
        """Stop the assistant."""
        self.is_running = False
        self.is_listening = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        print("👋 Assistant stopped.")

def main():
    """Main function to run Tunisian voice assistant."""
    assistant = TunisianVoiceAssistant()
    
    try:
        assistant.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        assistant.stop()

if __name__ == "__main__":
    main()
