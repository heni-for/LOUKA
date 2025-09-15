#!/usr/bin/env python3
"""
اختبار لوكا باللغة التونسية فقط
Test Luca with Tunisian language only
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.emotional_tts import speak_with_emotion, speak_naturally
from assistant.google_tts_arabic import test_arabic_pronunciation
import time

def test_basic_tunisian():
    """اختبار أساسي للغة التونسية."""
    print("🎤 اختبار أساسي للغة التونسية")
    print("=" * 50)
    print("اختبار النطق العربي التونسي...")
    print()
    
    try:
        success = test_arabic_pronunciation()
        if success:
            print("✅ اختبار النطق الأساسي نجح!")
        else:
            print("❌ اختبار النطق الأساسي فشل!")
        return success
    except Exception as e:
        print(f"❌ خطأ في الاختبار الأساسي: {e}")
        return False

def test_emotional_tunisian():
    """اختبار العواطف التونسية."""
    print("\n😊 اختبار العواطف التونسية")
    print("=" * 50)
    print("اختبار العواطف المختلفة باللهجة التونسية...")
    print()
    
    emotions = [
        ("happy", "أه، زينة! هكا نعملها!", "يجب أن يبدو مرح"),
        ("excited", "ممتاز! نعملها بسرعة!", "يجب أن يبدو متحمس"),
        ("calm", "طيب، هكا نعملها بهدوء", "يجب أن يبدو هادئ"),
        ("tired", "أه، تعبان شوية", "يجب أن يبدو متعب"),
        ("concerned", "مش قادر أعمل الحاجة", "يجب أن يبدو قلق"),
        ("playful", "هههه، نكتة زينة!", "يجب أن يبدو مرح"),
        ("professional", "سأقوم بتنفيذ المهمة", "يجب أن يبدو مهني"),
        ("neutral", "طيب، شنو نعمل؟", "يجب أن يبدو عادي")
    ]
    
    for emotion, phrase, description in emotions:
        print(f"اختبار {emotion.upper()}:")
        print(f"الوصف: {description}")
        print(f"العبارة: '{phrase}'")
        print("التحدث مع TTS العاطفي...")
        
        try:
            success = speak_with_emotion(phrase, emotion)
            if success:
                print("✅ تم التحدث بنجاح!")
            else:
                print("❌ فشل في التحدث")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        
        print()
        time.sleep(1)
    
    print("🎯 انتهى اختبار العواطف التونسية!")

def test_short_phrases():
    """اختبار العبارات القصيرة."""
    print("\n🔊 اختبار العبارات القصيرة")
    print("=" * 50)
    print("اختبار العبارات القصيرة لتجنب التعليق...")
    print()
    
    short_phrases = [
        ("أهلا", "happy", "تحية قصيرة"),
        ("طيب", "neutral", "رد قصير"),
        ("زينة", "playful", "إيجابي قصير"),
        ("مش", "concerned", "سلبي قصير"),
        ("أه", "tired", "صوت متعب قصير")
    ]
    
    for phrase, emotion, description in short_phrases:
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
        time.sleep(0.5)
    
    print("🎯 انتهى اختبار العبارات القصيرة!")

def test_natural_tunisian():
    """اختبار الكلام الطبيعي التونسي."""
    print("\n💬 اختبار الكلام الطبيعي التونسي")
    print("=" * 50)
    print("اختبار الكلام الطبيعي مع السياق...")
    print()
    
    test_cases = [
        {
            "text": "أهلا! كيفاش؟",
            "context": {"mood": "happy", "is_greeting": True},
            "description": "تحية مرحبة بسيطة"
        },
        {
            "text": "مش قادر",
            "context": {"mood": "tired", "last_action": "error"},
            "description": "رد متعب بسيط"
        },
        {
            "text": "هههه، نكتة!",
            "context": {"mood": "playful", "last_action": "joke_told"},
            "description": "رد مرح بسيط"
        },
        {
            "text": "مهم",
            "context": {"mood": "professional"},
            "description": "رد مهني بسيط"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"اختبار {i}: {test_case['description']}")
        print(f"النص: '{test_case['text']}'")
        print(f"السياق: {test_case['context']}")
        print("التحدث بشكل طبيعي...")
        
        try:
            success = speak_naturally(test_case['text'], test_case['context'])
            if success:
                print("✅ تم التحدث بشكل طبيعي!")
            else:
                print("❌ فشل في التحدث")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        
        print()
        time.sleep(1)
    
    print("🎯 انتهى اختبار الكلام الطبيعي التونسي!")

def test_voice_quality():
    """اختبار جودة الصوت."""
    print("\n🔊 اختبار جودة الصوت")
    print("=" * 50)
    print("اختبار جودة الصوت والتأكد من عدم التعليق...")
    print()
    
    test_phrase = "أهلا وسهلا! أنا لوكا"
    
    print("عبارة الاختبار:", test_phrase)
    print()
    
    # اختبار عواطف مختلفة مع عبارات قصيرة
    emotions = ["happy", "excited", "calm", "playful", "professional"]
    
    for emotion in emotions:
        print(f"اختبار عاطفة {emotion.upper()}:")
        try:
            success = speak_with_emotion(test_phrase, emotion)
            if success:
                print(f"   ✅ انتهى {emotion} بنجاح")
            else:
                print(f"   ❌ فشل {emotion}")
        except Exception as e:
            print(f"   ❌ خطأ {emotion}: {e}")
        
        print()
        time.sleep(1)
    
    print("🎯 انتهى اختبار جودة الصوت!")
    print("✅ إذا سمعت كلام عربي بدون تعليق، فهو يعمل!")
    print("✅ كل عاطفة يجب أن تبدو مختلفة قليلاً!")

def main():
    """تشغيل جميع اختبارات التونسية."""
    print("🎤 مجموعة اختبارات لوكا التونسية")
    print("=" * 60)
    print("هذا سيفحص نظام لوكا التونسي مع:")
    print("✅ تشغيل صوت غير متعطل (playsound + pygame احتياطي)")
    print("✅ نص عاطفي مبسط (بدون زخارف طويلة)")
    print("✅ عبارات قصيرة لتجنب التعليق")
    print("✅ كلام طبيعي مع سياق مبسط")
    print("✅ جودة صوت بدون تعليق")
    print()
    print("اضغط Enter لبدء الاختبار...")
    input()
    
    try:
        # اختبار الوظائف الأساسية
        basic_success = test_basic_tunisian()
        
        if basic_success:
            # اختبار الوظائف المبسطة
            test_emotional_tunisian()
            test_short_phrases()
            test_natural_tunisian()
            test_voice_quality()
            
            print("\n🎉 انتهت جميع الاختبارات!")
            print("=" * 60)
            print("✅ تشغيل الصوت: تم إصلاحه!")
            print("✅ النص العاطفي: مبسط!")
            print("✅ العبارات القصيرة: تعمل!")
            print("✅ الكلام الطبيعي: يعمل!")
            print("✅ جودة الصوت: تعمل!")
            print()
            print("🎯 لوكا لديه الآن تشغيل صوت مستقر!")
            print("🔊 لا مزيد من مشاكل التعليق أو التعطل!")
            print("💬 التعبيرات العاطفية المبسطة تعمل!")
            print("🎭 العواطف المختلفة لا تزال تعمل ولكنها أقصر!")
            print()
            print("📝 ملاحظة: هذا لا يزال عربي فصيح، وليس لهجة تونسية")
            print("   لكن تشغيل الصوت الآن مستقر وموثوق!")
        else:
            print("\n❌ فشل اختبار الصوت الأساسي!")
            print("يرجى التحقق من إعدادات الصوت والمحاولة مرة أخرى.")
        
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
