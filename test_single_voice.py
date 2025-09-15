#!/usr/bin/env python3
"""
اختبار صوت واحد فقط
Test single voice only
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.emotional_tts import speak_with_emotion
import time

def test_single_voice():
    """اختبار صوت واحد فقط."""
    print("🎤 اختبار صوت واحد فقط")
    print("=" * 40)
    print("اختبار للتأكد من أن هناك صوت واحد فقط...")
    print()
    
    test_phrases = [
        ("أهلا وسهلا", "happy", "تحية مرحبة"),
        ("طيب، شنو نعمل؟", "neutral", "سؤال عادي"),
        ("زينة!", "playful", "إيجابي مرح")
    ]
    
    for phrase, emotion, description in test_phrases:
        print(f"اختبار: '{phrase}' ({emotion})")
        print(f"الوصف: {description}")
        print("التحدث...")
        
        try:
            success = speak_with_emotion(phrase, emotion)
            if success:
                print("✅ تم التحدث بنجاح!")
            else:
                print("❌ فشل في التحدث")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        
        print()
        time.sleep(2)
    
    print("🎯 انتهى الاختبار!")
    print("✅ إذا سمعت صوت واحد فقط لكل عبارة، فالمشكلة تم حلها!")

if __name__ == "__main__":
    test_single_voice()
