#!/usr/bin/env python3
"""
Siri-like Voice Assistant with natural conversation flow
"""

import threading
import time
import queue
import json
import msvcrt
from typing import Optional, Dict, Any
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from rich import print

from .llm import chat_with_ai
from .tts import speak
from .smart_features import handle_smart_command, is_smart_command

class SiriLikeAssistant:
    def __init__(self):
        self.is_running = False
        self.is_listening = False
        self.conversation_history = []
        self.last_interaction = time.time()
        self.sleep_timeout = 30  # Sleep after 30 seconds of inactivity
        
        # Initialize speech recognition
        self.model_path = "vosk-model-en-us-0.22"
        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        
        # Audio settings
        self.sample_rate = 16000
        self.audio_queue = queue.Queue()
        self.stream = None
        
        # Wake words (more natural)
        self.wake_words = ["hey", "okay", "yes", "luca", "assistant", "help"]
        
        # Conversation state
        self.in_conversation = False
        self.waiting_for_response = False
        
    def start(self):
        """Start the Siri-like assistant."""
        self.is_running = True
        print("🎤 Siri-like Assistant is now active!")
        print("💡 Just start talking naturally - no wake words needed!")
        print("💡 Press 'l' to interrupt speech, Ctrl+C to quit")
        
        # Welcome message
        self.speak("Hello! I'm your AI assistant. How can I help you today?")
        
        # Start listening
        self.start_listening()
        
        # Main conversation loop
        self.conversation_loop()
    
    def start_listening(self):
        """Start audio input stream."""
        try:
            self.stream = sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            )
            self.stream.start()
            self.is_listening = True
            print("🎧 Listening...")
        except Exception as e:
            print(f"❌ Audio error: {e}")
    
    def audio_callback(self, indata, frames, time, status):
        """Audio input callback."""
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(bytes(indata))
    
    def conversation_loop(self):
        """Main conversation loop."""
        while self.is_running:
            try:
                # Listen for speech
                text = self.listen_for_speech()
                
                if text:
                    self.last_interaction = time.time()
                    self.process_command(text)
                else:
                    # Check if we should go to sleep
                    if time.time() - self.last_interaction > self.sleep_timeout:
                        if self.in_conversation:
                            self.speak("I'm here if you need anything else!")
                            self.in_conversation = False
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in conversation loop: {e}")
                time.sleep(1)
    
    def listen_for_speech(self, timeout=5.0):
        """Listen for speech with timeout."""
        start_time = time.time()
        audio_buffer = b""
        
        while time.time() - start_time < timeout:
            try:
                # Get audio data
                if not self.audio_queue.empty():
                    data = self.audio_queue.get_nowait()
                    audio_buffer += data
                    
                    # Process when we have enough data
                    if len(audio_buffer) >= 8000:  # 0.5 seconds of audio
                        if self.recognizer.AcceptWaveform(audio_buffer):
                            result = json.loads(self.recognizer.Result())
                            text = result.get("text", "").strip()
                            if text and len(text) > 2:
                                print(f"👂 Heard: {text}")
                                return text
                        audio_buffer = b""
                
                time.sleep(0.1)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Speech recognition error: {e}")
                break
        
        return None
    
    def process_command(self, text: str):
        """Process user command naturally."""
        text_lower = text.lower().strip()
        
        # Check for conversation enders
        if any(word in text_lower for word in ["goodbye", "bye", "see you", "thanks", "thank you"]):
            self.speak("Goodbye! Have a great day!")
            self.in_conversation = False
            return
        
        # Check for smart commands first
        smart_intent = is_smart_command(text)
        if smart_intent:
            self.speak("Sure! Let me help you with that.")
            response = handle_smart_command(smart_intent, text)
            self.speak(response)
            self.in_conversation = True
            return
        
        # Natural conversation with AI
        try:
            self.speak("Let me think about that...")
            
            # Add context to make responses more natural
            context = "You are a helpful AI assistant. Respond naturally and conversationally, like Siri or Alexa. Keep responses concise but helpful."
            
            response = chat_with_ai(f"{context}\n\nUser: {text}", self.conversation_history)
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": text})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            self.speak(response)
            self.in_conversation = True
            
        except Exception as e:
            self.speak("Sorry, I had trouble understanding that. Could you try again?")
            print(f"AI Chat error: {e}")
    
    def speak(self, text: str):
        """Speak text with interrupt capability."""
        print(f"🤖 Assistant: {text}")
        
        # Use simple TTS that works
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 200)
            engine.setProperty('volume', 0.9)
            
            # Try to find a good voice
            try:
                voices = engine.getProperty('voices')
                preferred = None
                voice_preferences = ['zira', 'david', 'aria', 'hazel', 'susan', 'mark', 'richard']
                
                for preference in voice_preferences:
                    for v in voices:
                        name = (getattr(v, 'name', '') or '').lower()
                        if preference in name:
                            preferred = v.id
                            break
                    if preferred:
                        break
                
                if preferred:
                    engine.setProperty('voice', preferred)
            except:
                pass
            
            engine.say(text)
            engine.runAndWait()
            
        except Exception as e:
            print(f"TTS error: {e}")
            # Just print if TTS fails
            print(f"🔊 [TTS Failed] {text}")
    
    def stop(self):
        """Stop the assistant."""
        self.is_running = False
        self.is_listening = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        print("👋 Assistant stopped.")

def main():
    """Main function to run Siri-like assistant."""
    assistant = SiriLikeAssistant()
    
    try:
        assistant.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        assistant.stop()

if __name__ == "__main__":
    main()
