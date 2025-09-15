#!/usr/bin/env python3
"""
AI Chatty Brain for Luca
Natural conversation using AI with Derja personality and context awareness
"""

import json
import time
from typing import Dict, List, Optional, Any
from .config import GEMINI_API_KEY
from .conversational_personality import get_ai_personality_prompt, update_conversation_context
from .memory_manager import get_memory_manager

class AIChattyBrain:
    """AI-powered chatty brain for natural conversation."""
    
    def __init__(self):
        self.memory_manager = get_memory_manager()
        self.conversation_history = []
        self.context = {}
        self.gemini_available = bool(GEMINI_API_KEY)
    
    def _configure_gemini(self):
        """Configure Gemini AI."""
        if not self.gemini_available:
            raise ValueError("Gemini API key not available")
        
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel("gemini-1.5-flash")
    
    def get_context_summary(self) -> str:
        """Get current context summary."""
        context_parts = []
        
        if self.context.get('last_email_subject'):
            context_parts.append(f"Last email: {self.context['last_email_subject']}")
        
        if self.context.get('last_sender'):
            context_parts.append(f"Last sender: {self.context['last_sender']}")
        
        if self.context.get('mood'):
            context_parts.append(f"Mood: {self.context['mood']}")
        
        if self.context.get('conversation_topic'):
            context_parts.append(f"Topic: {self.context['conversation_topic']}")
        
        return "; ".join(context_parts) if context_parts else "No specific context"
    
    def chat_naturally(self, user_input: str, intent: str = None) -> str:
        """Have natural conversation with Derja personality."""
        try:
            if not self.gemini_available:
                return self._fallback_response(user_input, intent)
            
            model = self._configure_gemini()
            
            # Get personality prompt
            personality_prompt = get_ai_personality_prompt(user_input)
            
            # Add conversation history
            history_text = ""
            if self.conversation_history:
                history_text = "\n\nRecent conversation:\n"
                for msg in self.conversation_history[-6:]:  # Last 6 exchanges
                    role = "User" if msg["role"] == "user" else "Luca"
                    history_text += f"{role}: {msg['content']}\n"
            
            # Create full prompt
            full_prompt = f"{personality_prompt}{history_text}\n\nRespond naturally in Derja:"
            
            # Generate response
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "max_output_tokens": 200,
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "top_k": 40
                }
            )
            
            ai_response = response.text.strip()
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Keep only last 20 exchanges
            if len(self.conversation_history) > 40:
                self.conversation_history = self.conversation_history[-40:]
            
            # Update context
            self._update_context_from_conversation(user_input, ai_response, intent)
            
            return ai_response
            
        except Exception as e:
            print(f"AI Chat error: {e}")
            return self._fallback_response(user_input, intent)
    
    def _fallback_response(self, user_input: str, intent: str = None) -> str:
        """Fallback response when AI is not available."""
        if intent == "greeting":
            return "أهلا وسهلا! شنو نعمللك؟"
        elif intent == "goodbye":
            return "باي باي! نراك تاني!"
        elif intent == "joke":
            return "هههه، نكتة زينة! تريد نكتة تاني؟"
        elif intent == "time":
            current_time = time.strftime("%I:%M %p")
            return f"أه، الوقت {current_time}"
        else:
            return "أه، شنو تريد نعمل؟"
    
    def _update_context_from_conversation(self, user_input: str, ai_response: str, intent: str = None):
        """Update context based on conversation."""
        # Extract email information
        if "إيميل" in user_input.lower() or "email" in user_input.lower():
            self.context['conversation_topic'] = 'email'
        
        # Extract mood indicators
        if any(word in user_input.lower() for word in ["زينة", "طيب", "أه"]):
            self.context['mood'] = 'positive'
        elif any(word in user_input.lower() for word in ["مش", "لا", "مش زينة"]):
            self.context['mood'] = 'negative'
        
        # Update based on intent
        if intent:
            self.context['last_action'] = intent
            
            if intent == "fetch_email":
                self.context['conversation_topic'] = 'email'
            elif intent == "prepare_reply":
                self.context['conversation_topic'] = 'drafting'
            elif intent == "send_email":
                self.context['conversation_topic'] = 'sending'
    
    def get_contextual_email_response(self, email_data: Dict[str, Any]) -> str:
        """Get contextual response for email actions."""
        sender = email_data.get('sender', 'مجهول')
        subject = email_data.get('subject', 'بدون موضوع')
        
        # Update context
        self.context['last_sender'] = sender
        self.context['last_email_subject'] = subject
        
        # Generate contextual response
        if self.gemini_available:
            try:
                model = self._configure_gemini()
                
                prompt = f"""
                You are Luca, a friendly Tunisian AI assistant. 
                
                Context: User just received an email from {sender} with subject "{subject}"
                
                Respond naturally in Derja, mentioning the sender and subject casually.
                Be friendly and conversational.
                
                Example style: "أه، هكا فما إيميل من {sender} يريد يشوفك"
                
                Respond:
                """
                
                response = model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                print(f"Contextual email response error: {e}")
        
        # Fallback response
        return f"أه، هكا فما إيميل من {sender} يريد يشوفك"
    
    def get_draft_context_response(self, draft_content: str, original_email: Dict[str, Any] = None) -> str:
        """Get contextual response for draft actions."""
        if original_email:
            sender = original_email.get('sender', 'مجهول')
            subject = original_email.get('subject', 'بدون موضوع')
            
            # Update context
            self.context['last_sender'] = sender
            self.context['last_email_subject'] = subject
            self.context['last_draft'] = draft_content
            
            if self.gemini_available:
                try:
                    model = self._configure_gemini()
                    
                    prompt = f"""
                    You are Luca, a friendly Tunisian AI assistant.
                    
                    Context: User asked to prepare a reply to an email from {sender} with subject "{subject}"
                    You've prepared a draft response.
                    
                    Respond naturally in Derja, mentioning the sender and that you've prepared a reply.
                    Be friendly and conversational.
                    
                    Example style: "أه، هكا حضرتلك رد على '{subject}' لي بعثلك {sender}"
                    
                    Respond:
                    """
                    
                    response = model.generate_content(prompt)
                    return response.text.strip()
                    
                except Exception as e:
                    print(f"Draft context response error: {e}")
            
            # Fallback response
            return f"أه، هكا حضرتلك رد على '{subject}' لي بعثلك {sender}"
        
        return "أه، هكا حضرتلك رد زينة"
    
    def get_small_talk_response(self) -> str:
        """Get small talk response."""
        small_talk_topics = [
            "شنو نعمل اليوم؟",
            "كيفاش الطقس؟",
            "شنو الأخبار؟",
            "كيفاش الحال؟",
            "شنو نعمل؟",
            "كيفاش اليوم؟",
            "شنو نعمل اليوم؟",
            "كيفاش الطقس؟"
        ]
        
        if self.gemini_available:
            try:
                model = self._configure_gemini()
                
                prompt = f"""
                You are Luca, a friendly Tunisian AI assistant.
                
                Context: {self.get_context_summary()}
                
                Start a casual small talk conversation in Derja.
                Be friendly and conversational.
                
                Respond:
                """
                
                response = model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                print(f"Small talk response error: {e}")
        
        # Fallback response
        return random.choice(small_talk_topics)
    
    def get_joke_response(self) -> str:
        """Get joke response."""
        jokes = [
            "شنو الفرق بين المدرس و الطبيب؟ المدرس يقول 'افتح كتابك' و الطبيب يقول 'افتح فمك'! هههه",
            "شنو الفرق بين الحمار و الحصان؟ الحمار يقول 'حمار' و الحصان يقول 'حصان'! هههه",
            "شنو الفرق بين القط و الكلب؟ القط يقول 'مواء' و الكلب يقول 'نباح'! هههه",
            "شنو الفرق بين السمك و الطيور؟ السمك يقول 'غوغو' و الطيور يقول 'تغريد'! هههه",
            "شنو الفرق بين الفيل و الفأر؟ الفيل يقول 'فيل' و الفأر يقول 'فأر'! هههه"
        ]
        
        if self.gemini_available:
            try:
                model = self._configure_gemini()
                
                prompt = f"""
                You are Luca, a friendly Tunisian AI assistant.
                
                Tell a funny joke in Derja (Tunisian dialect).
                Make it appropriate and family-friendly.
                End with "هههه" or similar laughter.
                
                Respond:
                """
                
                response = model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                print(f"Joke response error: {e}")
        
        # Fallback response
        import random
        return random.choice(jokes)
    
    def get_weather_response(self, weather_data: str = None) -> str:
        """Get weather response."""
        if weather_data:
            if self.gemini_available:
                try:
                    model = self._configure_gemini()
                    
                    prompt = f"""
                    You are Luca, a friendly Tunisian AI assistant.
                    
                    Weather data: {weather_data}
                    
                    Respond naturally in Derja about the weather.
                    Be conversational and friendly.
                    
                    Respond:
                    """
                    
                    response = model.generate_content(prompt)
                    return response.text.strip()
                    
                except Exception as e:
                    print(f"Weather response error: {e}")
            
            # Fallback response
            return f"أه، هكا الطقس {weather_data}"
        
        return "أه، شنو تريد تعرف على الطقس؟"
    
    def get_time_response(self) -> str:
        """Get time response."""
        current_time = time.strftime("%I:%M %p")
        current_date = time.strftime("%A, %B %d")
        
        if self.gemini_available:
            try:
                model = self._configure_gemini()
                
                prompt = f"""
                You are Luca, a friendly Tunisian AI assistant.
                
                Current time: {current_time}
                Current date: {current_date}
                
                Respond naturally in Derja about the time.
                Be conversational and friendly.
                
                Respond:
                """
                
                response = model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                print(f"Time response error: {e}")
        
        # Fallback response
        return f"أه، الوقت {current_time} و اليوم {current_date}"
    
    def get_help_response(self) -> str:
        """Get help response."""
        help_text = """
        أه، أنا لوكا! نخدمك في:
        
        📧 الإيميلات:
        • "أعطيني الإيميلات" - جيب الإيميلات
        • "أقرا الإيميل" - اقرا الإيميل
        • "حضرلي رد" - حضر رد
        • "أبعت الرد" - ابعت الرد
        
        🕐 الوقت والطقس:
        • "شنادي الوقت" - الوقت الحالي
        • "شنادي الطقس" - حالة الطقس
        
        😄 الترفيه:
        • "أعطني نكتة" - نكتة مضحكة
        • "أحسب لي" - حساب رياضي
        
        💬 دردشة:
        • تقدر تحكي معايا عن أي حاجة!
        """
        
        if self.gemini_available:
            try:
                model = self._configure_gemini()
                
                prompt = f"""
                You are Luca, a friendly Tunisian AI assistant.
                
                User asked for help. Provide a friendly, conversational help response in Derja.
                List your capabilities in a casual, friendly way.
                
                Respond:
                """
                
                response = model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                print(f"Help response error: {e}")
        
        return help_text
    
    def get_conversation_continuation(self) -> str:
        """Get conversation continuation."""
        if self.context.get('last_action') == 'email_sent':
            return "طيب، هكا بعثتلك الرد! شنو تريد نعمل تاني؟"
        elif self.context.get('last_action') == 'joke_told':
            return "هههه، زينة! تريد نكتة تاني؟"
        elif self.context.get('last_action') == 'email_read':
            return "أه، هكا قرأتلك الإيميل. تريد نعمل شي تاني؟"
        else:
            return "طيب، شنو تريد نعمل تاني؟"
    
    def should_continue_conversation(self) -> bool:
        """Determine if should continue conversation."""
        return (
            len(self.conversation_history) > 0 and
            self.context.get('mood') in ['positive', 'casual', 'playful'] and
            random.random() < 0.3
        )
    
    def get_context(self) -> Dict[str, Any]:
        """Get current context."""
        return self.context.copy()
    
    def update_context(self, **kwargs):
        """Update context."""
        self.context.update(kwargs)
        update_conversation_context(**kwargs)


