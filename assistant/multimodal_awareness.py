#!/usr/bin/env python3
"""
Multimodal Awareness System for Luca
Visual context, document reading, and attachment processing
"""

import os
import json
import time
import base64
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageGrab
import pytesseract
import PyPDF2
import docx
from .config import GEMINI_API_KEY

class MultimodalAwareness:
    """Multimodal awareness system for visual and document processing."""
    
    def __init__(self):
        self.gemini_available = bool(GEMINI_API_KEY)
        self.screen_capture_enabled = True
        self.document_cache = {}
        self.visual_context = {}
        
    def _configure_gemini_vision(self):
        """Configure Gemini for vision processing."""
        if not self.gemini_available:
            raise ValueError("Gemini API key not available")
        
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel("gemini-1.5-flash")
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[np.ndarray]:
        """Capture screen or specific region."""
        try:
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()
            
            # Convert to OpenCV format
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return screenshot_cv
            
        except Exception as e:
            print(f"Screen capture error: {e}")
            return None
    
    def analyze_screen_content(self, screenshot: np.ndarray) -> Dict[str, Any]:
        """Analyze screen content using AI vision."""
        try:
            if not self.gemini_available:
                return self._fallback_screen_analysis(screenshot)
            
            model = self._configure_gemini_vision()
            
            # Convert image to base64
            _, buffer = cv2.imencode('.jpg', screenshot)
            image_data = base64.b64encode(buffer).decode('utf-8')
            
            prompt = """
            Analyze this screenshot and provide:
            1. What applications are visible
            2. Any meetings, calendars, or time-sensitive information
            3. Email or document content visible
            4. Any notifications or alerts
            5. Overall context and what the user might be working on
            
            Respond in JSON format with keys: apps, meetings, emails, notifications, context
            """
            
            response = model.generate_content([
                prompt,
                {
                    "mime_type": "image/jpeg",
                    "data": image_data
                }
            ])
            
            # Parse JSON response
            try:
                analysis = json.loads(response.text)
                return analysis
            except json.JSONDecodeError:
                return self._fallback_screen_analysis(screenshot)
                
        except Exception as e:
            print(f"Screen analysis error: {e}")
            return self._fallback_screen_analysis(screenshot)
    
    def _fallback_screen_analysis(self, screenshot: np.ndarray) -> Dict[str, Any]:
        """Fallback screen analysis using OCR."""
        try:
            # Use OCR to extract text
            text = pytesseract.image_to_string(screenshot)
            
            # Basic analysis
            analysis = {
                "apps": [],
                "meetings": [],
                "emails": [],
                "notifications": [],
                "context": "Screen content analyzed via OCR"
            }
            
            # Look for common patterns
            if "meeting" in text.lower() or "zoom" in text.lower():
                analysis["meetings"].append("Meeting detected")
            
            if "email" in text.lower() or "@" in text:
                analysis["emails"].append("Email content detected")
            
            if "notification" in text.lower() or "alert" in text.lower():
                analysis["notifications"].append("Notification detected")
            
            return analysis
            
        except Exception as e:
            print(f"Fallback analysis error: {e}")
            return {"apps": [], "meetings": [], "emails": [], "notifications": [], "context": "Analysis failed"}
    
    def get_proactive_suggestions(self, screen_analysis: Dict[str, Any]) -> List[str]:
        """Generate proactive suggestions based on screen analysis."""
        suggestions = []
        
        # Meeting suggestions
        if screen_analysis.get("meetings"):
            suggestions.append("أه، شفتك في ميتينغ! تريد أحضرلك أجندة أو ملاحظات؟")
        
        # Email suggestions
        if screen_analysis.get("emails"):
            suggestions.append("شفتك في الإيميلات! تريد ألخصلك المحتوى أو أحضر ردود؟")
        
        # Notification suggestions
        if screen_analysis.get("notifications"):
            suggestions.append("فما إشعارات جديدة! تريد أشوفلك شنو فيها؟")
        
        # Time-based suggestions
        current_hour = time.localtime().tm_hour
        if 9 <= current_hour <= 17:
            suggestions.append("وقت العمل! تريد أخططلك اليوم أو أشوفلك المهام؟")
        elif 17 <= current_hour <= 21:
            suggestions.append("وقت المساء! تريد ألخصلك يومك أو أخططلك بكرة؟")
        
        return suggestions
    
    def read_document(self, file_path: str) -> Dict[str, Any]:
        """Read and analyze document content."""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {"error": "File not found", "content": "", "summary": ""}
            
            # Check if already cached
            if str(file_path) in self.document_cache:
                return self.document_cache[str(file_path)]
            
            content = ""
            file_type = file_path.suffix.lower()
            
            if file_type == '.pdf':
                content = self._read_pdf(file_path)
            elif file_type in ['.docx', '.doc']:
                content = self._read_word(file_path)
            elif file_type in ['.txt', '.md']:
                content = self._read_text(file_path)
            elif file_type in ['.jpg', '.jpeg', '.png', '.bmp']:
                content = self._read_image(file_path)
            else:
                return {"error": "Unsupported file type", "content": "", "summary": ""}
            
            # Generate summary
            summary = self._summarize_content(content)
            
            result = {
                "content": content,
                "summary": summary,
                "file_type": file_type,
                "file_name": file_path.name
            }
            
            # Cache the result
            self.document_cache[str(file_path)] = result
            
            return result
            
        except Exception as e:
            return {"error": str(e), "content": "", "summary": ""}
    
    def _read_pdf(self, file_path: Path) -> str:
        """Read PDF content."""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                content = ""
                for page in reader.pages:
                    content += page.extract_text() + "\n"
                return content
        except Exception as e:
            print(f"PDF reading error: {e}")
            return ""
    
    def _read_word(self, file_path: Path) -> str:
        """Read Word document content."""
        try:
            doc = docx.Document(file_path)
            content = ""
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
            return content
        except Exception as e:
            print(f"Word reading error: {e}")
            return ""
    
    def _read_text(self, file_path: Path) -> str:
        """Read text file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Text reading error: {e}")
            return ""
    
    def _read_image(self, file_path: Path) -> str:
        """Read image content using OCR."""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Image reading error: {e}")
            return ""
    
    def _summarize_content(self, content: str) -> str:
        """Summarize document content using AI."""
        if not content or not self.gemini_available:
            return "محتوى غير قابل للتحليل"
        
        try:
            model = self._configure_gemini_vision()
            
            prompt = f"""
            Summarize this document content in Tunisian Derja:
            
            {content[:2000]}  # Limit content length
            
            Provide:
            1. Main points (النقاط الرئيسية)
            2. Key information (المعلومات المهمة)
            3. Action items if any (المهام المطلوبة)
            
            Respond in Derja:
            """
            
            response = model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Content summarization error: {e}")
            return "مش قادر ألخص المحتوى"
    
    def process_email_attachments(self, attachments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and summarize email attachments."""
        processed_attachments = []
        
        for attachment in attachments:
            try:
                file_path = attachment.get('file_path', '')
                if file_path and os.path.exists(file_path):
                    doc_info = self.read_document(file_path)
                    processed_attachments.append({
                        'name': attachment.get('name', ''),
                        'type': attachment.get('type', ''),
                        'summary': doc_info.get('summary', ''),
                        'content': doc_info.get('content', '')[:500],  # Limit content
                        'processed': True
                    })
                else:
                    processed_attachments.append({
                        'name': attachment.get('name', ''),
                        'type': attachment.get('type', ''),
                        'summary': 'مش قادر أقرا الملف',
                        'content': '',
                        'processed': False
                    })
            except Exception as e:
                processed_attachments.append({
                    'name': attachment.get('name', ''),
                    'type': attachment.get('type', ''),
                    'summary': f'خطأ في المعالجة: {str(e)}',
                    'content': '',
                    'processed': False
                })
        
        return processed_attachments
    
    def get_visual_context_response(self, screen_analysis: Dict[str, Any]) -> str:
        """Generate contextual response based on visual analysis."""
        if not screen_analysis:
            return "مش قادر أشوف شنو عملك"
        
        context_parts = []
        
        if screen_analysis.get("meetings"):
            context_parts.append("أه، شفتك في ميتينغ!")
        
        if screen_analysis.get("emails"):
            context_parts.append("شفتك في الإيميلات!")
        
        if screen_analysis.get("notifications"):
            context_parts.append("فما إشعارات جديدة!")
        
        if screen_analysis.get("apps"):
            apps = screen_analysis["apps"]
            if apps:
                context_parts.append(f"شفتك في {', '.join(apps)}")
        
        if context_parts:
            return " ".join(context_parts) + " تريد أساعدك في شنو؟"
        else:
            return "شفتك شغال! تريد أساعدك في شنو؟"
    
    def monitor_desktop_changes(self, callback=None) -> None:
        """Monitor desktop for changes and provide suggestions."""
        print("🖥️ Starting desktop monitoring...")
        
        last_analysis = None
        while True:
            try:
                # Capture screen
                screenshot = self.capture_screen()
                if screenshot is None:
                    time.sleep(5)
                    continue
                
                # Analyze content
                analysis = self.analyze_screen_content(screenshot)
                
                # Check for significant changes
                if last_analysis != analysis:
                    suggestions = self.get_proactive_suggestions(analysis)
                    if suggestions and callback:
                        for suggestion in suggestions:
                            callback(suggestion)
                    
                    last_analysis = analysis
                
                time.sleep(10)  # Check every 10 seconds
                
            except KeyboardInterrupt:
                print("🛑 Desktop monitoring stopped")
                break
            except Exception as e:
                print(f"Desktop monitoring error: {e}")
                time.sleep(5)
    
    def get_document_summary(self, file_path: str) -> str:
        """Get quick document summary."""
        doc_info = self.read_document(file_path)
        
        if doc_info.get("error"):
            return f"مش قادر أقرا الملف: {doc_info['error']}"
        
        summary = doc_info.get("summary", "مش قادر ألخص المحتوى")
        file_name = doc_info.get("file_name", "الملف")
        
        return f"ملخص {file_name}:\n{summary}"
    
    def clear_cache(self):
        """Clear document cache."""
        self.document_cache.clear()
        print("🗑️ Document cache cleared")


# Global instance
multimodal_awareness = MultimodalAwareness()

def capture_and_analyze_screen(region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
    """Capture screen and analyze content."""
    screenshot = multimodal_awareness.capture_screen(region)
    if screenshot is not None:
        return multimodal_awareness.analyze_screen_content(screenshot)
    return {}

def get_proactive_suggestions(screen_analysis: Dict[str, Any]) -> List[str]:
    """Get proactive suggestions based on screen analysis."""
    return multimodal_awareness.get_proactive_suggestions(screen_analysis)

def read_document(file_path: str) -> Dict[str, Any]:
    """Read and analyze document."""
    return multimodal_awareness.read_document(file_path)

def process_email_attachments(attachments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process email attachments."""
    return multimodal_awareness.process_email_attachments(attachments)

def get_visual_context_response(screen_analysis: Dict[str, Any]) -> str:
    """Get visual context response."""
    return multimodal_awareness.get_visual_context_response(screen_analysis)

def monitor_desktop_changes(callback=None):
    """Monitor desktop for changes."""
    multimodal_awareness.monitor_desktop_changes(callback)

def get_document_summary(file_path: str) -> str:
    """Get document summary."""
    return multimodal_awareness.get_document_summary(file_path)
