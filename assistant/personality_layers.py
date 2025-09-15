#!/usr/bin/env python3
"""
Personality Layers System for Luca
Customizable personality modes (Professional, Friendly, Coach)
"""

import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from .conversational_personality import get_personality_response
from .ai_chatty_brain import chat_naturally
from .emotional_tts import speak_with_emotion

@dataclass
class PersonalityMode:
    """Represents a personality mode configuration."""
    mode_id: str
    name: str
    description: str
    characteristics: Dict[str, Any]
    phrases: Dict[str, List[str]]
    response_style: str
    tts_settings: Dict[str, Any]
    enabled: bool = True

class PersonalityLayers:
    """Personality layers system for customizable personas."""
    
    def __init__(self):
        self.current_mode = "friendly"
        self.personality_modes = self._load_personality_modes()
        self.mode_history = []
        self.mode_preferences = {}
        self._init_default_modes()
    
    def _init_default_modes(self):
        """Initialize default personality modes."""
        # Professional Mode
        professional_mode = PersonalityMode(
            mode_id="professional",
            name="الوضع المهني",
            description="شخصية مهنية و رسمية للعمل",
            characteristics={
                "formality": "high",
                "humor": "low",
                "proactivity": "medium",
                "detail_level": "high",
                "emotion": "neutral"
            },
            phrases={
                "greetings": [
                    "صباح الخير",
                    "مساء الخير",
                    "أهلا وسهلا"
                ],
                "confirmations": [
                    "تم",
                    "مفهوم",
                    "حاضر",
                    "سأقوم بذلك"
                ],
                "questions": [
                    "هل تريد",
                    "هل يمكنني",
                    "ما هي متطلباتك",
                    "كيف يمكنني مساعدتك"
                ],
                "responses": [
                    "سأقوم بتنفيذ المهمة",
                    "تم إنجاز المهمة بنجاح",
                    "هل هناك شيء آخر",
                    "تم حفظ المعلومات"
                ]
            },
            response_style="formal",
            tts_settings={
                "rate": 160,
                "volume": 0.85,
                "pitch": 1.0,
                "emotion": "professional"
            }
        )
        
        # Friendly Mode
        friendly_mode = PersonalityMode(
            mode_id="friendly",
            name="الوضع الودود",
            description="شخصية ودودة و مرحة للاستخدام اليومي",
            characteristics={
                "formality": "low",
                "humor": "high",
                "proactivity": "high",
                "detail_level": "medium",
                "emotion": "warm"
            },
            phrases={
                "greetings": [
                    "أهلا وسهلا! كيفاش؟",
                    "أهلا! شنو أحوالك؟",
                    "أهلا! شنو نعمل اليوم؟",
                    "أهلا! كيفاش الحال؟"
                ],
                "confirmations": [
                    "طيب، هكا",
                    "أه، زينة",
                    "طيب، نعملها",
                    "أه، نخدمك"
                ],
                "questions": [
                    "شنو تريد نعمل؟",
                    "شنو نخدمك؟",
                    "شنو تريد؟",
                    "كيفاش نخدمك؟"
                ],
                "responses": [
                    "أه، هكا فما",
                    "طيب، نعملها زينة",
                    "أه، شنو تريد نعمل تاني؟",
                    "طيب، هكا نعمل"
                ]
            },
            response_style="casual",
            tts_settings={
                "rate": 180,
                "volume": 0.9,
                "pitch": 1.1,
                "emotion": "happy"
            }
        )
        
        # Coach Mode
        coach_mode = PersonalityMode(
            mode_id="coach",
            name="وضع المدرب",
            description="شخصية تحفيزية و توجيهية للمساعدة في الأهداف",
            characteristics={
                "formality": "medium",
                "humor": "medium",
                "proactivity": "very_high",
                "detail_level": "high",
                "emotion": "motivational"
            },
            phrases={
                "greetings": [
                    "أهلا! جاهز للعمل؟",
                    "أهلا! شنو أهدافك اليوم؟",
                    "أهلا! وقت الإنجاز!",
                    "أهلا! شنو نعمل اليوم؟"
                ],
                "confirmations": [
                    "ممتاز!",
                    "زينة!",
                    "هكا صح!",
                    "نعملها!"
                ],
                "questions": [
                    "شنو هدفك اليوم؟",
                    "شنو تريد تحقق؟",
                    "كيفاش نصل للهدف؟",
                    "شنو الخطوة التالية؟"
                ],
                "responses": [
                    "هكا صح! نعملها!",
                    "ممتاز! تقدم زينة!",
                    "هكا نصل للهدف!",
                    "نعملها خطوة بخطوة!"
                ]
            },
            response_style="motivational",
            tts_settings={
                "rate": 200,
                "volume": 0.95,
                "pitch": 1.2,
                "emotion": "excited"
            }
        )
        
        # Add modes to system
        self.personality_modes["professional"] = professional_mode
        self.personality_modes["friendly"] = friendly_mode
        self.personality_modes["coach"] = coach_mode
    
    def _load_personality_modes(self) -> Dict[str, PersonalityMode]:
        """Load personality modes from file."""
        try:
            with open("personality_modes.json", "r", encoding="utf-8") as f:
                modes_data = json.load(f)
            
            modes = {}
            for mode_data in modes_data:
                mode = PersonalityMode(**mode_data)
                modes[mode.mode_id] = mode
            
            return modes
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"Error loading personality modes: {e}")
            return {}
    
    def _save_personality_modes(self):
        """Save personality modes to file."""
        try:
            modes_data = [asdict(mode) for mode in self.personality_modes.values()]
            with open("personality_modes.json", "w", encoding="utf-8") as f:
                json.dump(modes_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving personality modes: {e}")
    
    def set_personality_mode(self, mode_id: str) -> bool:
        """Set the current personality mode."""
        try:
            if mode_id not in self.personality_modes:
                print(f"❌ Personality mode '{mode_id}' not found")
                return False
            
            if not self.personality_modes[mode_id].enabled:
                print(f"❌ Personality mode '{mode_id}' is disabled")
                return False
            
            # Record mode change
            self.mode_history.append({
                "from_mode": self.current_mode,
                "to_mode": mode_id,
                "timestamp": time.time()
            })
            
            self.current_mode = mode_id
            print(f"✅ Personality mode changed to: {self.personality_modes[mode_id].name}")
            return True
            
        except Exception as e:
            print(f"Error setting personality mode: {e}")
            return False
    
    def get_current_mode(self) -> PersonalityMode:
        """Get the current personality mode."""
        return self.personality_modes.get(self.current_mode, self.personality_modes["friendly"])
    
    def get_mode_response(self, user_input: str, intent: str = None, context: Dict[str, Any] = None) -> str:
        """Get response based on current personality mode."""
        try:
            current_mode = self.get_current_mode()
            
            # Get base response
            if current_mode.mode_id == "professional":
                response = self._get_professional_response(user_input, intent, context)
            elif current_mode.mode_id == "friendly":
                response = self._get_friendly_response(user_input, intent, context)
            elif current_mode.mode_id == "coach":
                response = self._get_coach_response(user_input, intent, context)
            else:
                response = self._get_default_response(user_input, intent, context)
            
            # Apply mode-specific enhancements
            response = self._apply_mode_enhancements(response, current_mode)
            
            return response
            
        except Exception as e:
            print(f"Error getting mode response: {e}")
            return user_input
    
    def _get_professional_response(self, user_input: str, intent: str, context: Dict[str, Any]) -> str:
        """Get professional mode response."""
        try:
            if intent == "greeting":
                return "صباح الخير، كيف يمكنني مساعدتك اليوم؟"
            elif intent == "email":
                return "سأقوم بفحص بريدك الإلكتروني وإعداد الردود المناسبة"
            elif intent == "meeting":
                return "تم جدولة الاجتماع، هل تريد إعداد جدول الأعمال؟"
            elif intent == "task":
                return "سأقوم بتنفيذ المهمة المطلوبة، هل هناك متطلبات إضافية؟"
            else:
                return f"مفهوم، سأقوم بتنفيذ: {user_input}"
                
        except Exception as e:
            print(f"Professional response error: {e}")
            return user_input
    
    def _get_friendly_response(self, user_input: str, intent: str, context: Dict[str, Any]) -> str:
        """Get friendly mode response."""
        try:
            if intent == "greeting":
                return "أهلا وسهلا! كيفاش؟ شنو نعمل اليوم؟"
            elif intent == "email":
                return "أه، هكا فما إيميلات جديدة! تريد ألخصلك المحتوى؟"
            elif intent == "meeting":
                return "طيب، هكا ميتينغ جديد! تريد أحضرلك أجندة؟"
            elif intent == "task":
                return "أه، هكا مهمة جديدة! تريد نعملها زينة؟"
            else:
                return f"طيب، هكا! {user_input} - شنو تريد نعمل تاني؟"
                
        except Exception as e:
            print(f"Friendly response error: {e}")
            return user_input
    
    def _get_coach_response(self, user_input: str, intent: str, context: Dict[str, Any]) -> str:
        """Get coach mode response."""
        try:
            if intent == "greeting":
                return "أهلا! جاهز للعمل؟ شنو أهدافك اليوم؟"
            elif intent == "email":
                return "ممتاز! وقت الإيميلات! تريد نعملها بسرعة؟"
            elif intent == "meeting":
                return "زينة! ميتينغ جديد! تريد نخطط الأهداف؟"
            elif intent == "task":
                return "هكا صح! مهمة جديدة! تريد نعملها خطوة بخطوة؟"
            else:
                return f"ممتاز! {user_input} - هكا نصل للهدف!"
                
        except Exception as e:
            print(f"Coach response error: {e}")
            return user_input
    
    def _get_default_response(self, user_input: str, intent: str, context: Dict[str, Any]) -> str:
        """Get default response."""
        return get_personality_response(intent or "default", user_input, **context or {})
    
    def _apply_mode_enhancements(self, response: str, mode: PersonalityMode) -> str:
        """Apply mode-specific enhancements to response."""
        try:
            # Add mode-specific phrases
            if mode.characteristics["humor"] == "high":
                # Add humor elements
                humor_phrases = ["هههه", "زينة", "طيب"]
                if any(phrase in response for phrase in humor_phrases):
                    response += " 😄"
            
            # Add motivational elements for coach mode
            if mode.mode_id == "coach":
                motivational_phrases = ["ممتاز", "زينة", "هكا صح"]
                if any(phrase in response for phrase in motivational_phrases):
                    response += " 🚀"
            
            # Add professional elements
            if mode.mode_id == "professional":
                if "تم" in response or "سأقوم" in response:
                    response += " ✅"
            
            return response
            
        except Exception as e:
            print(f"Mode enhancement error: {e}")
            return response
    
    def speak_with_mode(self, text: str, context: Dict[str, Any] = None) -> bool:
        """Speak text with current mode's TTS settings."""
        try:
            current_mode = self.get_current_mode()
            tts_settings = current_mode.tts_settings
            
            # Use emotional TTS with mode settings
            emotion = tts_settings.get("emotion", "neutral")
            return speak_with_emotion(text, emotion)
            
        except Exception as e:
            print(f"Mode TTS error: {e}")
            return False
    
    def create_custom_mode(self, mode_data: Dict[str, Any]) -> bool:
        """Create a custom personality mode."""
        try:
            mode_id = mode_data.get("mode_id", "")
            if not mode_id:
                print("❌ Mode ID is required")
                return False
            
            if mode_id in self.personality_modes:
                print(f"❌ Mode '{mode_id}' already exists")
                return False
            
            # Create new mode
            mode = PersonalityMode(
                mode_id=mode_id,
                name=mode_data.get("name", mode_id),
                description=mode_data.get("description", ""),
                characteristics=mode_data.get("characteristics", {}),
                phrases=mode_data.get("phrases", {}),
                response_style=mode_data.get("response_style", "default"),
                tts_settings=mode_data.get("tts_settings", {}),
                enabled=mode_data.get("enabled", True)
            )
            
            self.personality_modes[mode_id] = mode
            self._save_personality_modes()
            
            print(f"✅ Custom mode created: {mode.name}")
            return True
            
        except Exception as e:
            print(f"Error creating custom mode: {e}")
            return False
    
    def update_mode(self, mode_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing personality mode."""
        try:
            if mode_id not in self.personality_modes:
                print(f"❌ Mode '{mode_id}' not found")
                return False
            
            mode = self.personality_modes[mode_id]
            
            # Update mode properties
            for key, value in updates.items():
                if hasattr(mode, key):
                    setattr(mode, key, value)
            
            self._save_personality_modes()
            print(f"✅ Mode updated: {mode.name}")
            return True
            
        except Exception as e:
            print(f"Error updating mode: {e}")
            return False
    
    def delete_mode(self, mode_id: str) -> bool:
        """Delete a personality mode."""
        try:
            if mode_id not in self.personality_modes:
                print(f"❌ Mode '{mode_id}' not found")
                return False
            
            if mode_id in ["professional", "friendly", "coach"]:
                print(f"❌ Cannot delete default mode: {mode_id}")
                return False
            
            mode_name = self.personality_modes[mode_id].name
            del self.personality_modes[mode_id]
            self._save_personality_modes()
            
            print(f"✅ Mode deleted: {mode_name}")
            return True
            
        except Exception as e:
            print(f"Error deleting mode: {e}")
            return False
    
    def list_modes(self) -> List[Dict[str, Any]]:
        """List all available personality modes."""
        modes = []
        for mode in self.personality_modes.values():
            modes.append({
                "mode_id": mode.mode_id,
                "name": mode.name,
                "description": mode.description,
                "enabled": mode.enabled,
                "is_current": mode.mode_id == self.current_mode
            })
        return modes
    
    def get_mode_statistics(self) -> Dict[str, Any]:
        """Get statistics about mode usage."""
        try:
            total_changes = len(self.mode_history)
            mode_usage = {}
            
            for change in self.mode_history:
                mode = change["to_mode"]
                mode_usage[mode] = mode_usage.get(mode, 0) + 1
            
            return {
                "total_mode_changes": total_changes,
                "mode_usage": mode_usage,
                "current_mode": self.current_mode,
                "available_modes": len(self.personality_modes)
            }
            
        except Exception as e:
            print(f"Error getting mode statistics: {e}")
            return {}
    
    def auto_switch_mode(self, context: Dict[str, Any]) -> bool:
        """Automatically switch mode based on context."""
        try:
            # Determine appropriate mode based on context
            if context.get("work_hours", False) and context.get("formal_task", False):
                return self.set_personality_mode("professional")
            elif context.get("motivational_needed", False) or context.get("goal_oriented", False):
                return self.set_personality_mode("coach")
            else:
                return self.set_personality_mode("friendly")
                
        except Exception as e:
            print(f"Error auto-switching mode: {e}")
            return False


# Global instance
personality_layers = PersonalityLayers()

def set_personality_mode(mode_id: str) -> bool:
    """Set personality mode."""
    return personality_layers.set_personality_mode(mode_id)

def get_mode_response(user_input: str, intent: str = None, context: Dict[str, Any] = None) -> str:
    """Get mode-based response."""
    return personality_layers.get_mode_response(user_input, intent, context)

def speak_with_mode(text: str, context: Dict[str, Any] = None) -> bool:
    """Speak with current mode."""
    return personality_layers.speak_with_mode(text, context)

def create_custom_mode(mode_data: Dict[str, Any]) -> bool:
    """Create custom mode."""
    return personality_layers.create_custom_mode(mode_data)

def list_modes() -> List[Dict[str, Any]]:
    """List all modes."""
    return personality_layers.list_modes()

def get_mode_statistics() -> Dict[str, Any]:
    """Get mode statistics."""
    return personality_layers.get_mode_statistics()

def auto_switch_mode(context: Dict[str, Any]) -> bool:
    """Auto switch mode."""
    return personality_layers.auto_switch_mode(context)
