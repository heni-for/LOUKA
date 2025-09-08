#!/usr/bin/env python3
"""
Test Gmail API Connection and Authentication
"""

import os
import webbrowser
from assistant.gmail_api import GmailAPI

def test_gmail_connection():
    """Test Gmail API connection and authentication."""
    print("🧪 Testing Gmail API Connection")
    print("=" * 40)
    
    # Check if credentials exist
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("   Please make sure the file is in the current directory")
        return False
    
    print("✅ credentials.json found")
    
    # Initialize Gmail API
    gmail_api = GmailAPI()
    
    print("🔐 Attempting authentication...")
    print("   This will open a browser window for authentication")
    print("   Please complete the authentication process")
    
    try:
        # Test authentication
        if gmail_api.authenticate():
            print("✅ Authentication successful!")
            
            # Test reading an email
            print("📧 Testing email reading...")
            email = gmail_api.get_last_email()
            
            if email:
                print("✅ Successfully read email!")
                print(f"   Subject: {email['subject']}")
                print(f"   From: {email['sender']}")
                print(f"   Date: {email['date']}")
                print(f"   Preview: {email['snippet'][:100]}...")
                
                print("\n🎉 Gmail API is working perfectly!")
                print("   You can now say 'read my last email' to Luca!")
                return True
            else:
                print("⚠️ No emails found in inbox")
                print("   But authentication is working!")
                return True
        else:
            print("❌ Authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_gmail_connection()
    
    if success:
        print("\n🚀 Next steps:")
        print("1. Go back to Luca")
        print("2. Say 'read my last email'")
        print("3. Luca will automatically read your emails!")
    else:
        print("\n🔧 Troubleshooting:")
        print("1. Make sure credentials.json is in the current directory")
        print("2. Check that Gmail API is enabled in Google Cloud Console")
        print("3. Verify the OAuth consent screen is configured")
