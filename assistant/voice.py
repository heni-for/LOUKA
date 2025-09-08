from __future__ import annotations

import json
import queue
import sys
import time
import threading
import msvcrt

import sounddevice as sd
from vosk import Model, KaldiRecognizer
try:
	import webrtcvad
	HAS_VAD = True
except Exception:
	HAS_VAD = False
from rich import print

from .tts import speak
from .cli import inbox as cmd_inbox, read_message as cmd_read, organize as cmd_organize, draft as cmd_draft
from .llm import chat_with_ai
from .config import VOSK_MODEL_PATH

WAKE_PHRASES = ["luca", "hey luca", "ok luca", "okay luca", "hi luca"]
SAMPLE_RATE = 16000
FRAME_MS = 30  # 10/20/30ms supported by VAD
BYTES_PER_SAMPLE = 2  # int16
CHANNELS = 1
VAD_AGGRESSIVENESS = 2

# Noise filtering settings
MIN_UTTERANCE_LENGTH = 2  # Minimum characters for valid command (lowered)
NOISE_THRESHOLD = 0.01  # Minimum audio level to consider as speech (much lower)
SILENCE_TIMEOUT = 3.0  # Seconds of silence before giving up (increased)
MIN_WAKE_LENGTH = 2  # Minimum characters for wake word detection (lowered)

COMMAND_KEYWORDS = ["inbox", "list", "read", "organize", "organise", "draft", "cancel", "stop", "help", "chat", "ask", "question", "tell", "explain", "what", "how", "why", "when", "where", "who"]
WAKE_GRAMMAR = json.dumps(WAKE_PHRASES)
CMD_GRAMMAR = json.dumps(COMMAND_KEYWORDS)


def _frame_bytes(num_ms: int = FRAME_MS) -> int:
	return int(SAMPLE_RATE * (num_ms / 1000.0)) * BYTES_PER_SAMPLE * CHANNELS


def find_best_microphone() -> int | None:
	"""Automatically detect and return the best available microphone device index."""
	try:
		devices = sd.query_devices()
		input_devices = []
		
		for i, device in enumerate(devices):
			# Check if device has input channels
			if device.get('max_input_channels', 0) > 0:
				device_info = {
					'index': i,
					'name': device.get('name', f'Device {i}'),
					'channels': device.get('max_input_channels', 0),
					'is_default': device.get('is_default', False),
					'hostapi': device.get('hostapi', 0)
				}
				input_devices.append(device_info)
		
		if not input_devices:
			print("No input devices found!")
			return None
		
		# Sort by priority: default first, then by channel count, then by hostapi
		input_devices.sort(key=lambda x: (
			not x['is_default'],  # Default devices first
			-x['channels'],       # More channels first
			x['hostapi']          # Lower hostapi first (usually system audio)
		))
		
		best_device = input_devices[0]
		print(f"Auto-selected microphone: {best_device['name']} (Device {best_device['index']})")
		print(f"  Channels: {best_device['channels']}, Default: {best_device['is_default']}")
		
		return best_device['index']
		
	except Exception as e:
		print(f"Error detecting microphones: {e}")
		return None


