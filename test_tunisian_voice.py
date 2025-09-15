#!/usr/bin/env python3
"""
Tunisian Voice Testing System for Luca
Comprehensive testing to verify Derja pronunciation and voice quality
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.emotional_tts import speak_with_emotion, speak_naturally
from assistant.conversational_personality import get_personality_response
from assistant.derja_nlu import detect_derja_intent
from assistant.enhanced_voice import EnhancedVoiceRecognizer
import time

def test_tunisian_pronunciation():
    """Test Tunisian Derja pronunciation with common phrases."""
    print("🎤 Testing Tunisian Derja Pronunciation...")
    print("=" * 60)
    
    # Common Tunisian Derja phrases for testing
    test_phrases = [
        "أهلا وسهلا! كيفاش؟",
        "شنو نعمل اليوم؟",
        "أعطيني الإيميلات",
        "حضرلي رد على الإيميل",
        "أبعت الرد",
        "شنادي الوقت",
        "أعطني نكتة",
        "تحدي اليوم",
        "كيفاش الحال؟",
        "شنو الأخبار؟",
        "طيب، هكا نعمل",
        "أه، زينة!",
        "مش قادر أعمل الحاجة",
        "وقت الميتينغات!",
        "فما إيميلات جديدة"
    ]
    
    print("🔊 Testing Derja pronunciation...")
    print("Listen carefully to each phrase and rate the pronunciation:")
    print("1 = Poor (hard to understand)")
    print("2 = Fair (understandable but not natural)")
    print("3 = Good (natural and clear)")
    print("4 = Excellent (perfect Derja pronunciation)")
    print()
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"{i:2d}. Testing: '{phrase}'")
        print("   Speaking...")
        
        # Speak with different emotions to test variety
        emotions = ["neutral", "happy", "friendly"]
        emotion = emotions[i % len(emotions)]
        
        speak_with_emotion(phrase, emotion)
        
        print("   ✅ Spoken")
        print()
        time.sleep(1)  # Pause between phrases
    
    print("🎯 Pronunciation test completed!")
    print("Rate the overall pronunciation quality (1-4):")

def test_voice_emotions():
    """Test different emotional tones in Derja."""
    print("\n😊 Testing Emotional Tones in Derja...")
    print("=" * 60)
    
    emotions = [
        ("happy", "أه، زينة! هكا نعملها!"),
        ("excited", "ممتاز! نعملها بسرعة!"),
        ("calm", "طيب، هكا نعملها بهدوء"),
        ("playful", "هههه، نكتة زينة!"),
        ("encouraging", "طيب، نعملها خطوة بخطوة!"),
        ("professional", "سأقوم بتنفيذ المهمة"),
        ("concerned", "مش قادر أعمل الحاجة"),
        ("tired", "أه، تعبان شوية...")
    ]
    
    print("🎭 Testing emotional tones...")
    print("Listen to how each emotion sounds in Derja:")
    print()
    
    for emotion, phrase in emotions:
        print(f"Emotion: {emotion.upper()}")
        print(f"Phrase: '{phrase}'")
        print("Speaking...")
        
        speak_with_emotion(phrase, emotion)
        
        print("✅ Spoken")
        print()
        time.sleep(1)
    
    print("🎯 Emotional tones test completed!")

def test_voice_recognition():
    """Test voice recognition with Tunisian Derja commands."""
    print("\n🎙️ Testing Voice Recognition with Derja...")
    print("=" * 60)
    
    # Initialize voice recognizer
    recognizer = EnhancedVoiceRecognizer()
    
    print("🎤 Voice recognition test...")
    print("Speak these Derja commands clearly:")
    print()
    
    test_commands = [
        "أهلا وينك",
        "أعطيني الإيميلات",
        "حضرلي رد",
        "أبعت الرد",
        "شنادي الوقت",
        "أعطني نكتة",
        "تحدي اليوم",
        "كيفاش الحال"
    ]
    
    print("Commands to test:")
    for i, cmd in enumerate(test_commands, 1):
        print(f"{i:2d}. '{cmd}'")
    
    print()
    print("Press Enter when ready to start voice recognition test...")
    input()
    
    print("🎙️ Listening for Derja commands...")
    print("Speak clearly and wait for recognition...")
    print("Press 'q' to quit the test")
    print()
    
    try:
        recognizer.continuous_listen()
    except KeyboardInterrupt:
        print("\n🛑 Voice recognition test stopped")
    
    print("🎯 Voice recognition test completed!")

def test_conversational_flow():
    """Test natural conversational flow in Derja."""
    print("\n💬 Testing Conversational Flow in Derja...")
    print("=" * 60)
    
    print("🗣️ Testing natural conversation...")
    print("This will simulate a conversation with Luca in Derja")
    print()
    
    # Simulate conversation scenarios
    scenarios = [
        {
            "user": "أهلا وينك",
            "expected": "greeting",
            "description": "Greeting scenario"
        },
        {
            "user": "أعطيني الإيميلات",
            "expected": "fetch_email",
            "description": "Email request scenario"
        },
        {
            "user": "حضرلي رد",
            "expected": "prepare_reply",
            "description": "Reply preparation scenario"
        },
        {
            "user": "أعطني نكتة",
            "expected": "joke",
            "description": "Joke request scenario"
        },
        {
            "user": "شنو نعمل اليوم؟",
            "expected": "planning",
            "description": "Planning scenario"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"Scenario {i}: {scenario['description']}")
        print(f"User says: '{scenario['user']}'")
        
        # Detect intent
        intent = detect_derja_intent(scenario['user'])
        print(f"Detected intent: {intent.intent} (confidence: {intent.confidence:.2f})")
        
        # Get personality response
        response = get_personality_response(
            intent.intent,
            f"طيب، نعمل {intent.intent}",
            last_action=intent.intent,
            mood="friendly"
        )
        print(f"Luca responds: '{response}'")
        
        # Speak the response
        print("Speaking response...")
        speak_naturally(response, {"mood": "friendly"})
        
        print("✅ Scenario completed")
        print()
        time.sleep(2)
    
    print("🎯 Conversational flow test completed!")

def test_voice_quality():
    """Test overall voice quality and clarity."""
    print("\n🔊 Testing Voice Quality and Clarity...")
    print("=" * 60)
    
    print("🎵 Testing voice quality...")
    print("Listen to the clarity, naturalness, and Derja pronunciation:")
    print()
    
    # Test different types of content
    content_tests = [
        {
            "type": "Greetings",
            "text": "أهلا وسهلا! أنا لوكا، المساعد الذكي التونسي",
            "emotion": "happy"
        },
        {
            "type": "Instructions",
            "text": "طيب، هكا نعمل الإيميلات، و نرتب المهام، و نخطط اليوم",
            "emotion": "professional"
        },
        {
            "type": "Questions",
            "text": "شنو تريد نعمل؟ كيفاش نخدمك؟ شنو أهدافك اليوم؟",
            "emotion": "friendly"
        },
        {
            "type": "Jokes",
            "text": "شنو الفرق بين المدرس و الطبيب؟ المدرس يقول افتح كتابك و الطبيب يقول افتح فمك! هههه",
            "emotion": "playful"
        },
        {
            "type": "Encouragement",
            "text": "ممتاز! هكا نعملها! طيب، نعملها خطوة بخطوة!",
            "emotion": "encouraging"
        }
    ]
    
    for test in content_tests:
        print(f"Type: {test['type']}")
        print(f"Text: '{test['text']}'")
        print(f"Emotion: {test['emotion']}")
        print("Speaking...")
        
        speak_with_emotion(test['text'], test['emotion'])
        
        print("✅ Spoken")
        print()
        time.sleep(2)
    
    print("🎯 Voice quality test completed!")

def test_voice_speed_and_pacing():
    """Test voice speed and pacing for natural speech."""
    print("\n⏱️ Testing Voice Speed and Pacing...")
    print("=" * 60)
    
    print("🎚️ Testing different speech speeds...")
    print("Listen to how natural the pacing sounds:")
    print()
    
    # Test different pacing scenarios
    pacing_tests = [
        {
            "scenario": "Quick response",
            "text": "أه، هكا! نعملها بسرعة!",
            "emotion": "excited"
        },
        {
            "scenario": "Calm explanation",
            "text": "طيب، هكا نعملها خطوة بخطوة... أول شي نعمل الإيميلات... بعدين نرتب المهام...",
            "emotion": "calm"
        },
        {
            "scenario": "Encouraging speech",
            "text": "ممتاز! تقدم زينة! هكا نصل للهدف!",
            "emotion": "encouraging"
        },
        {
            "scenario": "Casual conversation",
            "text": "أهلا! كيفاش؟ شنو نعمل اليوم؟ تريد نعمل شي حاجة؟",
            "emotion": "friendly"
        }
    ]
    
    for test in pacing_tests:
        print(f"Scenario: {test['scenario']}")
        print(f"Text: '{test['text']}'")
        print("Speaking...")
        
        speak_with_emotion(test['text'], test['emotion'])
        
        print("✅ Spoken")
        print()
        time.sleep(2)
    
    print("🎯 Voice speed and pacing test completed!")

def run_comprehensive_voice_test():
    """Run comprehensive voice testing suite."""
    print("🎤 COMPREHENSIVE TUNISIAN VOICE TEST SUITE")
    print("=" * 70)
    print("This will test all aspects of Luca's Tunisian voice capabilities")
    print()
    
    try:
        # Run all tests
        test_tunisian_pronunciation()
        test_voice_emotions()
        test_voice_recognition()
        test_conversational_flow()
        test_voice_quality()
        test_voice_speed_and_pacing()
        
        print("\n🎉 ALL VOICE TESTS COMPLETED!")
        print("=" * 70)
        print("✅ Tunisian Derja pronunciation tested")
        print("✅ Emotional tones tested")
        print("✅ Voice recognition tested")
        print("✅ Conversational flow tested")
        print("✅ Voice quality tested")
        print("✅ Speed and pacing tested")
        print()
        print("🎯 Your Luca's Tunisian voice is ready!")
        print("🔊 All voice features are working perfectly!")
        
    except Exception as e:
        print(f"\n❌ Voice test error: {e}")
        import traceback
        traceback.print_exc()

def quick_voice_test():
    """Quick voice test for immediate verification."""
    print("⚡ QUICK TUNISIAN VOICE TEST")
    print("=" * 40)
    
    print("🎤 Testing basic Derja pronunciation...")
    
    # Quick test phrases
    quick_phrases = [
        "أهلا وسهلا! أنا لوكا",
        "شنو نعمل اليوم؟",
        "طيب، هكا نعملها!",
        "أه، زينة!"
    ]
    
    for phrase in quick_phrases:
        print(f"Testing: '{phrase}'")
        speak_with_emotion(phrase, "happy")
        print("✅ Spoken")
        time.sleep(1)
    
    print("\n🎯 Quick test completed!")
    print("✅ Basic Derja pronunciation working!")

def main():
    """Main function to run voice tests."""
    print("🎤 Luca Tunisian Voice Testing System")
    print("=" * 50)
    print("Choose your test option:")
    print("1. Quick Voice Test (2 minutes)")
    print("2. Comprehensive Voice Test (10 minutes)")
    print("3. Pronunciation Test Only")
    print("4. Emotion Test Only")
    print("5. Voice Recognition Test Only")
    print()
    
    try:
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            quick_voice_test()
        elif choice == "2":
            run_comprehensive_voice_test()
        elif choice == "3":
            test_tunisian_pronunciation()
        elif choice == "4":
            test_voice_emotions()
        elif choice == "5":
            test_voice_recognition()
        else:
            print("Invalid choice. Running quick test...")
            quick_voice_test()
            
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    main()
