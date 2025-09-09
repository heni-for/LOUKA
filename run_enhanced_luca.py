#!/usr/bin/env python3
"""
Enhanced Luca Voice Assistant Launcher
Choose between different modes: GUI, Continuous Voice, or Command Line
"""

import sys
import os
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    parser = argparse.ArgumentParser(description="Luca AI Voice Assistant - Enhanced Siri-like Experience")
    parser.add_argument("mode", nargs="?", choices=["gui", "continuous", "voice", "cli"], 
                       default="gui", help="Mode to run Luca in")
    parser.add_argument("--language", "-l", choices=["en", "ar", "tn"], 
                       default="en", help="Language for voice recognition")
    parser.add_argument("--mic", "-m", type=int, help="Microphone device index")
    
    args = parser.parse_args()
    
    print("🎤 Luca AI Voice Assistant - Enhanced Edition")
    print("=" * 50)
    
    if args.mode == "gui":
        print("Starting GUI mode...")
        try:
            from assistant.gui import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"❌ GUI mode not available: {e}")
            print("Falling back to voice mode...")
            run_voice_mode(args)
    
    elif args.mode == "continuous":
        print("Starting continuous voice mode (Siri-like)...")
        try:
            from assistant.continuous_voice import main as continuous_main
            continuous_main()
        except ImportError as e:
            print(f"❌ Continuous mode not available: {e}")
            print("Falling back to voice mode...")
            run_voice_mode(args)
    
    elif args.mode == "voice":
        run_voice_mode(args)
    
    elif args.mode == "cli":
        print("Starting CLI mode...")
        try:
            from assistant.cli import main as cli_main
            cli_main()
        except ImportError as e:
            print(f"❌ CLI mode not available: {e}")
            print("Falling back to voice mode...")
            run_voice_mode(args)

def run_voice_mode(args):
    """Run voice mode with enhanced features."""
    print("Starting enhanced voice mode...")
    try:
        from assistant.voice import main as voice_main
        # Set language if specified
        if args.language:
            os.environ["DEFAULT_LANGUAGE"] = args.language
        voice_main()
    except ImportError as e:
        print(f"❌ Voice mode not available: {e}")
        print("Please check your dependencies and try again.")

def show_help():
    """Show help information."""
    print("""
🎤 Luca AI Voice Assistant - Enhanced Edition

MODES:
  gui         - Graphical user interface (default)
  continuous  - Continuous listening mode (Siri-like)
  voice       - Push-to-talk voice mode
  cli         - Command line interface

FEATURES:
  ✨ Multi-language support (English, Arabic, Tunisian)
  🎯 Smart command recognition
  📧 Email management
  🌤️  Weather information
  ⏰ Time and date
  😄 Jokes and quotes
  💬 Natural conversation with AI
  🎵 High-quality text-to-speech

EXAMPLES:
  python run_enhanced_luca.py                    # Start GUI
  python run_enhanced_luca.py continuous         # Siri-like mode
  python run_enhanced_luca.py voice --language ar # Arabic voice mode
  python run_enhanced_luca.py cli                # Command line

VOICE COMMANDS:
  "Hey Luca, what's the weather?"               # Weather
  "Hey Luca, tell me a joke"                    # Jokes
  "Hey Luca, what time is it?"                  # Time
  "Hey Luca, read my emails"                    # Email
  "Hey Luca, help me draft an email"            # Email drafting
  "Hey Luca, calculate 2 plus 2"                # Math
  "Hey Luca, define artificial intelligence"    # Definitions

For more help, visit: https://github.com/your-repo/luca
    """)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_help()
    main()
