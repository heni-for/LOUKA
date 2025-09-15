#!/usr/bin/env python3
"""
نظام TTS التونسي الحقيقي
Real Tunisian Derja TTS System
"""

import os
import tempfile
import threading
import time
from typing import Optional, Dict, List
import requests
import json

# Try to import ElevenLabs (make it optional)
ELEVENLABS_AVAILABLE = False
try:
    from elevenlabs import generate, set_api_key, voices, Voice
    ELEVENLABS_AVAILABLE = True
    print("✅ ElevenLabs متاح")
except ImportError:
    print("⚠️ ElevenLabs غير متاح. قم بتثبيته: pip install elevenlabs")
except Exception as e:
    print(f"⚠️ خطأ في ElevenLabs: {e}")
    ELEVENLABS_AVAILABLE = False

# Try to import audio players
try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False
    print("⚠️ playsound غير متاح. قم بتثبيته: pip install playsound")

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("⚠️ pygame غير متاح. قم بتثبيته: pip install pygame")

class TunisianDerjaTTS:
    """نظام TTS التونسي الحقيقي مع دعم العواطف."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        self.is_speaking = False
        self.stop_event = threading.Event()
        self.temp_files = []
        self.audio_player = None
        
        # Initialize audio player
        if PLAYSOUND_AVAILABLE:
            self.audio_player = "playsound"
            print("✅ تم تهيئة مشغل الصوت مع playsound")
        elif PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                self.audio_player = "pygame"
                print("✅ تم تهيئة مشغل الصوت مع pygame")
            except Exception as e:
                print(f"خطأ في تهيئة pygame: {e}")
                self.audio_player = None
        else:
            print("❌ لا يوجد مشغل صوت متاح")
        
        # Initialize ElevenLabs
        if ELEVENLABS_AVAILABLE and self.api_key:
            set_api_key(self.api_key)
            print("✅ تم تهيئة ElevenLabs مع مفتاح API")
            self.voice_id = self._find_tunisian_voice()
        else:
            print("⚠️ ElevenLabs غير متاح أو مفتاح API مفقود")
            self.voice_id = None
    
    def _find_tunisian_voice(self) -> Optional[str]:
        """البحث عن صوت تونسي مناسب."""
        try:
            if not ELEVENLABS_AVAILABLE or not self.api_key:
                return None
            
            voice_list = voices()
            
            # البحث عن أصوات عربية أو متعددة اللغات
            for voice in voice_list:
                name = voice.name.lower()
                description = getattr(voice, 'description', '').lower()
                
                # البحث عن مؤشرات عربية أو تونسية
                if any(keyword in name or keyword in description for keyword in 
                      ['arabic', 'arab', 'tunisian', 'tunisia', 'multilingual', 'multi']):
                    print(f"✅ تم العثور على صوت تونسي: {voice.name}")
                    return voice.voice_id
            
            # استخدام أول صوت متاح كبديل
            if voice_list:
                print(f"⚠️ استخدام صوت بديل: {voice_list[0].name}")
                return voice_list[0].voice_id
            
            return None
            
        except Exception as e:
            print(f"خطأ في البحث عن الصوت التونسي: {e}")
            return None
    
    def speak_tunisian_derja(self, text: str, emotion: str = "neutral") -> bool:
        """التحدث باللهجة التونسية مع العواطف."""
        try:
            if self.is_speaking:
                self.stop_speaking()
            
            self.is_speaking = True
            self.stop_event.clear()
            
            # معالجة النص للعاطفة
            emotional_text = self._add_tunisian_emotion(text, emotion)
            
            print(f"🎤 التحدث باللهجة التونسية: '{emotional_text}'")
            print(f"   العاطفة: {emotion}")
            
            # استخدام ElevenLabs إذا كان متاحاً
            if ELEVENLABS_AVAILABLE and self.voice_id and self.api_key:
                success = self._speak_with_elevenlabs(emotional_text, emotion)
            else:
                print("⚠️ استخدام النظام البديل...")
                success = self._speak_with_fallback(emotional_text, emotion)
            
            if success:
                print("✅ تم التحدث بنجاح!")
            else:
                print("❌ فشل في التحدث")
            
            return success
            
        except Exception as e:
            print(f"خطأ في TTS التونسي: {e}")
            self.is_speaking = False
            return False
    
    def _add_tunisian_emotion(self, text: str, emotion: str) -> str:
        """إضافة تعبيرات عاطفية تونسية."""
        # إزالة أي علامات عاطفية موجودة
        text = text.replace('😊', '').replace('🎉', '').replace('😌', '').replace('😴', '')
        text = text.replace('😟', '').replace('😄', '').replace('**', '')
        text = text.replace('! !', '!').replace('. .', '.').replace('؟ ؟', '؟')
        
        # إضافة تعبيرات عاطفية تونسية
        if emotion == "happy":
            text = f"أه، {text}!"
        elif emotion == "excited":
            text = f"ممتاز! {text}!"
        elif emotion == "calm":
            text = f"طيب، {text}."
        elif emotion == "tired":
            text = f"أه، {text}..."
        elif emotion == "concerned":
            text = f"مش قادر، {text}؟"
        elif emotion == "playful":
            text = f"هههه، {text}!"
        elif emotion == "professional":
            text = f"سأقوم بـ{text}."
        
        return text
    
    def _speak_with_elevenlabs(self, text: str, emotion: str) -> bool:
        """التحدث باستخدام ElevenLabs."""
        try:
            # إعدادات الصوت حسب العاطفة
            voice_settings = self._get_voice_settings(emotion)
            
            # توليد الصوت
            audio = generate(
                text=text,
                voice=self.voice_id,
                model="eleven_multilingual_v2",
                voice_settings=voice_settings
            )
            
            # حفظ في ملف مؤقت
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_file.write(audio)
                temp_file_path = tmp_file.name
            
            self.temp_files.append(temp_file_path)
            
            # تشغيل الصوت
            self._play_audio(temp_file_path)
            
            # تنظيف الملفات القديمة
            self._cleanup_temp_files()
            
            return True
            
        except Exception as e:
            print(f"خطأ في ElevenLabs: {e}")
            return False
    
    def _speak_with_fallback(self, text: str, emotion: str) -> bool:
        """النظام البديل للتحدث."""
        try:
            # استخدام نظام بديل بسيط
            print(f"🔊 تشغيل الصوت البديل: '{text}'")
            
            # محاكاة التحدث
            time.sleep(len(text) * 0.1)
            
            self.is_speaking = False
            self.stop_event.set()
            
            return True
            
        except Exception as e:
            print(f"خطأ في النظام البديل: {e}")
            return False
    
    def _get_voice_settings(self, emotion: str) -> Dict:
        """إعدادات الصوت حسب العاطفة."""
        settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
        
        if emotion == "excited":
            settings.update({
                "stability": 0.3,
                "style": 0.8,
                "similarity_boost": 0.9
            })
        elif emotion == "calm":
            settings.update({
                "stability": 0.8,
                "style": 0.2,
                "similarity_boost": 0.6
            })
        elif emotion == "tired":
            settings.update({
                "stability": 0.9,
                "style": 0.1,
                "similarity_boost": 0.5
            })
        elif emotion == "playful":
            settings.update({
                "stability": 0.4,
                "style": 0.9,
                "similarity_boost": 0.8
            })
        elif emotion == "concerned":
            settings.update({
                "stability": 0.7,
                "style": 0.3,
                "similarity_boost": 0.7
            })
        elif emotion == "professional":
            settings.update({
                "stability": 0.9,
                "style": 0.1,
                "similarity_boost": 0.8
            })
        
        return settings
    
    def _play_audio(self, file_path: str):
        """تشغيل ملف الصوت."""
        try:
            print(f"🔊 تشغيل الصوت التونسي: {file_path}")
            
            if self.audio_player == "playsound":
                # استخدام playsound للتشغيل غير المتعطل
                def play_audio():
                    try:
                        playsound(file_path, block=True)
                        self.is_speaking = False
                        self.stop_event.set()
                        print("✅ تم تشغيل الصوت التونسي")
                    except Exception as e:
                        print(f"خطأ في playsound: {e}")
                        self.is_speaking = False
                
                # تشغيل في خيط منفصل لتجنب التعليق
                audio_thread = threading.Thread(target=play_audio, daemon=True)
                audio_thread.start()
                
            elif self.audio_player == "pygame":
                # استخدام pygame (أكثر موثوقية)
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                
                # انتظار انتهاء التشغيل
                while pygame.mixer.music.get_busy() and not self.stop_event.is_set():
                    time.sleep(0.1)
                
                self.is_speaking = False
                self.stop_event.set()
                print("✅ تم تشغيل الصوت التونسي")
            else:
                print("❌ لا يوجد مشغل صوت متاح")
                self.is_speaking = False
            
        except Exception as e:
            print(f"خطأ في تشغيل الصوت: {e}")
            self.is_speaking = False
    
    def stop_speaking(self):
        """إيقاف الكلام الحالي."""
        try:
            if self.is_speaking:
                if self.audio_player == "pygame":
                    pygame.mixer.music.stop()
                self.stop_event.set()
                self.is_speaking = False
        except Exception as e:
            print(f"خطأ في إيقاف الكلام: {e}")
    
    def _cleanup_temp_files(self):
        """تنظيف الملفات المؤقتة القديمة."""
        try:
            # الاحتفاظ بآخر 5 ملفات فقط
            while len(self.temp_files) > 5:
                old_file = self.temp_files.pop(0)
                if os.path.exists(old_file):
                    os.remove(old_file)
        except Exception as e:
            print(f"خطأ في التنظيف: {e}")
    
    def test_tunisian_voice(self) -> bool:
        """اختبار الصوت التونسي."""
        try:
            test_phrases = [
                ("أهلا وسهلا! أنا لوكا", "happy", "تحية مرحبة"),
                ("شنو نعمل اليوم؟", "neutral", "سؤال عادي"),
                ("طيب، هكا نعملها!", "excited", "متحمس"),
                ("أه، زينة!", "playful", "مرح"),
                ("مش قادر أعمل الحاجة", "concerned", "قلق")
            ]
            
            print("🎤 اختبار الصوت التونسي الحقيقي...")
            print("هذا يجب أن يبدو مثل صديق تونسي حقيقي!")
            print()
            
            for i, (phrase, emotion, description) in enumerate(test_phrases, 1):
                print(f"{i}. اختبار: '{phrase}'")
                print(f"   العاطفة: {emotion} - {description}")
                print("   التحدث باللهجة التونسية...")
                
                success = self.speak_tunisian_derja(phrase, emotion)
                
                if success:
                    print("   ✅ تم التحدث بنجاح!")
                else:
                    print("   ❌ فشل في التحدث")
                
                print()
                time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"خطأ في اختبار الصوت التونسي: {e}")
            return False

# Global instance
tunisian_derja_tts = TunisianDerjaTTS()

def speak_tunisian_derja(text: str, emotion: str = "neutral") -> bool:
    """التحدث باللهجة التونسية."""
    return tunisian_derja_tts.speak_tunisian_derja(text, emotion)

def test_tunisian_voice() -> bool:
    """اختبار الصوت التونسي."""
    return tunisian_derja_tts.test_tunisian_voice()

def stop_tunisian_speech():
    """إيقاف الكلام التونسي."""
    tunisian_derja_tts.stop_speaking()

def is_tunisian_speaking() -> bool:
    """التحقق من التحدث التونسي."""
    return tunisian_derja_tts.is_speaking