# Global instance
ai_chatty_brain = AIChattyBrain()

def chat_naturally(user_input: str, intent: str = None) -> str:
    """Have natural conversation with Derja personality."""
    return ai_chatty_brain.chat_naturally(user_input, intent)

def get_contextual_email_response(email_data: Dict[str, Any]) -> str:
    """Get contextual response for email actions."""
    return ai_chatty_brain.get_contextual_email_response(email_data)

def get_draft_context_response(draft_content: str, original_email: Dict[str, Any] = None) -> str:
    """Get contextual response for draft actions."""
    return ai_chatty_brain.get_draft_context_response(draft_content, original_email)

def get_small_talk_response() -> str:
    """Get small talk response."""
    return ai_chatty_brain.get_small_talk_response()

def get_joke_response() -> str:
    """Get joke response."""
    return ai_chatty_brain.get_joke_response()

def get_weather_response(weather_data: str = None) -> str:
    """Get weather response."""
    return ai_chatty_brain.get_weather_response(weather_data)

def get_time_response() -> str:
    """Get time response."""
    return ai_chatty_brain.get_time_response()

def get_help_response() -> str:
    """Get help response."""
    return ai_chatty_brain.get_help_response()

def get_conversation_continuation() -> str:
    """Get conversation continuation."""
    return ai_chatty_brain.get_conversation_continuation()

def should_continue_conversation() -> bool:
    """Determine if should continue conversation."""
    return ai_chatty_brain.should_continue_conversation()

def get_context() -> Dict[str, Any]:
    """Get current context."""
    return ai_chatty_brain.get_context()

def update_context(**kwargs):
    """Update context."""
    ai_chatty_brain.update_context(**kwargs)
