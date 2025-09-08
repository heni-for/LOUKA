#!/usr/bin/env python3
"""
Setup multiple language models for Luca
"""

import os
import shutil
from pathlib import Path

def setup_multilang_models():
    """Setup multiple language models for Luca."""
    print("🌍 Setting up Multi-Language Models for Luca")
    print("=" * 50)
    
    # Create models directory
    models_dir = Path('vosk-models')
    models_dir.mkdir(exist_ok=True)
    
    # Check if we have the English model
    english_model_path = Path('vosk-model-en-us-0.22')
    if english_model_path.exists():
        print("✅ English model found")
        
        # Copy English model for different language configurations
        arabic_model_path = models_dir / 'vosk-model-ar-0.22'
        tunisian_model_path = models_dir / 'vosk-model-tn-0.22'
        
        if not arabic_model_path.exists():
            print("📁 Creating Arabic model directory...")
            shutil.copytree(english_model_path, arabic_model_path)
            print("✅ Arabic model directory created")
        
        if not tunisian_model_path.exists():
            print("📁 Creating Tunisian model directory...")
            shutil.copytree(english_model_path, tunisian_model_path)
            print("✅ Tunisian model directory created")
        
        print("\n🎉 Multi-language setup complete!")
        print("📁 Models are located in: vosk-models/")
        print("\n📝 Update your .env file with:")
        print("VOSK_MODEL_PATH=./vosk-model-en-us-0.22")
        print("ARABIC_MODEL_PATH=./vosk-models/vosk-model-ar-0.22")
        print("TUNISIAN_MODEL_PATH=./vosk-models/vosk-model-tn-0.22")
        
    else:
        print("❌ English model not found at vosk-model-en-us-0.22")
        print("Please download the English model first:")
        print("1. Go to https://alphacephei.com/vosk/models")
        print("2. Download vosk-model-en-us-0.22.zip")
        print("3. Extract it to the current directory")
        print("4. Run this script again")

if __name__ == "__main__":
    setup_multilang_models()
