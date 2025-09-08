#!/usr/bin/env python3
"""
Test AI voice processing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant.ai_voice_processor import AIVoiceProcessor

def test_ai_voice():
    print("🤖 Testing AI Voice Processing")
    print("=" * 40)
    
    try:
        processor = AIVoiceProcessor()
        
        # Test with various inputs that might come from poor speech recognition
        test_inputs = [
            "the",
            "the the the",
            "read the",
            "read my last email",
            "reed my last emale",
            "inbox",
            "check emails",
            "draft email",
            "help",
            "what can you do"
        ]
        
        for text in test_inputs:
            print(f"\n🔤 Input: '{text}'")
            result = processor.process_voice_command(text, 'en')
            print(f"✅ Command: '{result['command']}'")
            print(f"📊 Confidence: {result['confidence']:.2f}")
            print(f"🔧 Corrected: '{result['corrected']}'")
            print(f"💭 Reason: {result['reason']}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_ai_voice()
