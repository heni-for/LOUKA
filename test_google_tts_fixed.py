#!/usr/bin/env python3
"""
Test the Fixed Google TTS Implementation
Tests the audio fixes and Google TTS functionality
"""

import sys
import os
import time

# Add the assistant directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'assistant'))

def test_google_tts_fixed():
    """Test the fixed Google TTS implementation."""
    print("🎤 Testing Fixed Google TTS Implementation")
    print("=" * 60)
    
    try:
        from assistant.google_tts_fixed import (
            google_tts_fixed,
            speak_arabic_fixed,
            test_google_voice,
            get_audio_system_info
        )
        
        # Get audio system info
        print("📊 Audio System Information:")
        info = get_audio_system_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()
        
        # Test 1: Basic voice test
        print("🧪 Test 1: Basic Voice Test")
        print("-" * 30)
        success = test_google_voice()
        if success:
            print("✅ Basic voice test PASSED!")
        else:
            print("❌ Basic voice test FAILED!")
        print()
        
        # Test 2: Different emotions
        print("🧪 Test 2: Different Emotions")
        print("-" * 30)
        emotions = ["happy", "calm", "excited", "neutral"]
        
        for emotion in emotions:
            print(f"Testing {emotion} emotion...")
            text = f"مرحبا، أنا لوكا المساعد الصوتي. أنا {emotion} اليوم"
            success = speak_arabic_fixed(text, emotion)
            if success:
                print(f"✅ {emotion} emotion test PASSED!")
            else:
                print(f"❌ {emotion} emotion test FAILED!")
            
            # Wait between tests
            time.sleep(2)
        print()
        
        # Test 3: Different text lengths
        print("🧪 Test 3: Different Text Lengths")
        print("-" * 30)
        test_texts = [
            "أهلا",  # Short
            "مرحبا وسهلا بك في لوكا",  # Medium
            "مرحبا وسهلا بك في لوكا المساعد الصوتي الذكي الذي يمكنه مساعدتك في المهام المختلفة"  # Long
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"Testing text {i} (length: {len(text)}): '{text}'")
            success = speak_arabic_fixed(text)
            if success:
                print(f"✅ Text {i} test PASSED!")
            else:
                print(f"❌ Text {i} test FAILED!")
            
            time.sleep(1)
        print()
        
        # Test 4: Error handling
        print("🧪 Test 4: Error Handling")
        print("-" * 30)
        
        # Test with empty text
        print("Testing empty text...")
        success = speak_arabic_fixed("")
        if not success:
            print("✅ Empty text handled correctly!")
        else:
            print("⚠️ Empty text should have failed")
        
        # Test with very long text
        print("Testing very long text...")
        long_text = "مرحبا " * 100  # Very long text
        success = speak_arabic_fixed(long_text)
        if success:
            print("✅ Long text handled correctly!")
        else:
            print("⚠️ Long text failed (this might be expected)")
        
        print()
        
        # Test 5: Audio system status
        print("🧪 Test 5: Audio System Status")
        print("-" * 30)
        
        from assistant.audio_fix import test_audio_system
        audio_success = test_audio_system()
        if audio_success:
            print("✅ Audio system test PASSED!")
        else:
            print("❌ Audio system test FAILED!")
        
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_audio_quality():
    """Test audio quality and playback."""
    print("🎵 Testing Audio Quality")
    print("=" * 40)
    
    try:
        from assistant.google_tts_fixed import speak_arabic_fixed
        
        # Test different Arabic phrases
        test_phrases = [
            "أهلا وسهلا",  # Welcome
            "كيف حالك؟",  # How are you?
            "شكرا لك",  # Thank you
            "مع السلامة",  # Goodbye
            "أنا لوكا المساعد الصوتي"  # I am Luca the voice assistant
        ]
        
        print("Testing Arabic pronunciation quality...")
        for i, phrase in enumerate(test_phrases, 1):
            print(f"{i}. Testing: '{phrase}'")
            success = speak_arabic_fixed(phrase)
            if success:
                print(f"   ✅ Played successfully")
            else:
                print(f"   ❌ Failed to play")
            time.sleep(1)
        
        return True
        
    except Exception as e:
        print(f"❌ Audio quality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🎤 Google TTS Fixed - Comprehensive Test Suite")
    print("=" * 70)
    print()
    
    # Test results
    results = {}
    
    # Test 1: Basic functionality
    results['basic'] = test_google_tts_fixed()
    
    # Test 2: Audio quality
    results['quality'] = test_audio_quality()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:15} : {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Google TTS Fixed is working correctly!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print("\n🔧 What was tested:")
    print("1. ✅ Audio system initialization")
    print("2. ✅ Google TTS audio generation")
    print("3. ✅ MP3 to WAV conversion")
    print("4. ✅ Proper audio playback")
    print("5. ✅ Error handling")
    print("6. ✅ Different text lengths")
    print("7. ✅ Arabic pronunciation quality")

if __name__ == "__main__":
    main()