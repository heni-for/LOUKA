#!/usr/bin/env python3
"""
Meeting Intelligence System for Luca
Real-time meeting analysis, action items, and sentiment analysis
"""

import json
import time
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from .conversational_personality import get_personality_response
from .ai_chatty_brain import chat_naturally
from .config import GEMINI_API_KEY

@dataclass
class ActionItem:
    """Represents an action item from a meeting."""
    id: str
    description: str
    assignee: str
    due_date: Optional[str] = None
    priority: str = "medium"  # low, medium, high
    status: str = "pending"  # pending, in_progress, completed
    created_at: float = 0.0

@dataclass
class MeetingParticipant:
    """Represents a meeting participant."""
    name: str
    role: str
    sentiment: str  # positive, negative, neutral
    participation_level: str  # high, medium, low
    key_points: List[str]

@dataclass
class MeetingAnalysis:
    """Represents meeting analysis results."""
    meeting_id: str
    title: str
    participants: List[MeetingParticipant]
    action_items: List[ActionItem]
    key_decisions: List[str]
    overall_sentiment: str
    duration: int  # minutes
    summary: str
    created_at: float

class MeetingIntelligence:
    """Meeting intelligence system for real-time analysis."""
    
    def __init__(self):
        self.active_meetings = {}
        self.meeting_history = []
        self.action_items = []
        self.gemini_available = bool(GEMINI_API_KEY)
        self._load_meeting_data()
    
    def _load_meeting_data(self):
        """Load meeting data from file."""
        try:
            with open("meeting_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.meeting_history = data.get("meeting_history", [])
            self.action_items = data.get("action_items", [])
            
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading meeting data: {e}")
    
    def _save_meeting_data(self):
        """Save meeting data to file."""
        try:
            data = {
                "meeting_history": self.meeting_history,
                "action_items": self.action_items
            }
            
            with open("meeting_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error saving meeting data: {e}")
    
    def start_meeting(self, meeting_id: str, title: str, participants: List[str]) -> bool:
        """Start a new meeting session."""
        try:
            self.active_meetings[meeting_id] = {
                "title": title,
                "participants": participants,
                "start_time": time.time(),
                "transcript": [],
                "action_items": [],
                "key_points": [],
                "sentiment_data": {}
            }
            
            print(f"✅ Meeting started: {title}")
            return True
            
        except Exception as e:
            print(f"Error starting meeting: {e}")
            return False
    
    def add_meeting_transcript(self, meeting_id: str, speaker: str, text: str) -> bool:
        """Add transcript entry to active meeting."""
        try:
            if meeting_id not in self.active_meetings:
                print(f"❌ Meeting {meeting_id} not found")
                return False
            
            entry = {
                "speaker": speaker,
                "text": text,
                "timestamp": time.time(),
                "sentiment": self._analyze_sentiment(text)
            }
            
            self.active_meetings[meeting_id]["transcript"].append(entry)
            
            # Real-time analysis
            self._analyze_real_time(meeting_id, entry)
            
            return True
            
        except Exception as e:
            print(f"Error adding transcript: {e}")
            return False
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text."""
        try:
            if not self.gemini_available:
                return self._fallback_sentiment_analysis(text)
            
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
            Analyze the sentiment of this text in a meeting context:
            "{text}"
            
            Return only one of: positive, negative, neutral
            """
            
            response = model.generate_content(prompt)
            sentiment = response.text.strip().lower()
            
            if sentiment in ["positive", "negative", "neutral"]:
                return sentiment
            else:
                return "neutral"
                
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return "neutral"
    
    def _fallback_sentiment_analysis(self, text: str) -> str:
        """Fallback sentiment analysis using keywords."""
        try:
            positive_words = ["ممتاز", "زينة", "طيب", "أه", "نعم", "موافق", "جيد", "رائع"]
            negative_words = ["مش", "لا", "غلط", "مش زينة", "مش طيب", "مش موافق", "مش جيد"]
            
            text_lower = text.lower()
            
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            if positive_count > negative_count:
                return "positive"
            elif negative_count > positive_count:
                return "negative"
            else:
                return "neutral"
                
        except Exception as e:
            print(f"Fallback sentiment analysis error: {e}")
            return "neutral"
    
    def _analyze_real_time(self, meeting_id: str, entry: Dict[str, Any]):
        """Analyze meeting entry in real-time."""
        try:
            text = entry["text"]
            speaker = entry["speaker"]
            
            # Extract action items
            action_items = self._extract_action_items(text, speaker)
            if action_items:
                self.active_meetings[meeting_id]["action_items"].extend(action_items)
            
            # Extract key points
            key_points = self._extract_key_points(text)
            if key_points:
                self.active_meetings[meeting_id]["key_points"].extend(key_points)
            
            # Update sentiment data
            if speaker not in self.active_meetings[meeting_id]["sentiment_data"]:
                self.active_meetings[meeting_id]["sentiment_data"][speaker] = []
            
            self.active_meetings[meeting_id]["sentiment_data"][speaker].append({
                "sentiment": entry["sentiment"],
                "timestamp": entry["timestamp"]
            })
            
        except Exception as e:
            print(f"Real-time analysis error: {e}")
    
    def _extract_action_items(self, text: str, speaker: str) -> List[ActionItem]:
        """Extract action items from text."""
        try:
            action_items = []
            
            # Look for action item patterns
            action_patterns = [
                r"نعمل\s+(.+)",
                r"نحضر\s+(.+)",
                r"نرسل\s+(.+)",
                r"نتابع\s+(.+)",
                r"نراجع\s+(.+)",
                r"نخطط\s+(.+)",
                r"ننظم\s+(.+)",
                r"نحل\s+(.+)"
            ]
            
            for pattern in action_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    action_item = ActionItem(
                        id=f"action_{int(time.time())}_{len(action_items)}",
                        description=match.strip(),
                        assignee=speaker,
                        created_at=time.time()
                    )
                    action_items.append(action_item)
            
            return action_items
            
        except Exception as e:
            print(f"Action item extraction error: {e}")
            return []
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text."""
        try:
            key_points = []
            
            # Look for key point patterns
            key_patterns = [
                r"مهم\s+(.+)",
                r"ضروري\s+(.+)",
                r"عاجل\s+(.+)",
                r"قرار\s+(.+)",
                r"اتفاق\s+(.+)",
                r"مشروع\s+(.+)",
                r"هدف\s+(.+)"
            ]
            
            for pattern in key_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    key_points.append(match.strip())
            
            return key_points
            
        except Exception as e:
            print(f"Key point extraction error: {e}")
            return []
    
    def end_meeting(self, meeting_id: str) -> Optional[MeetingAnalysis]:
        """End meeting and generate analysis."""
        try:
            if meeting_id not in self.active_meetings:
                print(f"❌ Meeting {meeting_id} not found")
                return None
            
            meeting_data = self.active_meetings[meeting_id]
            duration = int((time.time() - meeting_data["start_time"]) / 60)
            
            # Generate analysis
            analysis = self._generate_meeting_analysis(meeting_id, meeting_data, duration)
            
            # Save to history
            self.meeting_history.append(asdict(analysis))
            
            # Save action items
            self.action_items.extend(analysis.action_items)
            
            # Remove from active meetings
            del self.active_meetings[meeting_id]
            
            # Save data
            self._save_meeting_data()
            
            print(f"✅ Meeting ended: {analysis.title}")
            return analysis
            
        except Exception as e:
            print(f"Error ending meeting: {e}")
            return None
    
    def _generate_meeting_analysis(self, meeting_id: str, meeting_data: Dict[str, Any], duration: int) -> MeetingAnalysis:
        """Generate comprehensive meeting analysis."""
        try:
            # Analyze participants
            participants = self._analyze_participants(meeting_data)
            
            # Analyze overall sentiment
            overall_sentiment = self._analyze_overall_sentiment(meeting_data)
            
            # Generate summary
            summary = self._generate_meeting_summary(meeting_data)
            
            # Create analysis
            analysis = MeetingAnalysis(
                meeting_id=meeting_id,
                title=meeting_data["title"],
                participants=participants,
                action_items=meeting_data["action_items"],
                key_decisions=meeting_data["key_points"],
                overall_sentiment=overall_sentiment,
                duration=duration,
                summary=summary,
                created_at=time.time()
            )
            
            return analysis
            
        except Exception as e:
            print(f"Meeting analysis generation error: {e}")
            return None
    
    def _analyze_participants(self, meeting_data: Dict[str, Any]) -> List[MeetingParticipant]:
        """Analyze meeting participants."""
        try:
            participants = []
            sentiment_data = meeting_data.get("sentiment_data", {})
            
            for participant_name in meeting_data["participants"]:
                # Calculate participation level
                participant_entries = [entry for entry in meeting_data["transcript"] if entry["speaker"] == participant_name]
                participation_level = "high" if len(participant_entries) > 5 else "medium" if len(participant_entries) > 2 else "low"
                
                # Calculate average sentiment
                participant_sentiments = sentiment_data.get(participant_name, [])
                if participant_sentiments:
                    sentiment_counts = {}
                    for sentiment_entry in participant_sentiments:
                        sentiment = sentiment_entry["sentiment"]
                        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
                    
                    overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)
                else:
                    overall_sentiment = "neutral"
                
                # Extract key points from participant
                participant_key_points = [entry["text"] for entry in participant_entries if len(entry["text"]) > 20]
                
                participant = MeetingParticipant(
                    name=participant_name,
                    role="participant",  # Could be enhanced with role detection
                    sentiment=overall_sentiment,
                    participation_level=participation_level,
                    key_points=participant_key_points[:3]  # Top 3 key points
                )
                
                participants.append(participant)
            
            return participants
            
        except Exception as e:
            print(f"Participant analysis error: {e}")
            return []
    
    def _analyze_overall_sentiment(self, meeting_data: Dict[str, Any]) -> str:
        """Analyze overall meeting sentiment."""
        try:
            sentiments = [entry["sentiment"] for entry in meeting_data["transcript"]]
            if not sentiments:
                return "neutral"
            
            sentiment_counts = {}
            for sentiment in sentiments:
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            
            return max(sentiment_counts, key=sentiment_counts.get)
            
        except Exception as e:
            print(f"Overall sentiment analysis error: {e}")
            return "neutral"
    
    def _generate_meeting_summary(self, meeting_data: Dict[str, Any]) -> str:
        """Generate meeting summary."""
        try:
            if not self.gemini_available:
                return self._fallback_meeting_summary(meeting_data)
            
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # Prepare transcript for analysis
            transcript_text = "\n".join([f"{entry['speaker']}: {entry['text']}" for entry in meeting_data["transcript"]])
            
            prompt = f"""
            Summarize this meeting transcript in Arabic:
            
            {transcript_text}
            
            Provide:
            1. Main topics discussed
            2. Key decisions made
            3. Action items
            4. Overall outcome
            
            Keep it concise and professional.
            """
            
            response = model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Meeting summary generation error: {e}")
            return self._fallback_meeting_summary(meeting_data)
    
    def _fallback_meeting_summary(self, meeting_data: Dict[str, Any]) -> str:
        """Fallback meeting summary."""
        try:
            title = meeting_data["title"]
            duration = int((time.time() - meeting_data["start_time"]) / 60)
            action_count = len(meeting_data["action_items"])
            key_points_count = len(meeting_data["key_points"])
            
            summary = f"""
            ملخص الاجتماع: {title}
            المدة: {duration} دقيقة
            عدد المهام: {action_count}
            النقاط الرئيسية: {key_points_count}
            """
            
            return summary.strip()
            
        except Exception as e:
            print(f"Fallback summary error: {e}")
            return "ملخص الاجتماع غير متوفر"
    
    def get_meeting_insights(self, meeting_id: str) -> Dict[str, Any]:
        """Get insights for a specific meeting."""
        try:
            meeting = next((m for m in self.meeting_history if m["meeting_id"] == meeting_id), None)
            if not meeting:
                return {"error": "Meeting not found"}
            
            insights = {
                "meeting_id": meeting_id,
                "title": meeting["title"],
                "duration": meeting["duration"],
                "participant_count": len(meeting["participants"]),
                "action_items_count": len(meeting["action_items"]),
                "overall_sentiment": meeting["overall_sentiment"],
                "key_decisions": meeting["key_decisions"],
                "summary": meeting["summary"]
            }
            
            return insights
            
        except Exception as e:
            print(f"Meeting insights error: {e}")
            return {"error": str(e)}
    
    def get_action_items(self, status: str = None) -> List[ActionItem]:
        """Get action items, optionally filtered by status."""
        try:
            if status:
                return [item for item in self.action_items if item.status == status]
            else:
                return self.action_items
                
        except Exception as e:
            print(f"Action items retrieval error: {e}")
            return []
    
    def update_action_item_status(self, item_id: str, status: str) -> bool:
        """Update action item status."""
        try:
            for item in self.action_items:
                if item.id == item_id:
                    item.status = status
                    self._save_meeting_data()
                    return True
            
            return False
            
        except Exception as e:
            print(f"Action item update error: {e}")
            return False
    
    def get_meeting_recommendations(self, meeting_id: str) -> List[str]:
        """Get recommendations for meeting improvement."""
        try:
            meeting = next((m for m in self.meeting_history if m["meeting_id"] == meeting_id), None)
            if not meeting:
                return []
            
            recommendations = []
            
            # Analyze meeting duration
            if meeting["duration"] > 120:  # More than 2 hours
                recommendations.append("المدة طويلة جداً، حاول تقسم الاجتماع لعدة جلسات")
            
            # Analyze participation
            low_participants = [p for p in meeting["participants"] if p["participation_level"] == "low"]
            if low_participants:
                recommendations.append(f"بعض المشاركين لم يشاركوا كثيراً: {', '.join([p['name'] for p in low_participants])}")
            
            # Analyze sentiment
            if meeting["overall_sentiment"] == "negative":
                recommendations.append("الاجتماع كان سلبي، حاول تحسن الجو في الاجتماعات القادمة")
            
            # Analyze action items
            if len(meeting["action_items"]) == 0:
                recommendations.append("لم يتم تحديد مهام واضحة، حاول تحدد مهام محددة في كل اجتماع")
            
            return recommendations
            
        except Exception as e:
            print(f"Meeting recommendations error: {e}")
            return []


# Global instance
meeting_intelligence = MeetingIntelligence()

def start_meeting(meeting_id: str, title: str, participants: List[str]) -> bool:
    """Start a meeting."""
    return meeting_intelligence.start_meeting(meeting_id, title, participants)

def add_meeting_transcript(meeting_id: str, speaker: str, text: str) -> bool:
    """Add transcript entry."""
    return meeting_intelligence.add_meeting_transcript(meeting_id, speaker, text)

def end_meeting(meeting_id: str) -> Optional[MeetingAnalysis]:
    """End meeting and get analysis."""
    return meeting_intelligence.end_meeting(meeting_id)

def get_meeting_insights(meeting_id: str) -> Dict[str, Any]:
    """Get meeting insights."""
    return meeting_intelligence.get_meeting_insights(meeting_id)

def get_action_items(status: str = None) -> List[ActionItem]:
    """Get action items."""
    return meeting_intelligence.get_action_items(status)

def update_action_item_status(item_id: str, status: str) -> bool:
    """Update action item status."""
    return meeting_intelligence.update_action_item_status(item_id, status)

def get_meeting_recommendations(meeting_id: str) -> List[str]:
    """Get meeting recommendations."""
    return meeting_intelligence.get_meeting_recommendations(meeting_id)
