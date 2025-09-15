#!/usr/bin/env python3
"""
Test Voice Communication System
Tests the complete voice interaction: Speech Recognition + TTS
"""

import sys
import os
import time
import threading
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Add the assistant directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'assistant'))

class VoiceCommunicationTest:
    """Test the complete voice communication system."""
    
    def __init__(self):
        self.is_listening = False
        self.is_speaking = False
        self.audio_queue = queue.Queue()
        self.stream = None
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 4000
        
        # Initialize speech recognition
        self.model_path = "vosk-model-en-us-0.22"
        if not os.path.exists(self.model_path):
            print(f"❌ Vosk model not found at {self.model_path}")
            print("Please download the model or update the path")
            return
        
        try:
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            print("✅ Speech recognition model loaded")
        except Exception as e:
            print(f"❌ Failed to load speech model: {e}")
            return
        
        # Initialize TTS
        try:
            from assistant.google_tts_fixed import speak_arabic_fixed
            self.speak_arabic = speak_arabic_fixed
            print("✅ Google TTS loaded")
        except Exception as e:
            print(f"❌ Failed to load TTS: {e}")
            return
        
        # Initialize AI chat
        try:
            from assistant.llm import chat_with_ai
            self.chat_with_ai = chat_with_ai
            print("✅ AI chat loaded")
        except Exception as e:
            print(f"❌ Failed to load AI chat: {e}")
            return
    
    def audio_callback(self, indata, frames, time, status):
        """Audio input callback."""
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(bytes(indata))
    
    def start_listening(self):
        """Start listening for speech."""
        try:
            self.stream = sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            )
            self.stream.start()
            self.is_listening = True
            print("🎤 Listening started...")
        except Exception as e:
            print(f"❌ Failed to start listening: {e}")
    
    def stop_listening(self):
        """Stop listening for speech."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.is_listening = False
            print("🔇 Listening stopped")
    
    def listen_for_speech(self, timeout=5.0):
        """Listen for speech and return recognized text."""
        if not self.is_listening:
            self.start_listening()
        
        print("🎤 Speak now...")
        start_time = time.time()
        last_activity = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Get audio data
                if not self.audio_queue.empty():
                    data = self.audio_queue.get_nowait()
                    last_activity = time.time()
                    
                    # Process with Vosk
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        text = result.get("text", "").strip()
                        
                        if text and len(text) > 2:
                            print(f"🎯 Recognized: '{text}'")
                            return text
                    
                    # Check partial results
                    partial = json.loads(self.recognizer.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text and len(partial_text) > 2:
                        print(f"📝 Partial: '{partial_text}'")
                
                # Check for silence timeout
                if time.time() - last_activity > 2.0:
                    print("⏰ Silence timeout")
                    break
                
                time.sleep(0.1)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Listening error: {e}")
                break
        
        return ""
    
    def speak_response(self, text, emotion="neutral"):
        """Speak the response using TTS."""
        try:
            print(f"🔊 Speaking: '{text}'")
            self.is_speaking = True
            success = self.speak_arabic(text, emotion)
            self.is_speaking = False
            return success
        except Exception as e:
            print(f"❌ Speaking error: {e}")
            self.is_speaking = False
            return False
    
    def chat_loop(self):
        """Main chat loop."""
        print("\n🎤 Voice Communication Test Started!")
        print("=" * 50)
        print("Commands:")
        print("  - Say 'hello' or 'مرحبا' to start")
        print("  - Say 'quit' or 'وداعا' to exit")
        print("  - Press Ctrl+C to stop")
        print("=" * 50)
        
        # Welcome message
        self.speak_response("مرحبا! أنا لوكا المساعد الصوتي. كيف يمكنني مساعدتك؟", "happy")
        
        try:
            while True:
                # Listen for speech
                user_input = self.listen_for_speech(timeout=10.0)
                
                if not user_input:
                    print("⏰ No speech detected, continuing...")
                    continue
                
                # Check for quit commands
                if any(word in user_input.lower() for word in ['quit', 'exit', 'stop', 'وداعا', 'مع السلامة']):
                    print("👋 Goodbye!")
                    self.speak_response("وداعا! كان من دواعي سروري مساعدتك", "calm")
                    break
                
                # Process the input
                print(f"🤔 Processing: '{user_input}'")
                
                # Get AI response
                try:
                    ai_response = self.chat_with_ai(user_input)
                    print(f"🧠 AI Response: '{ai_response}'")
                    
                    # Speak the response
                    self.speak_response(ai_response, "neutral")
                    
                except Exception as e:
                    error_msg = f"عذراً، حدث خطأ: {str(e)}"
                    print(f"❌ Error: {e}")
                    self.speak_response(error_msg, "concerned")
                
                print("-" * 30)
                
        except KeyboardInterrupt:
            print("\n👋 Stopping voice communication...")
            self.speak_response("وداعا!", "calm")
        finally:
            self.stop_listening()
    
    def test_speech_recognition(self):
        """Test speech recognition only."""
        print("🧪 Testing Speech Recognition")
        print("-" * 30)
        
        self.start_listening()
        
        try:
            for i in range(3):
                print(f"Test {i+1}/3: Say something...")
                text = self.listen_for_speech(timeout=5.0)
                
                if text:
                    print(f"✅ Recognized: '{text}'")
                else:
                    print("❌ No speech recognized")
                
                time.sleep(1)
                
        finally:
            self.stop_listening()
    
    def test_tts_only(self):
        """Test TTS only."""
        print("🧪 Testing Text-to-Speech")
        print("-" * 30)
        
        test_phrases = [
            "مرحبا، أنا لوكا",
            "كيف حالك؟",
            "شكرا لك",
            "وداعا"
        ]
        
        for phrase in test_phrases:
            print(f"Testing: '{phrase}'")
            success = self.speak_response(phrase)
            if success:
                print("✅ Played successfully")
            else:
                print("❌ Failed to play")
            time.sleep(2)
    
    def test_full_communication(self):
        """Test the complete communication system."""
        print("🧪 Testing Full Communication System")
        print("-" * 40)
        
        # Test 1: Speech Recognition
        print("1. Testing Speech Recognition...")
        self.test_speech_recognition()
        print()
        
        # Test 2: TTS
        print("2. Testing Text-to-Speech...")
        self.test_tts_only()
        print()
        
        # Test 3: Full Chat
        print("3. Testing Full Chat System...")
        self.chat_loop()

def main():
    """Main function."""
    print("🎤 Luca Voice Communication Test")
    print("=" * 50)
    
    # Check if required models exist
    if not os.path.exists("vosk-model-en-us-0.22"):
        print("❌ Vosk model not found!")
        print("Please download the model:")
        print("1. Go to https://alphacephei.com/vosk/models")
        print("2. Download vosk-model-en-us-0.22")
        print("3. Extract it to the current directory")
        return
    
    # Initialize test
    test = VoiceCommunicationTest()
    
    if not hasattr(test, 'model'):
        print("❌ Failed to initialize voice system")
        return
    
    print("\nChoose test mode:")
    print("1. Full Communication Test (Interactive Chat)")
    print("2. Speech Recognition Only")
    print("3. TTS Only")
    print("4. All Tests")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            test.chat_loop()
        elif choice == "2":
            test.test_speech_recognition()
        elif choice == "3":
            test.test_tts_only()
        elif choice == "4":
            test.test_full_communication()
        else:
            print("Invalid choice, running full communication test...")
            test.chat_loop()
            
    except KeyboardInterrupt:
        print("\n👋 Test stopped by user")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()
