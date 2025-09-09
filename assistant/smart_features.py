#!/usr/bin/env python3
"""
Smart features for Luca voice assistant - weather, time, reminders, etc.
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
from .config import GEMINI_API_KEY
from .intent_library import detect_intent, intent_library

def get_current_time() -> str:
    """Get current time in a friendly format."""
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    day_str = now.strftime("%A, %B %d")
    
    # Add some personality
    hour = now.hour
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    elif 17 <= hour < 21:
        greeting = "Good evening"
    else:
        greeting = "Good evening"
    
    return f"{greeting}! It's {time_str} on {day_str}."

def get_weather(city: str = "Tunis") -> str:
    """Get weather information for a city."""
    try:
        # Using OpenWeatherMap API (free tier)
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return "I'd love to tell you the weather, but I need an OpenWeatherMap API key. You can get one free at openweathermap.org!"
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            # Add personality to weather response
            temp_desc = "warm" if temp > 25 else "cool" if temp < 15 else "pleasant"
            
            return f"The weather in {city} is {temp_desc} at {temp:.1f}°C with {description}. Humidity is {humidity}% and wind speed is {wind_speed} m/s."
        else:
            return f"Sorry, I couldn't get the weather for {city}. The weather service might be unavailable."
    
    except Exception as e:
        return f"I'm having trouble getting the weather right now. Error: {str(e)}"

def get_news_summary() -> str:
    """Get a brief news summary using AI."""
    try:
        # This would require a news API key
        # For now, return a placeholder
        return "I'd love to give you the latest news! To enable this feature, I'd need a news API key. Would you like me to help you set that up?"
    except Exception as e:
        return f"Sorry, I can't get the news right now. {str(e)}"

def create_reminder(text: str, time_delta_minutes: int = 0) -> str:
    """Create a simple reminder (in-memory for now)."""
    # This is a simple implementation - in a real app, you'd use a database
    reminder_time = datetime.now() + timedelta(minutes=time_delta_minutes)
    
    if time_delta_minutes == 0:
        return f"Got it! I'll remind you about: {text}"
    else:
        return f"Perfect! I'll remind you about '{text}' in {time_delta_minutes} minutes at {reminder_time.strftime('%I:%M %p')}"

def calculate(expression: str) -> str:
    """Simple calculator for basic math."""
    try:
        # Basic safety check - only allow numbers and basic operators
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "I can only do basic math with numbers and operators like +, -, *, /, and parentheses."
        
        result = eval(expression)
        return f"The answer is {result}"
    except Exception as e:
        return f"Sorry, I couldn't calculate that. Make sure it's a valid math expression."

def get_definition(word: str) -> str:
    """Get word definition using AI."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"Give me a simple, clear definition of the word '{word}' in 1-2 sentences."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Sorry, I couldn't look up the definition of '{word}'. {str(e)}"

def get_joke() -> str:
    """Get a random joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
        "Why don't eggs tell jokes? They'd crack each other up! 🥚",
        "What do you call a fake noodle? An impasta! 🍝",
        "Why did the math book look so sad? Because it had too many problems! 📚"
    ]
    
    import random
    return random.choice(jokes)

def get_motivational_quote() -> str:
    """Get a motivational quote."""
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "It is during our darkest moments that we must focus to see the light. - Aristotle",
        "The way to get started is to quit talking and begin doing. - Walt Disney"
    ]
    
    import random
    return random.choice(quotes)

def handle_smart_command(intent: str, user_input: str = "") -> str:
    """Handle smart commands based on intent."""
    intent = intent.lower()
    
    # Time and date intents
    if intent == "time":
        return get_current_time()
    elif intent == "date":
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_str}"
    
    # Weather intents
    elif intent in ["weather", "weather_specific"]:
        # Extract city from user input if mentioned
        city = "Tunis"  # Default
        words = user_input.lower().split()
        for i, word in enumerate(words):
            if word in ["in", "at", "for", "في", "في", "عند"] and i + 1 < len(words):
                city = words[i + 1].title()
                break
        return get_weather(city)
    
    # Greeting and conversation intents
    elif intent == "greeting":
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! I'm here to assist you.",
            "Good to see you! How can I help?"
        ]
        import random
        return random.choice(greetings)
    
    elif intent == "how_are_you":
        responses = [
            "I'm doing great, thank you for asking! How are you?",
            "I'm excellent and ready to help! How about you?",
            "I'm fantastic! Thanks for checking in. How are you doing?",
            "I'm wonderful! Always happy to chat. How are you?"
        ]
        import random
        return random.choice(responses)
    
    # Entertainment intents
    elif intent == "joke":
        return get_joke()
    elif intent == "quote":
        return get_motivational_quote()
    
    # Information intents
    elif intent == "news":
        return get_news_summary()
    elif intent == "define":
        # Extract word to define
        word = user_input.replace("define", "").replace("what is", "").replace("what's", "").strip()
        return get_definition(word)
    
    # Email intents
    elif intent == "email_inbox":
        return "I'll check your email inbox for you. Let me connect to your email account..."
    elif intent == "email_compose":
        return "I'll help you compose an email. What would you like to write about?"
    elif intent == "gmail":
        return "I'll open Gmail for you. Let me access your Gmail account..."
    
    # Calculator intents
    elif intent == "calculate":
        # Extract math expression from user input
        math_expr = user_input.replace("calculate", "").replace("what is", "").replace("what's", "").strip()
        return calculate(math_expr)
    
    # Help intents
    elif intent == "help":
        return """I can help you with many things! Here's what I can do:
        
🕐 Time & Date: "What time is it?", "What's today's date?"
🌤️ Weather: "What's the weather?", "Is it raining?"
📧 Email: "Check my email", "Open Gmail", "Compose email"
🧮 Math: "Calculate 2 plus 2", "What's 15 times 8?"
😄 Entertainment: "Tell me a joke", "Give me a quote"
📰 News: "What's the news?", "Latest headlines"
🔍 Definitions: "Define artificial intelligence"
🎵 Music: "Play music", "Play a song"
📱 Apps: "Open Gmail", "Open Spotify"
        
Just say 'Hey Luca' followed by what you need!"""
    
    # Search intents
    elif intent == "search":
        return "I can help you search for information. What would you like to search for?"
    
    # Reminder intents
    elif intent == "reminder":
        return "I'll help you set a reminder. What would you like to be reminded about and when?"
    
    # Music intents
    elif intent == "music":
        return "I'll help you with music. Would you like me to play something or open a music app?"
    
    # App intents
    elif intent == "open_app":
        return "I'll help you open an app. Which app would you like to open?"
    elif intent == "close_app":
        return "I'll help you close an app. Which app would you like to close?"
    
    # Don't understand intent
    elif intent == "dont_understand":
        return "I don't understand. Please try again or say 'help' for available commands."
    
    else:
        return "I don't understand. Please try again or say 'help' for available commands."

def is_smart_command(text: str, language: str = 'en') -> Optional[str]:
    """Check if the text is a smart command and return the intent using comprehensive library."""
    # Use the comprehensive intent library
    intent_match = detect_intent(text, language)
    if intent_match:
        return intent_match.intent
    
    # Fallback to basic pattern matching for edge cases
    text_lower = text.lower()
    
    # Math commands (check for operators)
    if any(op in text_lower for op in ["+", "-", "*", "/", "plus", "minus", "times", "divided", "="]):
        return "calculate"
    
    return None
