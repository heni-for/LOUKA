#!/usr/bin/env python3
"""
Enhanced Emotional TTS System for Luca
Natural voice with emotional tones, pacing, and Derja pronunciation
"""

import pyttsx3
import threading
import time
import random
from typing import Optional, Dict, List, Any
from .config import GEMINI_API_KEY
from .simple_working_tts import speak_tunisian_derja, is_speaking

class EmotionalTTS:
    """Enhanced TTS with emotional tones and natural pacing."""
    
    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self.current_text = ""
        self.stop_event = threading.Event()
        self.emotion_settings = self._load_emotion_settings()
        self._init_engine()
    
    def _load_emotion_settings(self) -> Dict[str, Dict[str, Any]]:
        """Load emotion-specific TTS settings."""
        return {
            "happy": {
                "rate": 200,
                "volume": 0.9,
                "pitch": 1.1,
                "pause_factor": 0.8,
                "prefix": "😊 ",
                "suffix": "!",
                "emphasis_words": ["زينة", "طيب", "أه", "زينة"]
            },
            "excited": {
                "rate": 220,
                "volume": 0.95,
                "pitch": 1.2,
                "pause_factor": 0.7,
                "prefix": "🎉 ",
                "suffix": "!",
                "emphasis_words": ["زينة", "طيب", "أه", "زينة", "نعملها"]
            },
            "calm": {
                "rate": 160,
                "volume": 0.8,
                "pitch": 0.9,
                "pause_factor": 1.2,
                "prefix": "😌 ",
                "suffix": ".",
                "emphasis_words": ["طيب", "هكا", "أه"]
            },
            "tired": {
                "rate": 140,
                "volume": 0.7,
                "pitch": 0.8,
                "pause_factor": 1.5,
                "prefix": "😴 ",
                "suffix": "...",
                "emphasis_words": ["أه", "طيب", "هكا"]
            },
            "concerned": {
                "rate": 170,
                "volume": 0.85,
                "pitch": 0.95,
                "pause_factor": 1.1,
                "prefix": "😟 ",
                "suffix": "?",
                "emphasis_words": ["مش", "لا", "مش زينة"]
            },
            "playful": {
                "rate": 190,
                "volume": 0.9,
                "pitch": 1.05,
                "pause_factor": 0.9,
                "prefix": "😄 ",
                "suffix": "!",
                "emphasis_words": ["هههه", "زينة", "نكتة", "مضحك"]
            },
            "professional": {
                "rate": 180,
                "volume": 0.85,
                "pitch": 1.0,
                "pause_factor": 1.0,
                "prefix": "",
                "suffix": ".",
                "emphasis_words": ["مهم", "ضروري", "عاجل"]
            },
            "neutral": {
                "rate": 180,
                "volume": 0.9,
                "pitch": 1.0,
                "pause_factor": 1.0,
                "prefix": "",
                "suffix": ".",
                "emphasis_words": []
            }
        }
    
    def _init_engine(self):
        """Initialize TTS engine with optimal settings."""
        try:
            self.engine = pyttsx3.init()
            
            # Set default properties
            self.engine.setProperty('rate', 180)
            self.engine.setProperty('volume', 0.9)
            
            # Find best voice for Arabic/Derja
            voices = self.engine.getProperty('voices')
            best_voice = self._find_best_voice(voices)
            
            if best_voice:
                self.engine.setProperty('voice', best_voice)
                print(f"استخدام الصوت: {best_voice}")
            
            # Set up event callbacks
            self.engine.connect('started-utterance', self._on_start)
            self.engine.connect('finished-utterance', self._on_finish)
            
        except Exception as e:
            print(f"خطأ في تهيئة محرك TTS: {e}")
            self.engine = None
    
    def _find_best_voice(self, voices) -> Optional[str]:
        """Find the best voice for Derja/Arabic."""
        if not voices:
            return None
        
        # Voice preferences for Arabic/Derja
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
        print("🎤 يتحدث...")
    
    def _on_finish(self, name, completed):
        """Called when speech finishes."""
        self.is_speaking = False
        self.stop_event.set()
        if completed:
            print("✅ تم التحدث")
        else:
            print("⏹️ تم إيقاف الكلام")
    
    def _preprocess_derja_text(self, text: str, emotion: str = "neutral") -> str:
        """Preprocess text for better Derja pronunciation and emotion (simplified)."""
        # Get emotion settings
        settings = self.emotion_settings.get(emotion, self.emotion_settings["neutral"])
        
        # Remove any existing emotional markers to avoid long audio
        text = text.replace('😊', '').replace('🎉', '').replace('😌', '').replace('😴', '')
        text = text.replace('😟', '').replace('😄', '').replace('**', '')
        text = text.replace('! !', '!').replace('. .', '.').replace('؟ ؟', '؟')
        
        # Add simple emotional prefixes/suffixes (keep it short)
        if settings["prefix"] and not text.startswith(settings["prefix"]):
            text = settings["prefix"] + text
        if settings["suffix"] and not text.endswith(settings["suffix"]):
            text = text + settings["suffix"]
        
        # Add natural pauses (simplified)
        text = self._add_natural_pauses(text, emotion)
        
        # Convert common Derja words to more pronounceable forms (simplified)
        derja_replacements = {
            'أهلا': 'أهلا وسهلا',
            'وينك': 'وينك كيفاش',
            'شنادي': 'شنادي نعمل'
        }
        
        for derja, replacement in derja_replacements.items():
            text = text.replace(derja, replacement)
        
        return text
    
    def _add_natural_pauses(self, text: str, emotion: str) -> str:
        """Add natural pauses to text based on emotion."""
        settings = self.emotion_settings.get(emotion, self.emotion_settings["neutral"])
        pause_factor = settings["pause_factor"]
        
        # Add pauses after certain punctuation
        text = text.replace('.', '. ')
        text = text.replace('!', '! ')
        text = text.replace('?', '? ')
        text = text.replace(',', ', ')
        
        # Add longer pauses for certain emotions
        if emotion == "tired":
            text = text.replace('. ', '... ')
            text = text.replace('! ', '!... ')
        elif emotion == "excited":
            text = text.replace('! ', '! ')
            text = text.replace('. ', '. ')
        
        return text
    
    def speak_with_emotion(self, text: str, emotion: str = "neutral", interrupt: bool = True) -> bool:
        """Speak text with specific emotion using ElevenLabs TTS (primary) or Google TTS (fallback)."""
        try:
            # Get emotion settings
            settings = self.emotion_settings.get(emotion, self.emotion_settings["neutral"])
            
            # Stop current speech if interrupting
            if interrupt and self.is_speaking:
                self.stop_speaking()
                time.sleep(0.1)
            
            # Preprocess text
            processed_text = self._preprocess_derja_text(text, emotion)
            self.current_text = processed_text
            
            # Use Tunisian Derja TTS directly
            print(f"🎤 التحدث مع عاطفة {emotion}: '{processed_text}'")
            
            # Call Tunisian Derja TTS with emotion
            success = speak_tunisian_derja(processed_text, emotion)
            if success:
                self.is_speaking = True
                # Wait for TTS to finish
                while is_speaking():
                    time.sleep(0.1)
                self.is_speaking = False
                print("✅ تم إكمال TTS التونسي")
            return success
            
        except Exception as e:
            print(f"خطأ في TTS العاطفي: {e}")
            print("⚠️ العودة إلى TTS التونسي...")
            # Fallback to basic Tunisian TTS
            return speak_tunisian_derja(text, "neutral")
    
    def speak_naturally(self, text: str, context: Dict[str, Any] = None) -> bool:
        """Speak text with natural emotion based on context using Google TTS."""
        if not context:
            context = {}
        
        # Determine emotion from context
        emotion = self._determine_emotion_from_context(text, context)
        
        # Use Tunisian Derja TTS directly for better pronunciation
        print(f"🎤 التحدث بشكل طبيعي مع عاطفة {emotion}: '{text}'")
        return speak_tunisian_derja(text, emotion)
    
    def _determine_emotion_from_context(self, text: str, context: Dict[str, Any]) -> str:
        """Determine emotion from text and context."""
        # Check for explicit emotion indicators
        if "😊" in text or "زينة" in text or "طيب" in text:
            return "happy"
        elif "🎉" in text or "نعملها" in text or "زينة" in text:
            return "excited"
        elif "😌" in text or "هكا" in text:
            return "calm"
        elif "😴" in text or "تعبان" in text:
            return "tired"
        elif "😟" in text or "مش" in text or "لا" in text:
            return "concerned"
        elif "😄" in text or "هههه" in text or "نكتة" in text:
            return "playful"
        elif "مهم" in text or "ضروري" in text or "عاجل" in text:
            return "professional"
        
        # Check context
        if context.get('mood') == 'energetic':
            return "excited"
        elif context.get('mood') == 'relaxed':
            return "calm"
        elif context.get('mood') == 'tired':
            return "tired"
        elif context.get('mood') == 'playful':
            return "playful"
        elif context.get('mood') == 'professional':
            return "professional"
        
        # Check last action
        if context.get('last_action') == 'email_sent':
            return "happy"
        elif context.get('last_action') == 'error':
            return "concerned"
        elif context.get('last_action') == 'joke_told':
            return "playful"
        
        # Default to neutral
        return "neutral"
    
    def speak_conversationally(self, text: str, conversation_context: Dict[str, Any] = None) -> bool:
        """Speak text with conversational flow using Google TTS."""
        if not conversation_context:
            conversation_context = {}
        
        # Add conversational elements
        if conversation_context.get('is_greeting'):
            text = f"أهلا! {text}"
        elif conversation_context.get('is_question'):
            text = f"{text}؟"
        elif conversation_context.get('is_exclamation'):
            text = f"{text}!"
        
        # Determine emotion
        emotion = self._determine_emotion_from_context(text, conversation_context)
        
        # Use Tunisian Derja TTS directly
        print(f"التحدث بشكل محادثة مع عاطفة {emotion}: '{text}'")
        return speak_tunisian_derja(text, emotion)
    
    def speak_with_ai_enhancement(self, text: str, emotion: str = "neutral") -> bool:
        """Use AI to enhance speech for better Derja pronunciation."""
        if not GEMINI_API_KEY:
            return speak_tunisian_derja(text, emotion)
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""Convert this Tunisian Derja text to be more natural and emotional for speech synthesis:

