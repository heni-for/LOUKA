#!/usr/bin/env python3
"""
ElevenLabs TTS for Real Tunisian Derja Voice
Supports emotional modulation and voice cloning
"""

import os
import tempfile
import pygame
from typing import Optional, Dict, List
import threading
import time

# Try to import ElevenLabs, but make it optional
try:
    from elevenlabs import generate, play, set_api_key, voices, Voice
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    print("⚠️ ElevenLabs not available. Install with: pip install elevenlabs")

class ElevenLabsTTS:
    """ElevenLabs TTS for Tunisian Derja with emotional support."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        self.is_speaking = False
        self.stop_event = threading.Event()
        self.temp_files = []
        
        # Initialize pygame for audio playback
        try:
            pygame.mixer.init()
            print("✅ ElevenLabs TTS initialized")
        except Exception as e:
            print(f"Error initializing pygame: {e}")
        
        # Set API key if available and ElevenLabs is installed
        if ELEVENLABS_AVAILABLE and self.api_key:
            set_api_key(self.api_key)
            print("✅ ElevenLabs API key set")
        elif ELEVENLABS_AVAILABLE:
            print("⚠️ ElevenLabs API key not found. Set ELEVENLABS_API_KEY environment variable.")
        else:
            print("⚠️ ElevenLabs not available. Using Google TTS fallback.")
    
    def get_available_voices(self) -> List[Dict]:
        """Get list of available ElevenLabs voices."""
        try:
            if not ELEVENLABS_AVAILABLE or not self.api_key:
                return []
            
            voice_list = voices()
            voices_info = []
            
            for voice in voice_list:
                voice_info = {
                    'voice_id': voice.voice_id,
                    'name': voice.name,
                    'category': voice.category,
                    'description': voice.description,
                    'labels': voice.labels
                }
                voices_info.append(voice_info)
            
            return voices_info
            
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    def find_arabic_voice(self) -> Optional[str]:
        """Find the best Arabic/Tunisian voice."""
        try:
            voices_list = self.get_available_voices()
            
            # Look for Arabic or multilingual voices
            for voice in voices_list:
                name = voice['name'].lower()
                description = voice.get('description', '').lower()
                labels = voice.get('labels', {})
                
                # Check for Arabic indicators
                if any(keyword in name or keyword in description for keyword in 
                      ['arabic', 'arab', 'tunisian', 'tunisia', 'multilingual', 'multi']):
                    return voice['voice_id']
                
                # Check labels for language info
                if labels and 'language' in labels:
                    if 'arabic' in str(labels['language']).lower():
                        return voice['voice_id']
            
            # Fallback to first available voice
            if voices_list:
                return voices_list[0]['voice_id']
            
            return None
            
        except Exception as e:
            print(f"Error finding Arabic voice: {e}")
            return None
    
    def speak_tunisian_derja(self, text: str, emotion: str = "neutral", voice_id: str = None) -> bool:
        """Speak Tunisian Derja with emotional modulation."""
        try:
            if not ELEVENLABS_AVAILABLE:
                print("❌ ElevenLabs not available")
                return False
            
            if not self.api_key:
                print("❌ ElevenLabs API key required")
                return False
            
            if self.is_speaking:
                self.stop_speaking()
            
            self.is_speaking = True
            self.stop_event.clear()
            
            # Use provided voice or find Arabic voice
            if not voice_id:
                voice_id = self.find_arabic_voice()
                if not voice_id:
                    print("❌ No suitable voice found")
                    return False
            
            # Modify text based on emotion
            emotional_text = self._add_emotional_expression(text, emotion)
            
            # Generate voice settings based on emotion
            voice_settings = self._get_voice_settings(emotion)
            
            print(f"🎤 Speaking with ElevenLabs: '{emotional_text}'")
            print(f"   Emotion: {emotion}, Voice: {voice_id}")
            
            # Generate audio
            audio = generate(
                text=emotional_text,
                voice=voice_id,
                model="eleven_multilingual_v2",  # Best for Arabic
                voice_settings=voice_settings
            )
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_file.write(audio)
                temp_file_path = tmp_file.name
            
            self.temp_files.append(temp_file_path)
            
            # Play audio
            self._play_audio(temp_file_path)
            
            # Clean up old temp files
            self._cleanup_temp_files()
            
            return True
            
        except Exception as e:
            print(f"ElevenLabs TTS error: {e}")
            self.is_speaking = False
            return False
    
    def _add_emotional_expression(self, text: str, emotion: str) -> str:
        """Add emotional expression to text for better TTS output."""
        # Remove any existing emotional markers
        text = text.replace('😊', '').replace('🎉', '').replace('😌', '').replace('😴', '')
        text = text.replace('😟', '').replace('😄', '').replace('**', '')
        
        # Add emotional expressions in Derja
        if emotion == "happy":
            text = f"أه، {text}!"
        elif emotion == "excited":
            text = f"ممتاز! {text}!"
        elif emotion == "calm":
            text = f"طيب، {text}."
        elif emotion == "tired":
            text = f"أه، {text}..."
        elif emotion == "concerned":
            text = f"مش قادر، {text}؟"
        elif emotion == "playful":
            text = f"هههه، {text}!"
        elif emotion == "professional":
            text = f"سأقوم بـ{text}."
        
        return text
    
    def _get_voice_settings(self, emotion: str) -> Dict:
        """Get voice settings based on emotion."""
        settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
        
        if emotion == "excited":
            settings.update({
                "stability": 0.3,
                "style": 0.8,
                "similarity_boost": 0.9
            })
        elif emotion == "calm":
            settings.update({
                "stability": 0.8,
                "style": 0.2,
                "similarity_boost": 0.6
            })
        elif emotion == "tired":
            settings.update({
                "stability": 0.9,
                "style": 0.1,
                "similarity_boost": 0.5
            })
        elif emotion == "playful":
            settings.update({
                "stability": 0.4,
                "style": 0.9,
                "similarity_boost": 0.8
            })
        elif emotion == "concerned":
            settings.update({
                "stability": 0.7,
                "style": 0.3,
                "similarity_boost": 0.7
            })
        elif emotion == "professional":
            settings.update({
                "stability": 0.9,
                "style": 0.1,
                "similarity_boost": 0.8
            })
        
        return settings
    
    def _play_audio(self, file_path: str):
        """Play audio file using pygame."""
        try:
            print(f"🔊 Playing ElevenLabs audio: {file_path}")
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy() and not self.stop_event.is_set():
                time.sleep(0.1)
            
            self.is_speaking = False
            self.stop_event.set()
            print("✅ ElevenLabs speech completed")
            
        except Exception as e:
            print(f"Audio playback error: {e}")
            self.is_speaking = False
    
    def stop_speaking(self):
        """Stop current speech."""
        try:
            if self.is_speaking:
                pygame.mixer.music.stop()
                self.stop_event.set()
                self.is_speaking = False
        except Exception as e:
            print(f"Error stopping speech: {e}")
    
    def _cleanup_temp_files(self):
        """Clean up old temporary files."""
        try:
            # Keep only last 5 files
            while len(self.temp_files) > 5:
                old_file = self.temp_files.pop(0)
                if os.path.exists(old_file):
                    os.remove(old_file)
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    def test_tunisian_voice(self) -> bool:
        """Test Tunisian Derja voice with different emotions."""
        try:
            test_phrases = [
                ("أهلا وسهلا! أنا لوكا", "happy", "Greeting"),
                ("شنو نعمل اليوم؟", "neutral", "Question"),
                ("طيب، هكا نعملها!", "excited", "Excitement"),
                ("أه، زينة!", "playful", "Playful"),
                ("مش قادر أعمل الحاجة", "concerned", "Concerned")
            ]
            
            print("🎤 Testing ElevenLabs Tunisian Derja voice...")
            print("This should sound much more natural than gTTS!")
            print()
            
            for i, (phrase, emotion, description) in enumerate(test_phrases, 1):
                print(f"{i}. {description}: '{phrase}'")
                print(f"   Emotion: {emotion}")
                print("   Speaking with ElevenLabs...")
                
                success = self.speak_tunisian_derja(phrase, emotion)
                
                if success:
                    print("   ✅ SUCCESS - Should sound natural and Tunisian!")
                else:
                    print("   ❌ FAILED")
                
                print()
                time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"Tunisian voice test error: {e}")
            return False

# Global instance
elevenlabs_tts = ElevenLabsTTS()

def speak_tunisian_derja_elevenlabs(text: str, emotion: str = "neutral", voice_id: str = None) -> bool:
    """Speak Tunisian Derja using ElevenLabs TTS."""
    return elevenlabs_tts.speak_tunisian_derja(text, emotion, voice_id)

def test_elevenlabs_voice() -> bool:
    """Test ElevenLabs voice."""
    return elevenlabs_tts.test_tunisian_voice()

def get_available_voices() -> List[Dict]:
    """Get available ElevenLabs voices."""
    return elevenlabs_tts.get_available_voices()

def stop_elevenlabs_speech():
    """Stop ElevenLabs speech."""
    elevenlabs_tts.stop_speaking()

def is_elevenlabs_speaking() -> bool:
    """Check if ElevenLabs is speaking."""
    return elevenlabs_tts.is_speaking
