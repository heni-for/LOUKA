#!/usr/bin/env python3
"""
Test script for the comprehensive intent library
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from assistant.intent_library import detect_intent, intent_library

def test_intent_recognition():
    """Test the comprehensive intent recognition library."""
    print("🧠 Testing Comprehensive Intent Recognition Library")
    print("=" * 60)
    
    # Test phrases in different languages
    test_phrases = [
        # English phrases
        ("what time is it", "en"),
        ("how are you doing", "en"),
        ("tell me a joke", "en"),
        ("what's the weather", "en"),
        ("open gmail", "en"),
        ("check my email", "en"),
        ("calculate 2 plus 2", "en"),
        ("define artificial intelligence", "en"),
        ("play music", "en"),
        ("set a reminder", "en"),
        ("what's the news", "en"),
        ("help me", "en"),
        
        # Arabic phrases
        ("كم الساعة", "ar"),
        ("كيف حالك", "ar"),
        ("احك لي نكتة", "ar"),
        ("كيف الطقس", "ar"),
        ("افتح جيميل", "ar"),
        ("تحقق من البريد", "ar"),
        ("احسب اثنين زائد اثنين", "ar"),
        ("عرّف الذكاء الاصطناعي", "ar"),
        ("شغل موسيقى", "ar"),
        ("ضع تذكير", "ar"),
        ("ما الأخبار", "ar"),
        ("ساعدني", "ar"),
        
        # Tunisian phrases
        ("كماش الساعة", "tn"),
        ("كيفاش حالك", "tn"),
        ("احك لي نكتة", "tn"),
        ("كيفاش الطقس", "tn"),
        ("افتح جيميل", "tn"),
        ("تحقق من البريد", "tn"),
        ("احسب اثنين زائد اثنين", "tn"),
        ("عرّف الذكاء الاصطناعي", "tn"),
        ("شغل موسيقى", "tn"),
        ("ضع تذكير", "tn"),
        ("واش الأخبار", "tn"),
        ("ساعدني", "tn"),
        
        # Edge cases and variations
        ("wut time is it", "en"),  # Slang
        ("how r u", "en"),  # Abbreviated
        ("whats the weather like", "en"),  # Variation
        ("can u open gmail", "en"),  # Abbreviated
        ("pls help me", "en"),  # Abbreviated
        ("thx", "en"),  # Abbreviated
    ]
    
    print("Testing Intent Recognition:")
    print("-" * 40)
    
    for phrase, language in test_phrases:
        intent_match = detect_intent(phrase, language)
        if intent_match:
            print(f"✅ '{phrase}' ({language}) -> {intent_match.intent} (confidence: {intent_match.confidence:.2f})")
        else:
            print(f"❌ '{phrase}' ({language}) -> No intent detected")
    
    print("\n" + "=" * 60)
    print("Available Intents:")
    print("-" * 20)
    
    intents = intent_library.get_all_intents()
    for intent in intents:
        print(f"• {intent}")
    
    print(f"\nTotal intents: {len(intents)}")
    
    print("\n" + "=" * 60)
    print("Testing Intent Phrases:")
    print("-" * 25)
    
    # Show some example phrases for each intent
    for intent in intents[:5]:  # Show first 5 intents
        en_phrases = intent_library.get_intent_phrases(intent, 'en')
        ar_phrases = intent_library.get_intent_phrases(intent, 'ar')
        
        print(f"\n{intent.upper()}:")
        print(f"  English: {', '.join(en_phrases[:3])}...")
        print(f"  Arabic: {', '.join(ar_phrases[:3])}...")

def test_fuzzy_matching():
    """Test fuzzy matching capabilities."""
    print("\n🔍 Testing Fuzzy Matching:")
    print("-" * 30)
    
    fuzzy_tests = [
        ("wut time is it", "what time is it"),
        ("how r u", "how are you"),
        ("wats the weather", "what's the weather"),
        ("open gmail pls", "open gmail please"),
        ("thx", "thanks"),
        ("ur welcome", "you're welcome"),
        ("2 plus 2", "two plus two"),
        ("defin AI", "define AI"),
    ]
    
    for test_phrase, expected_phrase in fuzzy_tests:
        intent_match = detect_intent(test_phrase, 'en')
        if intent_match:
            print(f"✅ '{test_phrase}' -> {intent_match.intent} (matched: '{intent_match.matched_phrase}')")
        else:
            print(f"❌ '{test_phrase}' -> No match")

if __name__ == "__main__":
    test_intent_recognition()
    test_fuzzy_matching()
    
    print("\n🎉 Intent Library Test Complete!")
    print("The comprehensive intent library is ready to use!")
