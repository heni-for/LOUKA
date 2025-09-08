#!/usr/bin/env python3
"""
Tunisian Arabic Text-to-Speech using online services
"""

import requests
import os
import tempfile
import subprocess
from typing import Optional

def speak_arabic(text: str) -> None:
    """Speak text in Tunisian Arabic using online TTS."""
    try:
        # Try Google Translate TTS for Arabic
        url = "https://translate.google.com/translate_tts"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://translate.google.com/',
            'Accept': 'audio/mpeg,audio/*,*/*;q=0.9'
        }
        params = {
            'ie': 'UTF-8',
            'q': text,
            'tl': 'ar',  # Arabic
            'client': 'tw-ob',
            'idx': '0',
            'total': '1',
            'textlen': str(len(text)),
            'tk': '0'  # Add token parameter
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_file.write(response.content)
                tmp_file_path = tmp_file.name
            
            # Play the audio file
            try:
                subprocess.run(['start', tmp_file_path], shell=True, check=True)
            except:
                # Fallback to default player
                os.startfile(tmp_file_path)
            
            # Clean up after a delay
            import threading
            import time
            def cleanup():
                time.sleep(5)
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass
            threading.Thread(target=cleanup, daemon=True).start()
            
        else:
            print(f"TTS Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Arabic TTS Error: {e}")
        # Fallback to regular TTS
        from .tts import speak
        speak(text)

def speak_tunisian(text: str) -> None:
    """Speak text in Tunisian Arabic."""
    # Convert common English phrases to Arabic
    arabic_text = convert_to_arabic(text)
    speak_arabic(arabic_text)

def speak_fast(text: str) -> None:
    """Speak text with faster rate."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 200)  # Natural speech rate
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Fast TTS error: {e}")
        # Fallback to regular TTS
        speak(text)

def convert_to_arabic(text: str) -> str:
    """Convert common English phrases to Arabic."""
    translations = {
        "Hello": "مرحبا",
        "Hi": "أهلا",
        "Thank you": "شكرا",
        "Yes": "نعم",
        "No": "لا",
        "Good": "جيد",
        "Bad": "سيء",
        "Email": "بريد إلكتروني",
        "Inbox": "صندوق الوارد",
        "Read": "اقرأ",
        "Draft": "مسودة",
        "Organize": "تنظيم",
        "Help": "مساعدة",
        "Error": "خطأ",
        "Success": "نجح",
        "Loading": "جاري التحميل",
        "Ready": "جاهز",
        "Listening": "أستمع",
        "From": "من",
        "Subject": "الموضوع",
        "Last email": "آخر بريد إلكتروني",
        "Recent emails": "البريد الإلكتروني الأخير",
        "Would you like me to": "هل تريد مني",
        "Draft a reply": "كتابة رد",
        "Read another email": "قراءة بريد إلكتروني آخر",
        "Read the full content": "قراءة المحتوى الكامل"
    }
    
    # Convert text to Arabic
    arabic_text = text
    for english, arabic in translations.items():
        arabic_text = arabic_text.replace(english, arabic)
    
    return arabic_text
