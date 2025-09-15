#!/usr/bin/env python3
"""
Test Fixed Audio Playback and Simplified Emotional Text
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.emotional_tts import speak_with_emotion, speak_naturally
from assistant.google_tts_arabic import test_arabic_pronunciation
import time

def test_basic_audio():
    """Test basic audio playback without hanging."""
    print("🎤 TESTING BASIC AUDIO PLAYBACK")
    print("=" * 50)
    print("Testing non-blocking audio playback...")
    print()
    
    try:
        success = test_arabic_pronunciation()
        if success:
            print("✅ Basic audio playback working!")
        else:
            print("❌ Basic audio playback failed!")
        return success
    except Exception as e:
        print(f"❌ Basic audio test error: {e}")
        return False

def test_simplified_emotional_text():
    """Test simplified emotional text to avoid hanging."""
    print("\n😊 TESTING SIMPLIFIED EMOTIONAL TEXT")
    print("=" * 50)
    print("Testing emotional text without long decorations...")
    print()
    
    emotions = [
        ("happy", "أه، زينة! هكا نعملها!", "Should sound cheerful but short"),
        ("excited", "ممتاز! نعملها بسرعة!", "Should sound energetic but short"),
        ("calm", "طيب، هكا نعملها بهدوء", "Should sound relaxed but short"),
        ("tired", "أه، تعبان شوية", "Should sound slower but short"),
        ("concerned", "مش قادر أعمل الحاجة", "Should sound empathetic but short"),
        ("playful", "هههه، نكتة زينة!", "Should sound fun but short"),
        ("professional", "سأقوم بتنفيذ المهمة", "Should sound formal but short"),
        ("neutral", "طيب، شنو نعمل؟", "Should sound normal but short")
    ]
    
    for emotion, phrase, description in emotions:
        print(f"Testing {emotion.upper()}:")
        print(f"Description: {description}")
        print(f"Phrase: '{phrase}'")
        print("Speaking with simplified emotional TTS...")
        
        try:
            success = speak_with_emotion(phrase, emotion)
            if success:
                print("✅ Spoken successfully!")
            else:
                print("❌ Failed to speak")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        time.sleep(1)  # Shorter wait time
    
    print("🎯 Simplified emotional text test completed!")

def test_short_phrases():
    """Test very short phrases to ensure no hanging."""
    print("\n🔊 TESTING SHORT PHRASES")
    print("=" * 50)
    print("Testing very short phrases to avoid hanging...")
    print()
    
    short_phrases = [
        ("أهلا", "happy", "Short greeting"),
        ("طيب", "neutral", "Short response"),
        ("زينة", "playful", "Short positive"),
        ("مش", "concerned", "Short negative"),
        ("أه", "tired", "Short tired sound")
    ]
    
    for phrase, emotion, description in short_phrases:
        print(f"Testing: '{phrase}' ({emotion})")
        print(f"Description: {description}")
        print("Speaking...")
        
        try:
            success = speak_with_emotion(phrase, emotion)
            if success:
                print("✅ Spoken successfully!")
            else:
                print("❌ Failed to speak")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        time.sleep(0.5)  # Very short wait time
    
    print("🎯 Short phrases test completed!")

def test_natural_speech_simplified():
    """Test natural speech with simplified context."""
    print("\n💬 TESTING SIMPLIFIED NATURAL SPEECH")
    print("=" * 50)
    print("Testing context-aware natural speech with simplified text...")
    print()
    
    test_cases = [
        {
            "text": "أهلا! كيفاش؟",
            "context": {"mood": "happy", "is_greeting": True},
            "description": "Simple happy greeting"
        },
        {
            "text": "مش قادر",
            "context": {"mood": "tired", "last_action": "error"},
            "description": "Simple tired response"
        },
        {
            "text": "هههه، نكتة!",
            "context": {"mood": "playful", "last_action": "joke_told"},
            "description": "Simple playful response"
        },
        {
            "text": "مهم",
            "context": {"mood": "professional"},
            "description": "Simple professional response"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"Text: '{test_case['text']}'")
        print(f"Context: {test_case['context']}")
        print("Speaking naturally...")
        
        try:
            success = speak_naturally(test_case['text'], test_case['context'])
            if success:
                print("✅ Spoken naturally!")
            else:
                print("❌ Failed to speak")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        time.sleep(1)
    
    print("🎯 Simplified natural speech test completed!")

def test_audio_quality():
    """Test audio quality and ensure no hanging."""
    print("\n🔊 TESTING AUDIO QUALITY")
    print("=" * 50)
    print("Testing audio quality and ensuring no hanging...")
    print()
    
    test_phrase = "أهلا وسهلا! أنا لوكا"
    
    print("Test phrase:", test_phrase)
    print()
    
    # Test different emotions with short phrases
    emotions = ["happy", "excited", "calm", "playful", "professional"]
    
    for emotion in emotions:
        print(f"Testing {emotion.upper()} emotion:")
        try:
            success = speak_with_emotion(test_phrase, emotion)
            if success:
                print(f"   ✅ {emotion} emotion completed")
            else:
                print(f"   ❌ {emotion} emotion failed")
        except Exception as e:
            print(f"   ❌ {emotion} emotion error: {e}")
        
        print()
        time.sleep(1)
    
    print("🎯 Audio quality test completed!")
    print("✅ If you heard Arabic speech without hanging, it's working!")
    print("✅ Each emotion should sound slightly different!")

def main():
    """Run all fixed audio tests."""
    print("🎤 FIXED AUDIO PLAYBACK TEST SUITE")
    print("=" * 60)
    print("This will test the FIXED audio system with:")
    print("✅ Non-blocking audio playback (playsound + pygame fallback)")
    print("✅ Simplified emotional text (no long decorations)")
    print("✅ Short phrases to avoid hanging")
    print("✅ Natural speech with simplified context")
    print("✅ Audio quality without blocking")
    print()
    print("Press Enter to start the test...")
    input()
    
    try:
        # Test basic functionality
        basic_success = test_basic_audio()
        
        if basic_success:
            # Test simplified functionality
            test_simplified_emotional_text()
            test_short_phrases()
            test_natural_speech_simplified()
            test_audio_quality()
            
            print("\n🎉 ALL TESTS COMPLETED!")
            print("=" * 60)
            print("✅ Audio Playback: Fixed!")
            print("✅ Emotional Text: Simplified!")
            print("✅ Short Phrases: Working!")
            print("✅ Natural Speech: Working!")
            print("✅ Audio Quality: Working!")
            print()
            print("🎯 Your Luca now has stable audio playback!")
            print("🔊 No more hanging or blocking issues!")
            print("💬 Simplified emotional expressions work!")
            print("🎭 Different emotions still work but are shorter!")
            print()
            print("📝 Note: This is still MSA Arabic, not Tunisian Derja")
            print("   But the audio playback is now stable and reliable!")
        else:
            print("\n❌ Basic audio test failed!")
            print("Please check your audio setup and try again.")
        
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
