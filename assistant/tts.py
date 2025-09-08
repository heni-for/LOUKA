import pyttsx3

_engine = None

def _get_engine():
	global _engine
	if _engine is None:
		_engine = pyttsx3.init()
		_engine.setProperty('rate', 180)
		_engine.setProperty('volume', 1.0)
		# Try to choose a common Windows voice if present
		try:
			voices = _engine.getProperty('voices')
			preferred = None
			for v in voices:
				name = (getattr(v, 'name', '') or '').lower()
				if 'zira' in name or 'david' in name or 'aria' in name:
					preferred = v.id
					break
			if preferred:
				_engine.setProperty('voice', preferred)
		except Exception:
			pass
	return _engine


def speak(text: str) -> None:
	engine = _get_engine()
	engine.say(text)
	engine.runAndWait()
