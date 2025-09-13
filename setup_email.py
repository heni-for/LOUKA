#!/usr/bin/env python3
"""
Setup email access for Luca voice assistant
"""

import os
import sys

def setup_email():
    """Setup email access."""
    print("📧 Email Setup for Luca Voice Assistant")
    print("=" * 50)
    
    # Check if credentials exist
    if os.path.exists('credentials.json'):
        print("✅ Gmail credentials found!")
        
        # Test Gmail access
        try:
            from assistant.gmail_simple import setup_gmail
            if setup_gmail():
                print("🎉 Gmail setup complete!")
                return True
        except Exception as e:
            print(f"❌ Gmail setup failed: {e}")
    
    else:
        print("❌ Gmail credentials not found!")
        print("\nTo set up Gmail access:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials")
        print("5. Download credentials.json to this folder")
        print("6. Run this script again")
    
    # Check Outlook
    print("\n📧 Checking Outlook...")
    try:
        from assistant.outlook_local import list_inbox
        messages = list_inbox(top=1)
        print("✅ Outlook is working!")
        print(f"Found {len(messages)} messages in Outlook")
        return True
    except Exception as e:
        print(f"❌ Outlook not available: {e}")
        print("Make sure Microsoft Outlook is installed and running")
    
    print("\n💡 Email setup options:")
    print("1. Set up Gmail API (recommended)")
    print("2. Install Microsoft Outlook")
    print("3. Use web-based email (browser will open)")
    
    return False

if __name__ == "__main__":
    setup_email()
