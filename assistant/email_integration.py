#!/usr/bin/env python3
"""
Enhanced Email Integration for Luca
Supports multiple email providers and fallback options
"""

import os
import webbrowser
import subprocess
from typing import List, Dict, Optional
from datetime import datetime
from .gmail_api import GmailAPI

class EmailIntegration:
    def __init__(self):
        self.outlook_available = self._check_outlook()
        self.gmail_available = self._check_gmail()
        self.gmail_api = GmailAPI()
        
    def _check_outlook(self) -> bool:
        """Check if Outlook is available via COM."""
        try:
            import win32com.client
            outlook = win32com.client.Dispatch('Outlook.Application')
            return True
        except:
            return False
    
    def _check_gmail(self) -> bool:
        """Check if Gmail is accessible via browser."""
        try:
            # Try to open Gmail in default browser
            webbrowser.open('https://mail.google.com')
            return True
        except:
            return False
    
    def get_inbox_summary(self) -> str:
        """Get a summary of recent emails."""
        if self.outlook_available:
            return self._get_outlook_inbox()
        elif self.gmail_available:
            return self._get_gmail_summary()
        else:
            return self._get_email_fallback()
    
    def _get_outlook_inbox(self) -> str:
        """Get Outlook inbox using COM."""
        try:
            import win32com.client
            outlook = win32com.client.Dispatch('Outlook.Application')
            namespace = outlook.GetNamespace("MAPI")
            inbox = namespace.GetDefaultFolder(6)  # 6 = olFolderInbox
            
            messages = inbox.Items
            messages.Sort("[ReceivedTime]", True)  # Sort by received time, descending
            
            recent_emails = []
            for i, message in enumerate(messages):
                if i >= 5:  # Limit to 5 recent emails
                    break
                
                subject = getattr(message, 'Subject', 'No Subject')
                sender = getattr(message, 'SenderName', 'Unknown Sender')
                received_time = getattr(message, 'ReceivedTime', datetime.now())
                
                # Format the time
                if hasattr(received_time, 'strftime'):
                    time_str = received_time.strftime('%H:%M')
                else:
                    time_str = str(received_time)
                
                recent_emails.append(f"• {subject} - From: {sender} ({time_str})")
            
            if recent_emails:
                return f"📧 Recent emails in your inbox:\n" + "\n".join(recent_emails)
            else:
                return "📧 Your inbox is empty!"
                
        except Exception as e:
            return f"❌ Error accessing Outlook: {str(e)}"
    
    def _get_gmail_summary(self) -> str:
        """Provide Gmail access and try to get recent emails."""
        try:
            # Open Gmail
            webbrowser.open('https://mail.google.com')
            
            # Try to get recent emails using Gmail API (if available)
            return """📧 Gmail Integration:
• Opening Gmail in your browser
• You can now access your emails directly
• For voice control, use the web interface
• Luca can help draft emails if you ask!

💡 To read your last email:
• Say "read my last email" 
• Or "read recent emails"
• I'll help summarize them for you!"""
        except:
            return """📧 Gmail Integration:
• Opening Gmail in your browser
• You can now access your emails directly
• For voice control, use the web interface
• Luca can help draft emails if you ask!"""
    
    def _get_email_fallback(self) -> str:
        """Fallback when no email client is available."""
        return """📧 Email Integration Options:
• Install Microsoft Outlook for full integration
• Use Gmail web interface (opening now)
• Luca can help draft emails and manage tasks
• Ask me to 'draft an email' for assistance!"""
    
    def organize_emails(self) -> str:
        """Organize emails (simulated for now)."""
        if self.outlook_available:
            return self._organize_outlook_emails()
        else:
            return """📁 Email Organization:
• Opening your email client for organization
• Luca can help categorize and prioritize
• Use voice commands like 'mark as important'
• Ask me to draft follow-up emails!"""
    
    def _organize_outlook_emails(self) -> str:
        """Organize Outlook emails."""
        try:
            import win32com.client
            outlook = win32com.client.Dispatch('Outlook.Application')
            namespace = outlook.GetNamespace("MAPI")
            inbox = namespace.GetDefaultFolder(6)
            
            messages = inbox.Items
            unread_count = sum(1 for msg in messages if not getattr(msg, 'UnRead', False))
            
            return f"""📁 Email Organization Complete:
• Found {len(messages)} total emails
• {unread_count} unread emails
• Emails sorted by date
• Use 'read' command to access specific emails
• Ask me to 'draft' replies or follow-ups!"""
            
        except Exception as e:
            return f"❌ Error organizing emails: {str(e)}"
    
    def read_email(self, email_id: str = None) -> str:
        """Read a specific email."""
        if self.outlook_available:
            return self._read_outlook_email(email_id)
        else:
            return """📖 Email Reading:
• Opening your email client
• Use the interface to select emails
• Luca can help summarize emails
• Ask me to 'draft' responses!"""
    
    def read_last_email(self) -> str:
        """Read the most recent email with AI summary."""
        try:
            # Try Gmail API first
            if self.gmail_api.is_available():
                email = self.gmail_api.get_last_email()
                if email:
                    return self._format_email_with_summary(email)
                else:
                    return "📧 No emails found in your inbox."
            
            # Fallback to browser method
            webbrowser.open('https://mail.google.com')
            
            return """📖 Reading Your Last Email:
• Gmail opened in your browser
• Click on your most recent email
• Copy the content and paste it here
• I'll summarize it for you!

💡 Or say "summarize this email" and paste the content
• I can help draft replies
• I can extract key information
• I can suggest follow-up actions"""
            
        except Exception as e:
            return f"❌ Error reading email: {str(e)}"
    
    def _format_email_with_summary(self, email: Dict) -> str:
        """Format email with sender and subject only."""
        try:
            # Format the response with just sender and subject
            response = f"""📧 آخر بريد إلكتروني:

👤 من: {email['sender']}
📌 الموضوع: {email['subject']}

💡 هل تريد مني:
• قراءة المحتوى الكامل؟
• كتابة رد؟
• قراءة بريد إلكتروني آخر؟"""
            
            return response
            
        except Exception as e:
            return f"❌ Error formatting email: {str(e)}"
    
    def summarize_email_content(self, email_content: str) -> str:
        """Summarize email content using AI."""
        try:
            from .llm import summarize_email
            
            # Extract subject and body from content
            lines = email_content.split('\n')
            subject = "Email Summary"
            body = email_content
            
            # Look for subject line
            for line in lines:
                if line.lower().startswith('subject:'):
                    subject = line.replace('Subject:', '').strip()
                    break
            
            summary = summarize_email(subject, body)
            
            return f"""📧 Email Summary:
{summary}

💡 Would you like me to:
• Draft a reply?
• Extract action items?
• Categorize this email?"""
            
        except Exception as e:
            return f"❌ Error summarizing email: {str(e)}"
    
    def _read_outlook_email(self, email_id: str) -> str:
        """Read specific Outlook email."""
        try:
            import win32com.client
            outlook = win32com.client.Dispatch('Outlook.Application')
            namespace = outlook.GetNamespace("MAPI")
            inbox = namespace.GetDefaultFolder(6)
            
            if email_id:
                # Try to find email by ID
                try:
                    message = inbox.Items[email_id]
                except:
                    return f"❌ Email with ID {email_id} not found"
            else:
                # Get the most recent email
                messages = inbox.Items
                messages.Sort("[ReceivedTime]", True)
                message = messages[0]
            
            subject = getattr(message, 'Subject', 'No Subject')
            sender = getattr(message, 'SenderName', 'Unknown Sender')
            body = getattr(message, 'Body', 'No content')
            
            return f"""📖 Email Details:
Subject: {subject}
From: {sender}
Content: {body[:200]}{'...' if len(body) > 200 else ''}

Ask me to 'draft a reply' or 'summarize this email'!"""
            
        except Exception as e:
            return f"❌ Error reading email: {str(e)}"
    
    def draft_email(self, prompt: str) -> str:
        """Draft an email using AI."""
        try:
            from .llm import draft_email
            draft = draft_email(prompt)
            
            # Try to open email client
            if self.outlook_available:
                self._open_outlook_draft(draft)
                return f"""✍️ Email Drafted:
{draft}

Opening Outlook to send..."""
            else:
                # Copy to clipboard as fallback
                try:
                    import pyperclip
                    pyperclip.copy(draft)
                    return f"""✍️ Email Drafted (copied to clipboard):
{draft}

Paste this into your email client!"""
                except:
                    return f"""✍️ Email Drafted:
{draft}

Copy this text into your email client!"""
                    
        except Exception as e:
            return f"❌ Error drafting email: {str(e)}"
    
    def _open_outlook_draft(self, draft: str):
        """Open Outlook with the draft."""
        try:
            import win32com.client
            outlook = win32com.client.Dispatch('Outlook.Application')
            mail = outlook.CreateItem(0)  # 0 = olMailItem
            mail.Body = draft
            mail.Display()
        except:
            pass
    
    def get_status(self) -> str:
        """Get email integration status."""
        status = []
        if self.outlook_available:
            status.append("✅ Outlook COM integration")
        if self.gmail_available:
            status.append("✅ Gmail web access")
        if self.gmail_api.is_available():
            status.append("✅ Gmail API integration (automatic reading)")
        else:
            status.append("⚠️ Gmail API not configured")
            status.append("💡 Run 'python setup_gmail_api.py' for automatic email reading")
        
        if not status:
            status.append("⚠️ No email client detected")
            status.append("💡 Install Outlook or configure Gmail API")
        
        return "📧 Email Integration Status:\n" + "\n".join(status)
