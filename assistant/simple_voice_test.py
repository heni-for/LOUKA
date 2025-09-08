#!/usr/bin/env python3
"""
Simple voice test without wake words - just raw recognition
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant.multilang_voice import MultiLanguageVoiceRecognizer

def test_raw_voice():
    print("🎤 Testing Raw Voice Recognition")
    print("=" * 40)
    print("💡 Just say anything - no wake words needed")
    print("Press Ctrl+C to stop")
    
    try:
        recognizer = MultiLanguageVoiceRecognizer()
        recognizer.set_language('en')
        
        # Modify wake word detection to accept anything
        recognizer._detect_wake_word = lambda text: True  # Accept everything as wake word
        
        while True:
            print("\n🎧 Listening...")
            command = recognizer.listen_for_command(timeout=10.0)
            if command:
                print(f"✅ You said: '{command}'")
            else:
                print("❌ Nothing heard, try again...")
                
    except KeyboardInterrupt:
        print("\n👋 Test stopped")

if __name__ == "__main__":
    test_raw_voice()
