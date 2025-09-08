from __future__ import annotations

import google.generativeai as genai
from typing import Literal

from .config import GEMINI_API_KEY, DEFAULT_MODEL


def _configure_gemini():
    """Configure Gemini AI with API key."""
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in your .env file or environment variables.")
    
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(DEFAULT_MODEL)


def summarize_email(subject: str, body_text: str) -> str:
    """Summarize an email using Gemini."""
    model = _configure_gemini()
    content = f"Subject: {subject}\n\n{body_text}"
    prompt = (
        "Summarize the email in 2-3 bullet points focusing on actions, dates, and senders."
    )
    
    response = model.generate_content(
        f"{prompt}\n\nEmail:\n{content}",
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=200,
            temperature=0.3,
        )
    )
    return response.text.strip()


def categorize_email(subject: str, body_text: str) -> str:
    """Categorize an email using Gemini."""
    model = _configure_gemini()
    prompt = (
        "Classify the email into one of: Important, Newsletter, Social, Finance, Work, Personal, Spam."
    )
    
    response = model.generate_content(
        f"{prompt}\n\nSubject: {subject}\nBody:\n{body_text[:2000]}",
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=50,
            temperature=0.1,
        )
    )
    return response.text.strip()


def draft_email(user_prompt: str) -> str:
    """Draft an email using Gemini."""
    model = _configure_gemini()
    
    response = model.generate_content(
        f"Write a professional yet concise email based on this request: {user_prompt}",
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=500,
            temperature=0.7,
        )
    )
    return response.text.strip()


def chat_with_ai(user_message: str, conversation_history: list = None) -> str:
    """General AI chat function using Gemini."""
    model = _configure_gemini()
    
    # Build conversation context
    system_prompt = """You are Luca, a helpful AI voice assistant. You can help with:
    - Email management (inbox, organize, read, draft)
    - General questions and conversations
    - Information and explanations
    - Task planning and reminders
    - Creative writing and brainstorming
    
    Keep responses conversational and helpful. If asked about email commands, mention: inbox, organize, read, draft."""
    
    # Format conversation history
    conversation_text = system_prompt + "\n\n"
    
    if conversation_history:
        for msg in conversation_history[-10:]:  # Keep last 10 exchanges
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation_text += f"{role}: {msg['content']}\n"
    
    conversation_text += f"User: {user_message}\nAssistant:"
    
    response = model.generate_content(
        conversation_text,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=500,  # Keep responses concise for voice
            temperature=0.7
        )
    )
    return response.text.strip()