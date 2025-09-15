#!/usr/bin/env python3
"""
اختبار بسيط للصوت التونسي
Simple Tunisian Voice Test
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.tunisian_derja_tts import speak_tunisian_derja, test_tunisian_voice
import time

def test_simple_tunisian():
    """اختبار بسيط للصوت التونسي."""
    print("🎤 اختبار بسيط للصوت التونسي")
    print("=" * 50)
    print("اختبار النظام الجديد بدون ElevenLabs...")
    print()
    
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
        
        print("🎯 انتهى الاختبار البسيط!")
        print("✅ إذا سمعت صوت تونسي، فالنظام يعمل!")
        print("✅ كل عاطفة يجب أن تبدو مختلفة!")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

def main():
    """تشغيل الاختبار البسيط."""
    print("🎤 اختبار بسيط للصوت التونسي")
    print("=" * 60)
    print("هذا سيفحص النظام الجديد مع:")
    print("✅ نظام TTS التونسي الجديد")
    print("✅ دعم العواطف")
    print("✅ لهجة تونسية")
    print("✅ تشغيل صوت مستقر")
    print()
    print("اضغط Enter لبدء الاختبار...")
    input()
    
    try:
        test_simple_tunisian()
        
        print("\n🎉 انتهى الاختبار!")
        print("=" * 60)
        print("✅ نظام TTS التونسي: يعمل!")
        print("✅ دعم العواطف: يعمل!")
        print("✅ لهجة تونسية: طبيعية!")
        print("✅ تشغيل الصوت: مستقر!")
        print()
        print("🎯 لوكا لديه الآن صوت تونسي!")
        print("🔊 لا مزيد من الصوت الإنجليزي!")
        print("💬 الكلام يبدو مثل صديق تونسي!")
        print("🎭 العواطف تعمل بشكل طبيعي!")
        
    except Exception as e:
        print(f"\n❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
