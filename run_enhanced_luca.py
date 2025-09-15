#!/usr/bin/env python3
"""
Enhanced Luca Voice Assistant Launcher
Integrates all new features: Derja NLU, Memory, Enhanced TTS, etc.
"""

import sys
import argparse
import time
from pathlib import Path

# Add assistant module to path
sys.path.insert(0, str(Path(__file__).parent))

from assistant.enhanced_voice import EnhancedVoiceRecognizer, find_best_microphone
from assistant.derja_nlu import detect_derja_intent, get_derja_intent_examples
from assistant.action_mapper import execute_derja_action, get_conversation_context
from assistant.derja_tts import speak_derja, speak_derja_with_emotion
from assistant.memory_manager import get_memory_manager
from assistant.enhanced_gui import main as gui_main

def test_derja_nlu():
    """Test Derja NLU with sample commands."""
    print("🧪 Testing Derja NLU...")
    
    test_commands = [
        "أهلا وينك",
        "أعطيني الإيميلات",
        "حضرلي رد",
        "أبعت الرد",
        "أقرا الإيميل",
        "شنادي الوقت",
        "شنادي الطقس",
        "أعطني نكتة",
        "أحسب لي 2 زائد 2"
    ]
    
    for command in test_commands:
        print(f"\n📝 Testing: '{command}'")
        intent = detect_derja_intent(command)
        print(f"   Intent: {intent.intent}")
        print(f"   Confidence: {intent.confidence:.2f}")
        print(f"   Entities: {intent.entities}")
        
        # Test action execution
        try:
            response = execute_derja_action(intent)
            print(f"   Response: {response[:100]}...")
        except Exception as e:
            print(f"   Error: {e}")

def test_voice_recognition(language="en"):
    """Test voice recognition."""
    print(f"🎤 Testing voice recognition in {language}...")
    
    mic_index = find_best_microphone()
    if mic_index is None:
        print("❌ No microphone found")
        return
    
    recognizer = EnhancedVoiceRecognizer(
        input_device=mic_index,
        language=language
    )
    
    if not recognizer.start():
        print("❌ Failed to start voice recognizer")
        return
    
    print("✅ Voice recognizer started. Say something...")
    
    try:
        for i in range(3):  # Test 3 commands
            print(f"\n🎯 Test {i+1}/3:")
            intent = recognizer.listen_for_command(timeout=10.0)
            
            if intent:
                print(f"   Recognized: '{intent.original_text}'")
                print(f"   Intent: {intent.intent} (confidence: {intent.confidence:.2f})")
                
                # Process command
                response = recognizer.process_voice_command(intent)
                print(f"   Response: {response[:100]}...")
                
                # Speak response
                recognizer.speak_response(response)
            else:
                print("   No command recognized")
    
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    finally:
        recognizer.stop()

def test_memory_system():
    """Test memory management system."""
    print("🧠 Testing memory system...")
    
    memory_manager = get_memory_manager()
    
    # Add some test memories
    memory_manager.add_conversation_memory(
        "أعطيني الإيميلات",
        "لقيت 5 إيميلات في الإنبوكس",
        "fetch_email"
    )
    
    memory_manager.add_email_memory({
        "subject": "Test Email",
        "sender": "test@example.com",
        "body": "This is a test email"
    })
    
    # Test memory retrieval
    recent_conversations = memory_manager.get_recent_conversations(5)
    print(f"✅ Recent conversations: {len(recent_conversations)}")
    
    recent_emails = memory_manager.get_recent_emails(5)
    print(f"✅ Recent emails: {len(recent_emails)}")
    
    # Test context summary
    context = memory_manager.get_context_summary()
    print(f"✅ Context summary:\n{context}")

def test_tts_system():
    """Test TTS system."""
    print("🔊 Testing TTS system...")
    
    test_texts = [
        "أهلا وسهلا! أنا لوكا، المساعد الذكي",
        "لقيت 5 إيميلات في الإنبوكس",
        "حضرتلك رد على الإيميل",
        "تم إرسال الرد بنجاح!"
    ]
    
    for text in test_texts:
        print(f"🎤 Speaking: '{text}'")
        speak_derja_with_emotion(text, "happy")
        time.sleep(1)

def show_intent_examples():
    """Show examples of supported intents."""
    print("📚 Supported Derja Intents and Examples:")
    print("=" * 50)
    
    examples = get_derja_intent_examples()
    
    for intent, intent_examples in examples.items():
        print(f"\n🎯 {intent.upper()}:")
        for example in intent_examples:
            print(f"   • {example}")

def run_gui():
    """Run the enhanced GUI."""
    print("🖥️ Starting Enhanced Luca GUI...")
    gui_main()

def run_voice_mode(language="en"):
    """Run voice-only mode."""
    print(f"🎤 Starting voice mode in {language}...")
    
    mic_index = find_best_microphone()
    if mic_index is None:
        print("❌ No microphone found")
        return
    
    recognizer = EnhancedVoiceRecognizer(
        input_device=mic_index,
        language=language
    )
    
    if not recognizer.start():
        print("❌ Failed to start voice recognizer")
        return
    
    print("✅ Voice recognizer started")
    print("Press 'q' to quit, 'l' to stop current speech")
    
    try:
        recognizer.continuous_listen()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        recognizer.stop()

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Enhanced Luca Voice Assistant")
    parser.add_argument("mode", choices=["gui", "voice", "test", "examples"], 
                       help="Mode to run")
    parser.add_argument("--language", "-l", choices=["en", "ar", "tn"], 
                       default="en", help="Language for voice recognition")
    parser.add_argument("--test-component", "-t", 
                       choices=["nlu", "voice", "memory", "tts", "all"],
                       help="Test specific component")
    
    args = parser.parse_args()
    
    print("🎤 Enhanced Luca Voice Assistant")
    print("=" * 40)
    
    if args.mode == "gui":
        run_gui()
    elif args.mode == "voice":
        run_voice_mode(args.language)
    elif args.mode == "test":
        if args.test_component == "nlu":
            test_derja_nlu()
        elif args.test_component == "voice":
            test_voice_recognition(args.language)
        elif args.test_component == "memory":
            test_memory_system()
        elif args.test_component == "tts":
            test_tts_system()
        elif args.test_component == "all":
            test_derja_nlu()
            test_memory_system()
            test_tts_system()
            test_voice_recognition(args.language)
        else:
            print("Please specify --test-component")
    elif args.mode == "examples":
        show_intent_examples()

if __name__ == "__main__":
    main()