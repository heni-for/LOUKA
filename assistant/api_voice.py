#!/usr/bin/env python3
"""
API-based Voice Assistant using modern speech services
"""

import requests
import json
import threading
import time
import os
from typing import Optional, Dict, Any

from .llm import chat_with_ai
from .tts import speak
from .smart_features import handle_smart_command, is_smart_command

class APIVoiceAssistant:
    def __init__(self):
        self.conversation_history = []
        self.is_running = False
        
        # API endpoints (you can replace with your preferred services)
        self.speech_to_text_url = "https://api.openai.com/v1/audio/transcriptions"
        self.text_to_speech_url = "https://api.openai.com/v1/audio/speech"
        
        # You'll need to set these API keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
    def start(self):
        """Start the API-based assistant."""
        if not self.openai_api_key:
            print("❌ OpenAI API key not found!")
            print("Set OPENAI_API_KEY environment variable")
            return
        
        self.is_running = True
        print("🎤 API-based Voice Assistant is ready!")
        print("💡 This uses OpenAI's Whisper for speech recognition")
        print("💡 Press Ctrl+C to quit")
        
        # Welcome message
        self.speak("Hello! I'm your AI assistant powered by modern speech APIs. How can I help you?")
        
        # Start conversation loop
        self.conversation_loop()
    
    def conversation_loop(self):
        """Main conversation loop."""
        while self.is_running:
            try:
                print("\n🎤 Recording... (Press Enter when done)")
                input()  # Wait for user to press Enter
                
                # Here you would record audio and send to API
                # For now, let's simulate with text input
                text = input("👂 What did you say? (or type your message): ")
                
                if text.strip():
                    self.process_command(text)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def process_command(self, text: str):
        """Process user command."""
        text_lower = text.lower().strip()
        
        # Check for conversation enders
        if any(word in text_lower for word in ["goodbye", "bye", "see you", "thanks", "thank you"]):
            self.speak("Goodbye! Have a great day!")
            return
        
        # Check for smart commands first
        smart_intent = is_smart_command(text)
        if smart_intent:
            self.speak("Sure! Let me help you with that.")
            response = handle_smart_command(smart_intent, text)
            self.speak(response)
            return
        
        # Natural conversation with AI
        try:
            self.speak("Let me think about that...")
            
            # Enhanced context for better responses
            context = """You are a helpful AI assistant similar to Siri or Alexa. 
            Respond naturally and conversationally. Be friendly, helpful, and concise. 
            If the user asks about something you don't know, say so honestly."""
            
            response = chat_with_ai(f"{context}\n\nUser: {text}", self.conversation_history)
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": text})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            self.speak(response)
            
        except Exception as e:
            self.speak("Sorry, I had trouble understanding that. Could you try again?")
            print(f"AI Chat error: {e}")
    
    def speak(self, text: str):
        """Speak text."""
        print(f"🤖 Assistant: {text}")
        speak(text)
    
    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio using OpenAI Whisper API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            
            with open(audio_file_path, "rb") as audio_file:
                files = {"file": audio_file}
                data = {"model": "whisper-1"}
                
                response = requests.post(
                    self.speech_to_text_url,
                    headers=headers,
                    files=files,
                    data=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("text", "")
                else:
                    print(f"Transcription error: {response.status_code}")
                    return None
                    
        except Exception as e:
            print(f"Transcription error: {e}")
            return None

def main():
    """Main function to run API-based assistant."""
    assistant = APIVoiceAssistant()
    
    try:
        assistant.start()
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
