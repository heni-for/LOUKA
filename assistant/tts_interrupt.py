#!/usr/bin/env python3
"""
Simple TTS interrupt mechanism using keyboard listener
Press 'l' to stop current speech
"""

import threading
import msvcrt
import time
import pyttsx3

class TTSInterrupt:
    def __init__(self):
        self.should_stop = False
        self.is_speaking = False
        self.engine = None
        self.speak_thread = None
        
        # Start keyboard listener
        self.keyboard_thread = threading.Thread(target=self._keyboard_listener, daemon=True)
        self.keyboard_thread.start()
    
    def _keyboard_listener(self):
        """Listen for 'l' key press to interrupt speech."""
        while True:
            try:
                if msvcrt.kbhit():
                    key = msvcrt.getwch().lower()
                    if key == 'l' and self.is_speaking:
                        print("\n🛑 Speech interrupted by 'l' key!")
                        self.should_stop = True
                        if self.engine:
                            self.engine.stop()
            except Exception as e:
                pass
            time.sleep(0.1)
    
    def speak(self, text: str):
        """Speak text with interrupt capability."""
        self.should_stop = False
        self.is_speaking = True
        
        # Stop any existing speech
        if self.engine:
            self.engine.stop()
        
        # Create new engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200)
        self.engine.setProperty('volume', 0.9)
        
        # Try to find a good voice
        try:
            voices = self.engine.getProperty('voices')
            preferred = None
            voice_preferences = ['zira', 'david', 'aria', 'hazel', 'susan', 'mark', 'richard']
            
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
        except:
            pass
        
        # Speak in a separate thread
        self.speak_thread = threading.Thread(target=self._speak_text, daemon=True)
        self.speak_thread.start()
    
    def _speak_text(self):
        """Internal method to speak text."""
        try:
            self.engine.say("Hello, this is a test. Press l to stop me from talking.")
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {e}")
        finally:
            self.is_speaking = False
    
    def stop(self):
        """Stop current speech."""
        self.should_stop = True
        if self.engine:
            self.engine.stop()
        self.is_speaking = False

# Global instance
_tts_interrupt = TTSInterrupt()

def speak_with_interrupt(text: str):
    """Speak text with 'l' key interrupt capability."""
    _tts_interrupt.speak(text)

def stop_speech():
    """Stop current speech."""
    _tts_interrupt.stop()

def is_speaking():
    """Check if currently speaking."""
    return _tts_interrupt.is_speaking
