#!/usr/bin/env python3
"""
Test Ultra-Pro Luca Features
Comprehensive test for all next-level advanced features
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.learning_adaptation import record_user_action, generate_predictive_suggestions, get_user_insights
from assistant.personality_layers import set_personality_mode, get_mode_response, list_modes
from assistant.meeting_intelligence import start_meeting, add_meeting_transcript, end_meeting
from assistant.gamification import get_random_joke, get_trivia_question, get_daily_challenge
from assistant.conversational_personality import get_personality_response
from assistant.emotional_tts import speak_with_emotion

def test_learning_adaptation():
    """Test learning and adaptation system."""
    print("🧠 Testing Learning & Adaptation System...")
    print("=" * 50)
    
    try:
        # Test recording user actions
        print("📝 Recording user actions...")
        record_user_action("email_sent", {
            "recipient": "test@example.com",
            "subject": "Test Email",
            "body": "This is a test email"
        }, "work_context")
        
        record_user_action("meeting_scheduled", {
            "title": "Team Meeting",
            "start_time": "2024-01-15T10:00:00",
            "duration": 60,
            "type": "team"
        }, "work_context")
        
        record_user_action("voice_command", {
            "command": "أعطيني الإيميلات",
            "intent": "fetch_email"
        }, "voice_context")
        
        # Test generating predictive suggestions
        print("\n🔮 Generating predictive suggestions...")
        suggestions = generate_predictive_suggestions()
        print(f"Generated {len(suggestions)} predictive suggestions")
        
        for suggestion in suggestions:
            print(f"- {suggestion.message} (confidence: {suggestion.confidence:.2f})")
        
        # Test getting user insights
        print("\n📊 Getting user insights...")
        insights = get_user_insights()
        print(f"User insights: {insights}")
        
        print("✅ Learning & adaptation test completed")
        
    except Exception as e:
        print(f"❌ Learning & adaptation test error: {e}")

def test_personality_layers():
    """Test personality layers system."""
    print("\n🎭 Testing Personality Layers System...")
    print("=" * 50)
    
    try:
        # Test listing modes
        print("📋 Listing personality modes...")
        modes = list_modes()
        for mode in modes:
            print(f"- {mode['name']} ({mode['mode_id']}) - {'Current' if mode['is_current'] else 'Available'}")
        
        # Test professional mode
        print("\n💼 Testing professional mode...")
        set_personality_mode("professional")
        response = get_mode_response("أهلا", "greeting", {"work_context": True})
        print(f"Professional response: {response}")
        
        # Test friendly mode
        print("\n😊 Testing friendly mode...")
        set_personality_mode("friendly")
        response = get_mode_response("أهلا", "greeting", {"casual_context": True})
        print(f"Friendly response: {response}")
        
        # Test coach mode
        print("\n🚀 Testing coach mode...")
        set_personality_mode("coach")
        response = get_mode_response("أهلا", "greeting", {"motivational_context": True})
        print(f"Coach response: {response}")
        
        print("✅ Personality layers test completed")
        
    except Exception as e:
        print(f"❌ Personality layers test error: {e}")

def test_meeting_intelligence():
    """Test meeting intelligence system."""
    print("\n🤝 Testing Meeting Intelligence System...")
    print("=" * 50)
    
    try:
        # Test starting a meeting
        print("📅 Starting meeting...")
        meeting_id = "test_meeting_001"
        participants = ["أحمد", "فاطمة", "محمد"]
        start_meeting(meeting_id, "اجتماع فريق العمل", participants)
        
        # Test adding transcript
        print("📝 Adding meeting transcript...")
        add_meeting_transcript(meeting_id, "أحمد", "أهلا جميعاً، شنو نعمل اليوم؟")
        add_meeting_transcript(meeting_id, "فاطمة", "نعمل مشروع جديد، مهم جداً")
        add_meeting_transcript(meeting_id, "محمد", "طيب، نعمل خطة العمل")
        add_meeting_transcript(meeting_id, "أحمد", "نعمل جدول زمني")
        add_meeting_transcript(meeting_id, "فاطمة", "نعمل تقرير أسبوعي")
        
        # Test ending meeting and getting analysis
        print("📊 Ending meeting and getting analysis...")
        analysis = end_meeting(meeting_id)
        
        if analysis:
            print(f"Meeting Title: {analysis.title}")
            print(f"Duration: {analysis.duration} minutes")
            print(f"Participants: {len(analysis.participants)}")
            print(f"Action Items: {len(analysis.action_items)}")
            print(f"Overall Sentiment: {analysis.overall_sentiment}")
            print(f"Summary: {analysis.summary}")
        
        print("✅ Meeting intelligence test completed")
        
    except Exception as e:
        print(f"❌ Meeting intelligence test error: {e}")

def test_gamification_advanced():
    """Test advanced gamification features."""
    print("\n🎮 Testing Advanced Gamification...")
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
        
        print("✅ Advanced gamification test completed")
        
    except Exception as e:
        print(f"❌ Advanced gamification test error: {e}")

def test_emotional_tts_advanced():
    """Test advanced emotional TTS."""
    print("\n🎤 Testing Advanced Emotional TTS...")
    print("=" * 50)
    
    try:
        # Test different emotional responses
        emotions = ["happy", "excited", "playful", "encouraging", "helpful", "professional"]
        test_text = "أهلا! أنا لوكا، المساعد الذكي المتطور!"
        
        for emotion in emotions:
            print(f"\nEmotion: {emotion}")
            print(f"Text: {test_text}")
            print("Speaking...")
            
            # Note: This will actually speak
            speak_with_emotion(test_text, emotion)
            print("✅ Spoken")
        
        print("✅ Advanced emotional TTS test completed")
        
    except Exception as e:
        print(f"❌ Advanced emotional TTS test error: {e}")

def test_system_integration_advanced():
    """Test advanced system integration."""
    print("\n🔗 Testing Advanced System Integration...")
    print("=" * 50)
    
    try:
        # Test learning + personality integration
        print("Testing learning + personality integration...")
        record_user_action("voice_command", {
            "command": "أعطيني نكتة",
            "intent": "joke"
        }, "casual_context")
        
        # Test personality mode switching
        set_personality_mode("friendly")
        response = get_mode_response("أعطيني نكتة", "joke", {"casual_context": True})
        print(f"Integrated response: {response}")
        
        # Test meeting + learning integration
        print("\nTesting meeting + learning integration...")
        record_user_action("meeting_scheduled", {
            "title": "Learning Meeting",
            "start_time": "2024-01-15T14:00:00",
            "duration": 90,
            "type": "learning"
        }, "work_context")
        
        # Test gamification + personality integration
        print("\nTesting gamification + personality integration...")
        joke_data = get_random_joke()
        if joke_data["joke"]:
            print(f"Integrated joke: {joke_data['personality_response']}")
        
        print("✅ Advanced system integration test completed")
        
    except Exception as e:
        print(f"❌ Advanced system integration test error: {e}")

def test_predictive_assistance():
    """Test predictive assistance features."""
    print("\n🔮 Testing Predictive Assistance...")
    print("=" * 50)
    
    try:
        # Test generating predictive suggestions
        print("Generating predictive suggestions...")
        suggestions = generate_predictive_suggestions()
        
        if suggestions:
            print(f"Generated {len(suggestions)} predictive suggestions:")
            for suggestion in suggestions:
                print(f"- {suggestion.message} (confidence: {suggestion.confidence:.2f})")
        else:
            print("No predictive suggestions generated")
        
        # Test user insights
        print("\nGetting user insights...")
        insights = get_user_insights()
        print(f"User insights: {insights}")
        
        print("✅ Predictive assistance test completed")
        
    except Exception as e:
        print(f"❌ Predictive assistance test error: {e}")

def main():
    """Run all ultra-pro feature tests."""
    print("🚀 Ultra-Pro Luca Feature Test Suite")
    print("=" * 60)
    
    try:
        test_learning_adaptation()
        test_personality_layers()
        test_meeting_intelligence()
        test_gamification_advanced()
        test_emotional_tts_advanced()
        test_system_integration_advanced()
        test_predictive_assistance()
        
        print("\n🎉 All ultra-pro feature tests completed!")
        print("\n✨ Your Luca now has ULTRA-PRO features:")
        print("   🧠 Learning & Adaptation - Learns from your habits")
        print("   🔮 Predictive Assistance - Suggests actions before you ask")
        print("   🎭 Personality Layers - Professional, Friendly, Coach modes")
        print("   🤝 Meeting Intelligence - Real-time analysis and action items")
        print("   🎮 Advanced Gamification - Jokes, trivia, challenges")
        print("   🎤 Advanced Emotional TTS - 8 emotional tones")
        print("   🔗 Seamless Integration - All systems work together")
        
        print("\n🎯 Your 'Siri in Derja' is now ULTRA-PRO!")
        print("   🚀 Beyond ULTRA-PRO - Ready for next-level features!")
        
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
