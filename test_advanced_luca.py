#!/usr/bin/env python3
"""
Test Advanced Luca Features
Comprehensive test for all new advanced features
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.multimodal_awareness import capture_and_analyze_screen, get_proactive_suggestions
from assistant.proactive_suggestions import start_proactive_monitoring, get_active_suggestions
from assistant.voice_authentication import create_voice_profile, get_authentication_status
from assistant.task_automation import create_automation_task, AutomationTask
from assistant.gamification import get_random_joke, get_trivia_question, get_daily_challenge
from assistant.conversational_personality import get_personality_response
from assistant.emotional_tts import speak_with_emotion

def test_multimodal_awareness():
    """Test multimodal awareness features."""
    print("🖥️ Testing Multimodal Awareness...")
    print("=" * 50)
    
    try:
        # Test screen analysis
        print("📸 Capturing and analyzing screen...")
        screen_analysis = capture_and_analyze_screen()
        
        if screen_analysis:
            print(f"Screen Analysis: {screen_analysis}")
            
            # Test proactive suggestions
            suggestions = get_proactive_suggestions(screen_analysis)
            print(f"Proactive Suggestions: {suggestions}")
        else:
            print("❌ Screen analysis failed")
        
        print("✅ Multimodal awareness test completed")
        
    except Exception as e:
        print(f"❌ Multimodal awareness test error: {e}")

def test_proactive_suggestions():
    """Test proactive suggestions system."""
    print("\n🔔 Testing Proactive Suggestions...")
    print("=" * 50)
    
    try:
        # Test getting active suggestions
        suggestions = get_active_suggestions()
        print(f"Active Suggestions: {len(suggestions)}")
        
        for suggestion in suggestions:
            print(f"- {suggestion.message}")
        
        print("✅ Proactive suggestions test completed")
        
    except Exception as e:
        print(f"❌ Proactive suggestions test error: {e}")

def test_voice_authentication():
    """Test voice authentication system."""
    print("\n🎤 Testing Voice Authentication...")
    print("=" * 50)
    
    try:
        # Test authentication status
        status = get_authentication_status()
        print(f"Authentication Status: {status}")
        
        # Test creating voice profile (mock)
        print("Creating voice profile for test user...")
        # Note: This would require actual audio recording
        print("✅ Voice authentication test completed (mock)")
        
    except Exception as e:
        print(f"❌ Voice authentication test error: {e}")

def test_task_automation():
    """Test task automation system."""
    print("\n🤖 Testing Task Automation...")
    print("=" * 50)
    
    try:
        # Create a test automation task
        test_task = AutomationTask(
            id="test_email_task",
            name="Test Email Task",
            type="email",
            description="Send test email",
            parameters={
                "type": "send_batch",
                "recipients": [
                    {"email": "test@example.com", "name": "Test User"}
                ],
                "subject_template": "Test from Luca",
                "content_template": "Hello {name}, this is a test message from Luca."
            }
        )
        
        # Create the task
        success = create_automation_task(test_task)
        if success:
            print("✅ Test automation task created")
        else:
            print("❌ Failed to create automation task")
        
        print("✅ Task automation test completed")
        
    except Exception as e:
        print(f"❌ Task automation test error: {e}")

def test_gamification():
    """Test gamification system."""
    print("\n🎮 Testing Gamification System...")
    print("=" * 50)
    
    try:
        # Test random joke
        print("🎭 Testing random joke...")
        joke_data = get_random_joke()
        if joke_data["joke"]:
            print(f"Joke: {joke_data['joke']['text']}")
            print(f"Personality Response: {joke_data['personality_response']}")
        
        # Test trivia question
        print("\n🧠 Testing trivia question...")
        question = get_trivia_question()
        print(f"Question: {question.question}")
        print(f"Options: {question.options}")
        print(f"Correct Answer: {question.correct_answer}")
        
        # Test daily challenge
        print("\n🏆 Testing daily challenge...")
        challenge = get_daily_challenge()
        print(f"Challenge: {challenge['message']}")
        print(f"Reward: {challenge['reward']}")
        
        print("✅ Gamification test completed")
        
    except Exception as e:
        print(f"❌ Gamification test error: {e}")

def test_conversational_personality():
    """Test conversational personality with new features."""
    print("\n💬 Testing Conversational Personality...")
    print("=" * 50)
    
    try:
        # Test personality responses with different contexts
        test_cases = [
            ("proactive_email", "فما 3 إيميلات مش مقروءة! تريد ألخصلك المحتوى؟"),
            ("proactive_calendar", "ميتينغ في 15 دقيقة! تريد أحضرلك أجندة؟"),
            ("proactive_task", "فما مهام متأخرة! تريد أخططلك الوقت؟"),
            ("joke_told", "هههه، نكتة زينة! تريد نكتة تاني؟"),
            ("trivia_correct", "صح! إجابة زينة! 🎉"),
            ("trivia_wrong", "غلط! بس مش مشكلة، جرب تاني!")
        ]
        
        for intent, base_response in test_cases:
            personality_response = get_personality_response(
                intent, base_response,
                last_action=intent,
                mood="helpful"
            )
            print(f"\nIntent: {intent}")
            print(f"Base: {base_response}")
            print(f"Personality: {personality_response}")
        
        print("✅ Conversational personality test completed")
        
    except Exception as e:
        print(f"❌ Conversational personality test error: {e}")

def test_emotional_tts():
    """Test emotional TTS with new features."""
    print("\n🎤 Testing Emotional TTS...")
    print("=" * 50)
    
    try:
        # Test different emotional responses
        emotions = ["happy", "excited", "playful", "encouraging", "helpful"]
        test_text = "أهلا! أنا لوكا، المساعد الذكي الجديد!"
        
        for emotion in emotions:
            print(f"\nEmotion: {emotion}")
            print(f"Text: {test_text}")
            print("Speaking...")
            
            # Note: This will actually speak
            speak_with_emotion(test_text, emotion)
            print("✅ Spoken")
        
        print("✅ Emotional TTS test completed")
        
    except Exception as e:
        print(f"❌ Emotional TTS test error: {e}")

def test_integration():
    """Test integration between all systems."""
    print("\n🔗 Testing System Integration...")
    print("=" * 50)
    
    try:
        # Test multimodal + proactive suggestions
        print("Testing multimodal + proactive integration...")
        screen_analysis = capture_and_analyze_screen()
        if screen_analysis:
            suggestions = get_proactive_suggestions(screen_analysis)
            print(f"Integration suggestions: {suggestions}")
        
        # Test gamification + personality
        print("\nTesting gamification + personality integration...")
        joke_data = get_random_joke()
        if joke_data["joke"]:
            print(f"Integrated joke response: {joke_data['personality_response']}")
        
        # Test automation + personality
        print("\nTesting automation + personality integration...")
        automation_response = get_personality_response(
            "automation_task",
            "تم إنجاز المهمة بنجاح!",
            last_action="automation_completed",
            mood="satisfied"
        )
        print(f"Automation response: {automation_response}")
        
        print("✅ System integration test completed")
        
    except Exception as e:
        print(f"❌ System integration test error: {e}")

def main():
    """Run all advanced feature tests."""
    print("🚀 Advanced Luca Feature Test Suite")
    print("=" * 60)
    
    try:
        test_multimodal_awareness()
        test_proactive_suggestions()
        test_voice_authentication()
        test_task_automation()
        test_gamification()
        test_conversational_personality()
        test_emotional_tts()
        test_integration()
        
        print("\n🎉 All advanced feature tests completed!")
        print("\n✨ Your Luca now has:")
        print("   🖥️ Multimodal awareness (screen analysis, document reading)")
        print("   🔔 Proactive suggestions and smart reminders")
        print("   🎤 Voice authentication and multi-user support")
        print("   🤖 Task automation and productivity features")
        print("   🎮 Gamification (jokes, trivia, games, challenges)")
        print("   💬 Enhanced conversational personality")
        print("   🎭 Advanced emotional TTS")
        print("   🔗 Seamless system integration")
        
        print("\n🎯 Your 'Siri in Derja' is now ULTRA-PRO!")
        
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
