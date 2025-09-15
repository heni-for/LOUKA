#!/usr/bin/env python3
"""
Fixed Google TTS Implementation
Uses proper audio playback with MP3 to WAV conversion
"""

import os
import tempfile
import threading
import time
import requests
from typing import Optional, Dict, Any
from .audio_fix import audio_fix, play_audio_safely, stop_audio_safely, is_audio_playing

class GoogleTTSFixed:
    """Fixed Google TTS with proper audio playback."""
    
    def __init__(self):
        self.is_speaking = False
        self.stop_event = threading.Event()
        self.temp_files = []
        self.audio_fix = audio_fix
        
        print("✅ Google TTS Fixed initialized")
    
    def speak_arabic(self, text: str, emotion: str = "neutral") -> bool:
        """Speak Arabic text using Google TTS with proper audio playback."""
        try:
            if self.is_speaking:
                self.stop_speaking()
                time.sleep(0.1)
            
            self.is_speaking = True
            self.stop_event.clear()
            
            print(f"🎤 Google TTS: '{text}'")
            
            # Generate audio using Google TTS
            audio_file = self._generate_google_audio(text)
            if not audio_file:
                print("❌ Failed to generate audio")
                self.is_speaking = False
                return False
            
            # Play audio with proper blocking
            success = self._play_audio_properly(audio_file)
            
            self.is_speaking = False
            self.stop_event.set()
            
            # Clean up
            self._cleanup_temp_files()
            
            return success
            
        except Exception as e:
            print(f"❌ Google TTS error: {e}")
            self.is_speaking = False
            return False
    
    def _generate_google_audio(self, text: str) -> Optional[str]:
        """Generate audio using Google Translate TTS."""
        try:
            # Use Google Translate TTS for Arabic
            url = "https://translate.google.com/translate_tts"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
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
            
            print("🔄 Generating audio with Google TTS...")
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file.write(response.content)
                    temp_file_path = tmp_file.name
                
                self.temp_files.append(temp_file_path)
                print(f"✅ Audio generated: {temp_file_path}")
                return temp_file_path
            else:
                print(f"❌ Google TTS HTTP error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Google TTS generation error: {e}")
            return None
    
    def _play_audio_properly(self, file_path: str) -> bool:
        """Play audio file with proper blocking and error handling."""
        try:
            print(f"🔊 Playing audio: {file_path}")
            
            # Use the audio fix system for proper playback
            success = play_audio_safely(file_path, blocking=True)
            
            if success:
                print("✅ Audio playback completed")
            else:
                print("⚠️ Audio playback failed, using simulation")
                # Simulate speech duration
                time.sleep(len(file_path) * 0.01)  # Short simulation
            
            return success
            
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
            return False
    
    def stop_speaking(self):
        """Stop current speech."""
        try:
            if self.is_speaking:
                stop_audio_safely()
                self.stop_event.set()
                self.is_speaking = False
                print("✅ Speech stopped")
        except Exception as e:
            print(f"❌ Error stopping speech: {e}")
    
    def is_currently_speaking(self) -> bool:
        """Check if currently speaking."""
        return self.is_speaking or is_audio_playing()
    
    def _cleanup_temp_files(self):
        """Clean up temporary files."""
        try:
            for file_path in self.temp_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
            self.temp_files.clear()
            print("✅ Cleaned up temporary files")
        except Exception as e:
            print(f"❌ Cleanup error: {e}")
    
    def test_voice(self) -> bool:
        """Test the voice system."""
        try:
            print("🔊 Testing Google TTS...")
            test_text = "مرحبا، أنا لوكا المساعد الصوتي"
            return self.speak_arabic(test_text)
        except Exception as e:
            print(f"❌ Voice test error: {e}")
            return False
    
    def get_audio_info(self) -> Dict[str, Any]:
        """Get audio system information."""
        return self.audio_fix.get_audio_info()

# Global instance
google_tts_fixed = GoogleTTSFixed()

def speak_arabic_fixed(text: str, emotion: str = "neutral") -> bool:
    """Convenience function to speak Arabic with fixed audio."""
    return google_tts_fixed.speak_arabic(text, emotion)

def stop_google_speech():
    """Convenience function to stop Google speech."""
    google_tts_fixed.stop_speaking()

def is_google_speaking() -> bool:
    """Convenience function to check if Google is speaking."""
    return google_tts_fixed.is_currently_speaking()

def test_google_voice() -> bool:
    """Convenience function to test Google voice."""
    return google_tts_fixed.test_voice()
