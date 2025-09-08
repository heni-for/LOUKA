#!/usr/bin/env python3
"""
Simple speech recognition test to debug voice issues.
"""

import json
import sys
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue

SAMPLE_RATE = 16000
CHANNELS = 1

def test_speech_recognition(model_path, mic_index=1):
    """Test basic speech recognition."""
    print(f"Loading model from: {model_path}")
    model = Model(model_path)
    print("Model loaded successfully!")
    
    # Set up audio device
    if mic_index is not None:
        sd.default.device = (mic_index, None)
    
    # Get device info
    dev_info = sd.query_devices(mic_index, 'input') if mic_index is not None else sd.query_devices(kind='input')
    print(f"Using device: {dev_info['name']}")
    print(f"Max input channels: {dev_info.get('max_input_channels', 1)}")
    
    # Create recognizer
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    
    # Audio queue
    audio_queue = queue.Queue()
    
    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"Audio status: {status}")
        audio_queue.put(bytes(indata))
    
    # Start audio stream
    print("\nStarting audio stream...")
    print("Speak clearly and press Ctrl+C to stop")
    
    with sd.RawInputStream(samplerate=SAMPLE_RATE, 
                          blocksize=1024, 
                          dtype='int16', 
                          channels=CHANNELS, 
                          callback=audio_callback):
        
        print("Listening... Speak now!")
        
        try:
            while True:
                data = audio_queue.get()
                
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print(f"FINAL: '{text}'")
                else:
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text:
                        print(f"PARTIAL: '{partial_text}'", end='\r')
                        
        except KeyboardInterrupt:
            print("\nStopping...")
            # Get final result
            final_result = json.loads(rec.FinalResult())
            final_text = final_result.get("text", "").strip()
            if final_text:
                print(f"FINAL RESULT: '{final_text}'")

if __name__ == "__main__":
    model_path = "C:\\Users\\Heni2\\luca\\vosk-model-en-us-0.22"
    mic_index = 1
    
    if len(sys.argv) > 1:
        try:
            mic_index = int(sys.argv[1])
        except ValueError:
            model_path = sys.argv[1]
    
    if len(sys.argv) > 2:
        model_path = sys.argv[2]
    
    test_speech_recognition(model_path, mic_index)
