#!/usr/bin/env python3
"""
Simple voice recognition test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant.multilang_voice import MultiLanguageVoiceRecognizer

def test_simple_voice():
    print("🎤 Simple Voice Recognition Test")
    print("=" * 40)
    
    # Initialize recognizer
    recognizer = MultiLanguageVoiceRecognizer()
    
    # Set to English
    recognizer.set_language('en')
    
    print("💡 Say anything - just speak normally...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            command = recognizer.listen_for_command(timeout=10.0)
            if command:
                print(f"✅ You said: '{command}'")
            else:
                print("❌ Nothing heard, try again...")
    except KeyboardInterrupt:
        print("\n👋 Test stopped")

if __name__ == "__main__":
    test_simple_voice()
