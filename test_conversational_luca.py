#!/usr/bin/env python3
"""
Test Conversational Luca Features
Demonstrates the natural Derja conversation capabilities
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.conversational_personality import get_personality_response, get_greeting, get_small_talk
from assistant.ai_chatty_brain import chat_naturally, get_joke_response, get_time_response
from assistant.emotional_tts import speak_with_emotion, speak_naturally
from assistant.derja_nlu import detect_derja_intent

def test_conversational_personality():
    """Test conversational personality features."""
    print("🧠 Testing Conversational Personality...")
    print("=" * 50)
    
    # Test greetings
    greeting = get_greeting()
    print(f"Greeting: {greeting}")
    
    # Test personality responses
    test_cases = [
        ("fetch_email", "لقيت 5 إيميلات في الإنبوكس"),
        ("prepare_reply", "حضرتلك رد على الإيميل"),
        ("send_email", "تم إرسال الرد بنجاح!"),
        ("joke", "هههه، نكتة زينة!"),
        ("time", "الوقت 2:30 PM"),
        ("error", "مش قادر أعمل الحاجة")
    ]
    
    for intent, base_response in test_cases:
        personality_response = get_personality_response(
            intent, base_response, 
            last_action=intent, 
            mood="casual"
        )
        print(f"\nIntent: {intent}")
        print(f"Base: {base_response}")
        print(f"Personality: {personality_response}")
    
    # Test small talk
    small_talk = get_small_talk()
    print(f"\nSmall talk: {small_talk}")

def test_ai_chatty_brain():
    """Test AI chatty brain features."""
    print("\n🤖 Testing AI Chatty Brain...")
    print("=" * 50)
    
    # Test natural conversation
    test_inputs = [
        "أهلا وينك",
        "شنو نعمل اليوم؟",
        "كيفاش الحال؟",
        "أعطني نكتة",
        "شنادي الوقت"
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        response = chat_naturally(user_input)
        print(f"Luca: {response}")
    
    # Test specific responses
    print(f"\nJoke: {get_joke_response()}")
    print(f"Time: {get_time_response()}")

def test_emotional_tts():
    """Test emotional TTS features."""
    print("\n🎤 Testing Emotional TTS...")
    print("=" * 50)
    
    emotions = ["happy", "excited", "calm", "tired", "concerned", "playful"]
    test_text = "أهلا وسهلا! أنا لوكا، المساعد الذكي"
    
    for emotion in emotions:
        print(f"\nEmotion: {emotion}")
        print(f"Text: {test_text}")
        print("Speaking...")
        
        # Note: This will actually speak, so you'll hear it
        speak_with_emotion(test_text, emotion)
        print("✅ Spoken")

def test_derja_nlu_with_personality():
    """Test Derja NLU with personality integration."""
    print("\n🎯 Testing Derja NLU with Personality...")
    print("=" * 50)
    
    test_commands = [
        "أهلا وينك",
        "أعطيني الإيميلات",
        "حضرلي رد",
        "أبعت الرد",
        "شنادي الوقت",
        "أعطني نكتة"
    ]
    
    for command in test_commands:
        print(f"\nCommand: {command}")
        
        # Detect intent
        intent = detect_derja_intent(command)
        print(f"Intent: {intent.intent} (confidence: {intent.confidence:.2f})")
        
        # Get personality response
        base_response = f"طيب، نعمل {intent.intent}"
        personality_response = get_personality_response(
            intent.intent, base_response,
            last_action=intent.intent,
            mood="casual"
        )
        print(f"Personality Response: {personality_response}")

def test_conversation_flow():
    """Test natural conversation flow."""
    print("\n💬 Testing Conversation Flow...")
    print("=" * 50)
    
    conversation = [
        "أهلا وينك",
        "شنو نعمل اليوم؟",
        "أعطيني الإيميلات",
        "حضرلي رد",
        "أبعت الرد",
        "أعطني نكتة",
        "باي باي"
    ]
    
    for user_input in conversation:
        print(f"\nUser: {user_input}")
        
        # Detect intent
        intent = detect_derja_intent(user_input)
        
        # Get natural response
        response = chat_naturally(user_input, intent.intent)
        print(f"Luca: {response}")
        
        # Simulate speaking
        print("🎤 Speaking...")

def main():
    """Run all conversational tests."""
    print("🎤 Conversational Luca Test Suite")
    print("=" * 60)
    
    try:
        test_conversational_personality()
        test_ai_chatty_brain()
        test_emotional_tts()
        test_derja_nlu_with_personality()
        test_conversation_flow()
        
        print("\n✅ All conversational tests completed!")
        print("\n🎉 Your Luca now has natural Derja personality!")
        
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
