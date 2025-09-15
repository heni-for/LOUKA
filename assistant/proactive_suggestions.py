#!/usr/bin/env python3
"""
Proactive Suggestions System for Luca
Smart reminders and proactive task suggestions
"""

import time
import json
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from .email_integration import EmailIntegration
from .multimodal_awareness import get_proactive_suggestions, capture_and_analyze_screen
from .conversational_personality import get_personality_response
from .ai_chatty_brain import chat_naturally

@dataclass
class Suggestion:
    """Represents a proactive suggestion."""
    id: str
    type: str  # email, calendar, task, reminder, document
    priority: int  # 1-5, 5 being highest
    message: str
    action: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    created_at: float = 0.0
    expires_at: Optional[float] = None
    dismissed: bool = False

class ProactiveSuggestions:
    """Proactive suggestions and smart reminders system."""
    
    def __init__(self):
        self.email_integration = EmailIntegration()
        self.suggestions = []
        self.monitoring = False
        self.monitor_thread = None
        self.callback = None
        self.user_preferences = self._load_user_preferences()
        
    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences for suggestions."""
        try:
            with open("user_preferences.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "email_reminders": True,
                "calendar_reminders": True,
                "task_suggestions": True,
                "document_reminders": True,
                "proactive_mode": True,
                "suggestion_frequency": 300,  # 5 minutes
                "max_suggestions": 5
            }
    
    def _save_user_preferences(self):
        """Save user preferences."""
        try:
            with open("user_preferences.json", "w", encoding="utf-8") as f:
                json.dump(self.user_preferences, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving preferences: {e}")
    
    def add_suggestion(self, suggestion: Suggestion):
        """Add a new suggestion."""
        suggestion.created_at = time.time()
        self.suggestions.append(suggestion)
        
        # Sort by priority
        self.suggestions.sort(key=lambda x: x.priority, reverse=True)
        
        # Limit suggestions
        if len(self.suggestions) > self.user_preferences.get("max_suggestions", 5):
            self.suggestions = self.suggestions[:self.user_preferences["max_suggestions"]]
        
        # Notify callback
        if self.callback:
            self.callback(suggestion)
    
    def check_email_suggestions(self):
        """Check for email-related suggestions."""
        if not self.user_preferences.get("email_reminders", True):
            return
        
        try:
            # Check for unread emails
            if self.email_integration.gmail_api.is_available():
                emails = self.email_integration.gmail_api.get_emails(top=10)
                unread_count = sum(1 for email in emails if email.get("unread", False))
                
                if unread_count > 0:
                    suggestion = Suggestion(
                        id=f"email_unread_{int(time.time())}",
                        type="email",
                        priority=3,
                        message=f"فما {unread_count} إيميل مش مقروء! تريد ألخصلك المحتوى؟",
                        action="summarize_emails",
                        data={"unread_count": unread_count}
                    )
                    self.add_suggestion(suggestion)
                
                # Check for important emails
                important_emails = [email for email in emails if self._is_important_email(email)]
                if important_emails:
                    suggestion = Suggestion(
                        id=f"email_important_{int(time.time())}",
                        type="email",
                        priority=4,
                        message=f"فما {len(important_emails)} إيميل مهم! تريد أشوفلك المحتوى؟",
                        action="show_important_emails",
                        data={"important_emails": important_emails}
                    )
                    self.add_suggestion(suggestion)
            
        except Exception as e:
            print(f"Email suggestions error: {e}")
    
    def _is_important_email(self, email: Dict[str, Any]) -> bool:
        """Check if email is important based on content and sender."""
        important_keywords = ["urgent", "important", "asap", "deadline", "meeting", "urgent", "مهم", "عاجل", "ضروري"]
        
        subject = email.get("subject", "").lower()
        sender = email.get("sender", "").lower()
        
        # Check for important keywords
        if any(keyword in subject for keyword in important_keywords):
            return True
        
        # Check for important senders (HR, boss, etc.)
        important_senders = ["hr", "manager", "boss", "director", "admin"]
        if any(sender_keyword in sender for sender_keyword in important_senders):
            return True
        
        return False
    
    def check_calendar_suggestions(self):
        """Check for calendar-related suggestions."""
        if not self.user_preferences.get("calendar_reminders", True):
            return
        
        try:
            # This would integrate with Google Calendar API
            # For now, we'll create mock suggestions
            current_time = datetime.now()
            
            # Check for upcoming meetings (mock)
            upcoming_meetings = self._get_upcoming_meetings()
            
            for meeting in upcoming_meetings:
                time_diff = meeting["start_time"] - current_time
                minutes_until = time_diff.total_seconds() / 60
                
                if 0 < minutes_until <= 15:  # Meeting in next 15 minutes
                    suggestion = Suggestion(
                        id=f"meeting_reminder_{int(time.time())}",
                        type="calendar",
                        priority=5,
                        message=f"ميتينغ '{meeting['title']}' في {int(minutes_until)} دقيقة! تريد أحضرلك أجندة؟",
                        action="prepare_meeting_agenda",
                        data={"meeting": meeting}
                    )
                    self.add_suggestion(suggestion)
        
        except Exception as e:
            print(f"Calendar suggestions error: {e}")
    
    def _get_upcoming_meetings(self) -> List[Dict[str, Any]]:
        """Get upcoming meetings (mock implementation)."""
        # This would integrate with Google Calendar API
        return [
            {
                "title": "Team Meeting",
                "start_time": datetime.now() + timedelta(minutes=10),
                "duration": 60,
                "location": "Conference Room A"
            }
        ]
    
    def check_task_suggestions(self):
        """Check for task-related suggestions."""
        if not self.user_preferences.get("task_suggestions", True):
            return
        
        try:
            # Check for overdue tasks
            overdue_tasks = self._get_overdue_tasks()
            if overdue_tasks:
                suggestion = Suggestion(
                    id=f"overdue_tasks_{int(time.time())}",
                    type="task",
                    priority=4,
                    message=f"فما {len(overdue_tasks)} مهمة متأخرة! تريد أخططلك الوقت؟",
                    action="show_overdue_tasks",
                    data={"overdue_tasks": overdue_tasks}
                )
                self.add_suggestion(suggestion)
            
            # Check for time-based suggestions
            current_hour = datetime.now().hour
            
            if current_hour == 9:  # Morning
                suggestion = Suggestion(
                    id=f"morning_planning_{int(time.time())}",
                    type="task",
                    priority=2,
                    message="صباح الخير! تريد أخططلك اليوم؟",
                    action="plan_daily_tasks"
                )
                self.add_suggestion(suggestion)
            
            elif current_hour == 17:  # Evening
                suggestion = Suggestion(
                    id=f"evening_review_{int(time.time())}",
                    type="task",
                    priority=2,
                    message="وقت المساء! تريد ألخصلك يومك؟",
                    action="review_daily_progress"
                )
                self.add_suggestion(suggestion)
        
        except Exception as e:
            print(f"Task suggestions error: {e}")
    
    def _get_overdue_tasks(self) -> List[Dict[str, Any]]:
        """Get overdue tasks (mock implementation)."""
        # This would integrate with task management system
        return [
            {"title": "Review project proposal", "due_date": "2024-01-15"},
            {"title": "Send monthly report", "due_date": "2024-01-14"}
        ]
    
    def check_document_suggestions(self):
        """Check for document-related suggestions."""
        if not self.user_preferences.get("document_reminders", True):
            return
        
        try:
            # Check for recently modified documents
            recent_docs = self._get_recent_documents()
            if recent_docs:
                suggestion = Suggestion(
                    id=f"recent_docs_{int(time.time())}",
                    type="document",
                    priority=2,
                    message=f"فما {len(recent_docs)} وثيقة جديدة! تريد ألخصلك المحتوى؟",
                    action="summarize_documents",
                    data={"recent_docs": recent_docs}
                )
                self.add_suggestion(suggestion)
        
        except Exception as e:
            print(f"Document suggestions error: {e}")
    
    def _get_recent_documents(self) -> List[Dict[str, Any]]:
        """Get recently modified documents (mock implementation)."""
        # This would scan recent documents
        return [
            {"name": "Project_Report.docx", "modified": "2024-01-15"},
            {"name": "Meeting_Notes.pdf", "modified": "2024-01-15"}
        ]
    
    def check_screen_context_suggestions(self):
        """Check for suggestions based on screen context."""
        try:
            # Capture and analyze screen
            screen_analysis = capture_and_analyze_screen()
            
            if screen_analysis:
                suggestions = get_proactive_suggestions(screen_analysis)
                
                for i, suggestion_text in enumerate(suggestions):
                    suggestion = Suggestion(
                        id=f"screen_context_{int(time.time())}_{i}",
                        type="context",
                        priority=2,
                        message=suggestion_text,
                        action="handle_screen_context"
                    )
                    self.add_suggestion(suggestion)
        
        except Exception as e:
            print(f"Screen context suggestions error: {e}")
    
    def generate_smart_reminders(self):
        """Generate smart reminders based on patterns."""
        try:
            # Check for patterns in user behavior
            patterns = self._analyze_user_patterns()
            
            for pattern in patterns:
                if pattern["type"] == "email_frequency":
                    suggestion = Suggestion(
                        id=f"pattern_email_{int(time.time())}",
                        type="reminder",
                        priority=2,
                        message="وقت الإيميلات! تريد تشوفلك الوارد؟",
                        action="check_emails"
                    )
                    self.add_suggestion(suggestion)
                
                elif pattern["type"] == "break_time":
                    suggestion = Suggestion(
                        id=f"pattern_break_{int(time.time())}",
                        type="reminder",
                        priority=1,
                        message="وقت الراحة! تريد تاخد قسط من الراحة؟",
                        action="suggest_break"
                    )
                    self.add_suggestion(suggestion)
        
        except Exception as e:
            print(f"Smart reminders error: {e}")
    
    def _analyze_user_patterns(self) -> List[Dict[str, Any]]:
        """Analyze user patterns (mock implementation)."""
        # This would analyze user behavior patterns
        return [
            {"type": "email_frequency", "confidence": 0.8},
            {"type": "break_time", "confidence": 0.6}
        ]
    
    def start_monitoring(self, callback: Optional[Callable] = None):
        """Start proactive monitoring."""
        if self.monitoring:
            return
        
        self.callback = callback
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("🔄 Proactive monitoring started")
    
    def stop_monitoring(self):
        """Stop proactive monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("🛑 Proactive monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                # Check all suggestion types
                self.check_email_suggestions()
                self.check_calendar_suggestions()
                self.check_task_suggestions()
                self.check_document_suggestions()
                self.check_screen_context_suggestions()
                self.generate_smart_reminders()
                
                # Wait before next check
                time.sleep(self.user_preferences.get("suggestion_frequency", 300))
                
            except Exception as e:
                print(f"Monitoring loop error: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def get_active_suggestions(self) -> List[Suggestion]:
        """Get active (non-dismissed) suggestions."""
        current_time = time.time()
        active_suggestions = []
        
        for suggestion in self.suggestions:
            if suggestion.dismissed:
                continue
            
            if suggestion.expires_at and current_time > suggestion.expires_at:
                continue
            
            active_suggestions.append(suggestion)
        
        return active_suggestions
    
    def dismiss_suggestion(self, suggestion_id: str):
        """Dismiss a suggestion."""
        for suggestion in self.suggestions:
            if suggestion.id == suggestion_id:
                suggestion.dismissed = True
                break
    
    def get_suggestion_response(self, suggestion: Suggestion) -> str:
        """Get response for a suggestion."""
        if suggestion.type == "email":
            return get_personality_response(
                "proactive_email", 
                suggestion.message,
                last_action="proactive_suggestion",
                mood="helpful"
            )
        elif suggestion.type == "calendar":
            return get_personality_response(
                "proactive_calendar",
                suggestion.message,
                last_action="proactive_suggestion",
                mood="helpful"
            )
        elif suggestion.type == "task":
            return get_personality_response(
                "proactive_task",
                suggestion.message,
                last_action="proactive_suggestion",
                mood="helpful"
            )
        else:
            return suggestion.message
    
    def update_preferences(self, **kwargs):
        """Update user preferences."""
        self.user_preferences.update(kwargs)
        self._save_user_preferences()
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get current preferences."""
        return self.user_preferences.copy()


# Global instance
proactive_suggestions = ProactiveSuggestions()

def start_proactive_monitoring(callback=None):
    """Start proactive monitoring."""
    proactive_suggestions.start_monitoring(callback)

def stop_proactive_monitoring():
    """Stop proactive monitoring."""
    proactive_suggestions.stop_monitoring()

def get_active_suggestions() -> List[Suggestion]:
    """Get active suggestions."""
    return proactive_suggestions.get_active_suggestions()

def dismiss_suggestion(suggestion_id: str):
    """Dismiss a suggestion."""
    proactive_suggestions.dismiss_suggestion(suggestion_id)

def get_suggestion_response(suggestion: Suggestion) -> str:
    """Get suggestion response."""
    return proactive_suggestions.get_suggestion_response(suggestion)

def update_preferences(**kwargs):
    """Update preferences."""
    proactive_suggestions.update_preferences(**kwargs)

def get_preferences() -> Dict[str, Any]:
    """Get preferences."""
    return proactive_suggestions.get_preferences()
