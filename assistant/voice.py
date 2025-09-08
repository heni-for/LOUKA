from __future__ import annotations

import json
import queue
import sys
import time

import sounddevice as sd
from vosk import Model, KaldiRecognizer
from rich import print

from .tts import speak
from .cli import inbox as cmd_inbox, read_message as cmd_read, organize as cmd_organize, draft as cmd_draft

WAKE_WORDS_HEY = {"hey", "hi", "ok", "okay"}
WAKE_WORDS_LUCA = {"luca", "luka", "looka"}
SAMPLE_RATE = 16000
WAKE_WINDOW_SECONDS = 2.0

COMMAND_KEYWORDS = ["inbox", "list", "read", "organize", "organise", "draft", "cancel", "stop"]
WAKE_GRAMMAR = json.dumps(sorted(list(WAKE_WORDS_HEY | WAKE_WORDS_LUCA)))
CMD_GRAMMAR = json.dumps(COMMAND_KEYWORDS)


class SpeechRecognizer:
	def __init__(self, model_path: str, input_device: int | None = None) -> None:
		self.model = Model(model_path)
		self.input_device = input_device
		if input_device is not None:
			sd.default.device = (input_device, None)
		dev_info = sd.query_devices(input_device, 'input') if input_device is not None else sd.query_devices(kind='input')
		max_in = int(dev_info.get('max_input_channels', 1) or 1)
		self.input_channels = max_in if max_in > 0 else 1
		print(f"Mic device channels: using {self.input_channels} (max {max_in})")
		# Two recognizers: wake (restricted grammar) and command (restricted to keywords)
		self.wake_rec = KaldiRecognizer(self.model, SAMPLE_RATE, WAKE_GRAMMAR)
		self.cmd_rec = KaldiRecognizer(self.model, SAMPLE_RATE, CMD_GRAMMAR)
		self.free_rec = KaldiRecognizer(self.model, SAMPLE_RATE)
		self.active_rec = self.wake_rec
		self.audio_queue: "queue.Queue[bytes]" = queue.Queue()
		self.running = False
		self._last_partial = ""
		self._saw_hey_at = 0.0
		self._saw_luca_at = 0.0

	def _audio_callback(self, indata, frames, time_info, status):
		if status:
			print(status)
		self.audio_queue.put(bytes(indata))

	def start(self):
		self.running = True
		self.stream = sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=self.input_channels, callback=self._audio_callback)
		self.stream.start()

	def stop(self):
		self.running = False
		try:
			self.stream.stop()
			self.stream.close()
		except Exception:
			pass

	def _update_wake_memory(self, text: str) -> bool:
		now = time.time()
		low = text.lower()
		if any(w in low.split() for w in WAKE_WORDS_HEY):
			self._saw_hey_at = now
		if any(w in low.split() for w in WAKE_WORDS_LUCA) or "luca" in low:
			self._saw_luca_at = now
		return (now - self._saw_hey_at) <= WAKE_WINDOW_SECONDS and (now - self._saw_luca_at) <= WAKE_WINDOW_SECONDS

	def listen_text(self, mode: str = "wake") -> str:
		# mode: wake | cmd | free
		self.active_rec = {"wake": self.wake_rec, "cmd": self.cmd_rec}.get(mode, self.free_rec)
		while self.running:
			data = self.audio_queue.get()
			if self.active_rec.AcceptWaveform(data):
				res = json.loads(self.active_rec.Result())
				self._last_partial = ""
				text = res.get("text", "")
				if mode == "wake" and self._update_wake_memory(text):
					return "wake"
				return text
			partial_json = json.loads(self.active_rec.PartialResult())
			partial = partial_json.get("partial", "").strip()
			if partial and partial != self._last_partial:
				print(f"> {partial}")
				self._last_partial = partial
				if mode == "wake" and self._update_wake_memory(partial):
					return "wake"
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


def parse_command(text: str) -> None:
	low = text.lower().strip()
	if not low:
		return
	print(f"Heard: {low}")
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
		# Switch to free dictation for prompt
		prompt = rec.listen_text(mode="free") if 'rec' in globals() else ""
		if prompt:
			say("Creating a draft in Outlook.")
			cmd_draft(prompt, "", True, "local")
			say("Draft is ready.")
		else:
			say("I did not catch the prompt.")
	else:
		say("Try: inbox, organize, read, or draft.")


def main():
	print("Starting voice assistant. Wake word: 'hey luca'")
	print("Usage: python -m assistant.voice [mic_index] [model_path]")
	global rec
	model_path = "vosk-model-small-en-us-0.15"
	mic_index = None
	if len(sys.argv) >= 2:
		try:
			mic_index = int(sys.argv[1])
		except ValueError:
			model_path = sys.argv[1]
	if len(sys.argv) >= 3:
		model_path = sys.argv[2]
	try:
		rec = SpeechRecognizer(model_path, mic_index)
		if mic_index is not None:
			print(f"Using microphone device index: {mic_index}")
	except Exception as e:
		print("Voice setup error:", e)
		print("If it's a model error, download from https://alphacephei.com/vosk/models and unpack here.")
		return

	rec.start()
	say("Voice assistant is ready. Say hey luca.")
	try:
		while True:
			if rec.listen_text(mode="wake") != "wake":
				continue
			say("Yes?")
			cmd_word = rec.listen_text(mode="cmd")
			parse_command(cmd_word)
	except KeyboardInterrupt:
		pass
	finally:
		rec.stop()


if __name__ == "__main__":
	main()
