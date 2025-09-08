#!/usr/bin/env python3
"""
Test voice output for Luca
"""

from assistant.tts import speak

def test_voice():
    print("Testing voice output...")
    print("You should hear Luca speak now!")
    
    # Test different messages
    messages = [
        "Hello! This is Luca, your AI voice assistant.",
        "Voice output is working perfectly!",
        "You can now hear my responses.",
        "Try saying inbox, organize, read, or draft to test email commands."
    ]
    
    for message in messages:
        print(f"Speaking: {message}")
        speak(message)
        input("Press Enter to continue to next message...")
    
    print("Voice test complete!")

if __name__ == "__main__":
    test_voice()
