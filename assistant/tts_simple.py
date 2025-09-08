#!/usr/bin/env python3
"""
Simple TTS using Windows SAPI5 voices
"""

import pyttsx3
import threading
import time

class SimpleTTS:
    def __init__(self):
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize the TTS engine."""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 200)  # Natural speech rate
            self.engine.setProperty('volume', 1.0)
            
            # Try to find an Arabic voice
            voices = self.engine.getProperty('voices')
            arabic_voice = None
            
            for voice in voices:
                name = (getattr(voice, 'name', '') or '').lower()
                if any(keyword in name for keyword in ['arabic', 'ar-', 'ar_', 'tunisian']):
                    arabic_voice = voice.id
                    break
            
            if arabic_voice:
                self.engine.setProperty('voice', arabic_voice)
                print(f"🎤 Using Arabic voice: {arabic_voice}")
            else:
                print("⚠️ No Arabic voice found, using default")
                
        except Exception as e:
            print(f"❌ TTS initialization error: {e}")
            self.engine = None
    
    def speak(self, text: str):
        """Speak the given text."""
        if not self.engine:
            print("❌ TTS engine not available")
            return
        
        try:
            # Run TTS in a separate thread to avoid blocking
            def speak_thread():
                self.engine.say(text)
                self.engine.runAndWait()
            
            thread = threading.Thread(target=speak_thread, daemon=True)
            thread.start()
            
        except Exception as e:
            print(f"❌ TTS error: {e}")

# Global instance
_tts = SimpleTTS()

def speak(text: str):
    """Speak text using simple TTS."""
    _tts.speak(text)
