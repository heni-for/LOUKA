#!/usr/bin/env python3
"""
Test script for interruptible TTS functionality
Press 'l' to stop speaking
"""

import time
from assistant.tts_interruptible import speak, stop_speaking, is_speaking

def test_interrupt_tts():
    """Test the interruptible TTS functionality."""
    print("🎤 Testing Interruptible TTS")
    print("Press 'l' to interrupt speech")
    print("=" * 50)
    
    # Test 1: Long text that can be interrupted
    long_text = """
    This is a very long text that I'm going to read to you. 
    It contains multiple sentences and should take some time to complete.
    You can press the 'l' key at any time to interrupt this speech.
    The system should stop immediately when you press 'l'.
    This is sentence number five.
    And this is sentence number six.
    We're almost done with this long text.
    This is the final sentence of our test.
    """
    
    print("Starting long speech...")
    speak(long_text)
    
    # Wait a bit and check status
    time.sleep(2)
    if is_speaking():
        print("Still speaking...")
    else:
        print("Speech completed or interrupted")
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("If you pressed 'l', the speech should have stopped early.")
    print("If you didn't press 'l', the full text should have been spoken.")

if __name__ == "__main__":
    test_interrupt_tts()
