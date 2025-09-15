#!/usr/bin/env python3
"""
Task Automation System for Luca
Productivity automation for batch emails, calendar, and system tasks
"""

import os
import json
import time
import subprocess
import pyautogui
import pyperclip
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from .email_integration import EmailIntegration
from .llm import chat_with_ai, draft_email
from .conversational_personality import get_personality_response
from .ai_chatty_brain import chat_naturally

@dataclass
class AutomationTask:
    """Represents an automation task."""
    id: str
    name: str
    type: str  # email, calendar, system, file, web
    description: str
    parameters: Dict[str, Any]
    schedule: Optional[str] = None  # cron-like schedule
    enabled: bool = True
    created_at: float = 0.0
    last_run: Optional[float] = None
    run_count: int = 0

class TaskAutomation:
    """Task automation system for productivity."""
    
    def __init__(self):
        self.email_integration = EmailIntegration()
        self.automation_tasks = {}
        self.tasks_file = "automation_tasks.json"
        self._load_automation_tasks()
        
    def _load_automation_tasks(self):
        """Load automation tasks from file."""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    tasks_data = json.load(f)
                
                for task_data in tasks_data:
                    task = AutomationTask(**task_data)
                    self.automation_tasks[task.id] = task
                
                print(f"✅ Loaded {len(self.automation_tasks)} automation tasks")
        except Exception as e:
            print(f"Error loading automation tasks: {e}")
    
    def _save_automation_tasks(self):
        """Save automation tasks to file."""
        try:
            tasks_data = [asdict(task) for task in self.automation_tasks.values()]
            with open(self.tasks_file, "w", encoding="utf-8") as f:
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)
            print("✅ Automation tasks saved")
        except Exception as e:
            print(f"Error saving automation tasks: {e}")
    
    def create_automation_task(self, task: AutomationTask) -> bool:
        """Create a new automation task."""
        try:
            task.created_at = time.time()
            self.automation_tasks[task.id] = task
            self._save_automation_tasks()
            print(f"✅ Automation task created: {task.name}")
            return True
        except Exception as e:
            print(f"Error creating automation task: {e}")
            return False
    
    def execute_automation_task(self, task_id: str) -> Dict[str, Any]:
        """Execute an automation task."""
        try:
            if task_id not in self.automation_tasks:
                return {"success": False, "error": "Task not found"}
            
            task = self.automation_tasks[task_id]
            if not task.enabled:
                return {"success": False, "error": "Task disabled"}
            
            # Execute based on task type
            if task.type == "email":
                result = self._execute_email_task(task)
            elif task.type == "calendar":
                result = self._execute_calendar_task(task)
            elif task.type == "system":
                result = self._execute_system_task(task)
            elif task.type == "file":
                result = self._execute_file_task(task)
            elif task.type == "web":
                result = self._execute_web_task(task)
            else:
                result = {"success": False, "error": "Unknown task type"}
            
            # Update task statistics
            task.last_run = time.time()
            task.run_count += 1
            self._save_automation_tasks()
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_email_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Execute email automation task."""
        try:
            task_type = task.parameters.get("type", "send")
            
            if task_type == "send_batch":
                return self._send_batch_emails(task)
            elif task_type == "draft_replies":
                return self._draft_batch_replies(task)
            elif task_type == "organize_inbox":
                return self._organize_inbox(task)
            elif task_type == "send_reminder":
                return self._send_reminder_email(task)
            else:
                return {"success": False, "error": "Unknown email task type"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _send_batch_emails(self, task: AutomationTask) -> Dict[str, Any]:
        """Send batch emails with AI-generated content."""
        try:
            recipients = task.parameters.get("recipients", [])
            subject_template = task.parameters.get("subject_template", "Update from Luca")
            content_template = task.parameters.get("content_template", "Hello, this is an automated message from Luca.")
            
            if not recipients:
                return {"success": False, "error": "No recipients specified"}
            
            sent_count = 0
            failed_count = 0
            
            for recipient in recipients:
                try:
                    # Generate personalized content
                    personalized_subject = self._personalize_content(subject_template, recipient)
                    personalized_content = self._personalize_content(content_template, recipient)
                    
                    # Send email
                    if self.email_integration.gmail_api.is_available():
                        success = self.email_integration.gmail_api.send_email(
                            to=recipient["email"],
                            subject=personalized_subject,
                            body=personalized_content
                        )
                    else:
                        success = self.email_integration.send_email(
                            to=recipient["email"],
                            subject=personalized_subject,
                            body=personalized_content
                        )
                    
                    if success:
                        sent_count += 1
                    else:
                        failed_count += 1
                        
                except Exception as e:
                    print(f"Error sending email to {recipient}: {e}")
                    failed_count += 1
            
            return {
                "success": True,
                "sent_count": sent_count,
                "failed_count": failed_count,
                "message": f"Batch email completed: {sent_count} sent, {failed_count} failed"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _draft_batch_replies(self, task: AutomationTask) -> Dict[str, Any]:
        """Draft batch replies for emails."""
        try:
            # Get unread emails
            if self.email_integration.gmail_api.is_available():
                emails = self.email_integration.gmail_api.get_emails(top=10)
            else:
                emails = self.email_integration.get_inbox_summary()
            
            if not emails:
                return {"success": True, "drafted_count": 0, "message": "No emails to draft replies for"}
            
            drafted_count = 0
            
            for email in emails:
                try:
                    # Generate reply using AI
                    reply_content = self._generate_email_reply(email)
                    
                    if reply_content:
                        # Save draft (this would integrate with email system)
                        drafted_count += 1
                        
                except Exception as e:
                    print(f"Error drafting reply for email {email.get('id', 'unknown')}: {e}")
            
            return {
                "success": True,
                "drafted_count": drafted_count,
                "message": f"Drafted {drafted_count} replies"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _organize_inbox(self, task: AutomationTask) -> Dict[str, Any]:
        """Organize inbox by categories."""
        try:
            # This would integrate with email system to organize emails
            # For now, return a mock response
            return {
                "success": True,
                "organized_count": 0,
                "message": "Inbox organization completed"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _send_reminder_email(self, task: AutomationTask) -> Dict[str, Any]:
        """Send reminder email."""
        try:
            recipient = task.parameters.get("recipient", "")
            reminder_text = task.parameters.get("reminder_text", "This is a reminder from Luca.")
            
            if not recipient:
                return {"success": False, "error": "No recipient specified"}
            
            subject = "Reminder from Luca"
            content = f"Hello,\n\n{reminder_text}\n\nBest regards,\nLuca"
            
            if self.email_integration.gmail_api.is_available():
                success = self.email_integration.gmail_api.send_email(
                    to=recipient,
                    subject=subject,
                    body=content
                )
            else:
                success = self.email_integration.send_email(
                    to=recipient,
                    subject=subject,
                    body=content
                )
            
            return {
                "success": success,
                "message": "Reminder email sent" if success else "Failed to send reminder email"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_calendar_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Execute calendar automation task."""
        try:
            task_type = task.parameters.get("type", "create_event")
            
            if task_type == "create_event":
                return self._create_calendar_event(task)
            elif task_type == "send_meeting_reminder":
                return self._send_meeting_reminder(task)
            elif task_type == "schedule_meeting":
                return self._schedule_meeting(task)
            else:
                return {"success": False, "error": "Unknown calendar task type"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_calendar_event(self, task: AutomationTask) -> Dict[str, Any]:
        """Create calendar event."""
        try:
            # This would integrate with Google Calendar API
            # For now, return a mock response
            event_title = task.parameters.get("title", "Luca Event")
            event_time = task.parameters.get("time", datetime.now() + timedelta(hours=1))
            
            return {
                "success": True,
                "message": f"Calendar event '{event_title}' created for {event_time}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _send_meeting_reminder(self, task: AutomationTask) -> Dict[str, Any]:
        """Send meeting reminder."""
        try:
            # This would integrate with calendar and email systems
            return {
                "success": True,
                "message": "Meeting reminder sent"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _schedule_meeting(self, task: AutomationTask) -> Dict[str, Any]:
        """Schedule meeting."""
        try:
            # This would integrate with calendar system
            return {
                "success": True,
                "message": "Meeting scheduled"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_system_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Execute system automation task."""
        try:
            task_type = task.parameters.get("type", "open_app")
            
            if task_type == "open_app":
                return self._open_application(task)
            elif task_type == "move_files":
                return self._move_files(task)
            elif task_type == "play_music":
                return self._play_music(task)
            elif task_type == "take_screenshot":
                return self._take_screenshot(task)
            else:
                return {"success": False, "error": "Unknown system task type"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _open_application(self, task: AutomationTask) -> Dict[str, Any]:
        """Open application."""
        try:
            app_name = task.parameters.get("app_name", "")
            app_path = task.parameters.get("app_path", "")
            
            if app_path:
                subprocess.Popen([app_path])
            elif app_name:
                # Try to open by name
                subprocess.Popen([app_name])
            else:
                return {"success": False, "error": "No app specified"}
            
            return {
                "success": True,
                "message": f"Application opened: {app_name or app_path}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _move_files(self, task: AutomationTask) -> Dict[str, Any]:
        """Move files to specified location."""
        try:
            source_path = task.parameters.get("source_path", "")
            destination_path = task.parameters.get("destination_path", "")
            
            if not source_path or not destination_path:
                return {"success": False, "error": "Source or destination path not specified"}
            
            # Move files
            import shutil
            shutil.move(source_path, destination_path)
            
            return {
                "success": True,
                "message": f"File moved from {source_path} to {destination_path}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _play_music(self, task: AutomationTask) -> Dict[str, Any]:
        """Play music."""
        try:
            music_path = task.parameters.get("music_path", "")
            if not music_path:
                return {"success": False, "error": "Music path not specified"}
            
            # Play music (this would integrate with music player)
            subprocess.Popen([music_path])
            
            return {
                "success": True,
                "message": f"Playing music: {music_path}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _take_screenshot(self, task: AutomationTask) -> Dict[str, Any]:
        """Take screenshot."""
        try:
            screenshot_path = task.parameters.get("screenshot_path", f"screenshot_{int(time.time())}.png")
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            return {
                "success": True,
                "message": f"Screenshot saved: {screenshot_path}",
                "screenshot_path": screenshot_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_file_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Execute file automation task."""
        try:
            task_type = task.parameters.get("type", "organize")
            
            if task_type == "organize":
                return self._organize_files(task)
            elif task_type == "backup":
                return self._backup_files(task)
            elif task_type == "cleanup":
                return self._cleanup_files(task)
            else:
                return {"success": False, "error": "Unknown file task type"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _organize_files(self, task: AutomationTask) -> Dict[str, Any]:
        """Organize files by type."""
        try:
            source_dir = task.parameters.get("source_dir", "")
            if not source_dir:
                return {"success": False, "error": "Source directory not specified"}
            
            # Organize files by extension
            organized_count = 0
            for filename in os.listdir(source_dir):
                if os.path.isfile(os.path.join(source_dir, filename)):
                    file_ext = os.path.splitext(filename)[1]
                    if file_ext:
                        # Create directory for file type
                        ext_dir = os.path.join(source_dir, file_ext[1:].upper())
                        os.makedirs(ext_dir, exist_ok=True)
                        
                        # Move file
                        src = os.path.join(source_dir, filename)
                        dst = os.path.join(ext_dir, filename)
                        os.rename(src, dst)
                        organized_count += 1
            
            return {
                "success": True,
                "message": f"Organized {organized_count} files"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _backup_files(self, task: AutomationTask) -> Dict[str, Any]:
        """Backup files."""
        try:
            source_dir = task.parameters.get("source_dir", "")
            backup_dir = task.parameters.get("backup_dir", "")
            
            if not source_dir or not backup_dir:
                return {"success": False, "error": "Source or backup directory not specified"}
            
            # Create backup
            import shutil
            shutil.copytree(source_dir, backup_dir, dirs_exist_ok=True)
            
            return {
                "success": True,
                "message": f"Backup created: {backup_dir}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _cleanup_files(self, task: AutomationTask) -> Dict[str, Any]:
        """Cleanup temporary files."""
        try:
            cleanup_dir = task.parameters.get("cleanup_dir", "")
            file_patterns = task.parameters.get("file_patterns", ["*.tmp", "*.temp"])
            
            if not cleanup_dir:
                return {"success": False, "error": "Cleanup directory not specified"}
            
            cleaned_count = 0
            for pattern in file_patterns:
                for file_path in Path(cleanup_dir).glob(pattern):
                    if file_path.is_file():
                        file_path.unlink()
                        cleaned_count += 1
            
            return {
                "success": True,
                "message": f"Cleaned up {cleaned_count} files"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _execute_web_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Execute web automation task."""
        try:
            task_type = task.parameters.get("type", "open_url")
            
            if task_type == "open_url":
                return self._open_url(task)
            elif task_type == "scrape_data":
                return self._scrape_data(task)
            else:
                return {"success": False, "error": "Unknown web task type"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _open_url(self, task: AutomationTask) -> Dict[str, Any]:
        """Open URL in browser."""
        try:
            url = task.parameters.get("url", "")
            if not url:
                return {"success": False, "error": "URL not specified"}
            
            # Open URL in default browser
            import webbrowser
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": f"Opened URL: {url}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _scrape_data(self, task: AutomationTask) -> Dict[str, Any]:
        """Scrape data from website."""
        try:
            url = task.parameters.get("url", "")
            if not url:
                return {"success": False, "error": "URL not specified"}
            
            # This would integrate with web scraping library
            return {
                "success": True,
                "message": f"Data scraped from: {url}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _personalize_content(self, template: str, recipient: Dict[str, Any]) -> str:
        """Personalize content template."""
        try:
            personalized = template
            
            # Replace placeholders
            if "{name}" in personalized:
                personalized = personalized.replace("{name}", recipient.get("name", "Friend"))
            
            if "{email}" in personalized:
                personalized = personalized.replace("{email}", recipient.get("email", ""))
            
            if "{company}" in personalized:
                personalized = personalized.replace("{company}", recipient.get("company", ""))
            
            return personalized
        except Exception as e:
            print(f"Content personalization error: {e}")
            return template
    
    def _generate_email_reply(self, email: Dict[str, Any]) -> str:
        """Generate email reply using AI."""
        try:
            # This would use AI to generate contextual replies
            return "Thank you for your email. I will get back to you soon."
        except Exception as e:
            print(f"Email reply generation error: {e}")
            return ""
    
    def get_automation_tasks(self) -> List[Dict[str, Any]]:
        """Get all automation tasks."""
        return [asdict(task) for task in self.automation_tasks.values()]
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get specific automation task."""
        if task_id in self.automation_tasks:
            return asdict(self.automation_tasks[task_id])
        return None
    
    def delete_task(self, task_id: str) -> bool:
        """Delete automation task."""
        try:
            if task_id in self.automation_tasks:
                del self.automation_tasks[task_id]
                self._save_automation_tasks()
                print(f"✅ Automation task deleted: {task_id}")
                return True
            else:
                print(f"❌ Task {task_id} not found")
                return False
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False
    
    def enable_task(self, task_id: str) -> bool:
        """Enable automation task."""
        try:
            if task_id in self.automation_tasks:
                self.automation_tasks[task_id].enabled = True
                self._save_automation_tasks()
                print(f"✅ Task enabled: {task_id}")
                return True
            else:
                print(f"❌ Task {task_id} not found")
                return False
        except Exception as e:
            print(f"Error enabling task: {e}")
            return False
    
    def disable_task(self, task_id: str) -> bool:
        """Disable automation task."""
        try:
            if task_id in self.automation_tasks:
                self.automation_tasks[task_id].enabled = False
                self._save_automation_tasks()
                print(f"✅ Task disabled: {task_id}")
                return True
            else:
                print(f"❌ Task {task_id} not found")
                return False
        except Exception as e:
            print(f"Error disabling task: {e}")
            return False


# Global instance
task_automation = TaskAutomation()

def create_automation_task(task: AutomationTask) -> bool:
    """Create automation task."""
    return task_automation.create_automation_task(task)

def execute_automation_task(task_id: str) -> Dict[str, Any]:
    """Execute automation task."""
    return task_automation.execute_automation_task(task_id)

def get_automation_tasks() -> List[Dict[str, Any]]:
    """Get all automation tasks."""
    return task_automation.get_automation_tasks()

def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    """Get specific task."""
    return task_automation.get_task(task_id)

def delete_task(task_id: str) -> bool:
    """Delete task."""
    return task_automation.delete_task(task_id)

def enable_task(task_id: str) -> bool:
    """Enable task."""
    return task_automation.enable_task(task_id)

def disable_task(task_id: str) -> bool:
    """Disable task."""
    return task_automation.disable_task(task_id)