class SpeechRecognizer:
	def __init__(self, model_path: str, input_device: int | None = None) -> None:
		self.model = Model(model_path)
		self.input_device = input_device
		if input_device is not None:
			sd.default.device = (input_device, None)
		dev_info = sd.query_devices(input_device, 'input') if input_device is not None else sd.query_devices(kind='input')
		max_in = int(dev_info.get('max_input_channels', 1) or 1)
		self.input_channels = max_in if max_in > 0 else 1
		self.wake_rec = KaldiRecognizer(self.model, SAMPLE_RATE, WAKE_GRAMMAR)
		self.cmd_rec = KaldiRecognizer(self.model, SAMPLE_RATE, CMD_GRAMMAR)
		self.free_rec = KaldiRecognizer(self.model, SAMPLE_RATE)
		self.active_rec = self.wake_rec
		self.audio_queue: "queue.Queue[bytes]" = queue.Queue()
		self.running = False
		self._last_partial = ""
		self.vad = webrtcvad.Vad(VAD_AGGRESSIVENESS) if HAS_VAD else None

	def _audio_callback(self, indata, frames, time_info, status):
		if status:
			print(status)
		self.audio_queue.put(bytes(indata))

	def start(self):
		self.running = True
		self.stream = sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=_frame_bytes() // (BYTES_PER_SAMPLE * CHANNELS), dtype='int16', channels=self.input_channels, callback=self._audio_callback)
		self.stream.start()

	def stop(self):
		self.running = False
		try:
			self.stream.stop()
			self.stream.close()
		except Exception:
			pass

	def _read_frame(self) -> bytes:
		data = self.audio_queue.get()
		
		# If VAD is available, use it for better speech detection
		if self.vad is not None:
			if len(data) >= _frame_bytes() and self.vad.is_speech(data[:_frame_bytes()], SAMPLE_RATE):
				return data
			return b""
		
		# More aggressive noise filtering to prevent false positives
		if len(data) >= _frame_bytes():
			import numpy as np
			audio_data = np.frombuffer(data, dtype=np.int16)
			# Calculate audio level with safety check for empty arrays
			mean_squared = np.mean(audio_data**2)
			audio_level = np.sqrt(mean_squared) / 32768.0 if mean_squared > 0 else 0.0
			
			# Only process audio that's clearly above background noise
			if audio_level < 0.01:  # Higher threshold to filter out background noise
				return b""
			
			# Additional check: look for actual speech patterns
			# Check for variation in the audio signal (speech has more variation than noise)
			audio_variation = np.std(audio_data) / 32768.0
			if audio_variation < 0.005:  # Very low variation = likely noise
				return b""
		
		return data

	def listen_text(self, mode: str = "wake") -> str:
		self.active_rec = {"wake": self.wake_rec, "cmd": self.cmd_rec}.get(mode, self.free_rec)
		start_time = time.time()
		last_activity = time.time()
		frames_processed = 0
		speech_detected = False
		silence_frames = 0
		
		print(f"Listening in {mode} mode...")
		print("Speak clearly - I'll only respond to actual speech")
		
		while self.running:
			data = self._read_frame()
			if not data:
				silence_frames += 1
				# Check for silence timeout
				if time.time() - last_activity > SILENCE_TIMEOUT:
					print("Silence timeout reached")
					return ""
				continue
			
			last_activity = time.time()
			frames_processed += 1
			silence_frames = 0
			
			# Only process if we've detected some speech activity
			if not speech_detected:
				# Check if this looks like actual speech
				import numpy as np
				audio_data = np.frombuffer(data, dtype=np.int16)
				# Calculate audio level with safety check
				mean_squared = np.mean(audio_data**2)
				audio_level = np.sqrt(mean_squared) / 32768.0 if mean_squared > 0 else 0.0
				audio_variation = np.std(audio_data) / 32768.0
				
				if audio_level > 0.02 and audio_variation > 0.01:  # Clear speech indicators
					speech_detected = True
					print("Speech detected, processing...")
				else:
					continue
			
			# Process every frame for better recognition
			if self.active_rec.AcceptWaveform(data):
				res = json.loads(self.active_rec.Result())
				self._last_partial = ""
				text = res.get("text", "").strip()
				
				print(f"Final result: '{text}' (length: {len(text)})")
				
				# Filter out very short or common noise words
				if len(text) < 2 or text.lower() in ["the", "a", "an", "and", "or", "but"]:
					continue
					
				if text:
					print(f"= {text}")
					
				if mode == "wake" and text in WAKE_PHRASES:
					return "wake"
				elif mode == "cmd" and text in COMMAND_KEYWORDS:
					return text
				elif mode == "free":
					return text
					
			# Process partial results but be more selective
			partial_json = json.loads(self.active_rec.PartialResult())
			partial = partial_json.get("partial", "").strip()
			
			if partial and partial != self._last_partial and len(partial) >= 2:
				# Only show partial results that look like real words
				if not partial.lower() in ["the", "a", "an", "and", "or", "but"]:
					print(f"> {partial}")
				self._last_partial = partial
				
				# Check for wake phrases in partial results
				if mode == "wake" and partial in WAKE_PHRASES:
					return "wake"
			
			# Debug: show progress every 100 frames
			if frames_processed % 100 == 0:
				print(f"Processed {frames_processed} frames...")
				
		return ""


def say(text: str) -> None:
	print(text)
	speak(text)


def voice_inbox() -> None:
	try:
		from .outlook_local import list_inbox as list_inbox_local
		msgs = list_inbox_local(top=5)
		if not msgs:
			say("Your inbox is empty.")
			return
		subjects = [m.get("subject", "") or "no subject" for m in msgs]
		narration = "Here are your top messages: " + "; ".join(f"{i+1}. {s}" for i, s in enumerate(subjects))
		say(narration)
	except Exception:
		say("I couldn't access Outlook inbox.")


