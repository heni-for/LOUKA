#!/usr/bin/env python3
"""
Interactive Tunisian Voice Test
Interactive testing to verify Luca's Tunisian voice quality
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.emotional_tts import speak_with_emotion, speak_naturally
from assistant.conversational_personality import get_personality_response
from assistant.derja_nlu import detect_derja_intent
import time

def interactive_voice_test():
    """Interactive voice testing with user feedback."""
    print("🎤 INTERACTIVE TUNISIAN VOICE TEST")
    print("=" * 50)
    print("This will test Luca's voice and ask for your feedback")
    print()
    
    # Test phrases with different emotions
    test_cases = [
        {
            "phrase": "أهلا وسهلا! أنا لوكا",
            "emotion": "happy",
            "description": "Basic greeting"
        },
        {
            "phrase": "شنو نعمل اليوم؟",
            "emotion": "friendly", 
            "description": "Casual question"
        },
        {
            "phrase": "طيب، هكا نعملها!",
            "emotion": "excited",
            "description": "Encouraging response"
        },
        {
            "phrase": "أه، زينة! هكا صح!",
            "emotion": "playful",
            "description": "Playful affirmation"
        },
        {
            "phrase": "مش قادر أعمل الحاجة",
            "emotion": "concerned",
            "description": "Concerned response"
        }
    ]
    
    print("🔊 Testing Derja pronunciation and emotional tones...")
    print("After each phrase, rate the quality (1-4):")
    print("1 = Poor (hard to understand)")
    print("2 = Fair (understandable but not natural)")
    print("3 = Good (natural and clear)")
    print("4 = Excellent (perfect Derja pronunciation)")
    print()
    
    total_score = 0
    max_score = len(test_cases) * 4
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}/{len(test_cases)}: {test['description']}")
        print(f"Phrase: '{test['phrase']}'")
        print(f"Emotion: {test['emotion']}")
        print("Speaking...")
        
        # Speak the phrase
        speak_with_emotion(test['phrase'], test['emotion'])
        
        print("✅ Spoken")
        print()
        
        # Get user rating
        while True:
            try:
                rating = input(f"Rate this phrase (1-4): ").strip()
                if rating in ['1', '2', '3', '4']:
                    rating = int(rating)
                    total_score += rating
                    break
                else:
                    print("Please enter 1, 2, 3, or 4")
            except KeyboardInterrupt:
                print("\n🛑 Test interrupted")
                return
            except:
                print("Please enter a valid number")
        
        print(f"Rated: {rating}/4")
        print("-" * 30)
        print()
        time.sleep(1)
    
    # Calculate results
    percentage = (total_score / max_score) * 100
    
    print("🎯 TEST RESULTS")
    print("=" * 30)
    print(f"Total Score: {total_score}/{max_score}")
    print(f"Percentage: {percentage:.1f}%")
    print()
    
    if percentage >= 90:
        print("🎉 EXCELLENT! Your Tunisian voice is perfect!")
        print("✅ Pronunciation: Excellent")
        print("✅ Emotional tones: Perfect")
        print("✅ Naturalness: Outstanding")
    elif percentage >= 75:
        print("👍 GOOD! Your Tunisian voice is working well!")
        print("✅ Pronunciation: Good")
        print("✅ Emotional tones: Clear")
        print("✅ Naturalness: Good")
    elif percentage >= 60:
        print("⚠️ FAIR! Your Tunisian voice needs some improvement")
        print("🔧 Pronunciation: Needs work")
        print("🔧 Emotional tones: Could be better")
        print("🔧 Naturalness: Somewhat robotic")
    else:
        print("❌ POOR! Your Tunisian voice needs significant improvement")
        print("🔧 Pronunciation: Hard to understand")
        print("🔧 Emotional tones: Not clear")
        print("🔧 Naturalness: Very robotic")
    
    print()
    print("🎤 Your Luca is ready for Tunisian voice!")

def test_voice_commands():
    """Test voice recognition with Derja commands."""
    print("\n🎙️ TESTING VOICE COMMANDS")
    print("=" * 40)
    
    print("Testing Derja command recognition...")
    print("This will test if Luca understands Tunisian commands")
    print()
    
    # Test commands
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
    
    print("Testing command recognition:")
    print()
    
    for i, command in enumerate(test_commands, 1):
        print(f"{i:2d}. Testing: '{command}'")
        
        # Detect intent
        intent = detect_derja_intent(command)
        print(f"    Detected: {intent.intent} (confidence: {intent.confidence:.2f})")
        
        # Get response
        response = get_personality_response(
            intent.intent,
            f"طيب، نعمل {intent.intent}",
            last_action=intent.intent,
            mood="friendly"
        )
        print(f"    Response: '{response}'")
        
        # Speak response
        print("    Speaking...")
        speak_naturally(response, {"mood": "friendly"})
        print("    ✅ Spoken")
        print()
        time.sleep(1)
    
    print("🎯 Voice command test completed!")

def main():
    """Main function for interactive testing."""
    print("🎤 Luca Tunisian Voice Interactive Test")
    print("=" * 50)
    print("Choose your test:")
    print("1. Voice Quality Test (with ratings)")
    print("2. Voice Commands Test")
    print("3. Both tests")
    print()
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            interactive_voice_test()
        elif choice == "2":
            test_voice_commands()
        elif choice == "3":
            interactive_voice_test()
            test_voice_commands()
        else:
            print("Invalid choice. Running voice quality test...")
            interactive_voice_test()
            
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    main()
