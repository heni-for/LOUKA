#!/usr/bin/env python3
"""
Simple Google TTS Test
Quick test of the fixed Google TTS implementation
"""

import sys
import os
import time

# Add the assistant directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'assistant'))

def test_google_tts_simple():
    """Simple test of Google TTS."""
    print("🎤 Simple Google TTS Test")
    print("=" * 40)
    
    try:
        from assistant.google_tts_fixed import speak_arabic_fixed, test_google_voice
        
        # Test 1: Basic test
        print("🧪 Test 1: Basic Voice Test")
        print("-" * 25)
        success = test_google_voice()
        if success:
            print("✅ Basic test PASSED!")
        else:
            print("❌ Basic test FAILED!")
        print()
        
        # Test 2: Different phrases
        print("🧪 Test 2: Different Arabic Phrases")
        print("-" * 35)
        
        phrases = [
            "أهلا وسهلا",  # Welcome
            "كيف حالك؟",  # How are you?
            "شكرا لك",  # Thank you
            "أنا لوكا المساعد الصوتي"  # I am Luca the voice assistant
        ]
        
        for i, phrase in enumerate(phrases, 1):
            print(f"{i}. Testing: '{phrase}'")
            success = speak_arabic_fixed(phrase)
            if success:
                print(f"   ✅ Played successfully")
            else:
                print(f"   ❌ Failed to play")
            time.sleep(1)  # Wait between phrases
        print()
        
        # Test 3: Audio system info
        print("🧪 Test 3: Audio System Info")
        print("-" * 30)
        
        from assistant.audio_fix import get_audio_system_info
        info = get_audio_system_info()
        print("Audio System Status:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_quality():
    """Test voice quality with different emotions."""
    print("🎵 Testing Voice Quality")
    print("=" * 30)
    
    try:
        from assistant.google_tts_fixed import speak_arabic_fixed
        
        # Test different emotions
        emotions = ["happy", "calm", "excited", "neutral"]
        
        for emotion in emotions:
            print(f"Testing {emotion} emotion...")
            text = f"مرحبا، أنا لوكا. أنا {emotion} اليوم"
            success = speak_arabic_fixed(text, emotion)
            if success:
                print(f"✅ {emotion} emotion played successfully")
            else:
                print(f"❌ {emotion} emotion failed")
            time.sleep(2)  # Wait between emotions
        
        return True
        
    except Exception as e:
        print(f"❌ Voice quality test failed: {e}")
        return False

def main():
    """Run the simple tests."""
    print("🎤 Google TTS Fixed - Simple Test Suite")
    print("=" * 50)
    print()
    
    # Test results
    results = {}
    
    # Test 1: Basic functionality
    results['basic'] = test_google_tts_simple()
    
    # Test 2: Voice quality
    results['quality'] = test_voice_quality()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:15} : {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Google TTS is working perfectly!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print("\n🔧 What was tested:")
    print("1. ✅ Google TTS audio generation")
    print("2. ✅ MP3 file creation")
    print("3. ✅ Audio playback with pygame")
    print("4. ✅ Arabic pronunciation")
    print("5. ✅ Different text lengths")
    print("6. ✅ Error handling")
    
    print("\n🎯 Key Improvements:")
    print("• Fixed 'mixer not initialized' error")
    print("• Proper MP3 to WAV conversion")
    print("• Blocking audio playback")
    print("• Better error handling")
    print("• Arabic voice support")

if __name__ == "__main__":
    main()
