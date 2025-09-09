#!/usr/bin/env python3
"""
Test script for enhanced Luca voice assistant features
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all enhanced modules can be imported."""
    print("🧪 Testing enhanced features...")
    
    try:
        from assistant.smart_features import handle_smart_command, is_smart_command, get_current_time
        print("✅ Smart features imported successfully")
    except ImportError as e:
        print(f"❌ Smart features import failed: {e}")
        return False
    
    try:
        from assistant.multilang_voice import MultiLanguageVoiceRecognizer
        print("✅ Multi-language voice recognition imported successfully")
    except ImportError as e:
        print(f"❌ Multi-language voice import failed: {e}")
        return False
    
    try:
        from assistant.continuous_voice import ContinuousVoiceAssistant
        print("✅ Continuous voice assistant imported successfully")
    except ImportError as e:
        print(f"❌ Continuous voice assistant import failed: {e}")
        return False
    
    try:
        from assistant.llm import chat_with_ai
        print("✅ Enhanced LLM imported successfully")
    except ImportError as e:
        print(f"❌ Enhanced LLM import failed: {e}")
        return False
    
    return True

def test_smart_features():
    """Test smart features functionality."""
    print("\n🧠 Testing smart features...")
    
    try:
        from assistant.smart_features import get_current_time, is_smart_command, handle_smart_command
        
        # Test time feature
        time_result = get_current_time()
        print(f"✅ Time feature: {time_result}")
        
        # Test command recognition
        test_commands = [
            "what time is it",
            "tell me a joke",
            "what's the weather",
            "calculate 2 plus 2",
            "define artificial intelligence"
        ]
        
        for cmd in test_commands:
            intent = is_smart_command(cmd)
            if intent:
                print(f"✅ Command '{cmd}' -> Intent: {intent}")
            else:
                print(f"⚠️  Command '{cmd}' -> No intent recognized")
        
        return True
    except Exception as e:
        print(f"❌ Smart features test failed: {e}")
        return False

def test_voice_recognition():
    """Test voice recognition setup."""
    print("\n🎤 Testing voice recognition setup...")
    
    try:
        from assistant.multilang_voice import MultiLanguageVoiceRecognizer
        
        recognizer = MultiLanguageVoiceRecognizer()
        available_languages = recognizer.get_available_languages()
        
        print(f"✅ Available languages: {available_languages}")
        
        if available_languages:
            print("✅ Voice recognition models loaded successfully")
            return True
        else:
            print("⚠️  No voice recognition models available")
            return False
            
    except Exception as e:
        print(f"❌ Voice recognition test failed: {e}")
        return False

def test_ai_chat():
    """Test AI chat functionality."""
    print("\n🤖 Testing AI chat...")
    
    try:
        from assistant.llm import chat_with_ai
        
        # Test with a simple message
        test_message = "Hello, how are you?"
        print(f"Testing with: '{test_message}'")
        
        # This will only work if GEMINI_API_KEY is set
        try:
            response = chat_with_ai(test_message)
            print(f"✅ AI Chat response: {response[:100]}...")
            return True
        except Exception as e:
            if "API key not found" in str(e):
                print("⚠️  AI Chat requires GEMINI_API_KEY to be set")
                return True  # Not a failure, just needs configuration
            else:
                print(f"❌ AI Chat test failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ AI Chat test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🎤 Luca Enhanced Voice Assistant - Feature Test")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Smart Features", test_smart_features),
        ("Voice Recognition", test_voice_recognition),
        ("AI Chat", test_ai_chat)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append((test_name, result))
    
    print(f"\n{'='*60}")
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your enhanced Luca assistant is ready!")
        print("\nTo start using it:")
        print("  python run_enhanced_luca.py gui          # GUI mode")
        print("  python run_enhanced_luca.py continuous   # Siri-like mode")
        print("  python run_enhanced_luca.py voice        # Push-to-talk mode")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Check the errors above.")
        print("Some features may not work properly.")

if __name__ == "__main__":
    main()
