from __future__ import annotations

from typing import Literal

from openai import OpenAI

from .config import OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, DEFAULT_MODEL


def _client() -> OpenAI:
	if AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT:
		return OpenAI(
			api_key=OPENAI_API_KEY,
			base_url=f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}",
			azure=True,
		)
	return OpenAI(api_key=OPENAI_API_KEY)


def summarize_email(subject: str, body_text: str) -> str:
	client = _client()
	content = f"Subject: {subject}\n\n{body_text}"
	prompt = (
		"Summarize the email in 2-3 bullet points focusing on actions, dates, and senders."
	)
	resp = client.chat.completions.create(
		model=DEFAULT_MODEL,
		messages=[
			{"role": "system", "content": "You summarize emails succinctly."},
			{"role": "user", "content": f"{prompt}\n\nEmail:\n{content}"},
		],
	)
	return resp.choices[0].message.content.strip()


def categorize_email(subject: str, body_text: str) -> str:
	client = _client()
	prompt = (
		"Classify the email into one of: Important, Newsletter, Social, Finance, Work, Personal, Spam."
	)
	resp = client.chat.completions.create(
		model=DEFAULT_MODEL,
		messages=[
			{"role": "system", "content": "You categorize emails."},
			{"role": "user", "content": f"{prompt}\n\nSubject: {subject}\nBody:\n{body_text[:2000]}"},
		],
	)
	return resp.choices[0].message.content.strip()


def draft_email(user_prompt: str) -> str:
	client = _client()
	resp = client.chat.completions.create(
		model=DEFAULT_MODEL,
		messages=[
			{"role": "system", "content": "You write professional yet concise emails."},
			{"role": "user", "content": user_prompt},
		],
	)
	return resp.choices[0].message.content.strip()
