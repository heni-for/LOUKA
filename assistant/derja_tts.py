#!/usr/bin/env python3
"""
Tunisian Derja Text-to-Speech System
Provides natural-sounding Tunisian Arabic voice synthesis
"""

import pyttsx3
import threading
import time
from typing import Optional, Dict, List
from .config import GEMINI_API_KEY

class DerjaTTS:
    """Tunisian Derja Text-to-Speech engine."""
    
    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self.current_text = ""
        self.stop_event = threading.Event()
        self._init_engine()
    
    def _init_engine(self):
        """Initialize TTS engine with Tunisian-optimized settings."""
        try:
            self.engine = pyttsx3.init()
            
            # Set properties for better Tunisian pronunciation
            self.engine.setProperty('rate', 180)  # Slightly slower for clarity
            self.engine.setProperty('volume', 0.9)
            
            # Try to find the best voice for Arabic/Tunisian
            voices = self.engine.getProperty('voices')
            best_voice = self._find_best_voice(voices)
            
            if best_voice:
                self.engine.setProperty('voice', best_voice)
                print(f"Using voice: {best_voice}")
            
            # Set up event callbacks
            self.engine.connect('started-utterance', self._on_start)
            self.engine.connect('finished-utterance', self._on_finish)
            
        except Exception as e:
            print(f"TTS engine initialization error: {e}")
            self.engine = None
    
    def _find_best_voice(self, voices) -> Optional[str]:
        """Find the best voice for Tunisian Arabic."""
        if not voices:
            return None
        
        # Voice preferences for Arabic/Tunisian
        voice_preferences = [
            'arabic', 'tunisian', 'tunisia', 'ar-', 'ar_',
            'zira', 'david', 'aria', 'hazel', 'susan'
        ]
        
        for preference in voice_preferences:
            for voice in voices:
                name = (getattr(voice, 'name', '') or '').lower()
                if preference in name:
                    return voice.id
        
        # Fallback to first available voice
        return voices[0].id if voices else None
    
    def _on_start(self, name):
        """Called when speech starts."""
        self.is_speaking = True
        self.stop_event.clear()
        print("🎤 Speaking...")
    
    def _on_finish(self, name, completed):
        """Called when speech finishes."""
        self.is_speaking = False
        self.stop_event.set()
        if completed:
            print("✅ Speech completed")
        else:
            print("⏹️ Speech interrupted")
    
    def speak_derja(self, text: str, interrupt: bool = True) -> bool:
        """Speak Tunisian Derja text with natural pronunciation."""
        if not self.engine:
            print("❌ TTS engine not available")
            return False
        
        try:
            # Preprocess text for better Tunisian pronunciation
            processed_text = self._preprocess_derja_text(text)
            self.current_text = processed_text
            
            # Stop current speech if interrupting
            if interrupt and self.is_speaking:
                self.stop_speaking()
                time.sleep(0.1)  # Brief pause
            
            # Speak the text
            self.engine.say(processed_text)
            self.engine.runAndWait()
            
            return True
            
        except Exception as e:
            print(f"TTS error: {e}")
            return False
    
    def _preprocess_derja_text(self, text: str) -> str:
        """Preprocess text for better Tunisian pronunciation."""
        # Convert common Derja words to more pronounceable forms
        derja_replacements = {
            # Common Derja words
            'أهلا': 'أهلا وسهلا',
            'وينك': 'وينك كيفاش',
            'شنادي': 'شنادي نعمل',
            'أعطيني': 'أعطيني',
            'أعطني': 'أعطني',
            'حضر': 'حضر',
            'أبعت': 'أبعت',
            'أقرا': 'أقرا',
            'نظم': 'نظم',
            'رتب': 'رتب',
            
            # Common phrases
            'مش قادر': 'مش قادر',
            'مفيش': 'مفيش',
            'تقدر': 'تقدر',
            'جرب': 'جرب',
            'تاني': 'تاني',
            
            # Technical terms
            'إيميل': 'إيميل',
            'بريد': 'بريد إلكتروني',
            'إنبوكس': 'صندوق الوارد',
            'رد': 'رد',
            'جواب': 'جواب',
            'درافت': 'مسودة',
        }
        
        processed_text = text
        for derja, replacement in derja_replacements.items():
            processed_text = processed_text.replace(derja, replacement)
        
        return processed_text
    
    def stop_speaking(self):
        """Stop current speech."""
        if self.engine and self.is_speaking:
            try:
                self.engine.stop()
                self.stop_event.set()
            except Exception as e:
                print(f"Error stopping speech: {e}")
    
    def is_currently_speaking(self) -> bool:
        """Check if currently speaking."""
        return self.is_speaking
    
    def wait_for_speech(self, timeout: float = 10.0) -> bool:
        """Wait for speech to complete."""
        return self.stop_event.wait(timeout)
    
    def speak_with_emotion(self, text: str, emotion: str = "neutral") -> bool:
        """Speak text with emotional tone."""
        if not self.engine:
            return False
        
        # Adjust rate and volume based on emotion
        original_rate = self.engine.getProperty('rate')
        original_volume = self.engine.getProperty('volume')
        
        try:
            if emotion == "happy":
                self.engine.setProperty('rate', original_rate + 20)
                self.engine.setProperty('volume', min(1.0, original_volume + 0.1))
            elif emotion == "sad":
                self.engine.setProperty('rate', original_rate - 20)
                self.engine.setProperty('volume', max(0.5, original_volume - 0.1))
            elif emotion == "excited":
                self.engine.setProperty('rate', original_rate + 30)
                self.engine.setProperty('volume', min(1.0, original_volume + 0.2))
            elif emotion == "calm":
                self.engine.setProperty('rate', original_rate - 10)
                self.engine.setProperty('volume', original_volume)
            
            # Add emotional prefixes
            if emotion == "happy":
                text = f"😊 {text}"
            elif emotion == "sad":
                text = f"😢 {text}"
            elif emotion == "excited":
                text = f"🎉 {text}"
            elif emotion == "calm":
                text = f"😌 {text}"
            
            result = self.speak_derja(text, interrupt=True)
            
            # Restore original settings
            self.engine.setProperty('rate', original_rate)
            self.engine.setProperty('volume', original_volume)
            
            return result
            
        except Exception as e:
            print(f"Emotional TTS error: {e}")
            # Restore original settings
            self.engine.setProperty('rate', original_rate)
            self.engine.setProperty('volume', original_volume)
            return False
    
    def speak_derja_with_ai(self, text: str) -> bool:
        """Use AI to enhance Derja pronunciation."""
        if not GEMINI_API_KEY:
            return self.speak_derja(text)
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""Convert this Tunisian Derja text to a more natural, pronounceable form for TTS:

