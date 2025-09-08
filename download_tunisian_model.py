#!/usr/bin/env python3
"""
Download Tunisian Arabic Vosk model
"""

import os
import requests
import zipfile
import shutil
from pathlib import Path

def download_file(url: str, filename: str) -> bool:
    """Download a file from URL."""
    try:
        print(f"📥 Downloading {filename}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Error downloading {filename}: {e}")
        return False

def extract_zip(zip_path: str, extract_to: str) -> bool:
    """Extract a zip file."""
    try:
        print(f"📦 Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✅ Extracted to {extract_to}")
        return True
    except Exception as e:
        print(f"❌ Error extracting {zip_path}: {e}")
        return False

def download_tunisian_model():
    """Download and setup Tunisian Arabic Vosk model."""
    print("🇹🇳 Tunisian Arabic Vosk Model Downloader")
    print("=" * 50)
    
    # Model URLs - Updated with correct Vosk model URLs
    models = {
        'arabic': {
            'url': 'https://alphacephei.com/vosk/models/vosk-model-ar-0.22.zip',
            'name': 'vosk-model-ar-0.22',
            'description': 'Arabic Vosk Model'
        },
        'tunisian': {
            'url': 'https://alphacephei.com/vosk/models/vosk-model-ar-0.22.zip',  # Using Arabic as base for now
            'name': 'vosk-model-tn-0.22',
            'description': 'Tunisian Arabic Vosk Model (based on Arabic)'
        }
    }
    
    # Alternative: Use Hugging Face models
    huggingface_models = {
        'tunisian_hf': {
            'url': 'https://huggingface.co/linagora/linto-asr-ar-tn-0.1/resolve/main/model.tar.gz',
            'name': 'linto-asr-ar-tn-0.1',
            'description': 'LinTO ASR Arabic Tunisia Model'
        }
    }
    
    # Create models directory
    models_dir = Path('vosk-models')
    models_dir.mkdir(exist_ok=True)
    
    for model_key, model_info in models.items():
        model_dir = models_dir / model_info['name']
        
        if model_dir.exists():
            print(f"✅ {model_info['description']} already exists")
            continue
        
        # Download model
        zip_filename = f"{model_info['name']}.zip"
        zip_path = models_dir / zip_filename
        
        if not download_file(model_info['url'], str(zip_path)):
            continue
        
        # Extract model
        if not extract_zip(str(zip_path), str(models_dir)):
            continue
        
        # Rename if needed
        if model_key == 'tunisian':
            extracted_dir = models_dir / 'vosk-model-ar-0.22'
            if extracted_dir.exists():
                extracted_dir.rename(model_dir)
                print(f"✅ Renamed to {model_info['name']}")
        
        # Clean up zip file
        try:
            os.remove(zip_path)
            print(f"🗑️ Cleaned up {zip_filename}")
        except:
            pass
    
    print("\n🎉 Model download complete!")
    print("📁 Models are located in: vosk-models/")
    print("\n📝 To use these models, update your .env file:")
    print("VOSK_MODEL_PATH=./vosk-models/vosk-model-ar-0.22")
    print("TUNISIAN_MODEL_PATH=./vosk-models/vosk-model-tn-0.22")

if __name__ == "__main__":
    download_tunisian_model()
