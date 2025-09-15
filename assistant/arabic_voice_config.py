#!/usr/bin/env python3
"""
Arabic Voice Configuration for Luca
Proper Arabic/Tunisian voice setup and testing
"""

import pyttsx3
import sys
from typing import List, Dict, Optional

class ArabicVoiceConfig:
    """Arabic voice configuration and testing."""
    
    def __init__(self):
        self.engine = None
        self.arabic_voices = []
        self.current_voice = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize TTS engine and find Arabic voices."""
        try:
            self.engine = pyttsx3.init()
            self._find_arabic_voices()
        except Exception as e:
            print(f"Error initializing TTS engine: {e}")
    
    def _find_arabic_voices(self):
        """Find available Arabic voices."""
        try:
            voices = self.engine.getProperty('voices')
            self.arabic_voices = []
            
            for voice in voices:
                voice_name = getattr(voice, 'name', '').lower()
                voice_id = voice.id
                
                # Look for Arabic voices
                if any(keyword in voice_name for keyword in ['arabic', 'ar-', 'ar_', 'tunisia', 'tunisian']):
                    self.arabic_voices.append({
                        'id': voice_id,
                        'name': voice_name,
                        'language': 'Arabic'
                    })
                elif 'hazel' in voice_name or 'david' in voice_name:
                    # These sometimes work better for Arabic
                    self.arabic_voices.append({
                        'id': voice_id,
                        'name': voice_name,
                        'language': 'English (Arabic compatible)'
                    })
            
            print(f"Found {len(self.arabic_voices)} potential Arabic voices")
            
        except Exception as e:
            print(f"Error finding Arabic voices: {e}")
    
    def list_available_voices(self) -> List[Dict[str, str]]:
        """List all available voices."""
        try:
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
            
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []
    
    def test_voice_with_arabic(self, voice_id: str, test_text: str = "أهلا وسهلا") -> bool:
        """Test a voice with Arabic text."""
        try:
            self.engine.setProperty('voice', voice_id)
            self.engine.setProperty('rate', 150)  # Slower for Arabic
            self.engine.setProperty('volume', 0.9)
            
            print(f"Testing voice: {voice_id}")
            print(f"Text: {test_text}")
            print("Speaking...")
            
            self.engine.say(test_text)
            self.engine.runAndWait()
            
            print("✅ Test completed")
            return True
            
        except Exception as e:
            print(f"Error testing voice: {e}")
            return False
    
    def find_best_arabic_voice(self) -> Optional[str]:
        """Find the best available Arabic voice."""
        try:
            # First try to find actual Arabic voices
            for voice in self.arabic_voices:
                if 'arabic' in voice['name'] or 'ar-' in voice['name']:
                    print(f"Found Arabic voice: {voice['name']}")
                    return voice['id']
            
            # If no Arabic voices, try compatible ones
            for voice in self.arabic_voices:
                if 'hazel' in voice['name'] or 'david' in voice['name']:
                    print(f"Found compatible voice: {voice['name']}")
                    return voice['id']
            
            # Fallback to first available voice
            voices = self.engine.getProperty('voices')
            if voices:
                print(f"Using fallback voice: {voices[0].name}")
                return voices[0].id
            
            return None
            
        except Exception as e:
            print(f"Error finding best Arabic voice: {e}")
            return None
    
    def configure_arabic_voice(self) -> bool:
        """Configure the best Arabic voice."""
        try:
            best_voice = self.find_best_arabic_voice()
            if not best_voice:
                print("❌ No suitable Arabic voice found")
                return False
            
            self.engine.setProperty('voice', best_voice)
            self.engine.setProperty('rate', 150)  # Slower for Arabic
            self.engine.setProperty('volume', 0.9)
            
            self.current_voice = best_voice
            print(f"✅ Arabic voice configured: {best_voice}")
            return True
            
        except Exception as e:
            print(f"Error configuring Arabic voice: {e}")
            return False
    
    def test_tunisian_phrases(self) -> bool:
        """Test with Tunisian Derja phrases."""
        try:
            if not self.current_voice:
                if not self.configure_arabic_voice():
                    return False
            
            test_phrases = [
                "أهلا وسهلا! أنا لوكا",
                "شنو نعمل اليوم؟",
                "طيب، هكا نعملها!",
                "أه، زينة!",
                "كيفاش الحال؟"
            ]
            
            print("🎤 Testing Tunisian Derja phrases...")
            print("Listen to see if it sounds like Arabic/Tunisian:")
            print()
            
            for i, phrase in enumerate(test_phrases, 1):
                print(f"{i}. Testing: '{phrase}'")
                print("Speaking...")
                
                self.engine.say(phrase)
                self.engine.runAndWait()
                
                print("✅ Spoken")
                print()
            
            return True
            
        except Exception as e:
            print(f"Error testing Tunisian phrases: {e}")
            return False
    
    def install_arabic_voices_guide(self):
        """Provide guide for installing Arabic voices."""
        print("🔧 ARABIC VOICE INSTALLATION GUIDE")
        print("=" * 50)
        print()
        print("To get proper Arabic/Tunisian voice, you need to:")
        print()
        print("1. WINDOWS 10/11:")
        print("   - Go to Settings > Time & Language > Language")
        print("   - Add Arabic (Tunisia) or Arabic (Saudi Arabia)")
        print("   - Install Arabic language pack")
        print("   - Go to Speech settings and install Arabic voices")
        print()
        print("2. ALTERNATIVE - Use Google TTS:")
        print("   - Install: pip install gTTS")
        print("   - This provides better Arabic pronunciation")
        print()
        print("3. ALTERNATIVE - Use Azure Cognitive Services:")
        print("   - Better Arabic voices available")
        print("   - Requires API key")
        print()
        print("4. CURRENT WORKAROUND:")
        print("   - Using available English voice")
        print("   - Will sound robotic but understandable")
        print("   - Focus on Derja content, not perfect pronunciation")
        print()

def test_arabic_voice_setup():
    """Test Arabic voice setup."""
    print("🎤 TESTING ARABIC VOICE SETUP")
    print("=" * 40)
    
    config = ArabicVoiceConfig()
    
    # List all voices
    print("📋 Available voices:")
    voices = config.list_available_voices()
    for i, voice in enumerate(voices, 1):
        print(f"{i:2d}. {voice['name']} ({voice['id']})")
    
    print()
    
    # Test current voice
    print("🔊 Testing current voice with Arabic text...")
    config.test_voice_with_arabic(config.engine.getProperty('voice'), "أهلا وسهلا")
    
    print()
    
    # Try to configure better voice
    print("🔧 Trying to configure Arabic voice...")
    if config.configure_arabic_voice():
        print("✅ Arabic voice configured successfully!")
        config.test_tunisian_phrases()
    else:
        print("❌ Could not configure Arabic voice")
        config.install_arabic_voices_guide()

if __name__ == "__main__":
    test_arabic_voice_setup()