# Global conversation history
conversation_history = []

def parse_command(text: str) -> None:
	global conversation_history
	low = text.lower().strip()
	if not low or len(low) < MIN_UTTERANCE_LENGTH:
		return
	print(f"Heard: {low}")
	
	# Email-specific commands
	if low.startswith("read"):
		say("Say read then the message ID from the inbox list.")
	elif low.startswith("inbox") or low.startswith("list"):
		say("Listing your inbox.")
		cmd_inbox(10, "local")
		voice_inbox()
	elif low.startswith("organize") or low.startswith("organise"):
		say("Organizing recent emails in dry run mode.")
		cmd_organize(True, "local")
		say("Done organizing preview.")
	elif low.startswith("draft"):
		say("What should I write?")
		prompt = rec.listen_text(mode="free") if 'rec' in globals() else ""
		if prompt and len(prompt.strip()) >= MIN_UTTERANCE_LENGTH:
			say("Creating a draft in Outlook.")
			cmd_draft(prompt, "", True, "local")
			say("Draft is ready.")
		else:
			say("I did not catch the prompt.")
	elif low.startswith("help"):
		say("I can help with email commands: inbox, organize, read, draft. Or just ask me anything!")
	elif low.startswith("clear") or low.startswith("reset"):
		conversation_history = []
		say("Conversation history cleared.")
	else:
		# General AI chat for anything else
		try:
			say("Let me think about that...")
			response = chat_with_ai(text, conversation_history)
			
			# Add to conversation history
			conversation_history.append({"role": "user", "content": text})
			conversation_history.append({"role": "assistant", "content": response})
			
			# Keep only last 10 exchanges to manage memory
			if len(conversation_history) > 20:
				conversation_history = conversation_history[-20:]
			
			say(response)
		except Exception as e:
			say(f"Sorry, I had trouble processing that. Error: {str(e)}")
			print(f"AI Chat error: {e}")


def _ptt_listener(stop_event: threading.Event):
	while not stop_event.is_set():
		if msvcrt.kbhit():
			key = msvcrt.getwch()
			if key == "\r":  # Enter key
				return  # signal to start speech capture
			elif key == "\x03":  # Ctrl+C
				stop_event.set()
				return


def main():
	print("Starting Luca - Your AI Voice Assistant")
	print("Press Enter to speak (push-to-talk).")
	print("Usage: python -m assistant.voice [mic_index] [model_path]")
	print("\nCapabilities:")
	print("• Email: inbox, organize, read, draft")
	print("• General AI chat: ask questions, get help, brainstorm")
	print("• Commands: help, clear conversation")
	print("\nDebug mode: Shows detailed speech recognition info")
	global rec
	model_path = VOSK_MODEL_PATH
	mic_index = None
	
	# Parse command line arguments
	if len(sys.argv) >= 2:
		try:
			mic_index = int(sys.argv[1])
		except ValueError:
			model_path = sys.argv[1]
	if len(sys.argv) >= 3:
		model_path = sys.argv[2]
	
	# Auto-detect best microphone if not specified
	if mic_index is None:
		print("Auto-detecting best microphone...")
		mic_index = find_best_microphone()
		if mic_index is None:
			print("No suitable microphone found. Please check your audio devices.")
			return
	
	# Initialize voice recognition
	try:
		rec = SpeechRecognizer(model_path, mic_index)
		print(f"Using microphone device index: {mic_index}")
	except Exception as e:
		print("Voice setup error:", e)
		print("If it's a model error, set VOSK_MODEL_PATH in .env or pass the model path.")
		return

	rec.start()
	say("Voice assistant is ready. Press Enter to speak.")
	try:
		while True:
			# Only listen when explicitly triggered - no background listening
			print("Press Enter to speak or Ctrl+C to quit.")
			
			# Wait for Enter key press only
			stop_evt = threading.Event()
			listener = threading.Thread(target=_ptt_listener, args=(stop_evt,), daemon=True)
			listener.start()
			
			# Simple wait for Enter key
			while listener.is_alive():
				time.sleep(0.1)
			
			# Enter was pressed - start listening
			say("Listening…")
			utterance = rec.listen_text(mode="free")
			parse_command(utterance)
	except KeyboardInterrupt:
		pass
	finally:
		if rec:
			rec.stop()


if __name__ == "__main__":
	main()
