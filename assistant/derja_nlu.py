#!/usr/bin/env python3
"""
Natural Language Understanding (NLU) for Tunisian Derja
Handles speech-to-intent mapping for Tunisian Arabic dialect
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .config import GEMINI_API_KEY

@dataclass
class Intent:
    """Represents a detected intent with confidence and entities."""
    intent: str
    confidence: float
    entities: Dict[str, str]
    original_text: str
    normalized_text: str

class DerjaNLU:
    """Natural Language Understanding for Tunisian Derja commands."""
    
    def __init__(self):
        self.intent_patterns = self._load_derja_patterns()
        self.entity_patterns = self._load_entity_patterns()
        self.gemini_available = bool(GEMINI_API_KEY)
    
    def _load_derja_patterns(self) -> Dict[str, List[str]]:
        """Load Tunisian Derja intent patterns."""
        return {
            "fetch_email": [
                # Direct email requests
                r"a[a3]tini.*email", r"a[a3]tini.*inbox", r"a[a3]tini.*bariid",
                r"ch[a3]ndi.*email", r"ch[a3]ndi.*inbox", r"ch[a3]ndi.*bariid",
                r"a[a3]tini.*li.*3[a3]ndi", r"ch[a3]ndi.*li.*3[a3]ndi",
                r"a[a3]tini.*li.*f[a3]l.*email", r"ch[a3]ndi.*li.*f[a3]l.*email",
                r"a[a3]tini.*li.*f[a3]l.*inbox", r"ch[a3]ndi.*li.*f[a3]l.*inbox",
                # Check inbox
                r"ch[a3]f.*inbox", r"ch[a3]f.*email", r"ch[a3]f.*bariid",
                r"a[a3]tini.*ch[a3]f.*inbox", r"a[a3]tini.*ch[a3]f.*email",
                # Read emails
                r"a[a3]tini.*a[a3]ra.*email", r"ch[a3]ndi.*a[a3]ra.*email",
                r"a[a3]tini.*a[a3]ra.*inbox", r"ch[a3]ndi.*a[a3]ra.*inbox",
            ],
            "prepare_reply": [
                # Prepare response
                r"7[a3]dher.*rep[o0]nse", r"7[a3]dher.*r[a3]dd", r"7[a3]dher.*jaw[a3]b",
                r"a[a3]tini.*rep[o0]nse", r"a[a3]tini.*r[a3]dd", r"a[a3]tini.*jaw[a3]b",
                r"7[a3]dherli.*rep[o0]nse", r"7[a3]dherli.*r[a3]dd", r"7[a3]dherli.*jaw[a3]b",
                r"a[a3]tini.*li.*rep[o0]nse", r"a[a3]tini.*li.*r[a3]dd", r"a[a3]tini.*li.*jaw[a3]b",
                # Draft email
                r"7[a3]dher.*draft", r"7[a3]dher.*email", r"7[a3]dher.*bariid",
                r"a[a3]tini.*draft", r"a[a3]tini.*email", r"a[a3]tini.*bariid",
                r"7[a3]dherli.*draft", r"7[a3]dherli.*email", r"7[a3]dherli.*bariid",
                # Write response
                r"a[a3]tini.*a[a3]ktob.*rep[o0]nse", r"a[a3]tini.*a[a3]ktob.*r[a3]dd",
                r"7[a3]dher.*a[a3]ktob.*rep[o0]nse", r"7[a3]dher.*a[a3]ktob.*r[a3]dd",
            ],
            "send_email": [
                # Send email
                r"a[a3]b3[a3]th.*email", r"a[a3]b3[a3]th.*bariid", r"a[a3]b3[a3]th.*rep[o0]nse",
                r"a[a3]b3[a3]th.*r[a3]dd", r"a[a3]b3[a3]th.*jaw[a3]b",
                r"a[a3]b3[a3]thli.*email", r"a[a3]b3[a3]thli.*bariid", r"a[a3]b3[a3]thli.*rep[o0]nse",
                r"a[a3]b3[a3]thli.*r[a3]dd", r"a[a3]b3[a3]thli.*jaw[a3]b",
                r"a[a3]b3[a3]th.*li.*email", r"a[a3]b3[a3]th.*li.*bariid", r"a[a3]b3[a3]th.*li.*rep[o0]nse",
                # Send reply
                r"a[a3]b3[a3]th.*rep[o0]nse", r"a[a3]b3[a3]th.*r[a3]dd", r"a[a3]b3[a3]th.*jaw[a3]b",
                r"a[a3]b3[a3]thli.*rep[o0]nse", r"a[a3]b3[a3]thli.*r[a3]dd", r"a[a3]b3[a3]thli.*jaw[a3]b",
                # Send it
                r"a[a3]b3[a3]thha", r"a[a3]b3[a3]th.*ha", r"a[a3]b3[a3]th.*hiya",
                r"a[a3]b3[a3]th.*hiya", r"a[a3]b3[a3]th.*hiya.*email",
            ],
            "read_email": [
                # Read specific email
                r"a[a3]ra.*email", r"a[a3]ra.*bariid", r"a[a3]ra.*inbox",
                r"a[a3]tini.*a[a3]ra.*email", r"a[a3]tini.*a[a3]ra.*bariid",
                r"ch[a3]f.*a[a3]ra.*email", r"ch[a3]f.*a[a3]ra.*bariid",
                # Read next email
                r"a[a3]ra.*email.*j[a3]y", r"a[a3]ra.*bariid.*j[a3]y",
                r"a[a3]ra.*email.*li.*ba3[a3]d", r"a[a3]ra.*bariid.*li.*ba3[a3]d",
                r"a[a3]ra.*email.*li.*ba3[a3]d", r"a[a3]ra.*bariid.*li.*ba3[a3]d",
                # Read last email
                r"a[a3]ra.*email.*li.*a[a3]khir", r"a[a3]ra.*bariid.*li.*a[a3]khir",
                r"a[a3]ra.*email.*li.*a[a3]khir", r"a[a3]ra.*bariid.*li.*a[a3]khir",
            ],
            "organize_email": [
                # Organize emails
                r"n[a3]zz[a3]m.*email", r"n[a3]zz[a3]m.*bariid", r"n[a3]zz[a3]m.*inbox",
                r"a[a3]tini.*n[a3]zz[a3]m.*email", r"a[a3]tini.*n[a3]zz[a3]m.*bariid",
                r"ch[a3]f.*n[a3]zz[a3]m.*email", r"ch[a3]f.*n[a3]zz[a3]m.*bariid",
                # Sort emails
                r"r[a3]tt[a3]b.*email", r"r[a3]tt[a3]b.*bariid", r"r[a3]tt[a3]b.*inbox",
                r"a[a3]tini.*r[a3]tt[a3]b.*email", r"a[a3]tini.*r[a3]tt[a3]b.*bariid",
            ],
            "help": [
                # Help requests
                r"a[a3]3[a3]ni", r"a[a3]3[a3]ni.*ch[a3]ndi", r"a[a3]3[a3]ni.*a[a3]ml",
                r"ch[a3]ndi.*a[a3]ml", r"ch[a3]ndi.*a[a3]ml.*a[a3]ml",
                r"a[a3]3[a3]ni.*a[a3]ml.*a[a3]ml", r"a[a3]3[a3]ni.*a[a3]ml.*a[a3]ml",
                # What can you do
                r"ch[a3]ndi.*a[a3]ml", r"ch[a3]ndi.*a[a3]ml.*a[a3]ml",
                r"a[a3]3[a3]ni.*ch[a3]ndi.*a[a3]ml", r"a[a3]3[a3]ni.*ch[a3]ndi.*a[a3]ml",
            ],
            "time": [
                # Time requests
                r"ch[a3]ndi.*wa[a3]9t", r"ch[a3]ndi.*sa3[a3]a", r"ch[a3]ndi.*sa3[a3]a",
                r"a[a3]3[a3]ni.*ch[a3]ndi.*wa[a3]9t", r"a[a3]3[a3]ni.*ch[a3]ndi.*sa3[a3]a",
                r"a[a3]3[a3]ni.*wa[a3]9t", r"a[a3]3[a3]ni.*sa3[a3]a",
            ],
            "weather": [
                # Weather requests
                r"ch[a3]ndi.*ta[a3]s", r"ch[a3]ndi.*ta[a3]s.*a[a3]l.*jaw",
                r"a[a3]3[a3]ni.*ch[a3]ndi.*ta[a3]s", r"a[a3]3[a3]ni.*ch[a3]ndi.*ta[a3]s.*a[a3]l.*jaw",
                r"a[a3]3[a3]ni.*ta[a3]s", r"a[a3]3[a3]ni.*ta[a3]s.*a[a3]l.*jaw",
            ],
            "joke": [
                # Joke requests
                r"a[a3]3[a3]ni.*n[a3]kt[a3]", r"a[a3]3[a3]ni.*n[a3]kt[a3]a",
                r"ch[a3]ndi.*n[a3]kt[a3]", r"ch[a3]ndi.*n[a3]kt[a3]a",
                r"a[a3]3[a3]ni.*n[a3]kt[a3]a", r"a[a3]3[a3]ni.*n[a3]kt[a3]a",
            ],
            "calculate": [
                # Math requests
                r"a[a3]7[a3]s[a3]b", r"a[a3]7[a3]s[a3]b.*li", r"a[a3]7[a3]s[a3]b.*li.*a[a3]ml",
                r"ch[a3]ndi.*a[a3]7[a3]s[a3]b", r"ch[a3]ndi.*a[a3]7[a3]s[a3]b.*li",
                r"a[a3]3[a3]ni.*a[a3]7[a3]s[a3]b", r"a[a3]3[a3]ni.*a[a3]7[a3]s[a3]b.*li",
            ],
            "greeting": [
                # Greetings
                r"a[a3]hla", r"a[a3]hla.*win[a3]k", r"a[a3]hla.*win[a3]k.*a[a3]hla",
                r"a[a3]hla.*win[a3]k.*a[a3]hla.*win[a3]k", r"a[a3]hla.*win[a3]k.*a[a3]hla.*win[a3]k",
                r"a[a3]hla.*win[a3]k.*a[a3]hla.*win[a3]k.*a[a3]hla.*win[a3]k",
                r"a[a3]hla.*win[a3]k.*a[a3]hla.*win[a3]k.*a[a3]hla.*win[a3]k.*a[a3]hla.*win[a3]k",
            ],
            "goodbye": [
                # Goodbye
                r"b[a3]y", r"b[a3]y.*b[a3]y", r"b[a3]y.*b[a3]y.*b[a3]y",
                r"a[a3]hla.*b[a3]y", r"a[a3]hla.*b[a3]y.*b[a3]y",
                r"a[a3]hla.*b[a3]y.*b[a3]y.*b[a3]y",
            ]
        }
    
    def _load_entity_patterns(self) -> Dict[str, List[str]]:
        """Load entity extraction patterns for Derja."""
        return {
            "email_count": [
                r"(\d+).*email", r"(\d+).*bariid", r"(\d+).*inbox",
                r"a[a3]tini.*(\d+).*email", r"a[a3]tini.*(\d+).*bariid",
                r"ch[a3]ndi.*(\d+).*email", r"ch[a3]ndi.*(\d+).*bariid",
            ],
            "sender_name": [
                r"min.*([a-zA-Z\u0600-\u06FF\s]+)", r"min.*([a-zA-Z\u0600-\u06FF\s]+).*email",
                r"min.*([a-zA-Z\u0600-\u06FF\s]+).*bariid", r"min.*([a-zA-Z\u0600-\u06FF\s]+).*inbox",
            ],
            "city_name": [
                r"f[a3]l.*([a-zA-Z\u0600-\u06FF\s]+)", r"f[a3]l.*([a-zA-Z\u0600-\u06FF\s]+).*ta[a3]s",
                r"f[a3]l.*([a-zA-Z\u0600-\u06FF\s]+).*jaw", r"f[a3]l.*([a-zA-Z\u0600-\u06FF\s]+).*ta[a3]s.*a[a3]l.*jaw",
            ],
            "math_expression": [
                r"(\d+[\+\-\*\/]\d+)", r"(\d+[\+\-\*\/]\d+[\+\-\*\/]\d+)",
                r"a[a3]7[a3]s[a3]b.*(\d+[\+\-\*\/]\d+)", r"a[a3]7[a3]s[a3]b.*(\d+[\+\-\*\/]\d+[\+\-\*\/]\d+)",
            ]
        }
    
    def _normalize_derja_text(self, text: str) -> str:
        """Normalize Tunisian Derja text for better pattern matching."""
        # Convert to lowercase
        text = text.lower()
        
        # Normalize common Derja variations
        normalizations = {
            # Common letter variations
            '3': 'ع', '7': 'ح', '9': 'ق', '2': 'أ', '5': 'خ', '6': 'ط',
            '8': 'غ', '4': 'ش', '0': 'ص', '1': 'ض',
            # Common word variations
            'a[a3]tini': 'أعطيني', 'ch[a3]ndi': 'شنادي', 'a[a3]3[a3]ni': 'أعطني',
            'a[a3]hla': 'أهلا', 'win[a3]k': 'وينك', 'b[a3]y': 'باي',
            'a[a3]ra': 'أقرا', 'a[a3]ktob': 'أكتب', 'a[a3]b3[a3]th': 'أبعت',
            '7[a3]dher': 'حضر', 'n[a3]zz[a3]m': 'نظم', 'r[a3]tt[a3]b': 'رتب',
            'wa[a3]9t': 'وقت', 'sa3[a3]a': 'ساعة', 'ta[a3]s': 'طقس',
            'jaw': 'جو', 'n[a3]kt[a3]': 'نكتة', 'a[a3]7[a3]s[a3]b': 'أحسب',
            'email': 'إيميل', 'bariid': 'بريد', 'inbox': 'إنبوكس',
            'rep[o0]nse': 'ريسبونس', 'r[a3]dd': 'رد', 'jaw[a3]b': 'جواب',
            'draft': 'درافت', 'a[a3]ml': 'أعمل', 'a[a3]ml': 'أعمل',
        }
        
        for pattern, replacement in normalizations.items():
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def _extract_entities(self, text: str) -> Dict[str, str]:
        """Extract entities from Derja text."""
        entities = {}
        normalized_text = self._normalize_derja_text(text)
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, normalized_text, re.IGNORECASE)
                if match:
                    entities[entity_type] = match.group(1).strip()
                    break
        
        return entities
    
    def _match_intent_patterns(self, text: str) -> Tuple[str, float]:
        """Match text against intent patterns and return best match."""
        normalized_text = self._normalize_derja_text(text)
        best_intent = "unknown"
        best_confidence = 0.0
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, normalized_text, re.IGNORECASE):
                    # Calculate confidence based on pattern complexity and match quality
                    confidence = 0.8 + (len(pattern) / 100)  # Base confidence + pattern complexity
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_intent = intent
        
        return best_intent, min(best_confidence, 1.0)
    
    def _use_gemini_for_nlu(self, text: str) -> Tuple[str, float]:
        """Use Gemini AI for advanced NLU when patterns fail."""
        if not self.gemini_available:
            return "unknown", 0.0
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""You are a Tunisian Derja language expert. Analyze this text and determine the user's intent.

Text: "{text}"

Common Tunisian Derja intents:
- fetch_email: "a[a3]tini email", "ch[a3]ndi inbox", "a[a3]tini li 3[a3]ndi fel email"
- prepare_reply: "7[a3]dher reponse", "a[a3]tini jaw[a3]b", "7[a3]dherli draft"
- send_email: "a[a3]b3[a3]th email", "a[a3]b3[a3]th reponse", "a[a3]b3[a3]thha"
- read_email: "a[a3]ra email", "ch[a3]f inbox", "a[a3]ra email li j[a3]y"
- organize_email: "n[a3]zz[a3]m email", "r[a3]tt[a3]b inbox"
- help: "a[a3]3[a3]ni", "ch[a3]ndi a[a3]ml"
- time: "ch[a3]ndi wa[a3]9t", "a[a3]3[a3]ni sa3[a3]a"
- weather: "ch[a3]ndi ta[a3]s", "a[a3]3[a3]ni ta[a3]s al jaw"
- joke: "a[a3]3[a3]ni n[a3]kt[a3]", "ch[a3]ndi n[a3]kt[a3]a"
- calculate: "a[a3]7[a3]s[a3]b", "a[a3]7[a3]s[a3]b li"
- greeting: "a[a3]hla", "a[a3]hla win[a3]k"
- goodbye: "b[a3]y", "a[a3]hla b[a3]y"

Respond with only the intent name and confidence (0.0-1.0) in this format:
intent: confidence

Example: fetch_email: 0.9"""
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            if ":" in response_text:
                intent, confidence_str = response_text.split(":", 1)
                intent = intent.strip()
                confidence = float(confidence_str.strip())
                return intent, confidence
            
        except Exception as e:
            print(f"Gemini NLU error: {e}")
        
        return "unknown", 0.0
    
    def detect_intent(self, text: str) -> Intent:
        """Detect intent from Tunisian Derja text."""
        # First try pattern matching
        intent, confidence = self._match_intent_patterns(text)
        
        # If pattern matching fails or confidence is low, try Gemini
        if intent == "unknown" or confidence < 0.6:
            gemini_intent, gemini_confidence = self._use_gemini_for_nlu(text)
            if gemini_confidence > confidence:
                intent = gemini_intent
                confidence = gemini_confidence
        
        # Extract entities
        entities = self._extract_entities(text)
        
        return Intent(
            intent=intent,
            confidence=confidence,
            entities=entities,
            original_text=text,
            normalized_text=self._normalize_derja_text(text)
        )
    
    def get_supported_intents(self) -> List[str]:
        """Get list of supported intents."""
        return list(self.intent_patterns.keys())
    
    def get_intent_examples(self, intent: str) -> List[str]:
        """Get example phrases for a specific intent."""
        if intent in self.intent_patterns:
            # Convert patterns to readable examples
            examples = []
            for pattern in self.intent_patterns[intent][:3]:  # First 3 patterns
                # Convert regex to readable example
                example = pattern.replace(r"[a3]", "ع").replace(r"[a3]", "ع")
                example = example.replace(r"\.", "").replace(r"\*", "")
                example = example.replace(r"\(.*?\)", "").replace(r"\[.*?\]", "")
                examples.append(example)
            return examples
        return []


# Global instance
derja_nlu = DerjaNLU()

def detect_derja_intent(text: str) -> Intent:
    """Convenience function to detect Derja intent."""
    return derja_nlu.detect_intent(text)

def get_derja_intent_examples() -> Dict[str, List[str]]:
    """Get examples for all Derja intents."""
    examples = {}
    for intent in derja_nlu.get_supported_intents():
        examples[intent] = derja_nlu.get_intent_examples(intent)
    return examples