Original: "{text}"
Emotion: {emotion}

Rules:
1. Keep the meaning exactly the same
2. Make it more natural for speech synthesis
3. Use proper Arabic pronunciation
4. Keep Tunisian dialect flavor
5. Make it flow better when spoken
6. Add emotional elements for {emotion} emotion

Converted text:"""
            
            response = model.generate_content(prompt)
            enhanced_text = response.text.strip()
            
            # Remove quotes if present
            if enhanced_text.startswith('"') and enhanced_text.endswith('"'):
                enhanced_text = enhanced_text[1:-1]
            
            print(f"🎤 كلام محسن بالذكاء الاصطناعي مع عاطفة {emotion}: '{enhanced_text}'")
            return speak_tunisian_derja(enhanced_text, emotion)
            
        except Exception as e:
            print(f"خطأ في TTS المحسن بالذكاء الاصطناعي: {e}")
            return speak_tunisian_derja(text, emotion)
    
    def stop_speaking(self):
        """Stop current speech."""
        try:
            # Stop TTS speech
            from .simple_working_tts import stop_speech
            stop_speech()
            self.is_speaking = False
            self.stop_event.set()
        except Exception as e:
            print(f"خطأ في إيقاف الكلام: {e}")
    
    def is_currently_speaking(self) -> bool:
        """Check if currently speaking."""
        return self.is_speaking
    
    def wait_for_speech(self, timeout: float = 10.0) -> bool:
        """Wait for speech to complete."""
        return self.stop_event.wait(timeout)
    
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
            print(f"خطأ في تعيين الصوت: {e}")
            return False
    
    def set_emotion_settings(self, emotion: str, settings: Dict[str, Any]) -> bool:
        """Set custom emotion settings."""
        if emotion in self.emotion_settings:
            self.emotion_settings[emotion].update(settings)
            return True
        return False
    
    def get_emotion_settings(self, emotion: str) -> Dict[str, Any]:
        """Get emotion settings."""
        return self.emotion_settings.get(emotion, self.emotion_settings["neutral"])


# Global instance
emotional_tts = EmotionalTTS()

def speak_with_emotion(text: str, emotion: str = "neutral", interrupt: bool = True) -> bool:
    """Convenience function to speak with emotion."""
    return emotional_tts.speak_with_emotion(text, emotion, interrupt)

def speak_naturally(text: str, context: Dict[str, Any] = None) -> bool:
    """Convenience function to speak naturally."""
    return emotional_tts.speak_naturally(text, context)

def speak_conversationally(text: str, conversation_context: Dict[str, Any] = None) -> bool:
    """Convenience function to speak conversationally."""
    return emotional_tts.speak_conversationally(text, conversation_context)

def speak_with_ai_enhancement(text: str, emotion: str = "neutral") -> bool:
    """Convenience function to speak with AI enhancement."""
    return emotional_tts.speak_with_ai_enhancement(text, emotion)

def stop_emotional_speech():
    """Convenience function to stop speech."""
    emotional_tts.stop_speaking()

def is_emotional_speaking() -> bool:
    """Convenience function to check if speaking."""
    return emotional_tts.is_currently_speaking()
