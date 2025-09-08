#!/usr/bin/env python3
"""
Install Arabic voices for Windows TTS
"""

import pyttsx3
import subprocess
import sys

def check_voices():
    """Check available voices."""
    print("🎤 Checking available TTS voices...")
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        print(f"Found {len(voices)} voice(s):")
        
        arabic_voices = []
        for i, voice in enumerate(voices):
            name = getattr(voice, 'name', f'Voice {i}')
            voice_id = getattr(voice, 'id', 'Unknown')
            languages = getattr(voice, 'languages', [])
            
            print(f"{i+1:2d}. {name}")
            print(f"    ID: {voice_id}")
            print(f"    Languages: {languages}")
            
            # Check if it's an Arabic voice
            name_lower = name.lower()
            if any(keyword in name_lower for keyword in ['arabic', 'ar-', 'ar_', 'tunisian', 'tunisia']):
                arabic_voices.append((name, voice_id))
                print("    ✅ ARABIC VOICE DETECTED!")
            print()
        
        if arabic_voices:
            print("🎉 Arabic voices found:")
            for name, voice_id in arabic_voices:
                print(f"   • {name} ({voice_id})")
        else:
            print("⚠️  No Arabic voices found")
            print("\n💡 To install Arabic voices:")
            print("1. Go to Windows Settings > Time & Language > Language")
            print("2. Click 'Add a language'")
            print("3. Search for 'Arabic' and add it")
            print("4. Go to Speech settings and install Arabic speech pack")
            print("5. Restart this script")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def install_arabic_language():
    """Try to install Arabic language pack."""
    print("🌍 Attempting to install Arabic language pack...")
    
    try:
        # Try to open language settings
        subprocess.run(['start', 'ms-settings:regionlanguage'], shell=True, check=True)
        print("✅ Language settings opened")
        print("Please add Arabic language and install speech pack")
    except Exception as e:
        print(f"❌ Could not open language settings: {e}")

if __name__ == "__main__":
    check_voices()
    
    if input("\nWould you like to open language settings to install Arabic? (y/n): ").lower() == 'y':
        install_arabic_language()
