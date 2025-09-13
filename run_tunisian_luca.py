#!/usr/bin/env python3
"""
Launch Tunisian Voice Assistant - Speaks like a Tunisian friend
"""

import sys
import os

# Add the assistant module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'assistant'))

def main():
    print("🇹🇳 Starting Tunisian Voice Assistant...")
    print("=" * 50)
    
    try:
        from assistant.tunisian_voice import main as tunisian_main
        tunisian_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install vosk sounddevice pyttsx3 rich")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
