#!/usr/bin/env python3
"""
AI-powered voice command processor
Uses AI to interpret and correct speech recognition results
"""

import google.generativeai as genai
from .config import GEMINI_API_KEY

class AIVoiceProcessor:
    """AI-powered voice command processor."""
    
    def __init__(self):
        self.model = None
        self._configure_gemini()
    
    def _configure_gemini(self):
        """Configure Gemini AI."""
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def process_voice_command(self, raw_text: str, language: str = 'en') -> dict:
        """
        Process raw speech recognition text and return the best command.
        
        Args:
            raw_text: Raw text from speech recognition
            language: Language code ('en', 'ar', 'tn')
        
        Returns:
            dict: {
                'command': str,      # The best command
                'confidence': float, # Confidence score (0-1)
                'original': str,     # Original raw text
                'corrected': str     # AI-corrected text
            }
        """
        try:
            # Define available commands based on language
            commands = self._get_commands_for_language(language)
            
            # Create prompt for AI
            prompt = self._create_prompt(raw_text, commands, language)
            
            # Get AI response
            response = self.model.generate_content(prompt)
            result = self._parse_ai_response(response.text)
            
            return result
            
        except Exception as e:
            print(f"❌ AI Voice Processor Error: {e}")
            return {
                'command': raw_text,
                'confidence': 0.0,
                'original': raw_text,
                'corrected': raw_text
            }
    
    def _get_commands_for_language(self, language: str) -> list:
        """Get available commands for the specified language."""
        commands = {
            'en': [
                'read my last email', 'read last email', 'last email', 'recent email',
                'inbox', 'read emails', 'check emails', 'show emails',
                'draft email', 'compose email', 'write email',
                'organize emails', 'sort emails', 'categorize emails',
                'help', 'what can you do', 'commands'
            ],
            'ar': [
                'اقرأ آخر بريد', 'آخر بريد إلكتروني', 'قراءة آخر بريد',
                'صندوق', 'اقرأ البريد', 'تحقق من البريد',
                'مسودة بريد', 'كتابة بريد', 'إنشاء بريد',
                'تنظيم البريد', 'ترتيب البريد', 'تصنيف البريد',
                'مساعدة', 'ماذا يمكنك أن تفعل', 'أوامر'
            ],
            'tn': [
                'اقرأ آخر بريد', 'آخر بريد إلكتروني', 'قراءة آخر بريد',
                'صندوق', 'اقرأ البريد', 'تحقق من البريد',
                'مسودة بريد', 'كتابة بريد', 'إنشاء بريد',
                'تنظيم البريد', 'ترتيب البريد', 'تصنيف البريد',
                'مساعدة', 'ماذا يمكنك أن تفعل', 'أوامر',
                'read my last email', 'inbox', 'draft email', 'help'
            ]
        }
        return commands.get(language, commands['en'])
    
    def _create_prompt(self, raw_text: str, commands: list, language: str) -> str:
        """Create AI prompt for command processing."""
        lang_names = {'en': 'English', 'ar': 'Arabic', 'tn': 'Tunisian Arabic'}
        lang_name = lang_names.get(language, 'English')
        
        prompt = f"""
You are an AI voice command processor. Your job is to interpret speech recognition results and find the best matching command.

Language: {lang_name}
Raw speech recognition text: "{raw_text}"

Available commands:
{chr(10).join(f"- {cmd}" for cmd in commands)}

Please:
1. Correct any speech recognition errors
2. Find the best matching command from the list
3. Provide a confidence score (0.0 to 1.0)
4. If no good match, return the original text

Respond in this exact format:
COMMAND: [best matching command or original text]
CONFIDENCE: [0.0 to 1.0]
CORRECTED: [corrected text if needed, otherwise original]
REASON: [brief explanation of your choice]

Examples:
- If user says "read my last email" → COMMAND: read my last email, CONFIDENCE: 1.0
- If user says "reed my last emale" → COMMAND: read my last email, CONFIDENCE: 0.9
- If user says "check my inbox" → COMMAND: inbox, CONFIDENCE: 0.8
- If user says "help me" → COMMAND: help, CONFIDENCE: 0.9
"""
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> dict:
        """Parse AI response and extract command information."""
        try:
            lines = response_text.strip().split('\n')
            result = {
                'command': '',
                'confidence': 0.0,
                'original': '',
                'corrected': '',
                'reason': ''
            }
            
            for line in lines:
                line = line.strip()
                if line.startswith('COMMAND:'):
                    result['command'] = line.replace('COMMAND:', '').strip()
                elif line.startswith('CONFIDENCE:'):
                    try:
                        result['confidence'] = float(line.replace('CONFIDENCE:', '').strip())
                    except:
                        result['confidence'] = 0.0
                elif line.startswith('CORRECTED:'):
                    result['corrected'] = line.replace('CORRECTED:', '').strip()
                elif line.startswith('REASON:'):
                    result['reason'] = line.replace('REASON:', '').strip()
            
            # If no command found, use original
            if not result['command']:
                result['command'] = result['original']
            
            return result
            
        except Exception as e:
            print(f"❌ Error parsing AI response: {e}")
            return {
                'command': '',
                'confidence': 0.0,
                'original': '',
                'corrected': '',
                'reason': 'Parse error'
            }

def test_ai_voice_processor():
    """Test the AI voice processor."""
    print("🤖 Testing AI Voice Processor")
    print("=" * 40)
    
    try:
        processor = AIVoiceProcessor()
        
        # Test cases
        test_cases = [
            ("read my last email", "en"),
            ("reed my last emale", "en"),
            ("check inbox", "en"),
            ("اقرأ آخر بريد", "ar"),
            ("آخر بريد", "ar"),
            ("inbox help", "en"),
            ("draft email", "en")
        ]
        
        for raw_text, lang in test_cases:
            print(f"\n🔤 Raw: '{raw_text}' ({lang})")
            result = processor.process_voice_command(raw_text, lang)
            print(f"✅ Command: '{result['command']}'")
            print(f"📊 Confidence: {result['confidence']:.2f}")
            print(f"🔧 Corrected: '{result['corrected']}'")
            print(f"💭 Reason: {result['reason']}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_ai_voice_processor()
