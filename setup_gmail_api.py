#!/usr/bin/env python3
"""
Gmail API Setup Script for Luca
This script helps you set up Gmail API for automatic email reading
"""

import os
import json
from assistant.gmail_api import GmailAPI

def setup_gmail_api():
    """Setup Gmail API for automatic email reading."""
    print("📧 Gmail API Setup for Luca")
    print("=" * 40)
    print()
    
    gmail_api = GmailAPI()
    
    # Check if already configured
    if gmail_api.is_available():
        print("✅ Gmail API is already configured!")
        print("   You can now say 'read my last email' and Luca will automatically read it!")
        return
    
    # Show setup instructions
    instructions = gmail_api.get_setup_instructions()
    print(instructions)
    print()
    
    # Check if credentials.json exists
    if os.path.exists('credentials.json'):
        print("🔧 Found credentials.json file!")
        print("   Testing Gmail API connection...")
        
        try:
            if gmail_api.authenticate():
                print("✅ Gmail API authentication successful!")
                print("   Luca can now automatically read your emails!")
                
                # Test reading an email
                print("\n🧪 Testing email reading...")
                email = gmail_api.get_last_email()
                if email:
                    print(f"✅ Successfully read email: '{email['subject']}'")
                    print("   From:", email['sender'])
                else:
                    print("⚠️ No emails found in inbox")
            else:
                print("❌ Gmail API authentication failed")
                print("   Please check your credentials.json file")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("📋 Next Steps:")
        print("1. Follow the instructions above to create credentials.json")
        print("2. Run this script again: python setup_gmail_api.py")
        print("3. Say 'read my last email' to Luca!")

if __name__ == "__main__":
    setup_gmail_api()
