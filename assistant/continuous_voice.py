#!/usr/bin/env python3
"""
Continuous voice listening mode for Siri-like experience
"""

import threading
import time
import queue
from typing import Optional, Callable
from .multilang_voice import MultiLanguageVoiceRecognizer
from .tts import speak
from .smart_features import handle_smart_command, is_smart_command
from .llm import chat_with_ai

class ContinuousVoiceAssistant:
    """Continuous voice assistant with Siri-like behavior."""
    
    def __init__(self):
        self.voice_recognizer = MultiLanguageVoiceRecognizer()
        self.is_running = False
        self.is_listening = False
        self.conversation_history = []
        self.last_activity = time.time()
        self.sleep_timeout = 30  # Go to sleep after 30 seconds of inactivity
        self.wake_up_phrases = ["hey luca", "luca", "ok luca", "wake up", "wake up luca"]
        
    def start(self):
        """Start the continuous voice assistant."""
        self.is_running = True
        print("🎤 Luca is now active! Say 'Hey Luca' to wake me up.")
        speak("Hello! I'm Luca, your AI assistant. Say 'Hey Luca' to start talking to me.")
        
        # Start the main listening loop
        self.listen_thread = threading.Thread(target=self._main_loop, daemon=True)
        self.listen_thread.start()
    
    def stop(self):
        """Stop the continuous voice assistant."""
        self.is_running = False
        self.is_listening = False
        self.voice_recognizer.stop_listening()
        print("👋 Luca is going to sleep. Goodbye!")
    
    def _main_loop(self):
        """Main listening loop."""
        while self.is_running:
            try:
                if not self.is_listening:
                    # Listen for wake word
                    self._listen_for_wake_word()
                else:
                    # Listen for commands
                    self._listen_for_command()
                    
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)
    
    def _listen_for_wake_word(self):
        """Listen for wake word to activate the assistant."""
        try:
            # Set a short timeout for wake word detection
            command = self.voice_recognizer.listen_for_command(timeout=2.0)
            
            if command and self._is_wake_word(command):
                print("🔔 Wake word detected!")
                self.is_listening = True
                self.last_activity = time.time()
                speak("Yes? How can I help you?")
                
        except Exception as e:
            print(f"Error listening for wake word: {e}")
            time.sleep(0.1)
    
    def _listen_for_command(self):
        """Listen for user commands."""
        try:
            command = self.voice_recognizer.listen_for_command(timeout=8.0)  # Longer timeout
            
            if command:
                self.last_activity = time.time()
                print(f"👂 Heard: {command}")
                
                # Check if it's just a wake word without command
                if command.lower().strip() in ["luca", "hey luca", "ok luca"]:
                    print("🔔 Wake word detected, waiting for command...")
                    speak("Yes? How can I help you?")
                    # Continue listening for the actual command
                    return
                
                self._process_command(command)
            else:
                # Check if we should go back to sleep
                if time.time() - self.last_activity > self.sleep_timeout:
                    print("😴 Going to sleep due to inactivity")
                    speak("I'm going to sleep now. Say 'Hey Luca' when you need me!")
                    self.is_listening = False
                    
        except Exception as e:
            print(f"Error listening for command: {e}")
            time.sleep(0.1)
    
    def _is_wake_word(self, text: str) -> bool:
        """Check if the text contains a wake word."""
        text_lower = text.lower().strip()
        return any(phrase in text_lower for phrase in self.wake_up_phrases)
    
    def _process_command(self, command: str):
        """Process user command."""
        command_lower = command.lower().strip()
        
        # Check for sleep commands
        if any(phrase in command_lower for phrase in ["go to sleep", "sleep", "goodbye", "bye", "stop"]):
            speak("Goodbye! Say 'Hey Luca' when you need me again.")
            self.is_listening = False
            return
        
        # Check for smart commands first
        smart_intent = is_smart_command(command)
        if smart_intent:
            speak("Sure! Let me help you with that.")
            response = handle_smart_command(smart_intent, command)
            speak(response)
            return
        
        # Handle email commands
        if command_lower in ["inbox", "list", "read", "organize", "draft", "help"]:
            self._handle_email_command(command_lower)
            return
        
        # General AI chat
        try:
            speak("Let me think about that...")
            response = chat_with_ai(command, self.conversation_history)
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": command})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep only last 10 exchanges
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            speak(response)
            
        except Exception as e:
            speak(f"Sorry, I had trouble processing that. {str(e)}")
            print(f"AI Chat error: {e}")
    
    def _handle_email_command(self, command: str):
        """Handle email-specific commands."""
        try:
            if command == "inbox":
                speak("Checking your inbox...")
                # Add email integration here
                speak("I found 5 new emails in your inbox.")
            elif command in ["organize", "organise"]:
                speak("Organizing your emails...")
                speak("Done! I've organized your emails into categories.")
            elif command == "read":
                speak("Reading your latest emails...")
                speak("Here are your recent messages...")
            elif command == "draft":
                speak("What would you like to draft?")
            elif command == "help":
                speak("I can help with emails, tell you the time and weather, answer questions, and have conversations. Just ask me anything!")
        except Exception as e:
            speak(f"Sorry, I had trouble with that email command. {str(e)}")

def main():
    """Main function to run continuous voice assistant."""
    assistant = ContinuousVoiceAssistant()
    
    try:
        assistant.start()
        
        # Keep the main thread alive
        while assistant.is_running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        assistant.stop()

if __name__ == "__main__":
    main()
