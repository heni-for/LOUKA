#!/usr/bin/env python3
"""
Test microphone access and find working devices
"""

import sounddevice as sd
import numpy as np
import time

def test_microphones():
    """Test all available microphones."""
    print("🎤 Testing Microphone Access")
    print("=" * 40)
    
    try:
        # Get all devices
        devices = sd.query_devices()
        print(f"Found {len(devices)} audio devices:")
        
        working_devices = []
        
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"\nDevice {i}: {device['name']}")
                print(f"  Channels: {device['max_input_channels']}")
                print(f"  Default: {device.get('is_default', False)}")
                
                # Test if device works
                try:
                    print(f"  Testing device {i}...")
                    with sd.InputStream(
                        device=i,
                        channels=1,
                        samplerate=16000,
                        blocksize=1024
                    ) as stream:
                        print(f"  ✅ Device {i} is accessible!")
                        working_devices.append((i, device))
                except Exception as e:
                    print(f"  ❌ Device {i} error: {e}")
        
        if working_devices:
            print(f"\n🎉 Found {len(working_devices)} working microphone(s):")
            for device_id, device_info in working_devices:
                print(f"  • Device {device_id}: {device_info['name']}")
        else:
            print("\n❌ No working microphones found!")
            print("💡 Try:")
            print("  1. Check microphone permissions")
            print("  2. Restart the application")
            print("  3. Check Windows audio settings")
        
        return working_devices
        
    except Exception as e:
        print(f"❌ Error testing microphones: {e}")
        return []

def test_audio_recording(device_id):
    """Test recording from a specific device."""
    print(f"\n🎧 Testing recording from device {device_id}...")
    
    try:
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Audio status: {status}")
            # Calculate volume level
            volume = np.linalg.norm(indata) * 10
            print(f"Volume: {volume:.2f}", end='\r')
        
        with sd.InputStream(
            device=device_id,
            channels=1,
            samplerate=16000,
            callback=audio_callback
        ):
            print("Recording for 3 seconds... Speak into the microphone!")
            time.sleep(3)
            print("\n✅ Recording test completed!")
            
    except Exception as e:
        print(f"❌ Recording test failed: {e}")

if __name__ == "__main__":
    working_devices = test_microphones()
    
    if working_devices:
        # Test the first working device
        device_id, device_info = working_devices[0]
        test_audio_recording(device_id)
    else:
        print("\n❌ Cannot test recording - no working microphones found")
