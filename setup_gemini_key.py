#!/usr/bin/env python3
"""
Setup script for Gemini API key configuration.
This script helps you configure your Google Gemini API key for Luca.
"""

import os
from pathlib import Path

def setup_gemini_key():
    """Setup Gemini API key in .env file."""
    print("🔑 Luca Gemini API Key Setup")
    print("=" * 40)
    print()
    print("To get your Gemini API key:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the generated API key")
    print()
    
    # Get API key from user
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    # Check if .env file exists
    env_file = Path(".env")
    
    # Read existing .env content
    existing_content = ""
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # Remove old GEMINI_API_KEY if it exists
    lines = existing_content.split('\n')
    filtered_lines = [line for line in lines if not line.startswith('GEMINI_API_KEY=')]
    
    # Add new GEMINI_API_KEY
    filtered_lines.append(f"GEMINI_API_KEY={api_key}")
    
    # Write updated .env file
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(filtered_lines))
    
    print()
    print("✅ Gemini API key saved successfully!")
    print(f"📁 Saved to: {env_file.absolute()}")
    print()
    print("🚀 You can now run Luca with Gemini AI!")
    print("   python run_luca_gui.py")
    print()

if __name__ == "__main__":
    setup_gemini_key()
