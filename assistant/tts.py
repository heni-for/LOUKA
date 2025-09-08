import pyttsx3

_engine = None

def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', 200)  # Natural speech rate
        _engine.setProperty('volume', 1.0)
        # Try to choose a Tunisian Arabic voice if present
        try:
            voices = _engine.getProperty('voices')
            preferred = None
            for v in voices:
                name = (getattr(v, 'name', '') or '').lower()
                # Look for Arabic voices first
                if any(keyword in name for keyword in ['arabic', 'tunisian', 'tunisia', 'ar-', 'ar_']):
                    preferred = v.id
                    break
                # Fallback to common voices
                elif 'zira' in name or 'david' in name or 'aria' in name:
                    preferred = v.id
            if preferred:
                _engine.setProperty('voice', preferred)
                print(f"Using voice: {preferred}")
        except Exception as e:
            print(f"Voice selection error: {e}")
    return _engine


def speak(text: str) -> None:
	# Try fast TTS first
	try:
		from .tts_arabic import speak_fast
		speak_fast(text)
		return
	except Exception as e:
		print(f"Fast TTS failed: {e}")
	
	# Try simple TTS as fallback
	try:
		from .tts_simple import speak as simple_speak
		simple_speak(text)
		return
	except Exception as e:
		print(f"Simple TTS failed: {e}")
	
	# Final fallback to default TTS
	try:
		engine = _get_engine()
		engine.say(text)
		engine.runAndWait()
	except Exception as e:
		print(f"Default TTS failed: {e}")
		print("❌ All TTS methods failed - text will not be spoken")
