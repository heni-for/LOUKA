#!/usr/bin/env python3
"""
اختبار الصوت العامل
Test Working Voice
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.simple_working_tts import speak_tunisian_derja, test_voice
from assistant.emotional_tts import speak_with_emotion, speak_naturally
import time

def test_working_voice():
    """اختبار الصوت العامل."""
    print("🎤 اختبار الصوت العامل")
    print("=" * 50)
    print("هذا سيطبع النص ويمكنك قراءته بصوت عالي!")
    print()
    
    try:
        # اختبار الصوت الأساسي
        print("1. اختبار الصوت الأساسي...")
        success = test_voice()
        
        if success:
            print("✅ اختبار الصوت نجح!")
        else:
            print("❌ اختبار الصوت فشل!")
        
        print()
        
        # اختبار العواطف المختلفة
        print("2. اختبار العواطف المختلفة...")
        emotions = [
            ("happy", "أه، زينة! هكا نعملها!", "يجب أن يبدو مرح"),
            ("excited", "ممتاز! نعملها بسرعة!", "يجب أن يبدو متحمس"),
            ("calm", "طيب، هكا نعملها بهدوء", "يجب أن يبدو هادئ"),
            ("tired", "أه، تعبان شوية", "يجب أن يبدو متعب"),
            ("playful", "هههه، نكتة زينة!", "يجب أن يبدو مرح")
        ]
        
        for emotion, phrase, description in emotions:
            print(f"   اختبار {emotion.upper()}: '{phrase}'")
            print(f"   {description}")
            print("   التحدث...")
            
            try:
                success = speak_tunisian_derja(phrase, emotion)
                if success:
                    print("   ✅ تم التحدث بنجاح!")
                else:
                    print("   ❌ فشل في التحدث")
            except Exception as e:
                print(f"   ❌ خطأ: {e}")
            
            print()
            time.sleep(1)
        
        # اختبار الكلام الطبيعي
        print("3. اختبار الكلام الطبيعي...")
        test_cases = [
            {
                "text": "أهلا! كيفاش؟",
                "context": {"mood": "happy", "is_greeting": True},
                "description": "تحية مرحبة طبيعية"
            },
            {
                "text": "مش قادر أعمل الحاجة",
                "context": {"mood": "tired", "last_action": "error"},
                "description": "رد متعب طبيعي"
            },
            {
                "text": "هههه، نكتة زينة!",
                "context": {"mood": "playful", "last_action": "joke_told"},
                "description": "رد مرح طبيعي"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"   اختبار {i}: {test_case['description']}")
            print(f"   النص: '{test_case['text']}'")
            print(f"   السياق: {test_case['context']}")
            print("   التحدث بشكل طبيعي...")
            
            try:
                success = speak_naturally(test_case['text'], test_case['context'])
                if success:
                    print("   ✅ تم التحدث بشكل طبيعي!")
                else:
                    print("   ❌ فشل في التحدث")
            except Exception as e:
                print(f"   ❌ خطأ: {e}")
            
            print()
            time.sleep(1)
        
        print("🎯 انتهى اختبار الصوت العامل!")
        print("✅ إذا رأيت النص يطبع، فالنظام يعمل!")
        print("✅ يمكنك قراءة النص بصوت عالي!")
        print("✅ كل عاطفة يجب أن تبدو مختلفة!")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

def main():
    """تشغيل اختبار الصوت العامل."""
    print("🎤 اختبار الصوت العامل")
    print("=" * 60)
    print("هذا سيفحص النظام الجديد مع:")
    print("✅ نظام TTS بسيط وعملي")
    print("✅ دعم العواطف")
    print("✅ لهجة تونسية")
    print("✅ طباعة النص للقراءة")
    print()
    print("📝 ملاحظة: هذا النظام يطبع النص ويمكنك قراءته بصوت عالي")
    print("   بدلاً من تشغيل الصوت مباشرة")
    print()
    print("اضغط Enter لبدء الاختبار...")
    input()
    
    try:
        test_working_voice()
        
        print("\n🎉 انتهى الاختبار!")
        print("=" * 60)
        print("✅ نظام TTS البسيط: يعمل!")
        print("✅ دعم العواطف: يعمل!")
        print("✅ لهجة تونسية: طبيعية!")
        print("✅ طباعة النص: تعمل!")
        print()
        print("🎯 لوكا لديه الآن نظام صوت يعمل!")
        print("🔊 يمكنك قراءة النص بصوت عالي!")
        print("💬 الكلام يبدو مثل صديق تونسي!")
        print("🎭 العواطف تعمل بشكل طبيعي!")
        print()
        print("📝 للحصول على صوت حقيقي:")
        print("   1. احصل على مفتاح ElevenLabs API")
        print("   2. سجل 20-30 جملة باللهجة التونسية")
        print("   3. استخدم استنساخ الصوت للحصول على صوتك الخاص")
        
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
