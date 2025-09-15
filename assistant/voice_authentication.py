#!/usr/bin/env python3
"""
Voice Authentication System for Luca
Voice recognition and multi-user voice profiles
"""

import os
import json
import time
import numpy as np
import sounddevice as sd
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import librosa
import scipy.spatial.distance as distance
from sklearn.mixture import GaussianMixture
import pickle

@dataclass
class VoiceProfile:
    """Voice profile for a user."""
    user_id: str
    user_name: str
    voice_features: List[float]
    gmm_model: Optional[Any] = None
    created_at: float = 0.0
    last_used: float = 0.0
    confidence_threshold: float = 0.7
    is_active: bool = True

class VoiceAuthenticator:
    """Voice authentication system for multi-user support."""
    
    def __init__(self):
        self.voice_profiles = {}
        self.current_user = None
        self.voice_features_cache = {}
        self.profiles_file = "voice_profiles.json"
        self.models_dir = "voice_models"
        self._load_voice_profiles()
        self._ensure_models_dir()
    
    def _ensure_models_dir(self):
        """Ensure models directory exists."""
        Path(self.models_dir).mkdir(exist_ok=True)
    
    def _load_voice_profiles(self):
        """Load voice profiles from file."""
        try:
            if os.path.exists(self.profiles_file):
                with open(self.profiles_file, "r", encoding="utf-8") as f:
                    profiles_data = json.load(f)
                
                for profile_data in profiles_data:
                    profile = VoiceProfile(**profile_data)
                    # Load GMM model if exists
                    model_path = os.path.join(self.models_dir, f"{profile.user_id}_gmm.pkl")
                    if os.path.exists(model_path):
                        with open(model_path, "rb") as f:
                            profile.gmm_model = pickle.load(f)
                    
                    self.voice_profiles[profile.user_id] = profile
                
                print(f"✅ Loaded {len(self.voice_profiles)} voice profiles")
        except Exception as e:
            print(f"Error loading voice profiles: {e}")
    
    def _save_voice_profiles(self):
        """Save voice profiles to file."""
        try:
            profiles_data = []
            for profile in self.voice_profiles.values():
                profile_data = asdict(profile)
                # Don't save the GMM model in JSON
                profile_data["gmm_model"] = None
                profiles_data.append(profile_data)
            
            with open(self.profiles_file, "w", encoding="utf-8") as f:
                json.dump(profiles_data, f, ensure_ascii=False, indent=2)
            
            # Save GMM models separately
            for profile in self.voice_profiles.values():
                if profile.gmm_model:
                    model_path = os.path.join(self.models_dir, f"{profile.user_id}_gmm.pkl")
                    with open(model_path, "wb") as f:
                        pickle.dump(profile.gmm_model, f)
            
            print("✅ Voice profiles saved")
        except Exception as e:
            print(f"Error saving voice profiles: {e}")
    
    def extract_voice_features(self, audio_data: np.ndarray, sample_rate: int = 16000) -> List[float]:
        """Extract voice features from audio data."""
        try:
            # Extract MFCC features
            mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)
            
            # Extract spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate)
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sample_rate)
            zero_crossing_rate = librosa.feature.zero_crossing_rate(audio_data)
            
            # Extract rhythm features
            tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sample_rate)
            
            # Combine features
            features = []
            
            # MFCC statistics
            features.extend(np.mean(mfccs, axis=1))
            features.extend(np.std(mfccs, axis=1))
            
            # Spectral features
            features.extend(np.mean(spectral_centroids))
            features.extend(np.mean(spectral_rolloff))
            features.extend(np.mean(zero_crossing_rate))
            
            # Tempo
            features.append(tempo)
            
            # Additional features
            features.extend(self._extract_additional_features(audio_data, sample_rate))
            
            return features
            
        except Exception as e:
            print(f"Feature extraction error: {e}")
            return []
    
    def _extract_additional_features(self, audio_data: np.ndarray, sample_rate: int) -> List[float]:
        """Extract additional voice features."""
        try:
            # Pitch features
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sample_rate)
            pitch_mean = np.mean(pitches[pitches > 0])
            pitch_std = np.std(pitches[pitches > 0])
            
            # Energy features
            energy = librosa.feature.rms(y=audio_data)
            energy_mean = np.mean(energy)
            energy_std = np.std(energy)
            
            # Spectral features
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_data, sr=sample_rate)
            spectral_contrast = librosa.feature.spectral_contrast(y=audio_data, sr=sample_rate)
            
            return [
                pitch_mean if not np.isnan(pitch_mean) else 0,
                pitch_std if not np.isnan(pitch_std) else 0,
                energy_mean,
                energy_std,
                np.mean(spectral_bandwidth),
                np.mean(spectral_contrast)
            ]
        except Exception as e:
            print(f"Additional feature extraction error: {e}")
            return [0] * 6
    
    def create_voice_profile(self, user_id: str, user_name: str, audio_samples: List[np.ndarray], sample_rate: int = 16000) -> bool:
        """Create a new voice profile from audio samples."""
        try:
            if not audio_samples:
                print("❌ No audio samples provided")
                return False
            
            # Extract features from all samples
            all_features = []
            for audio_data in audio_samples:
                features = self.extract_voice_features(audio_data, sample_rate)
                if features:
                    all_features.append(features)
            
            if not all_features:
                print("❌ No valid features extracted")
                return False
            
            # Convert to numpy array
            features_array = np.array(all_features)
            
            # Train GMM model
            gmm = GaussianMixture(n_components=3, random_state=42)
            gmm.fit(features_array)
            
            # Calculate mean features
            mean_features = np.mean(features_array, axis=0).tolist()
            
            # Create voice profile
            profile = VoiceProfile(
                user_id=user_id,
                user_name=user_name,
                voice_features=mean_features,
                gmm_model=gmm,
                created_at=time.time(),
                last_used=time.time(),
                confidence_threshold=0.7,
                is_active=True
            )
            
            # Save profile
            self.voice_profiles[user_id] = profile
            self._save_voice_profiles()
            
            print(f"✅ Voice profile created for {user_name} ({user_id})")
            return True
            
        except Exception as e:
            print(f"Error creating voice profile: {e}")
            return False
    
    def authenticate_voice(self, audio_data: np.ndarray, sample_rate: int = 16000) -> Tuple[Optional[str], float]:
        """Authenticate voice against stored profiles."""
        try:
            if not self.voice_profiles:
                return None, 0.0
            
            # Extract features
            features = self.extract_voice_features(audio_data, sample_rate)
            if not features:
                return None, 0.0
            
            features_array = np.array(features).reshape(1, -1)
            
            best_match = None
            best_score = 0.0
            
            for user_id, profile in self.voice_profiles.items():
                if not profile.is_active or not profile.gmm_model:
                    continue
                
                try:
                    # Calculate log-likelihood
                    log_likelihood = profile.gmm_model.score(features_array)
                    
                    # Convert to probability (0-1)
                    score = min(1.0, max(0.0, (log_likelihood + 100) / 100))
                    
                    if score > best_score and score >= profile.confidence_threshold:
                        best_score = score
                        best_match = user_id
                
                except Exception as e:
                    print(f"Authentication error for {user_id}: {e}")
                    continue
            
            if best_match:
                # Update last used time
                self.voice_profiles[best_match].last_used = time.time()
                self._save_voice_profiles()
            
            return best_match, best_score
            
        except Exception as e:
            print(f"Voice authentication error: {e}")
            return None, 0.0
    
    def record_voice_sample(self, duration: float = 3.0, sample_rate: int = 16000) -> Optional[np.ndarray]:
        """Record a voice sample for training or authentication."""
        try:
            print(f"🎤 Recording voice sample for {duration} seconds...")
            print("Speak now...")
            
            # Record audio
            audio_data = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype=np.float32
            )
            sd.wait()  # Wait until recording is finished
            
            print("✅ Recording completed")
            return audio_data.flatten()
            
        except Exception as e:
            print(f"Recording error: {e}")
            return None
    
    def train_voice_profile(self, user_id: str, user_name: str, num_samples: int = 5) -> bool:
        """Train a voice profile with multiple samples."""
        try:
            print(f"🎤 Training voice profile for {user_name}")
            print(f"Please provide {num_samples} voice samples")
            
            audio_samples = []
            
            for i in range(num_samples):
                print(f"\nSample {i+1}/{num_samples}:")
                audio_data = self.record_voice_sample(duration=3.0)
                
                if audio_data is not None:
                    audio_samples.append(audio_data)
                    print("✅ Sample recorded")
                else:
                    print("❌ Sample recording failed")
            
            if len(audio_samples) >= 3:  # Minimum 3 samples
                success = self.create_voice_profile(user_id, user_name, audio_samples)
                if success:
                    print(f"✅ Voice profile training completed for {user_name}")
                    return True
                else:
                    print("❌ Voice profile training failed")
                    return False
            else:
                print("❌ Not enough valid samples")
                return False
                
        except Exception as e:
            print(f"Voice profile training error: {e}")
            return False
    
    def get_user_name(self, user_id: str) -> Optional[str]:
        """Get user name by ID."""
        profile = self.voice_profiles.get(user_id)
        return profile.user_name if profile else None
    
    def get_current_user(self) -> Optional[str]:
        """Get current authenticated user."""
        return self.current_user
    
    def set_current_user(self, user_id: str):
        """Set current user."""
        if user_id in self.voice_profiles:
            self.current_user = user_id
            print(f"✅ Current user set to: {self.voice_profiles[user_id].user_name}")
        else:
            print(f"❌ User {user_id} not found")
    
    def logout(self):
        """Logout current user."""
        if self.current_user:
            print(f"👋 Logged out: {self.voice_profiles[self.current_user].user_name}")
            self.current_user = None
        else:
            print("❌ No user logged in")
    
    def list_users(self) -> List[Dict[str, Any]]:
        """List all voice profiles."""
        users = []
        for profile in self.voice_profiles.values():
            users.append({
                "user_id": profile.user_id,
                "user_name": profile.user_name,
                "created_at": profile.created_at,
                "last_used": profile.last_used,
                "is_active": profile.is_active
            })
        return users
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a voice profile."""
        try:
            if user_id in self.voice_profiles:
                user_name = self.voice_profiles[user_id].user_name
                del self.voice_profiles[user_id]
                
                # Delete model file
                model_path = os.path.join(self.models_dir, f"{user_id}_gmm.pkl")
                if os.path.exists(model_path):
                    os.remove(model_path)
                
                self._save_voice_profiles()
                
                if self.current_user == user_id:
                    self.current_user = None
                
                print(f"✅ User {user_name} deleted")
                return True
            else:
                print(f"❌ User {user_id} not found")
                return False
                
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    def update_confidence_threshold(self, user_id: str, threshold: float) -> bool:
        """Update confidence threshold for a user."""
        try:
            if user_id in self.voice_profiles:
                self.voice_profiles[user_id].confidence_threshold = threshold
                self._save_voice_profiles()
                print(f"✅ Confidence threshold updated for {user_id}: {threshold}")
                return True
            else:
                print(f"❌ User {user_id} not found")
                return False
        except Exception as e:
            print(f"Error updating threshold: {e}")
            return False
    
    def get_authentication_status(self) -> Dict[str, Any]:
        """Get current authentication status."""
        return {
            "current_user": self.current_user,
            "user_name": self.get_user_name(self.current_user) if self.current_user else None,
            "total_users": len(self.voice_profiles),
            "active_users": sum(1 for p in self.voice_profiles.values() if p.is_active)
        }


# Global instance
voice_authenticator = VoiceAuthenticator()

def create_voice_profile(user_id: str, user_name: str, num_samples: int = 5) -> bool:
    """Create a voice profile."""
    return voice_authenticator.train_voice_profile(user_id, user_name, num_samples)

def authenticate_voice(audio_data: np.ndarray, sample_rate: int = 16000) -> Tuple[Optional[str], float]:
    """Authenticate voice."""
    return voice_authenticator.authenticate_voice(audio_data, sample_rate)

def record_voice_sample(duration: float = 3.0, sample_rate: int = 16000) -> Optional[np.ndarray]:
    """Record voice sample."""
    return voice_authenticator.record_voice_sample(duration, sample_rate)

def get_current_user() -> Optional[str]:
    """Get current user."""
    return voice_authenticator.get_current_user()

def set_current_user(user_id: str):
    """Set current user."""
    voice_authenticator.set_current_user(user_id)

def logout():
    """Logout current user."""
    voice_authenticator.logout()

def list_users() -> List[Dict[str, Any]]:
    """List all users."""
    return voice_authenticator.list_users()

def delete_user(user_id: str) -> bool:
    """Delete user."""
    return voice_authenticator.delete_user(user_id)

def get_authentication_status() -> Dict[str, Any]:
    """Get authentication status."""
    return voice_authenticator.get_authentication_status()
