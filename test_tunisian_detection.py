#!/usr/bin/env python3
"""
Test Tunisian Derja Detection
Forces the system to use the Tunisian model for speech recognition
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

def test_tunisian_detection():
    """Test if the system can detect Tunisian Derja speech."""
    print("🎤 Testing Tunisian Derja Detection")
    print("=" * 50)
    
    # Force Tunisian model
    model_path = "vosk-model-ar-tn-0.1-linto"
    
    if not os.path.exists(model_path):
        print(f"❌ Tunisian model not found at {model_path}")
        return False
    
    try:
        # Load Tunisian model
        print(f"🔄 Loading Tunisian model: {model_path}")
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)
        print("✅ Tunisian model loaded successfully!")
        
        # Audio settings
        sample_rate = 16000
        chunk_size = 4000
        audio_queue = queue.Queue()
        
        def audio_callback(indata, frames, time, status):
            audio_queue.put(bytes(indata))
        
        # Start audio stream
        print("🎤 Starting audio stream...")
        stream = sd.RawInputStream(
            samplerate=sample_rate,
            blocksize=chunk_size,
            dtype='int16',
            channels=1,
            callback=audio_callback
        )
        stream.start()
        
        print("🎤 Speak in Tunisian Derja now...")
        print("Try saying: 'أهلا وسهلا' or 'شنو نعمل اليوم؟'")
        print("Press Ctrl+C to stop")
        
        start_time = time.time()
        last_activity = time.time()
        
        try:
            while True:
                if not audio_queue.empty():
                    data = audio_queue.get_nowait()
                    last_activity = time.time()
                    
                    # Process with Tunisian recognizer
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "").strip()
                        
                        if text and len(text) > 2:
                            print(f"🎯 Tunisian detected: '{text}'")
                            print("✅ SUCCESS! Tunisian model is working!")
                            
                            # Test TTS
                            try:
                                from assistant.google_tts_fixed import speak_arabic_fixed
                                print("🔊 Testing TTS...")
                                speak_arabic_fixed(f"تم التعرف على: {text}")
                            except Exception as e:
                                print(f"TTS error: {e}")
                            
                            break
                    
                    # Check partial results
                    partial = json.loads(recognizer.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text and len(partial_text) > 2:
                        print(f"📝 Partial: '{partial_text}'")
                
                # Check for silence timeout
                if time.time() - last_activity > 3.0:
                    print("⏰ Silence timeout, continuing...")
                    last_activity = time.time()
                
                # Check for overall timeout
                if time.time() - start_time > 30.0:
                    print("⏰ Overall timeout reached")
                    break
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n👋 Test stopped by user")
        
        finally:
            stream.stop()
            stream.close()
            print("🔇 Audio stream stopped")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_english_vs_tunisian():
    """Compare English vs Tunisian model detection."""
    print("\n🔍 Comparing English vs Tunisian Detection")
    print("=" * 50)
    
    models = {
        "English": "vosk-model-en-us-0.22",
        "Tunisian": "vosk-model-ar-tn-0.1-linto"
    }
    
    results = {}
    
    for model_name, model_path in models.items():
        if not os.path.exists(model_path):
            print(f"❌ {model_name} model not found at {model_path}")
            continue
        
        try:
            print(f"\n🔄 Testing {model_name} model...")
            model = Model(model_path)
            recognizer = KaldiRecognizer(model, 16000)
            
            # Quick test
            print(f"🎤 Say something for {model_name} model...")
            print("Press Enter when ready, then speak for 3 seconds...")
            input()
            
            # Audio settings
            sample_rate = 16000
            chunk_size = 4000
            audio_queue = queue.Queue()
            
            def audio_callback(indata, frames, time, status):
                audio_queue.put(bytes(indata))
            
            stream = sd.RawInputStream(
                samplerate=sample_rate,
                blocksize=chunk_size,
                dtype='int16',
                channels=1,
                callback=audio_callback
            )
            stream.start()
            
            start_time = time.time()
            detected_text = ""
            
            while time.time() - start_time < 3.0:  # 3 second test
                if not audio_queue.empty():
                    data = audio_queue.get_nowait()
                    
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "").strip()
                        if text and len(text) > 2:
                            detected_text = text
                            break
                
                time.sleep(0.1)
            
            stream.stop()
            stream.close()
            
            if detected_text:
                print(f"✅ {model_name} detected: '{detected_text}'")
                results[model_name] = detected_text
            else:
                print(f"❌ {model_name} detected nothing")
                results[model_name] = "Nothing detected"
            
        except Exception as e:
            print(f"❌ {model_name} test failed: {e}")
            results[model_name] = f"Error: {e}"
    
    # Compare results
    print("\n📊 Comparison Results:")
    print("-" * 30)
    for model_name, result in results.items():
        print(f"{model_name:10}: {result}")
    
    return results

def main():
    """Main function."""
    print("🎤 Tunisian Derja Detection Test")
    print("=" * 40)
    
    # Check if models exist
    english_model = "vosk-model-en-us-0.22"
    tunisian_model = "vosk-model-ar-tn-0.1-linto"
    
    if not os.path.exists(english_model):
        print(f"❌ English model not found at {english_model}")
    if not os.path.exists(tunisian_model):
        print(f"❌ Tunisian model not found at {tunisian_model}")
    
    if not os.path.exists(tunisian_model):
        print("\nPlease download the Tunisian model:")
        print("1. Go to https://alphacephei.com/vosk/models")
        print("2. Download vosk-model-ar-tn-0.1-linto")
        print("3. Extract it to the current directory")
        return
    
    print("\nChoose test:")
    print("1. Test Tunisian Detection Only")
    print("2. Compare English vs Tunisian")
    print("3. Both tests")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            test_tunisian_detection()
        elif choice == "2":
            test_english_vs_tunisian()
        elif choice == "3":
            test_tunisian_detection()
            test_english_vs_tunisian()
        else:
            print("Invalid choice, running Tunisian test...")
            test_tunisian_detection()
            
    except KeyboardInterrupt:
        print("\n👋 Test stopped by user")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()
