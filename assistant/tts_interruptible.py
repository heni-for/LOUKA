#!/usr/bin/env python3
"""
Interruptible Text-to-Speech with keyboard interrupt support
Press 'l' to stop speaking
"""

import pyttsx3
import threading
import time
import msvcrt
from typing import Optional

class InterruptibleTTS:
    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self.stop_speaking = False
        self.speak_thread = None
        self._init_engine()
        
        # Start keyboard listener thread
        self.keyboard_thread = threading.Thread(target=self._keyboard_listener, daemon=True)
        self.keyboard_thread.start()
    
    def _init_engine(self):
        """Initialize the TTS engine."""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 200)
            self.engine.setProperty('volume', 0.9)
            
            # Try to find a good voice
            voices = self.engine.getProperty('voices')
            preferred = None
            
            voice_preferences = [
                'zira', 'david', 'aria', 'hazel', 'susan', 'mark', 'richard',
                'arabic', 'tunisian', 'tunisia', 'ar-', 'ar_'
            ]
            
            for preference in voice_preferences:
                for v in voices:
                    name = (getattr(v, 'name', '') or '').lower()
                    if preference in name:
                        preferred = v.id
                        break
                if preferred:
                    break
            
            if preferred:
                self.engine.setProperty('voice', preferred)
                print(f"🎤 Using voice: {preferred}")
            else:
                print("🎤 Using default voice")
                
        except Exception as e:
            print(f"❌ TTS initialization error: {e}")
            self.engine = None
    
    def _keyboard_listener(self):
        """Listen for 'l' key press to interrupt speech."""
        while True:
            try:
                if msvcrt.kbhit():
                    key = msvcrt.getwch().lower()
                    if key == 'l' and self.is_speaking:
                        print("\n🛑 Speech interrupted by 'l' key!")
                        self.stop_speaking = True
                        # Stop the engine immediately
                        if self.engine:
                            self.engine.stop()
            except Exception as e:
                print(f"Keyboard listener error: {e}")
            time.sleep(0.1)
    
    def speak(self, text: str):
        """Speak text with interrupt capability."""
        if not self.engine:
            print("❌ TTS engine not available")
            return
        
        # Stop any current speech
        self.stop_speaking = False
        if self.is_speaking:
            self.engine.stop()
            if self.speak_thread and self.speak_thread.is_alive():
                self.speak_thread.join(timeout=0.5)
        
        # Start new speech
        self.is_speaking = True
        self.speak_thread = threading.Thread(target=self._speak_text, args=(text,), daemon=True)
        self.speak_thread.start()
    
    def _speak_text(self, text: str):
        """Internal method to speak text."""
        try:
            # Create a new engine instance for each speech to avoid conflicts
            engine = pyttsx3.init()
            engine.setProperty('rate', 200)
            engine.setProperty('volume', 0.9)
            
            # Copy voice settings from main engine
            if self.engine:
                try:
                    voice = self.engine.getProperty('voice')
                    engine.setProperty('voice', voice)
                except:
                    pass
            
            engine.say(text)
            engine.runAndWait()
            
        except Exception as e:
            print(f"❌ TTS error: {e}")
        finally:
            self.is_speaking = False
    
    def stop(self):
        """Stop current speech."""
        self.stop_speaking = True
        if self.engine and self.is_speaking:
            self.engine.stop()
        self.is_speaking = False

# Global instance
_tts = InterruptibleTTS()

def speak(text: str):
    """Speak text with interrupt capability. Press 'l' to stop."""
    _tts.speak(text)

def stop_speaking():
    """Stop current speech."""
    _tts.stop()

def is_speaking():
    """Check if currently speaking."""
    return _tts.is_speaking