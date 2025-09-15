#!/usr/bin/env python3
"""
Learning & Adaptation System for Luca
Learns from user habits over weeks/months and provides predictive assistance
"""

import json
import time
import sqlite3
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from .conversational_personality import get_personality_response
from .ai_chatty_brain import chat_naturally
from .config import GEMINI_API_KEY

@dataclass
class UserPattern:
    """Represents a learned user pattern."""
    pattern_type: str  # email_time, meeting_preference, phrase_usage, etc.
    pattern_data: Dict[str, Any]
    confidence: float
    frequency: int
    last_seen: float
    created_at: float

@dataclass
class PredictiveSuggestion:
    """Represents a predictive suggestion."""
    id: str
    type: str  # email_draft, meeting_prep, task_suggestion, etc.
    confidence: float
    message: str
    action: str
    data: Dict[str, Any]
    created_at: float

class LearningAdaptationSystem:
    """Learning and adaptation system for Luca."""
    
    def __init__(self):
        self.db_path = "luca_learning.db"
        self.patterns = {}
        self.predictive_suggestions = []
        self.user_habits = defaultdict(list)
        self.phrase_preferences = defaultdict(int)
        self.time_patterns = defaultdict(list)
        self.contact_patterns = defaultdict(int)
        self._init_database()
        self._load_learned_patterns()
    
    def _init_database(self):
        """Initialize SQLite database for learning data."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    frequency INTEGER NOT NULL,
                    last_seen REAL NOT NULL,
                    created_at REAL NOT NULL
                )
            ''')
            
            # Create user_actions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_type TEXT NOT NULL,
                    action_data TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    context TEXT
                )
            ''')
            
            # Create predictive_suggestions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictive_suggestions (
                    id TEXT PRIMARY KEY,
                    suggestion_type TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    message TEXT NOT NULL,
                    action TEXT NOT NULL,
                    data TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    shown BOOLEAN DEFAULT FALSE,
                    accepted BOOLEAN DEFAULT FALSE
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Learning database initialized")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def _load_learned_patterns(self):
        """Load learned patterns from database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM patterns")
            rows = cursor.fetchall()
            
            for row in rows:
                pattern = UserPattern(
                    pattern_type=row[1],
                    pattern_data=json.loads(row[2]),
                    confidence=row[3],
                    frequency=row[4],
                    last_seen=row[5],
                    created_at=row[6]
                )
                self.patterns[f"{pattern.pattern_type}_{pattern.created_at}"] = pattern
            
            conn.close()
            print(f"✅ Loaded {len(self.patterns)} learned patterns")
            
        except Exception as e:
            print(f"Error loading patterns: {e}")
    
    def record_user_action(self, action_type: str, action_data: Dict[str, Any], context: str = ""):
        """Record a user action for learning."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_actions (action_type, action_data, timestamp, context)
                VALUES (?, ?, ?, ?)
            ''', (action_type, json.dumps(action_data), time.time(), context))
            
            conn.commit()
            conn.close()
            
            # Update in-memory patterns
            self._update_patterns_from_action(action_type, action_data)
            
        except Exception as e:
            print(f"Error recording user action: {e}")
    
    def _update_patterns_from_action(self, action_type: str, action_data: Dict[str, Any]):
        """Update patterns based on user action."""
        try:
            current_time = time.time()
            
            if action_type == "email_sent":
                # Learn email sending patterns
                self._learn_email_patterns(action_data)
            elif action_type == "meeting_scheduled":
                # Learn meeting preferences
                self._learn_meeting_patterns(action_data)
            elif action_type == "voice_command":
                # Learn phrase preferences
                self._learn_phrase_patterns(action_data)
            elif action_type == "task_completed":
                # Learn task completion patterns
                self._learn_task_patterns(action_data)
            
        except Exception as e:
            print(f"Error updating patterns: {e}")
    
    def _learn_email_patterns(self, email_data: Dict[str, Any]):
        """Learn email sending patterns."""
        try:
            # Learn preferred email times
            current_hour = datetime.now().hour
            self.time_patterns["email_sending"].append(current_hour)
            
            # Learn frequently contacted people
            recipient = email_data.get("recipient", "")
            if recipient:
                self.contact_patterns[recipient] += 1
            
            # Learn email length preferences
            body_length = len(email_data.get("body", ""))
            self.user_habits["email_length"].append(body_length)
            
            # Learn subject patterns
            subject = email_data.get("subject", "")
            if subject:
                self.user_habits["email_subjects"].append(subject)
            
        except Exception as e:
            print(f"Error learning email patterns: {e}")
    
    def _learn_meeting_patterns(self, meeting_data: Dict[str, Any]):
        """Learn meeting scheduling patterns."""
        try:
            # Learn preferred meeting times
            start_time = meeting_data.get("start_time", "")
            if start_time:
                hour = datetime.fromisoformat(start_time).hour
                self.time_patterns["meeting_scheduling"].append(hour)
            
            # Learn meeting duration preferences
            duration = meeting_data.get("duration", 60)
            self.user_habits["meeting_duration"].append(duration)
            
            # Learn meeting types
            meeting_type = meeting_data.get("type", "general")
            self.user_habits["meeting_types"].append(meeting_type)
            
        except Exception as e:
            print(f"Error learning meeting patterns: {e}")
    
    def _learn_phrase_patterns(self, command_data: Dict[str, Any]):
        """Learn phrase and command patterns."""
        try:
            command = command_data.get("command", "").lower()
            
            # Learn frequently used phrases
            self.phrase_preferences[command] += 1
            
            # Learn command patterns
            if "أعطيني" in command:
                self.user_habits["request_patterns"].append("أعطيني")
            elif "حضر" in command:
                self.user_habits["request_patterns"].append("حضر")
            elif "أبعت" in command:
                self.user_habits["request_patterns"].append("أبعت")
            
        except Exception as e:
            print(f"Error learning phrase patterns: {e}")
    
    def _learn_task_patterns(self, task_data: Dict[str, Any]):
        """Learn task completion patterns."""
        try:
            task_type = task_data.get("type", "")
            completion_time = task_data.get("completion_time", 0)
            
            # Learn task completion times
            self.user_habits["task_completion_times"].append({
                "type": task_type,
                "time": completion_time
            })
            
            # Learn task preferences
            self.user_habits["task_types"].append(task_type)
            
        except Exception as e:
            print(f"Error learning task patterns: {e}")
    
    def generate_predictive_suggestions(self) -> List[PredictiveSuggestion]:
        """Generate predictive suggestions based on learned patterns."""
        try:
            suggestions = []
            current_time = time.time()
            
            # Email suggestions
            email_suggestions = self._generate_email_suggestions()
            suggestions.extend(email_suggestions)
            
            # Meeting suggestions
            meeting_suggestions = self._generate_meeting_suggestions()
            suggestions.extend(meeting_suggestions)
            
            # Task suggestions
            task_suggestions = self._generate_task_suggestions()
            suggestions.extend(task_suggestions)
            
            # Time-based suggestions
            time_suggestions = self._generate_time_based_suggestions()
            suggestions.extend(time_suggestions)
            
            # Save suggestions to database
            self._save_predictive_suggestions(suggestions)
            
            return suggestions
            
        except Exception as e:
            print(f"Error generating predictive suggestions: {e}")
            return []
    
    def _generate_email_suggestions(self) -> List[PredictiveSuggestion]:
        """Generate email-related predictive suggestions."""
        suggestions = []
        
        try:
            # Check for unread emails that might need replies
            if len(self.user_habits["email_subjects"]) > 0:
                # Suggest drafting replies for important emails
                suggestion = PredictiveSuggestion(
                    id=f"email_reply_{int(time.time())}",
                    type="email_draft",
                    confidence=0.7,
                    message="فما إيميلات مهمة مش رديت عليها! تريد أحضرلك ردود؟",
                    action="draft_email_replies",
                    data={"unread_emails": True},
                    created_at=time.time()
                )
                suggestions.append(suggestion)
            
            # Suggest email sending based on time patterns
            current_hour = datetime.now().hour
            if self.time_patterns["email_sending"]:
                preferred_hours = Counter(self.time_patterns["email_sending"])
                most_common_hour = preferred_hours.most_common(1)[0][0]
                
                if abs(current_hour - most_common_hour) <= 1:
                    suggestion = PredictiveSuggestion(
                        id=f"email_time_{int(time.time())}",
                        type="email_reminder",
                        confidence=0.6,
                        message="وقت الإيميلات! تريد تشوفلك الوارد؟",
                        action="check_emails",
                        data={"time_based": True},
                        created_at=time.time()
                    )
                    suggestions.append(suggestion)
            
        except Exception as e:
            print(f"Error generating email suggestions: {e}")
        
        return suggestions
    
    def _generate_meeting_suggestions(self) -> List[PredictiveSuggestion]:
        """Generate meeting-related predictive suggestions."""
        suggestions = []
        
        try:
            # Suggest meeting preparation based on patterns
            if self.user_habits["meeting_types"]:
                most_common_type = Counter(self.user_habits["meeting_types"]).most_common(1)[0][0]
                
                suggestion = PredictiveSuggestion(
                    id=f"meeting_prep_{int(time.time())}",
                    type="meeting_preparation",
                    confidence=0.8,
                    message=f"تريد تحضر لميتينغ {most_common_type}؟ أحضرلك أجندة؟",
                    action="prepare_meeting_agenda",
                    data={"meeting_type": most_common_type},
                    created_at=time.time()
                )
                suggestions.append(suggestion)
            
            # Suggest meeting scheduling based on time patterns
            current_hour = datetime.now().hour
            if self.time_patterns["meeting_scheduling"]:
                preferred_hours = Counter(self.time_patterns["meeting_scheduling"])
                most_common_hour = preferred_hours.most_common(1)[0][0]
                
                if abs(current_hour - most_common_hour) <= 2:
                    suggestion = PredictiveSuggestion(
                        id=f"meeting_schedule_{int(time.time())}",
                        type="meeting_scheduling",
                        confidence=0.7,
                        message="وقت الميتينغات! تريد تخطط ميتينغ جديد؟",
                        action="schedule_meeting",
                        data={"time_based": True},
                        created_at=time.time()
                    )
                    suggestions.append(suggestion)
            
        except Exception as e:
            print(f"Error generating meeting suggestions: {e}")
        
        return suggestions
    
    def _generate_task_suggestions(self) -> List[PredictiveSuggestion]:
        """Generate task-related predictive suggestions."""
        suggestions = []
        
        try:
            # Suggest tasks based on completion patterns
            if self.user_habits["task_types"]:
                most_common_task = Counter(self.user_habits["task_types"]).most_common(1)[0][0]
                
                suggestion = PredictiveSuggestion(
                    id=f"task_suggestion_{int(time.time())}",
                    type="task_creation",
                    confidence=0.6,
                    message=f"تريد تعمل {most_common_task}؟ عادة تعمله في هذا الوقت",
                    action="create_task",
                    data={"task_type": most_common_task},
                    created_at=time.time()
                )
                suggestions.append(suggestion)
            
            # Suggest task prioritization based on patterns
            if len(self.user_habits["task_completion_times"]) > 5:
                suggestion = PredictiveSuggestion(
                    id=f"task_priority_{int(time.time())}",
                    type="task_prioritization",
                    confidence=0.5,
                    message="تريد أخططلك المهام حسب الأولوية؟",
                    action="prioritize_tasks",
                    data={"pattern_based": True},
                    created_at=time.time()
                )
                suggestions.append(suggestion)
            
        except Exception as e:
            print(f"Error generating task suggestions: {e}")
        
        return suggestions
    
    def _generate_time_based_suggestions(self) -> List[PredictiveSuggestion]:
        """Generate time-based predictive suggestions."""
        suggestions = []
        
        try:
            current_hour = datetime.now().hour
            
            # Morning suggestions
            if 8 <= current_hour <= 10:
                suggestion = PredictiveSuggestion(
                    id=f"morning_planning_{int(time.time())}",
                    type="daily_planning",
                    confidence=0.8,
                    message="صباح الخير! تريد أخططلك اليوم؟",
                    action="plan_daily_tasks",
                    data={"time_of_day": "morning"},
                    created_at=time.time()
                )
                suggestions.append(suggestion)
            
            # Afternoon suggestions
            elif 14 <= current_hour <= 16:
                suggestion = PredictiveSuggestion(
                    id=f"afternoon_review_{int(time.time())}",
                    type="progress_review",
                    confidence=0.7,
                    message="وقت المراجعة! تريد تشوف تقدمك اليوم؟",
                    action="review_daily_progress",
                    data={"time_of_day": "afternoon"},
                    created_at=time.time()
                )
                suggestions.append(suggestion)
            
            # Evening suggestions
            elif 18 <= current_hour <= 20:
                suggestion = PredictiveSuggestion(
                    id=f"evening_wrap_{int(time.time())}",
                    type="evening_wrap_up",
                    confidence=0.9,
                    message="وقت المساء! تريد تلخص يومك وتخطط بكرة؟",
                    action="evening_wrap_up",
                    data={"time_of_day": "evening"},
                    created_at=time.time()
                )
                suggestions.append(suggestion)
            
        except Exception as e:
            print(f"Error generating time-based suggestions: {e}")
        
        return suggestions
    
    def _save_predictive_suggestions(self, suggestions: List[PredictiveSuggestion]):
        """Save predictive suggestions to database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for suggestion in suggestions:
                cursor.execute('''
                    INSERT OR REPLACE INTO predictive_suggestions 
                    (id, suggestion_type, confidence, message, action, data, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    suggestion.id,
                    suggestion.type,
                    suggestion.confidence,
                    suggestion.message,
                    suggestion.action,
                    json.dumps(suggestion.data),
                    suggestion.created_at
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error saving predictive suggestions: {e}")
    
    def get_predictive_suggestions(self, limit: int = 5) -> List[PredictiveSuggestion]:
        """Get predictive suggestions for the user."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM predictive_suggestions 
                WHERE shown = FALSE 
                ORDER BY confidence DESC, created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            suggestions = []
            
            for row in rows:
                suggestion = PredictiveSuggestion(
                    id=row[0],
                    type=row[1],
                    confidence=row[2],
                    message=row[3],
                    action=row[4],
                    data=json.loads(row[5]),
                    created_at=row[6]
                )
                suggestions.append(suggestion)
            
            conn.close()
            return suggestions
            
        except Exception as e:
            print(f"Error getting predictive suggestions: {e}")
            return []
    
    def mark_suggestion_shown(self, suggestion_id: str):
        """Mark a suggestion as shown."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE predictive_suggestions 
                SET shown = TRUE 
                WHERE id = ?
            ''', (suggestion_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error marking suggestion as shown: {e}")
    
    def mark_suggestion_accepted(self, suggestion_id: str):
        """Mark a suggestion as accepted."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE predictive_suggestions 
                SET accepted = TRUE 
                WHERE id = ?
            ''', (suggestion_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error marking suggestion as accepted: {e}")
    
    def get_user_insights(self) -> Dict[str, Any]:
        """Get insights about user patterns and habits."""
        try:
            insights = {
                "email_patterns": {
                    "preferred_sending_times": Counter(self.time_patterns["email_sending"]).most_common(3),
                    "frequent_contacts": Counter(self.contact_patterns).most_common(5),
                    "average_email_length": np.mean(self.user_habits["email_length"]) if self.user_habits["email_length"] else 0
                },
                "meeting_patterns": {
                    "preferred_meeting_times": Counter(self.time_patterns["meeting_scheduling"]).most_common(3),
                    "common_meeting_types": Counter(self.user_habits["meeting_types"]).most_common(3),
                    "average_meeting_duration": np.mean(self.user_habits["meeting_duration"]) if self.user_habits["meeting_duration"] else 0
                },
                "command_patterns": {
                    "frequent_phrases": Counter(self.phrase_preferences).most_common(5),
                    "common_request_types": Counter(self.user_habits["request_patterns"]).most_common(3)
                },
                "task_patterns": {
                    "common_task_types": Counter(self.user_habits["task_types"]).most_common(3),
                    "average_completion_times": np.mean([t["time"] for t in self.user_habits["task_completion_times"]]) if self.user_habits["task_completion_times"] else 0
                }
            }
            
            return insights
            
        except Exception as e:
            print(f"Error getting user insights: {e}")
            return {}
    
    def get_adaptive_response(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Get adaptive response based on learned patterns."""
        try:
            # Use learned phrase preferences
            if user_input.lower() in self.phrase_preferences:
                # User frequently uses this phrase, respond accordingly
                frequency = self.phrase_preferences[user_input.lower()]
                if frequency > 5:
                    # High frequency phrase, use personalized response
                    return get_personality_response(
                        "adaptive_high_frequency",
                        f"أه، هكا! {user_input} - عرفت إنك تحب تقولي هكا!",
                        last_action="adaptive_response",
                        mood="personalized"
                    )
            
            # Use learned patterns for context-aware responses
            if context and context.get("action_type") == "email":
                # User is working with emails, use email-specific patterns
                if self.contact_patterns:
                    most_contacted = max(self.contact_patterns, key=self.contact_patterns.get)
                    return get_personality_response(
                        "adaptive_email_context",
                        f"أه، هكا! تريد تشوف إيميلات {most_contacted}؟",
                        last_action="adaptive_email",
                        mood="contextual"
                    )
            
            # Default adaptive response
            return get_personality_response(
                "adaptive_default",
                user_input,
                last_action="adaptive_response",
                mood="learning"
            )
            
        except Exception as e:
            print(f"Error getting adaptive response: {e}")
            return user_input


# Global instance
learning_system = LearningAdaptationSystem()

def record_user_action(action_type: str, action_data: Dict[str, Any], context: str = ""):
    """Record user action for learning."""
    learning_system.record_user_action(action_type, action_data, context)

def generate_predictive_suggestions() -> List[PredictiveSuggestion]:
    """Generate predictive suggestions."""
    return learning_system.generate_predictive_suggestions()

def get_predictive_suggestions(limit: int = 5) -> List[PredictiveSuggestion]:
    """Get predictive suggestions."""
    return learning_system.get_predictive_suggestions(limit)

def mark_suggestion_shown(suggestion_id: str):
    """Mark suggestion as shown."""
    learning_system.mark_suggestion_shown(suggestion_id)

def mark_suggestion_accepted(suggestion_id: str):
    """Mark suggestion as accepted."""
    learning_system.mark_suggestion_accepted(suggestion_id)

def get_user_insights() -> Dict[str, Any]:
    """Get user insights."""
    return learning_system.get_user_insights()

def get_adaptive_response(user_input: str, context: Dict[str, Any] = None) -> str:
    """Get adaptive response."""
    return learning_system.get_adaptive_response(user_input, context)
