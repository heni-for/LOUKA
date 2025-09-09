import pyttsx3

_engine = None

def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', 200)  # Faster rate for quicker responses
        _engine.setProperty('volume', 0.9)  # Slightly lower volume for comfort
        # Try to choose a high-quality voice
        try:
            voices = _engine.getProperty('voices')
            preferred = None
            
            # Voice preference order (best to worst)
            voice_preferences = [
                'zira', 'david', 'aria', 'hazel', 'susan', 'mark', 'richard',
                'arabic', 'tunisian', 'tunisia', 'ar-', 'ar_'
            ]
            
            for preference in voice_preferences:
                for v in voices:
                    name = (getattr(v, 'name', '') or '').lower()
                    if preference in name:
                        preferred = v.id
                        break
                if preferred:
                    break
            
            if preferred:
                _engine.setProperty('voice', preferred)
                print(f"Using voice: {preferred}")
            else:
                print("Using default voice")
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
