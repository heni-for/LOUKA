#!/usr/bin/env python3
"""
Simple Gmail access using Gmail API
"""

import os
import pickle
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Get authenticated Gmail service."""
    creds = None
    
    # Check if token file exists
    if os.path.exists('gmail_token.pickle'):
        with open('gmail_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists('credentials.json'):
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            else:
                return None
        
        # Save credentials for next run
        with open('gmail_token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Gmail service error: {e}")
        return None

def list_gmail_inbox(top: int = 10) -> List[Dict]:
    """List recent emails from Gmail inbox."""
    try:
        service = get_gmail_service()
        if not service:
            return []
        
        # Get messages from inbox
        results = service.users().messages().list(userId='me', maxResults=top).execute()
        messages = results.get('messages', [])
        
        email_list = []
        for msg in messages:
            # Get message details
            message = service.users().messages().get(userId='me', id=msg['id']).execute()
            
            # Extract headers
            headers = message['payload'].get('headers', [])
            subject = ''
            sender = ''
            
            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                elif header['name'] == 'From':
                    sender = header['value']
            
            # Check if unread
            unread = 'UNREAD' in message.get('labelIds', [])
            
            email_list.append({
                'id': msg['id'],
                'subject': subject or 'No subject',
                'sender': sender or 'Unknown',
                'unread': unread,
                'date': message.get('internalDate', '')
            })
        
        return email_list
        
    except Exception as e:
        print(f"Gmail access error: {e}")
        return []

def get_gmail_message(message_id: str) -> Optional[Dict]:
    """Get full Gmail message content."""
    try:
        service = get_gmail_service()
        if not service:
            return None
        
        message = service.users().messages().get(userId='me', id=message_id).execute()
        
        # Extract body
        body = ''
        payload = message.get('payload', {})
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        import base64
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
        else:
            if payload.get('mimeType') == 'text/plain':
                data = payload['body'].get('data', '')
                if data:
                    import base64
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        # Extract headers
        headers = payload.get('headers', [])
        subject = ''
        sender = ''
        
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            elif header['name'] == 'From':
                sender = header['value']
        
        return {
            'id': message_id,
            'subject': subject or 'No subject',
            'sender': sender or 'Unknown',
            'body': body or 'No content',
            'date': message.get('internalDate', '')
        }
        
    except Exception as e:
        print(f"Gmail message error: {e}")
        return None

def send_gmail_message(to: str, subject: str, body: str) -> bool:
    """Send an email via Gmail API."""
    try:
        service = get_gmail_service()
        if not service:
            return False
        
        # Create message
        message = create_message('me', to, subject, body)
        
        # Send message
        result = service.users().messages().send(userId='me', body=message).execute()
        
        print(f"✅ Email sent successfully! Message ID: {result['id']}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def create_message(sender: str, to: str, subject: str, body: str) -> Dict:
    """Create a message for an email."""
    import base64
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def get_last_email_with_content() -> Optional[Dict]:
    """Get the last email with full content."""
    try:
        service = get_gmail_service()
        if not service:
            return None
        
        # Get the most recent message
        results = service.users().messages().list(userId='me', maxResults=1).execute()
        messages = results.get('messages', [])
        
        if not messages:
            return None
        
        # Get full message content
        message_id = messages[0]['id']
        return get_gmail_message(message_id)
        
    except Exception as e:
        print(f"Gmail last email error: {e}")
        return None

def search_email_from_sender(sender_name: str, max_results: int = 10) -> List[Dict]:
    """Search for emails from a specific sender."""
    try:
        service = get_gmail_service()
        if not service:
            return []
        
        # Search for emails from the sender
        query = f"from:{sender_name}"
        results = service.users().messages().list(
            userId='me', 
            q=query, 
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        if not messages:
            return []
        
        email_list = []
        for msg in messages:
            # Get message details
            message = service.users().messages().get(userId='me', id=msg['id']).execute()
            
            # Extract headers
            headers = message['payload'].get('headers', [])
            subject = ''
            sender = ''
            
            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                elif header['name'] == 'From':
                    sender = header['value']
            
            # Check if unread
            unread = 'UNREAD' in message.get('labelIds', [])
            
            email_list.append({
                'id': msg['id'],
                'subject': subject or 'No subject',
                'sender': sender or 'Unknown',
                'unread': unread,
                'date': message.get('internalDate', '')
            })
        
        return email_list
        
    except Exception as e:
        print(f"Gmail search error: {e}")
        return []

def get_last_email_from_sender(sender_name: str) -> Optional[Dict]:
    """Get the last email from a specific sender with full content."""
    try:
        service = get_gmail_service()
        if not service:
            return None
        
        # Search for emails from the sender
        query = f"from:{sender_name}"
        results = service.users().messages().list(
            userId='me', 
            q=query, 
            maxResults=1
        ).execute()
        
        messages = results.get('messages', [])
        if not messages:
            return None
        
        # Get full message content
        message_id = messages[0]['id']
        return get_gmail_message(message_id)
        
    except Exception as e:
        print(f"Gmail sender search error: {e}")
        return None

def setup_gmail():
    """Setup Gmail API credentials."""
    if not os.path.exists('credentials.json'):
        print("❌ Gmail credentials not found!")
        print("To set up Gmail access:")
        print("1. Go to Google Cloud Console")
        print("2. Create a project and enable Gmail API")
        print("3. Create OAuth 2.0 credentials")
        print("4. Download credentials.json to this folder")
        return False
    
    print("✅ Gmail credentials found!")
    print("Running Gmail setup...")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open('gmail_token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        
        print("✅ Gmail setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Gmail setup failed: {e}")
        return False
