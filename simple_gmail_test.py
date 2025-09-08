#!/usr/bin/env python3
"""
Simple Gmail API Test
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def test_gmail_simple():
    """Simple Gmail API test."""
    print("🧪 Simple Gmail API Test")
    print("=" * 30)
    
    # Check credentials file
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        return False
    
    print("✅ credentials.json found")
    
    try:
        # Load credentials
        with open('credentials.json', 'r') as f:
            creds_data = json.load(f)
        
        print("✅ Credentials loaded")
        print(f"   Client ID: {creds_data['installed']['client_id'][:20]}...")
        
        # Create flow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        
        print("🔐 Starting authentication...")
        print("   This will open a browser window")
        
        # Run authentication
        credentials = flow.run_local_server(port=0)
        
        print("✅ Authentication successful!")
        
        # Build service
        service = build('gmail', 'v1', credentials=credentials)
        
        print("📧 Testing Gmail API...")
        
        # Get messages
        results = service.users().messages().list(userId='me', maxResults=1).execute()
        messages = results.get('messages', [])
        
        if messages:
            print(f"✅ Found {len(messages)} message(s)")
            
            # Get first message
            message_id = messages[0]['id']
            message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
            
            # Extract headers
            headers = message['payload'].get('headers', [])
            subject = ""
            sender = ""
            
            for header in headers:
                name = header.get('name', '').lower()
                value = header.get('value', '')
                
                if name == 'subject':
                    subject = value
                elif name == 'from':
                    sender = value
            
            print(f"   Subject: {subject}")
            print(f"   From: {sender}")
            print("🎉 Gmail API is working perfectly!")
            return True
        else:
            print("⚠️ No messages found in inbox")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_gmail_simple()
