#!/usr/bin/env python3
"""
Audio Fix Module for Luca Voice Assistant
Fixes common audio playback issues on Windows
"""

import os
import tempfile
import threading
import time
import pygame
from typing import Optional, Dict, Any
import subprocess
import platform

# Try to import audio conversion libraries
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("⚠️ pydub not available. Install with: pip install pydub")

try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False
    print("⚠️ playsound not available. Install with: pip install playsound")

class AudioFix:
    """Comprehensive audio fix for Windows TTS issues."""
    
    def __init__(self):
        self.is_initialized = False
        self.audio_player = None
        self.temp_files = []
        self._init_audio_system()
    
    def _init_audio_system(self):
        """Initialize audio system with proper error handling."""
        try:
            # Initialize pygame mixer with proper settings
            pygame.mixer.pre_init(
                frequency=22050,  # Standard frequency
                size=-16,         # 16-bit signed
                channels=2,       # Stereo
                buffer=1024       # Buffer size
            )
            pygame.mixer.init()
            
            # Test if mixer is working
            if pygame.mixer.get_init():
                self.audio_player = "pygame"
                self.is_initialized = True
                print("✅ Audio system initialized with pygame")
            else:
                raise Exception("Pygame mixer not properly initialized")
                
        except Exception as e:
            print(f"❌ Pygame initialization failed: {e}")
            
            # Fallback to playsound
            if PLAYSOUND_AVAILABLE:
                self.audio_player = "playsound"
                self.is_initialized = True
                print("✅ Audio system initialized with playsound")
            else:
                print("❌ No audio system available")
                self.is_initialized = False
    
    def convert_mp3_to_wav(self, mp3_path: str) -> str:
        """Convert MP3 file to WAV for better pygame compatibility."""
        if not PYDUB_AVAILABLE:
            print("⚠️ pydub not available, using MP3 directly")
            return mp3_path
        
        try:
            # Create WAV file path
            wav_path = mp3_path.replace('.mp3', '.wav')
            
            # Convert MP3 to WAV
            audio = AudioSegment.from_mp3(mp3_path)
            audio.export(wav_path, format="wav")
            
            # Clean up MP3 file
            if os.path.exists(mp3_path):
                os.remove(mp3_path)
            
            print(f"✅ Converted {mp3_path} to {wav_path}")
            return wav_path
            
        except Exception as e:
            print(f"⚠️ MP3 to WAV conversion failed: {e}")
            return mp3_path
    
    def play_audio_file(self, file_path: str, blocking: bool = True) -> bool:
        """Play audio file with proper error handling and blocking."""
        if not self.is_initialized:
            print("❌ Audio system not initialized")
            return False
        
        if not os.path.exists(file_path):
            print(f"❌ Audio file not found: {file_path}")
            return False
        
        try:
            print(f"🔊 Playing audio: {file_path}")
            
            # Convert MP3 to WAV if needed
            if file_path.endswith('.mp3'):
                file_path = self.convert_mp3_to_wav(file_path)
            
            if self.audio_player == "pygame":
                return self._play_with_pygame(file_path, blocking)
            elif self.audio_player == "playsound":
                return self._play_with_playsound(file_path, blocking)
            else:
                print("❌ No audio player available")
                return False
                
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
            return False
    
    def _play_with_pygame(self, file_path: str, blocking: bool) -> bool:
        """Play audio using pygame with proper channel monitoring."""
        try:
            # Load and play the audio
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            if blocking:
                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                print("✅ Audio playback completed")
            else:
                print("✅ Audio playback started")
            
            return True
            
        except Exception as e:
            print(f"❌ Pygame playback error: {e}")
            return False
    
    def _play_with_playsound(self, file_path: str, blocking: bool) -> bool:
        """Play audio using playsound."""
        try:
            if blocking:
                playsound(file_path, block=True)
            else:
                # Run in separate thread for non-blocking
                def play_audio():
                    playsound(file_path, block=True)
                
                audio_thread = threading.Thread(target=play_audio, daemon=True)
                audio_thread.start()
            
            print("✅ Audio playback completed")
            return True
            
        except Exception as e:
            print(f"❌ Playsound error: {e}")
            return False
    
    def stop_audio(self):
        """Stop current audio playback."""
        try:
            if self.audio_player == "pygame":
                pygame.mixer.music.stop()
            print("✅ Audio stopped")
        except Exception as e:
            print(f"❌ Error stopping audio: {e}")
    
    def is_playing(self) -> bool:
        """Check if audio is currently playing."""
        try:
            if self.audio_player == "pygame":
                return pygame.mixer.music.get_busy()
            return False
        except:
            return False
    
    def test_audio_system(self) -> bool:
        """Test the audio system with a simple sound."""
        try:
            print("🔊 Testing audio system...")
            
            # Create a simple test audio file
            test_file = self._create_test_audio()
            if not test_file:
                return False
            
            # Play the test audio
            success = self.play_audio_file(test_file, blocking=True)
            
            # Clean up test file
            if os.path.exists(test_file):
                os.remove(test_file)
            
            if success:
                print("✅ Audio system test passed")
            else:
                print("❌ Audio system test failed")
            
            return success
            
        except Exception as e:
            print(f"❌ Audio system test error: {e}")
            return False
    
    def _create_test_audio(self) -> Optional[str]:
        """Create a simple test audio file."""
        try:
            # Create a simple WAV file using pygame
            import numpy as np
            
            # Generate a simple sine wave
            sample_rate = 22050
            duration = 1.0  # 1 second
            frequency = 440  # A4 note
            
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            wave = np.sin(frequency * 2 * np.pi * t)
            
            # Convert to 16-bit integers
            wave = (wave * 32767).astype(np.int16)
            
            # Create stereo
            stereo_wave = np.array([wave, wave]).T
            
            # Save as WAV
            test_file = os.path.join(tempfile.gettempdir(), "test_audio.wav")
            pygame.sndarray.make_sound(stereo_wave).export(test_file)
            
            return test_file
            
        except Exception as e:
            print(f"❌ Test audio creation failed: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files."""
        try:
            for file_path in self.temp_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
            self.temp_files.clear()
            print("✅ Cleaned up temporary files")
        except Exception as e:
            print(f"❌ Cleanup error: {e}")
    
    def get_audio_info(self) -> Dict[str, Any]:
        """Get information about the audio system."""
        info = {
            "initialized": self.is_initialized,
            "audio_player": self.audio_player,
            "pygame_available": pygame.get_init() is not None,
            "pydub_available": PYDUB_AVAILABLE,
            "playsound_available": PLAYSOUND_AVAILABLE,
            "temp_files_count": len(self.temp_files)
        }
        
        if self.audio_player == "pygame":
            try:
                info["pygame_mixer_init"] = pygame.mixer.get_init()
            except:
                info["pygame_mixer_init"] = None
        
        return info

# Global audio fix instance
audio_fix = AudioFix()

def play_audio_safely(file_path: str, blocking: bool = True) -> bool:
    """Safely play audio file with all fixes applied."""
    return audio_fix.play_audio_file(file_path, blocking)

def stop_audio_safely():
    """Safely stop audio playback."""
    audio_fix.stop_audio()

def is_audio_playing() -> bool:
    """Check if audio is currently playing."""
    return audio_fix.is_playing()

def test_audio_system() -> bool:
    """Test the audio system."""
    return audio_fix.test_audio_system()

def get_audio_system_info() -> Dict[str, Any]:
    """Get audio system information."""
    return audio_fix.get_audio_info()

def cleanup_audio_files():
    """Clean up temporary audio files."""
    audio_fix.cleanup_temp_files()
