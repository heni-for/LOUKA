#!/usr/bin/env python3
"""
Test script for Gemini AI integration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_import():
    """Test if Gemini can be imported and configured."""
    try:
        import google.generativeai as genai
        print("✅ Gemini SDK imported successfully")
        
        # Test configuration
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            print("⚠️  GEMINI_API_KEY not found in .env file")
            print("   Run: python setup_gemini_key.py")
            return False
        
        genai.configure(api_key=api_key)
        print("✅ Gemini configured successfully")
        
        # Test model creation
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("✅ Gemini model created successfully")
        
        # Test simple generation
        response = model.generate_content("Say hello in one word")
        print(f"✅ Test response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Gemini AI Integration")
    print("=" * 40)
    
    if test_gemini_import():
        print("\n🎉 Gemini integration is working!")
        print("   You can now use Luca with Gemini AI")
    else:
        print("\n❌ Gemini integration failed")
        print("   Please check your API key and try again")
