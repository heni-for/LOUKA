#!/usr/bin/env python3
"""
Command-to-Action Mapping System for Luca
Maps intents to specific actions with context awareness
"""

import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from .derja_nlu import Intent
from .email_integration import EmailIntegration
from .llm import chat_with_ai, draft_email, summarize_email
from .smart_features import handle_smart_command
from .conversational_personality import get_personality_response, update_conversation_context
from .ai_chatty_brain import chat_naturally, get_contextual_email_response, get_draft_context_response
from .emotional_tts import speak_with_emotion, speak_naturally, speak_conversationally

@dataclass
class ConversationContext:
    """Stores conversation context and state."""
    last_email: Optional[Dict[str, Any]] = None
    last_draft: Optional[str] = None
    last_sender: Optional[str] = None
    last_subject: Optional[str] = None
    email_list: List[Dict[str, Any]] = None
    current_email_index: int = 0
    conversation_history: List[Dict[str, str]] = None
    last_action: Optional[str] = None
    last_timestamp: float = 0.0
    
    def __post_init__(self):
        if self.email_list is None:
            self.email_list = []
        if self.conversation_history is None:
            self.conversation_history = []

class ActionMapper:
    """Maps intents to actions with context awareness."""
    
    def __init__(self):
        self.email_integration = EmailIntegration()
        self.context = ConversationContext()
        self.action_handlers = self._initialize_action_handlers()
    
    def _initialize_action_handlers(self) -> Dict[str, callable]:
        """Initialize action handlers for each intent."""
        return {
            "fetch_email": self._handle_fetch_email,
            "prepare_reply": self._handle_prepare_reply,
            "send_email": self._handle_send_email,
            "read_email": self._handle_read_email,
            "organize_email": self._handle_organize_email,
            "help": self._handle_help,
            "time": self._handle_time,
            "weather": self._handle_weather,
            "joke": self._handle_joke,
            "calculate": self._handle_calculate,
            "greeting": self._handle_greeting,
            "goodbye": self._handle_goodbye,
            "unknown": self._handle_unknown
        }
    
    def execute_action(self, intent: Intent) -> str:
        """Execute action based on intent with context awareness."""
        try:
            # Update context timestamp
            self.context.last_timestamp = time.time()
            self.context.last_action = intent.intent
            
            # Get handler for intent
            handler = self.action_handlers.get(intent.intent, self._handle_unknown)
            
            # Execute action
            result = handler(intent)
            
            # Add to conversation history
            self.context.conversation_history.append({
                "role": "user",
                "content": intent.original_text,
                "timestamp": time.time()
            })
            self.context.conversation_history.append({
                "role": "assistant", 
                "content": result,
                "timestamp": time.time()
            })
            
            # Keep only last 20 exchanges
            if len(self.context.conversation_history) > 40:
                self.context.conversation_history = self.context.conversation_history[-40:]
            
            return result
            
        except Exception as e:
            error_msg = f"Error executing action {intent.intent}: {str(e)}"
            print(f"ActionMapper Error: {error_msg}")
            return f"عذراً، حدث خطأ في تنفيذ الأمر. {error_msg}"
    
    def _handle_fetch_email(self, intent: Intent) -> str:
        """Handle fetch email intent."""
        try:
            # Get email count from entities if specified
            email_count = 5  # Default
            if "email_count" in intent.entities:
                try:
                    email_count = int(intent.entities["email_count"])
                except ValueError:
                    pass
            
            # Fetch emails
            if self.email_integration.gmail_api.is_available():
                emails = self.email_integration.gmail_api.get_emails(top=email_count)
            else:
                # Fallback to basic email integration
                emails = self.email_integration.get_inbox_summary()
                if isinstance(emails, str):
                    return emails
                emails = emails if isinstance(emails, list) else []
            
            if not emails:
                base_response = "مفيش إيميلات في الإنبوكس. صندوق الوارد فاضي!"
                return get_personality_response("fetch_email", base_response, 
                                              last_action="fetch_email", mood="casual")
            
            # Store emails in context
            self.context.email_list = emails
            self.context.current_email_index = 0
            
            # Get contextual response
            if emails:
                email_data = emails[0]
                contextual_response = get_contextual_email_response(email_data)
            else:
                contextual_response = "أه، هكا فما إيميلات جديدة"
            
            # Format response in Derja
            response = f"{contextual_response}\n\nلقيت {len(emails)} إيميل في الإنبوكس:\n\n"
            for i, email in enumerate(emails, 1):
                status = "📧" if email.get("unread", False) else "📬"
                sender = email.get("sender", "مجهول")
                subject = email.get("subject", "بدون موضوع")
                response += f"{i}. {status} {subject} - من: {sender}\n"
            
            response += "\n💡 تقدر تقولي 'أقرا الإيميل' أو 'حضرلي رد'"
            
            # Update context
            update_conversation_context(
                last_action="fetch_email",
                last_email=emails[0] if emails else None,
                last_sender=emails[0].get("sender") if emails else None,
                last_subject=emails[0].get("subject") if emails else None
            )
            
            return response
            
        except Exception as e:
            error_response = f"مش قادر أجيب الإيميلات. خطأ: {str(e)}"
            return get_personality_response("fetch_email", error_response, 
                                          last_action="error", mood="concerned")
    
    def _handle_prepare_reply(self, intent: Intent) -> str:
        """Handle prepare reply intent."""
        try:
            # Check if we have emails in context
            if not self.context.email_list:
                return "مفيش إيميلات في السياق. قولي 'أعطيني الإيميلات' الأول"
            
            # Get the email to reply to
            if self.context.current_email_index < len(self.context.email_list):
                email = self.context.email_list[self.context.current_email_index]
            else:
                email = self.context.email_list[0]  # Default to first email
            
            # Store email details in context
            self.context.last_email = email
            self.context.last_sender = email.get("sender", "مجهول")
            self.context.last_subject = email.get("subject", "بدون موضوع")
            
            # Generate reply using AI
            email_content = email.get("body", "")
            if not email_content:
                email_content = f"Subject: {email.get('subject', '')}\nFrom: {email.get('sender', '')}"
            
            # Create prompt for AI
            prompt = f"""اكتب رد مهني على هذا الإيميل:

من: {email.get('sender', 'مجهول')}
الموضوع: {email.get('subject', 'بدون موضوع')}
المحتوى: {email_content[:500]}

اكتب رد مهني ومختصر باللغة العربية أو الإنجليزية حسب السياق."""
            
            # Generate draft
            draft = draft_email(prompt)
            self.context.last_draft = draft
            
            # Format response
            response = f"حضرتلك رد على إيميل من {email.get('sender', 'مجهول')}:\n\n"
            response += f"📧 الموضوع: {email.get('subject', 'بدون موضوع')}\n"
            response += f"✍️ الرد:\n{draft}\n\n"
            response += "💡 تقدر تقولي 'أبعت الرد' لإرساله"
            
            return response
            
        except Exception as e:
            return f"مش قادر أحضر رد. خطأ: {str(e)}"
    
    def _handle_send_email(self, intent: Intent) -> str:
        """Handle send email intent."""
        try:
            # Check if we have a draft in context
            if not self.context.last_draft:
                return "مفيش رد محضر. قولي 'حضرلي رد' الأول"
            
            # Check if we have email details
            if not self.context.last_email:
                return "مفيش تفاصيل الإيميل. قولي 'أعطيني الإيميلات' الأول"
            
            # Send the email
            sender_email = self.context.last_sender
            if '<' in sender_email and '>' in sender_email:
                sender_email = sender_email.split('<')[1].split('>')[0]
            elif '@' not in sender_email:
                sender_email = f"{sender_email}@example.com"
            
            subject = f"Re: {self.context.last_subject}" if not self.context.last_subject.startswith('Re:') else self.context.last_subject
            
            # Use Gmail API to send
            if self.email_integration.gmail_api.is_available():
                success = self.email_integration.gmail_api.send_email(
                    to=sender_email,
                    subject=subject,
                    body=self.context.last_draft
                )
                
                if success:
                    # Clear draft after sending
                    self.context.last_draft = None
                    return f"✅ تم إرسال الرد بنجاح إلى {self.context.last_sender}!"
                else:
                    return "❌ مش قادر أرسل الرد. جرب تاني"
            else:
                return "❌ Gmail API مش متاح. افتح Gmail يدوياً وانسخ الرد"
                
        except Exception as e:
            return f"مش قادر أرسل الرد. خطأ: {str(e)}"
    
    def _handle_read_email(self, intent: Intent) -> str:
        """Handle read email intent."""
        try:
            # Check if we have emails in context
            if not self.context.email_list:
                return "مفيش إيميلات في السياق. قولي 'أعطيني الإيميلات' الأول"
            
            # Get the email to read
            if self.context.current_email_index < len(self.context.email_list):
                email = self.context.email_list[self.context.current_email_index]
            else:
                email = self.context.email_list[0]
            
            # Store email in context
            self.context.last_email = email
            
            # Format email content
            response = f"📧 إيميل من {email.get('sender', 'مجهول')}:\n"
            response += f"📌 الموضوع: {email.get('subject', 'بدون موضوع')}\n\n"
            
            # Get email body
            body = email.get("body", "")
            if body:
                # Summarize long emails
                if len(body) > 200:
                    summary = summarize_email(email.get("subject", ""), body)
                    response += f"📝 الملخص:\n{summary}\n\n"
                    response += f"📄 المحتوى الكامل:\n{body[:200]}...\n"
                else:
                    response += f"📄 المحتوى:\n{body}\n"
            else:
                response += "📄 مفيش محتوى متاح\n"
            
            response += "\n💡 تقدر تقولي 'حضرلي رد' أو 'الإيميل الجاي'"
            
            return response
            
        except Exception as e:
            return f"مش قادر أقرا الإيميل. خطأ: {str(e)}"
    
    def _handle_organize_email(self, intent: Intent) -> str:
        """Handle organize email intent."""
        try:
            result = self.email_integration.organize_emails()
            
            # Translate to Derja
            if "Email Organization Complete" in result:
                return "✅ تم تنظيم الإيميلات بنجاح! الإيميلات مرتبة حسب التاريخ"
            elif "Gmail" in result:
                return "📁 فتحت Gmail للتنظيم. الإيميلات مرتبة حسب التاريخ"
            else:
                return f"📁 {result}"
                
        except Exception as e:
            return f"مش قادر أنظم الإيميلات. خطأ: {str(e)}"
    
    def _handle_help(self, intent: Intent) -> str:
        """Handle help intent."""
        return """أهلا! أنا لوكا، المساعد الذكي باللهجة التونسية! 🎤

📧 الإيميلات:
• "أعطيني الإيميلات" - جيب الإيميلات
• "أقرا الإيميل" - اقرا الإيميل الحالي
• "حضرلي رد" - حضر رد على الإيميل
• "أبعت الرد" - ابعت الرد المحضر
• "نظم الإيميلات" - نظم الإيميلات

🕐 الوقت والطقس:
• "شنادي الوقت" - الوقت الحالي
• "شنادي الطقس" - حالة الطقس

😄 الترفيه:
• "أعطني نكتة" - نكتة مضحكة
• "أحسب لي" - حساب رياضي

💡 تقدر تقولي أي حاجة باللهجة التونسية!"""
    
    def _handle_time(self, intent: Intent) -> str:
        """Handle time intent."""
        return handle_smart_command("time", intent.original_text)
    
    def _handle_weather(self, intent: Intent) -> str:
        """Handle weather intent."""
        return handle_smart_command("weather", intent.original_text)
    
    def _handle_joke(self, intent: Intent) -> str:
        """Handle joke intent."""
        return handle_smart_command("joke", intent.original_text)
    
    def _handle_calculate(self, intent: Intent) -> str:
        """Handle calculate intent."""
        return handle_smart_command("calculate", intent.original_text)
    
    def _handle_greeting(self, intent: Intent) -> str:
        """Handle greeting intent."""
        greetings = [
            "أهلا وسهلا! شنادي نعمللك؟",
            "أهلا! كيفاش؟ شنادي نخدمك؟",
            "أهلا! أنا لوكا، شنادي نعمللك؟",
            "أهلا! كيفاش الحال؟ شنادي نخدمك؟"
        ]
        import random
        return random.choice(greetings)
    
    def _handle_goodbye(self, intent: Intent) -> str:
        """Handle goodbye intent."""
        goodbyes = [
            "باي باي! نراك تاني!",
            "أهلا باي! نراك قريب!",
            "باي! نراك تاني!",
            "أهلا باي! نراك قريب!"
        ]
        import random
        return random.choice(goodbyes)
    
    def _handle_unknown(self, intent: Intent) -> str:
        """Handle unknown intent."""
        # Try to use AI chat for unknown intents
        try:
            response = chat_with_ai(intent.original_text, self.context.conversation_history)
            return response
        except Exception as e:
            return f"مش فاهم شنادي تقصد. جرب تقولي 'أعطني' أو 'شنادي نعمل'"
    
    def get_context(self) -> Dict[str, Any]:
        """Get current conversation context."""
        return asdict(self.context)
    
    def clear_context(self):
        """Clear conversation context."""
        self.context = ConversationContext()
    
    def set_email_context(self, email: Dict[str, Any]):
        """Set email context for conversation."""
        self.context.last_email = email
        self.context.last_sender = email.get("sender", "مجهول")
        self.context.last_subject = email.get("subject", "بدون موضوع")
    
    def next_email(self) -> str:
        """Move to next email in context."""
        if not self.context.email_list:
            return "مفيش إيميلات في السياق"
        
        self.context.current_email_index = (self.context.current_email_index + 1) % len(self.context.email_list)
        email = self.context.email_list[self.context.current_email_index]
        
        return f"الإيميل الجاي: {email.get('subject', 'بدون موضوع')} - من: {email.get('sender', 'مجهول')}"
    
    def previous_email(self) -> str:
        """Move to previous email in context."""
        if not self.context.email_list:
            return "مفيش إيميلات في السياق"
        
        self.context.current_email_index = (self.context.current_email_index - 1) % len(self.context.email_list)
        email = self.context.email_list[self.context.current_email_index]
        
        return f"الإيميل السابق: {email.get('subject', 'بدون موضوع')} - من: {email.get('sender', 'مجهول')}"


# Global instance
action_mapper = ActionMapper()

def execute_derja_action(intent: Intent) -> str:
    """Convenience function to execute Derja action."""
    return action_mapper.execute_action(intent)

def get_conversation_context() -> Dict[str, Any]:
    """Get current conversation context."""
    return action_mapper.get_context()

def clear_conversation_context():
    """Clear conversation context."""
    action_mapper.clear_context()