Original: "{text}"

Rules:
1. Keep the meaning exactly the same
2. Make it more natural for speech synthesis
3. Use proper Arabic pronunciation
4. Keep Tunisian dialect flavor
5. Make it flow better when spoken

Converted text:"""
            
            response = model.generate_content(prompt)
            enhanced_text = response.text.strip()
            
            # Remove quotes if present
            if enhanced_text.startswith('"') and enhanced_text.endswith('"'):
                enhanced_text = enhanced_text[1:-1]
            
            return self.speak_derja(enhanced_text)
            
        except Exception as e:
            print(f"AI-enhanced TTS error: {e}")
            return self.speak_derja(text)
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available voices."""
        if not self.engine:
            return []
        
        voices = self.engine.getProperty('voices')
        voice_list = []
        
        for voice in voices:
            voice_info = {
                'id': voice.id,
                'name': getattr(voice, 'name', 'Unknown'),
                'languages': getattr(voice, 'languages', []),
                'gender': getattr(voice, 'gender', 'Unknown')
            }
            voice_list.append(voice_info)
        
        return voice_list
    
    def set_voice(self, voice_id: str) -> bool:
        """Set specific voice by ID."""
        if not self.engine:
            return False
        
        try:
            self.engine.setProperty('voice', voice_id)
            return True
        except Exception as e:
            print(f"Error setting voice: {e}")
            return False
    
    def set_rate(self, rate: int) -> bool:
        """Set speech rate (words per minute)."""
        if not self.engine:
            return False
        
        try:
            self.engine.setProperty('rate', rate)
            return True
        except Exception as e:
            print(f"Error setting rate: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """Set speech volume (0.0 to 1.0)."""
        if not self.engine:
            return False
        
        try:
            self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
            return True
        except Exception as e:
            print(f"Error setting volume: {e}")
            return False


# Global instance
derja_tts = DerjaTTS()

def speak_derja(text: str, interrupt: bool = True) -> bool:
    """Convenience function to speak Derja text."""
    return derja_tts.speak_derja(text, interrupt)

def speak_derja_with_emotion(text: str, emotion: str = "neutral") -> bool:
    """Convenience function to speak with emotion."""
    return derja_tts.speak_with_emotion(text, emotion)

def speak_derja_with_ai(text: str) -> bool:
    """Convenience function to speak with AI enhancement."""
    return derja_tts.speak_derja_with_ai(text)

def stop_derja_speech():
    """Convenience function to stop speech."""
    derja_tts.stop_speaking()

def is_derja_speaking() -> bool:
    """Convenience function to check if speaking."""
    return derja_tts.is_currently_speaking()
