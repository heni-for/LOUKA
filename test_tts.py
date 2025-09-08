#!/usr/bin/env python3
"""
Test TTS functionality
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant.tts import speak
from assistant.tts_simple import speak as simple_speak

def test_tts():
    print("🎤 Testing TTS functionality...")
    
    # Test simple TTS
    print("Testing simple TTS...")
    simple_speak("Hello, this is a test of the simple TTS system")
    
    time.sleep(2)
    
    # Test main TTS
    print("Testing main TTS...")
    speak("Hello, this is Luca speaking. I can now talk to you in multiple languages!")
    
    print("✅ TTS test complete!")

if __name__ == "__main__":
    test_tts()
