#!/usr/bin/env python3
"""
Simple script to set up OpenAI API key for Luca
"""

import os
from pathlib import Path

def setup_api_key():
    print("🔑 Luca AI Voice Assistant - API Key Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ Found existing .env file")
        with open(env_file, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY=" in content and "your_openai_api_key_here" not in content:
                print("✅ OpenAI API key already configured!")
                return
    else:
        print("📝 Creating .env file...")
    
    print("\nTo use AI chat features, you need an OpenAI API key.")
    print("Get your free API key at: https://platform.openai.com/api-keys")
    print()
    
    api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️  Skipping API key setup. AI chat features will not work.")
        print("   You can still use email commands and voice recognition.")
        return
    
    # Create or update .env file
    env_content = f"""# OpenAI Configuration
OPENAI_API_KEY={api_key}

# Vosk Model Path
VOSK_MODEL_PATH=C:\\Users\\Heni2\\luca\\vosk-model-en-us-0.22

# Microsoft Graph (Optional - using local Outlook instead)
MS_CLIENT_ID=
MS_TENANT_ID=
MS_AUTH_MODE=local
MS_SCOPES=

# Azure OpenAI (Optional)
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT=
DEFAULT_MODEL=gpt-3.5-turbo
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✅ API key saved successfully!")
    print("🚀 You can now use AI chat features in Luca!")
    print("\nRestart Luca to use the new API key.")

if __name__ == "__main__":
    setup_api_key()
