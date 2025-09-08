#!/usr/bin/env python3
"""
Test multi-language voice recognition
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant.multilang_voice import MultiLanguageVoiceRecognizer

def main():
    print("🎤 Multi-Language Voice Recognition Test")
    print("=" * 50)
    
    # Initialize recognizer
    recognizer = MultiLanguageVoiceRecognizer()
    
    # Show available languages
    available = recognizer.get_available_languages()
    print(f"Available languages: {available}")
    
    if not available:
        print("❌ No models available. Please download Vosk models first.")
        print("Run: python download_tunisian_model.py")
        return
    
    # Test each available language
    for lang in available:
        print(f"\n🌍 Testing {lang.upper()}...")
        recognizer.set_language(lang)
        
        print("💡 Say a wake word followed by a command...")
        command = recognizer.listen_for_command(timeout=10.0)
        
        if command:
            print(f"✅ Recognized: '{command}'")
        else:
            print("❌ No command recognized")
    
    print("\n🎉 Test complete!")

if __name__ == "__main__":
    main()
