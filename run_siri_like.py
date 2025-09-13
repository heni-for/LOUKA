#!/usr/bin/env python3
"""
Launch Siri-like Voice Assistant
"""

import sys
import os

# Add the assistant module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'assistant'))

def main():
    print("🚀 Starting Siri-like Voice Assistant...")
    print("=" * 50)
    
    try:
        from assistant.siri_like_voice import main as siri_main
        siri_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install vosk sounddevice pyttsx3 rich")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
