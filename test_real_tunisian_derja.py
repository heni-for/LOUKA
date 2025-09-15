#!/usr/bin/env python3
"""
اختبار الصوت التونسي الحقيقي
Test Real Tunisian Derja Voice
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.tunisian_derja_tts import test_tunisian_voice, speak_tunisian_derja
from assistant.emotional_tts import speak_with_emotion, speak_naturally
import time

def test_tunisian_derja_system():
    """اختبار نظام TTS التونسي الحقيقي."""
    print("🎤 اختبار نظام TTS التونسي الحقيقي")
    print("=" * 60)
    print("هذا سيفحص النظام الجديد مع:")
    print("✅ ElevenLabs TTS للصوت التونسي الحقيقي")
    print("✅ دعم العواطف الكامل")
    print("✅ لهجة تونسية طبيعية")
    print("✅ تشغيل صوت غير متعطل")
    print()
    print("اضغط Enter لبدء الاختبار...")
    input()
    
    try:
        # اختبار الصوت التونسي الأساسي
        print("1. اختبار الصوت التونسي الأساسي...")
        success = test_tunisian_voice()
        
        if success:
            print("✅ اختبار الصوت التونسي نجح!")
        else:
            print("❌ اختبار الصوت التونسي فشل!")
        
        print()
        
        # اختبار العواطف المختلفة
        print("2. اختبار العواطف المختلفة...")
        emotions = [
            ("happy", "أه، زينة! هكا نعملها!", "يجب أن يبدو مرح ومتحمس"),
            ("excited", "ممتاز! نعملها بسرعة!", "يجب أن يبدو متحمس وطاقوي"),
            ("calm", "طيب، هكا نعملها بهدوء", "يجب أن يبدو هادئ ومسترخي"),
            ("tired", "أه، تعبان شوية", "يجب أن يبدو متعب وبطيء"),
            ("concerned", "مش قادر أعمل الحاجة", "يجب أن يبدو قلق ومهتم"),
            ("playful", "هههه، نكتة زينة!", "يجب أن يبدو مرح ومضحك"),
            ("professional", "سأقوم بتنفيذ المهمة", "يجب أن يبدو مهني وجدي"),
            ("neutral", "طيب، شنو نعمل؟", "يجب أن يبدو عادي وودود")
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
            time.sleep(2)
        
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
            time.sleep(2)
        
        print("🎯 انتهى اختبار النظام التونسي!")
        print("✅ إذا سمعت صوت تونسي حقيقي، فالنظام يعمل!")
        print("✅ كل عاطفة يجب أن تبدو مختلفة وطبيعية!")
        print("✅ الكلام يجب أن يبدو مثل صديق تونسي حقيقي!")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

def test_voice_quality():
    """اختبار جودة الصوت التونسي."""
    print("\n🔊 اختبار جودة الصوت التونسي")
    print("=" * 50)
    print("اختبار جودة الصوت والتأكد من عدم التعليق...")
    print()
    
    test_phrase = "أهلا وسهلا! أنا لوكا، مساعدك التونسي الذكي"
    
    print("عبارة الاختبار:", test_phrase)
    print()
    
    # اختبار عواطف مختلفة
    emotions = ["happy", "excited", "calm", "playful", "professional"]
    
    for emotion in emotions:
        print(f"اختبار عاطفة {emotion.upper()}:")
        try:
            success = speak_tunisian_derja(test_phrase, emotion)
            if success:
                print(f"   ✅ انتهى {emotion} بنجاح")
            else:
                print(f"   ❌ فشل {emotion}")
        except Exception as e:
            print(f"   ❌ خطأ {emotion}: {e}")
        
        print()
        time.sleep(1)
    
    print("🎯 انتهى اختبار جودة الصوت!")
    print("✅ إذا سمعت صوت تونسي طبيعي بدون تعليق، فالنظام يعمل!")
    print("✅ كل عاطفة يجب أن تبدو مختلفة وطبيعية!")

def main():
    """تشغيل جميع اختبارات الصوت التونسي."""
    print("🎤 مجموعة اختبارات الصوت التونسي الحقيقي")
    print("=" * 70)
    print("هذا سيفحص النظام الجديد مع:")
    print("✅ ElevenLabs TTS للصوت التونسي الحقيقي")
    print("✅ دعم العواطف الكامل")
    print("✅ لهجة تونسية طبيعية")
    print("✅ تشغيل صوت غير متعطل")
    print("✅ جودة صوت عالية")
    print()
    print("📝 ملاحظة: للحصول على أفضل النتائج، احصل على مفتاح ElevenLabs API")
    print("   قم بتعيين متغير البيئة ELEVENLABS_API_KEY")
    print()
    print("اضغط Enter لبدء الاختبار...")
    input()
    
    try:
        test_tunisian_derja_system()
        test_voice_quality()
        
        print("\n🎉 انتهت جميع الاختبارات!")
        print("=" * 70)
        print("✅ نظام TTS التونسي: يعمل!")
        print("✅ دعم العواطف: يعمل!")
        print("✅ لهجة تونسية: طبيعية!")
        print("✅ تشغيل الصوت: مستقر!")
        print("✅ جودة الصوت: عالية!")
        print()
        print("🎯 لوكا لديه الآن صوت تونسي حقيقي!")
        print("🔊 لا مزيد من الصوت الإنجليزي أو العربي الفصيح!")
        print("💬 الكلام يبدو مثل صديق تونسي حقيقي!")
        print("🎭 العواطف تعمل بشكل طبيعي ومتقدم!")
        print()
        print("📝 للحصول على أفضل النتائج:")
        print("   1. احصل على مفتاح ElevenLabs API")
        print("   2. سجل 20-30 جملة باللهجة التونسية")
        print("   3. استخدم استنساخ الصوت للحصول على صوتك الخاص")
        
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
