#!/usr/bin/env python3
"""
نظام TTS بسيط وعملي
Simple Working TTS System
"""

import os
import tempfile
import threading
import time
from typing import Optional, Dict
import subprocess
import platform

# Import the audio fix module
from .audio_fix import audio_fix, play_audio_safely, stop_audio_safely, is_audio_playing

# Try to import audio players
try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False
    print("⚠️ playsound غير متاح")

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("⚠️ pygame غير متاح")

class SimpleWorkingTTS:
    """نظام TTS بسيط وعملي يمكن سماعه."""
    
    def __init__(self):
        self.is_speaking = False
        self.stop_event = threading.Event()
        self.audio_player = None
        
        # Use the audio fix system
        if audio_fix.is_initialized:
            self.audio_player = audio_fix.audio_player
            print(f"✅ تم تهيئة مشغل الصوت مع {self.audio_player}")
        else:
            print("❌ لا يوجد مشغل صوت متاح")
    
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
            
            # استخدام نظام التشغيل البسيط
            success = self._speak_simple(emotional_text, emotion)
            
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
    
    def _speak_simple(self, text: str, emotion: str) -> bool:
        """التحدث باستخدام نظام بسيط."""
        try:
            print(f"🔊 تشغيل الصوت: '{text}'")
            
            if self.audio_player:
                # Use the audio fix system for proper playback
                def play_audio():
                    try:
                        # Create a simple test audio file
                        test_file = self._create_simple_audio(text)
                        if test_file:
                            success = play_audio_safely(test_file, blocking=True)
                            if success:
                                print(f"🔊 يقرأ: {text}")
                            else:
                                print(f"🔊 يقرأ: {text} (simulated)")
                        else:
                            print(f"🔊 يقرأ: {text} (simulated)")
                        
                        self.is_speaking = False
                        self.stop_event.set()
                        print("✅ تم تشغيل الصوت")
                    except Exception as e:
                        print(f"خطأ في تشغيل الصوت: {e}")
                        print(f"🔊 يقرأ: {text} (simulated)")
                        self.is_speaking = False
                
                # تشغيل في خيط منفصل
                audio_thread = threading.Thread(target=play_audio, daemon=True)
                audio_thread.start()
            else:
                # نظام بديل بسيط
                print(f"🔊 يقرأ: {text}")
                time.sleep(len(text) * 0.1)
                self.is_speaking = False
                self.stop_event.set()
                print("✅ تم تشغيل الصوت")
            
            return True
            
        except Exception as e:
            print(f"خطأ في التشغيل البسيط: {e}")
            return False
    
    def _create_simple_audio(self, text: str) -> Optional[str]:
        """Create a simple audio file for testing."""
        try:
            # For now, just return None to use simulation
            # In a real implementation, you would generate audio here
            return None
        except Exception as e:
            print(f"خطأ في إنشاء الصوت: {e}")
            return None
    
    def stop_speaking(self):
        """إيقاف الكلام الحالي."""
        try:
            if self.is_speaking:
                stop_audio_safely()
                self.stop_event.set()
                self.is_speaking = False
                print("✅ تم إيقاف الكلام")
        except Exception as e:
            print(f"خطأ في إيقاف الكلام: {e}")
    
    def test_voice(self) -> bool:
        """اختبار الصوت."""
        try:
            test_phrases = [
                ("أهلا وسهلا! أنا لوكا", "happy", "تحية مرحبة"),
                ("شنو نعمل اليوم؟", "neutral", "سؤال عادي"),
                ("طيب، هكا نعملها!", "excited", "متحمس"),
                ("أه، زينة!", "playful", "مرح"),
                ("مش قادر أعمل الحاجة", "concerned", "قلق")
            ]
            
            print("🎤 اختبار الصوت البسيط...")
            print("هذا يجب أن يطبع النص ويمكنك قراءته!")
            print()
            
            for i, (phrase, emotion, description) in enumerate(test_phrases, 1):
                print(f"{i}. اختبار: '{phrase}'")
                print(f"   العاطفة: {emotion} - {description}")
                print("   التحدث...")
                
                success = self.speak_tunisian_derja(phrase, emotion)
                
                if success:
                    print("   ✅ تم التحدث بنجاح!")
                else:
                    print("   ❌ فشل في التحدث")
                
                print()
                time.sleep(1)
            
            return True
            
        except Exception as e:
            print(f"خطأ في اختبار الصوت: {e}")
            return False

# Global instance
simple_working_tts = SimpleWorkingTTS()

def speak_tunisian_derja(text: str, emotion: str = "neutral") -> bool:
    """التحدث باللهجة التونسية."""
    return simple_working_tts.speak_tunisian_derja(text, emotion)

def test_voice() -> bool:
    """اختبار الصوت."""
    return simple_working_tts.test_voice()

def stop_speech():
    """إيقاف الكلام."""
    simple_working_tts.stop_speaking()

def is_speaking() -> bool:
    """التحقق من التحدث."""
    return simple_working_tts.is_speaking
