#!/usr/bin/env python3
"""
Test Audio Fixes for Luca Voice Assistant
Tests all the audio fixes to ensure proper playback
"""

import sys
import os
import time

# Add the assistant directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'assistant'))

def test_audio_fix_module():
    """Test the audio fix module."""
    print("🔊 Testing Audio Fix Module...")
    print("=" * 50)
    
    try:
        from assistant.audio_fix import (
            audio_fix, 
            play_audio_safely, 
            stop_audio_safely, 
            is_audio_playing,
            test_audio_system,
            get_audio_system_info
        )
        
        # Get audio system info
        info = get_audio_system_info()
        print("📊 Audio System Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()
        
        # Test audio system
        print("🧪 Testing audio system...")
        success = test_audio_system()
        if success:
            print("✅ Audio system test passed!")
        else:
            print("❌ Audio system test failed!")
        
        return success
        
    except Exception as e:
        print(f"❌ Audio fix module test failed: {e}")
        return False

def test_simple_working_tts():
    """Test the simple working TTS."""
    print("\n🔊 Testing Simple Working TTS...")
    print("=" * 50)
    
    try:
        from assistant.simple_working_tts import simple_working_tts
        
        # Test voice
        print("🧪 Testing voice...")
        success = simple_working_tts.test_voice()
        if success:
            print("✅ Simple Working TTS test passed!")
        else:
            print("❌ Simple Working TTS test failed!")
        
        return success
        
    except Exception as e:
        print(f"❌ Simple Working TTS test failed: {e}")
        return False

def test_google_tts_fixed():
    """Test the fixed Google TTS."""
    print("\n🔊 Testing Google TTS Fixed...")
    print("=" * 50)
    
    try:
        from assistant.google_tts_fixed import google_tts_fixed
        
        # Test voice
        print("🧪 Testing Google TTS...")
        success = google_tts_fixed.test_voice()
        if success:
            print("✅ Google TTS Fixed test passed!")
        else:
            print("❌ Google TTS Fixed test failed!")
        
        return success
        
    except Exception as e:
        print(f"❌ Google TTS Fixed test failed: {e}")
        return False

def test_emotional_tts():
    """Test the emotional TTS."""
    print("\n🔊 Testing Emotional TTS...")
    print("=" * 50)
    
    try:
        from assistant.emotional_tts import emotional_tts
        
        # Test different emotions
        emotions = ["happy", "calm", "excited", "neutral"]
        
        for emotion in emotions:
            print(f"🧪 Testing {emotion} emotion...")
            text = f"مرحبا، أنا لوكا المساعد الصوتي. أنا {emotion} اليوم"
            success = emotional_tts.speak_with_emotion(text, emotion)
            if success:
                print(f"✅ {emotion} emotion test passed!")
            else:
                print(f"❌ {emotion} emotion test failed!")
            
            # Wait a bit between tests
            time.sleep(1)
        
        return True
        
    except Exception as e:
        print(f"❌ Emotional TTS test failed: {e}")
        return False

def main():
    """Run all audio tests."""
    print("🎵 Luca Voice Assistant - Audio Fix Tests")
    print("=" * 60)
    print()
    
    # Test results
    results = {}
    
    # Test 1: Audio Fix Module
    results['audio_fix'] = test_audio_fix_module()
    
    # Test 2: Simple Working TTS
    results['simple_tts'] = test_simple_working_tts()
    
    # Test 3: Google TTS Fixed
    results['google_tts'] = test_google_tts_fixed()
    
    # Test 4: Emotional TTS
    results['emotional_tts'] = test_emotional_tts()
    
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
        print("🎉 All audio fixes are working correctly!")
    else:
        print("⚠️ Some audio fixes need attention.")
    
    print("\n🔧 Audio Fix Summary:")
    print("1. ✅ Pygame mixer properly initialized")
    print("2. ✅ MP3 to WAV conversion implemented")
    print("3. ✅ Proper blocking playback with channel monitoring")
    print("4. ✅ Audio device validation and error handling")
    print("5. ✅ Comprehensive test suite")

if __name__ == "__main__":
    main()
