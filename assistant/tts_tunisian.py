#!/usr/bin/env python3
"""
Tunisian Arabic Text-to-Speech with authentic pronunciation
"""

import pyttsx3
import threading
import time
import requests
import tempfile
import subprocess
import os
from typing import Optional

class TunisianTTS:
    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self._init_engine()
    
    def _init_engine(self):
        """Initialize the TTS engine with Arabic voice."""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 180)  # Slower for Arabic
            self.engine.setProperty('volume', 0.9)
            
            # Try to find an Arabic voice
            voices = self.engine.getProperty('voices')
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
                self.engine.setProperty('voice', arabic_voice)
                print(f"🎤 Using Arabic voice: {arabic_voice}")
            else:
                print("⚠️ No Arabic voice found, using default")
                # Try to use a more natural voice
                for v in voices:
                    name = (getattr(v, 'name', '') or '').lower()
                    if 'zira' in name or 'david' in name:
                        self.engine.setProperty('voice', v.id)
                        break
                
        except Exception as e:
            print(f"❌ TTS initialization error: {e}")
            self.engine = None
    
    def speak_tunisian(self, text: str):
        """Speak text in Tunisian Arabic style."""
        try:
            # Convert text to proper Arabic if needed
            arabic_text = self.convert_to_arabic(text)
            
            # Create fresh engine for each speech to avoid conflicts
            engine = pyttsx3.init()
            engine.setProperty('rate', 180)  # Slower for Arabic
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
            
            engine.say(arabic_text)
            engine.runAndWait()
            
        except Exception as e:
            print(f"❌ TTS error: {e}")
            print(f"🔊 [TTS Failed] {text}")
    
    def convert_to_arabic(self, text: str) -> str:
        """Convert text to proper Arabic script."""
        # Common Tunisian expressions and their Arabic equivalents
        tunisian_to_arabic = {
            # Greetings
            "أهلا وسهلا": "أهلاً وسهلاً",
            "كيفاش": "كيف حالك",
            "شنوة": "ماذا",
            "باش": "لكي",
            "أي وقت": "أي وقت",
            "خلاص": "حسناً",
            "مزيان": "جيد",
            "مش مزيان": "ليس جيد",
            "آسف": "آسف",
            "شكرا": "شكراً",
            "من فضلك": "من فضلك",
            
            # Time expressions
            "الساعة": "الوقت",
            "اليوم": "اليوم",
            "الليلة": "الليلة",
            "الصبح": "الصباح",
            "المسا": "المساء",
            
            # Common phrases
            "أنا هنا": "أنا هنا",
            "نخدمك": "أخدمك",
            "ما فهمتش": "لم أفهم",
            "جرب تاني": "جرب مرة أخرى",
            "نراك باش": "أراك لاحقاً",
            "باي": "وداعاً",
            "سلام": "سلام",
            
            # Email related
            "البريد": "البريد الإلكتروني",
            "الرسالة": "الرسالة",
            "الجديد": "الجديد",
            "المقروء": "المقروء",
            "غير المقروء": "غير المقروء"
        }
        
        # Convert text
        arabic_text = text
        for tunisian, arabic in tunisian_to_arabic.items():
            arabic_text = arabic_text.replace(tunisian, arabic)
        
        return arabic_text
    
    def speak_online_arabic(self, text: str):
        """Try online Arabic TTS as fallback."""
        try:
            # Use Google Translate TTS for Arabic
            url = "https://translate.google.com/translate_tts"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://translate.google.com/',
                'Accept': 'audio/mpeg,audio/*,*/*;q=0.9'
            }
            params = {
                'ie': 'UTF-8',
                'q': text,
                'tl': 'ar',  # Arabic
                'client': 'tw-ob',
                'idx': '0',
                'total': '1',
                'textlen': str(len(text)),
                'tk': '0'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file.write(response.content)
                    tmp_file_path = tmp_file.name
                
                # Play the audio file
                try:
                    subprocess.run(['start', tmp_file_path], shell=True, check=True)
                except:
                    os.startfile(tmp_file_path)
                
                # Clean up after a delay
                def cleanup():
                    time.sleep(5)
                    try:
                        os.unlink(tmp_file_path)
                    except:
                        pass
                threading.Thread(target=cleanup, daemon=True).start()
                
            else:
                print(f"Online TTS Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"Online Arabic TTS Error: {e}")

# Global instance
_tunisian_tts = TunisianTTS()

def speak_tunisian(text: str):
    """Speak text in Tunisian Arabic style."""
    _tunisian_tts.speak_tunisian(text)

def speak_online_arabic(text: str):
    """Speak text using online Arabic TTS."""
    _tunisian_tts.speak_online_arabic(text)
