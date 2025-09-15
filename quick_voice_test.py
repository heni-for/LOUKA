#!/usr/bin/env python3
"""
Quick Voice Test - Verify Tunisian Voice is Working
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.emotional_tts import speak_with_emotion
import time

def quick_test():
    """Quick test to verify Tunisian voice is working."""
    print("🎤 QUICK TUNISIAN VOICE TEST")
    print("=" * 40)
    print("Testing if Luca now speaks in Tunisian Arabic...")
    print()
    
    # Test phrases
    test_phrases = [
        ("أهلا وسهلا! أنا لوكا", "happy", "Greeting"),
        ("شنو نعمل اليوم؟", "neutral", "Question"),
        ("طيب، هكا نعملها!", "excited", "Excitement"),
        ("أه، زينة!", "playful", "Playful")
    ]
    
    for i, (phrase, emotion, description) in enumerate(test_phrases, 1):
        print(f"{i}. {description}: '{phrase}'")
        print(f"   Emotion: {emotion}")
        print("   Speaking with Google TTS Arabic...")
        
        try:
            success = speak_with_emotion(phrase, emotion)
            if success:
                print("   ✅ SUCCESS - Should sound in Arabic!")
            else:
                print("   ❌ FAILED")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        
        print()
        time.sleep(1)
    
    print("🎯 Quick test completed!")
    print("✅ If you heard Arabic speech, the fix worked!")
    print("❌ If you heard English, there's still an issue")

if __name__ == "__main__":
    quick_test()
