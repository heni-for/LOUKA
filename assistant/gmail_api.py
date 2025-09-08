#!/usr/bin/env python3
"""
Gmail API Integration for automatic email reading
"""

import os
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GMAIL_API_AVAILABLE = True
except ImportError:
    GMAIL_API_AVAILABLE = False

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailAPI:
    def __init__(self):
        self.service = None
        self.credentials = None
        self.token_file = 'gmail_token.pickle'
        
    def authenticate(self) -> bool:
        """Authenticate with Gmail API."""
        if not GMAIL_API_AVAILABLE:
            return False
            
        try:
            # Load existing credentials
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    self.credentials = pickle.load(token)
            
            # If there are no valid credentials, get new ones
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    # Create credentials.json file if it doesn't exist
                    if not os.path.exists('credentials.json'):
                        self._create_credentials_file()
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    self.credentials = flow.run_local_server(port=0)
                
                # Save credentials for next run
                with open(self.token_file, 'wb') as token:
                    pickle.dump(self.credentials, token)
            
            # Build the Gmail service
            self.service = build('gmail', 'v1', credentials=self.credentials)
            return True
            
        except Exception as e:
            print(f"Gmail authentication error: {e}")
            return False
    
    def _create_credentials_file(self):
        """Create a basic credentials.json file for Gmail API."""
        credentials = {
            "installed": {
                "client_id": "your_client_id_here",
                "project_id": "your_project_id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "your_client_secret_here",
                "redirect_uris": ["http://localhost"]
            }
        }
        
        with open('credentials.json', 'w') as f:
            import json
            json.dump(credentials, f, indent=2)
    
    def get_last_email(self) -> Optional[Dict]:
        """Get the most recent email."""
        if not self.service:
            if not self.authenticate():
                return None
        
        try:
            # Get the most recent email
            results = self.service.users().messages().list(
                userId='me', 
                maxResults=1,
                q='in:inbox'
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                return None
            
            # Get the full message
            message_id = messages[0]['id']
            message = self.service.users().messages().get(
                userId='me', 
                id=message_id,
                format='full'
            ).execute()
            
            return self._parse_message(message)
            
        except HttpError as error:
            print(f"Gmail API error: {error}")
            return None
    
    def get_recent_emails(self, count: int = 5) -> List[Dict]:
        """Get recent emails."""
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            results = self.service.users().messages().list(
                userId='me', 
                maxResults=count,
                q='in:inbox'
            ).execute()
            
            messages = results.get('messages', [])
            parsed_messages = []
            
            for msg in messages:
                message = self.service.users().messages().get(
                    userId='me', 
                    id=msg['id'],
                    format='full'
                ).execute()
                parsed_messages.append(self._parse_message(message))
            
            return parsed_messages
            
        except HttpError as error:
            print(f"Gmail API error: {error}")
            return []
    
    def _parse_message(self, message: Dict) -> Dict:
        """Parse Gmail message into readable format."""
        headers = message['payload'].get('headers', [])
        
        # Extract headers
        subject = ""
        sender = ""
        date = ""
        
        for header in headers:
            name = header.get('name', '').lower()
            value = header.get('value', '')
            
            if name == 'subject':
                subject = value
            elif name == 'from':
                sender = value
            elif name == 'date':
                date = value
        
        # Extract body
        body = self._extract_body(message['payload'])
        
        return {
            'id': message['id'],
            'subject': subject,
            'sender': sender,
            'date': date,
            'body': body,
            'snippet': message.get('snippet', '')
        }
    
    def _extract_body(self, payload: Dict) -> str:
        """Extract email body from payload."""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        import base64
                        body += base64.urlsafe_b64decode(data).decode('utf-8')
                elif part['mimeType'] == 'text/html' and not body:
                    data = part['body'].get('data', '')
                    if data:
                        import base64
                        body += base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body'].get('data', '')
                if data:
                    import base64
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body
    
    def is_available(self) -> bool:
        """Check if Gmail API is available and configured."""
        return GMAIL_API_AVAILABLE and os.path.exists('credentials.json')
    
    def get_setup_instructions(self) -> str:
        """Get instructions for setting up Gmail API."""
        if not GMAIL_API_AVAILABLE:
            return """❌ Gmail API not available. Please install required packages:
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client"""
        
        if not os.path.exists('credentials.json'):
            return """📧 Gmail API Setup Required:

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create a new project or select existing one
3. Enable Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop application"
   - Download the JSON file
5. Rename the downloaded file to 'credentials.json'
6. Place it in your Luca project folder
7. Run Luca again and say "read my last email"

The first time will open a browser for authentication."""
        
        return "✅ Gmail API is configured and ready!"
