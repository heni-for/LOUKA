#!/usr/bin/env python3
"""
Check available TTS voices on the system
"""

import pyttsx3

def check_voices():
    """Check all available TTS voices."""
    print("🎤 Available TTS Voices on Your System")
    print("=" * 50)
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if not voices:
            print("❌ No voices found!")
            return
        
        print(f"Found {len(voices)} voice(s):\n")
        
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
            if any(keyword in name_lower for keyword in ['arabic', 'tunisian', 'tunisia', 'ar-', 'ar_']):
                arabic_voices.append((name, voice_id))
                print("    ✅ ARABIC VOICE DETECTED!")
            print()
        
        if arabic_voices:
            print("🎉 Arabic voices found:")
            for name, voice_id in arabic_voices:
                print(f"   • {name} ({voice_id})")
        else:
            print("⚠️  No Arabic voices found")
            print("   You may need to install Arabic language pack")
            print("   Go to: Settings > Time & Language > Language > Add a language")
            print("   Add: Arabic (Tunisia) or Arabic (Saudi Arabia)")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_voices()
