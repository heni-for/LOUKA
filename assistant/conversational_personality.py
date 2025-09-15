#!/usr/bin/env python3
"""
Conversational Personality System for Luca
Natural Derja conversation with context awareness and friendly personality
"""

import random
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .memory_manager import get_memory_manager

@dataclass
class ConversationContext:
    """Enhanced conversation context for natural responses."""
    last_email_subject: str = ""
    last_draft: str = ""
    last_sender: str = ""
    mood: str = "casual"  # casual, professional, excited, tired
    conversation_topic: str = ""
    small_talk_count: int = 0
    last_action: str = ""
    user_name: str = ""
    time_of_day: str = "morning"
    weather_mood: str = "neutral"

class DerjaPersonality:
    """Natural Derja conversational personality for Luca."""
    
    def __init__(self):
        self.memory_manager = get_memory_manager()
        self.context = ConversationContext()
        self._load_personality_phrases()
        self._update_time_context()
    
    def _load_personality_phrases(self):
        """Load Derja personality phrases and responses."""
        self.greetings = [
            "أهلا! شنو أحوالك؟",
            "أهلا وسهلا! كيفاش؟",
            "أهلا! شنو نعمللك اليوم؟",
            "أهلا! كيفاش الحال؟",
            "أهلا! شنو الأخبار؟",
            "أهلا! كيفاش؟ شنو نخدمك؟"
        ]
        
        self.casual_responses = [
            "طيب، هكا",
            "أه، زينة",
            "طيب، شنو نعمل؟",
            "أه، شنو نخدمك؟",
            "طيب، هكا نعمل",
            "أه، شنو نعمللك؟"
        ]
        
        self.encouraging_phrases = [
            "طيب، نعملها!",
            "أه، نخدمك!",
            "طيب، نعملها زينة!",
            "أه، نخدمك زينة!",
            "طيب، نعملها صح!",
            "أه، نخدمك صح!"
        ]
        
        self.email_context_phrases = [
            "أه، هكا فما إيميل جديد لي جيك",
            "طيب، هكا فما إيميلات جديدة",
            "أه، هكا فما إيميل من {sender}",
            "طيب، هكا فما إيميل مهم",
            "أه، هكا فما إيميلات كتيرة"
        ]
        
        self.draft_context_phrases = [
            "أه، هكا حضرتلك رد على '{subject}'",
            "طيب، هكا حضرتلك رد زينة",
            "أه، هكا حضرتلك رد على الإيميل",
            "طيب، هكا حضرتلك رد مهم",
            "أه، هكا حضرتلك رد زينة على '{subject}'"
        ]
        
        self.small_talk_topics = [
            "شنو نعمل اليوم؟",
            "كيفاش الطقس؟",
            "شنو الأخبار؟",
            "كيفاش الحال؟",
            "شنو نعمل؟",
            "كيفاش اليوم؟"
        ]
        
        self.jokes_and_teasing = [
            "هههه، زينة!",
            "أه، نكتة زينة!",
            "هههه، طيب!",
            "أه، نكتة مضحكة!",
            "هههه، زينة!",
            "أه، نكتة زينة!"
        ]
        
        self.affirmation_phrases = [
            "أه، طيب",
            "طيب، زينة",
            "أه، صح",
            "طيب، صح",
            "أه، زينة",
            "طيب، زينة"
        ]
        
        self.curiosity_phrases = [
            "شنو تريد نعمل؟",
            "شنو نخدمك؟",
            "شنو تريد؟",
            "شنو نعمللك؟",
            "شنو تريد نعمل؟",
            "شنو نخدمك؟"
        ]
    
    def _update_time_context(self):
        """Update context based on time of day."""
        current_hour = time.localtime().tm_hour
        
        if 5 <= current_hour < 12:
            self.context.time_of_day = "morning"
            self.context.mood = "energetic"
        elif 12 <= current_hour < 17:
            self.context.time_of_day = "afternoon"
            self.context.mood = "productive"
        elif 17 <= current_hour < 21:
            self.context.time_of_day = "evening"
            self.context.mood = "relaxed"
        else:
            self.context.time_of_day = "night"
            self.context.mood = "calm"
    
    def get_greeting(self) -> str:
        """Get appropriate greeting based on context."""
        greeting = random.choice(self.greetings)
        
        # Add time-specific elements
        if self.context.time_of_day == "morning":
            greeting += " صباح الخير!"
        elif self.context.time_of_day == "evening":
            greeting += " مساء الخير!"
        
        return greeting
    
    def get_casual_response(self) -> str:
        """Get casual response."""
        return random.choice(self.casual_responses)
    
    def get_encouraging_response(self) -> str:
        """Get encouraging response."""
        return random.choice(self.encouraging_phrases)
    
    def get_email_context_response(self, sender: str = "") -> str:
        """Get email context response."""
        if sender:
            return random.choice(self.email_context_phrases).format(sender=sender)
        return random.choice(self.email_context_phrases)
    
    def get_draft_context_response(self, subject: str = "") -> str:
        """Get draft context response."""
        if subject:
            return random.choice(self.draft_context_phrases).format(subject=subject)
        return random.choice(self.draft_context_phrases)
    
    def get_small_talk(self) -> str:
        """Get small talk topic."""
        self.context.small_talk_count += 1
        return random.choice(self.small_talk_topics)
    
    def get_joke_response(self) -> str:
        """Get joke response."""
        return random.choice(self.jokes_and_teasing)
    
    def get_affirmation(self) -> str:
        """Get affirmation response."""
        return random.choice(self.affirmation_phrases)
    
    def get_curiosity(self) -> str:
        """Get curiosity response."""
        return random.choice(self.curiosity_phrases)
    
    def build_contextual_response(self, intent: str, base_response: str, **kwargs) -> str:
        """Build contextual response with personality."""
        # Start with casual acknowledgment
        response_parts = [self.get_casual_response()]
        
        # Add context-specific elements
        if intent == "fetch_email":
            if self.context.last_email_subject:
                response_parts.append(f"أه، هكا فما إيميلات جديدة، و فما واحد من '{self.context.last_sender}' يريد يشوفك")
            else:
                response_parts.append(self.get_email_context_response())
        
        elif intent == "prepare_reply":
            if self.context.last_email_subject:
                response_parts.append(f"أه، هكا حضرتلك رد على '{self.context.last_email_subject}' لي بعثلك {self.context.last_sender}")
            else:
                response_parts.append(self.get_draft_context_response())
        
        elif intent == "send_email":
            response_parts.append("طيب، هكا بعثتلك الرد!")
        
        elif intent == "read_email":
            response_parts.append("أه، هكا قرأتلك الإيميل")
        
        # Add the base response
        response_parts.append(base_response)
        
        # Add small talk occasionally
        if random.random() < 0.3 and self.context.small_talk_count < 3:
            response_parts.append(f"أه، و {self.get_small_talk()}")
        
        return " ".join(response_parts)
    
    def get_emotional_response(self, emotion: str, base_response: str) -> str:
        """Get emotional response based on mood."""
        if emotion == "happy":
            return f"أه، زينة! {base_response} 😊"
        elif emotion == "excited":
            return f"أه، زينة! {base_response} 🎉"
        elif emotion == "calm":
            return f"طيب، هكا {base_response} 😌"
        elif emotion == "tired":
            return f"أه، {base_response} 😴"
        else:
            return base_response
    
    def update_context(self, **kwargs):
        """Update conversation context."""
        for key, value in kwargs.items():
            if hasattr(self.context, key):
                setattr(self.context, key, value)
        
        # Update mood based on actions
        if kwargs.get('last_action') == 'email_sent':
            self.context.mood = 'satisfied'
        elif kwargs.get('last_action') == 'error':
            self.context.mood = 'concerned'
        elif kwargs.get('last_action') == 'joke_told':
            self.context.mood = 'playful'
    
    def get_personality_prompt(self, user_input: str) -> str:
        """Get personality-enhanced prompt for AI."""
        context_info = f"""
        Context:
        - Last email: {self.context.last_email_subject}
        - Last sender: {self.context.last_sender}
        - Mood: {self.context.mood}
        - Time: {self.context.time_of_day}
        - Small talk count: {self.context.small_talk_count}
        """
        
        personality_instructions = """
        You are Luca, a friendly Tunisian AI assistant. Your personality:
        
        - Speak in Tunisian Derja (mix of Arabic and French)
        - Be casual, friendly, and conversational
        - Use phrases like "أه", "طيب", "زينة", "هكا"
        - Reference previous conversations naturally
        - Add small talk and jokes occasionally
        - Be helpful but not robotic
        - Show personality and warmth
        
        Examples:
        - "أه، هكا فما إيميل جديد لي جيك"
        - "طيب، نعملها زينة!"
        - "أه، شنو تريد نعمل؟"
        - "هههه، نكتة زينة!"
        """
        
        return f"{personality_instructions}\n\n{context_info}\n\nUser said: {user_input}\n\nRespond naturally in Derja:"
    
    def should_add_small_talk(self) -> bool:
        """Determine if should add small talk."""
        return (
            self.context.small_talk_count < 2 and
            random.random() < 0.4 and
            self.context.mood in ["casual", "relaxed", "playful"]
        )
    
    def get_small_talk_addition(self) -> str:
        """Get small talk addition."""
        additions = [
            "أه، و كيفاش اليوم؟",
            "طيب، و شنو الأخبار؟",
            "أه، و كيفاش الحال؟",
            "طيب، و شنو نعمل؟",
            "أه، و كيفاش الطقس؟",
            "طيب، و شنو نعمل اليوم؟"
        ]
        return random.choice(additions)
    
    def get_conversation_continuation(self) -> str:
        """Get conversation continuation."""
        if self.context.last_action == "email_sent":
            return "طيب، هكا بعثتلك الرد! شنو تريد نعمل تاني؟"
        elif self.context.last_action == "joke_told":
            return "هههه، زينة! تريد نكتة تاني؟"
        elif self.context.last_action == "email_read":
            return "أه، هكا قرأتلك الإيميل. تريد نعمل شي تاني؟"
        else:
            return "طيب، شنو تريد نعمل تاني؟"
    
    def get_mood_based_response(self, base_response: str) -> str:
        """Get mood-based response."""
        if self.context.mood == "energetic":
            return f"أه، زينة! {base_response} 🚀"
        elif self.context.mood == "relaxed":
            return f"طيب، هكا {base_response} 😌"
        elif self.context.mood == "playful":
            return f"أه، زينة! {base_response} 😄"
        elif self.context.mood == "tired":
            return f"أه، {base_response} 😴"
        else:
            return base_response


# Global instance
derja_personality = DerjaPersonality()

def get_personality_response(intent: str, base_response: str, **context) -> str:
    """Get personality-enhanced response."""
    # Update context
    derja_personality.update_context(**context)
    
    # Build contextual response
    response = derja_personality.build_contextual_response(intent, base_response, **context)
    
    # Add mood-based elements
    response = derja_personality.get_mood_based_response(response)
    
    # Add small talk if appropriate
    if derja_personality.should_add_small_talk():
        response += " " + derja_personality.get_small_talk_addition()
    
    return response

def get_ai_personality_prompt(user_input: str) -> str:
    """Get AI prompt with personality instructions."""
    return derja_personality.get_personality_prompt(user_input)

def update_conversation_context(**kwargs):
    """Update conversation context."""
    derja_personality.update_context(**kwargs)

def get_greeting() -> str:
    """Get greeting with personality."""
    return derja_personality.get_greeting()

def get_small_talk() -> str:
    """Get small talk."""
    return derja_personality.get_small_talk()
