"""
Text-to-Speech Service - Simplified fallback version
Using pyttsx3 for TTS (cross-platform, no dependencies)
Generates simple viseme approximations for lip sync
"""

import logging
import base64
import uuid
from pathlib import Path
import tempfile
from models.messages import Viseme
from typing import List, Tuple

logger = logging.getLogger(__name__)

# Viseme mapping (phoneme to viseme for MetaHuman)
PHONEME_TO_VISEME = {
    'sil': 'sil',
    'pp': 'PP', 'ff': 'FF', 'th': 'TH', 'ss': 'SS', 'sh': 'CH',
    'aa': 'aa', 'ee': 'E', 'oo': 'O', 'uu': 'U', 'ih': 'I'
}

class TTSService:
    def __init__(self):
        logger.info("Loading TTS service (fallback mode - pyttsx3)...")
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Speed
            self.engine.setProperty('volume', 0.9)
            logger.info("TTS engine initialized (pyttsx3)")
        except Exception as e:
            logger.warning(f"Could not initialize pyttsx3: {e}. Using mock TTS.")
            self.engine = None
        
        self.temp_dir = Path(tempfile.gettempdir()) / "ai_classroom_audio"
        self.temp_dir.mkdir(exist_ok=True)
    
    def generate_speech(self, text: str) -> Tuple[str, List[Viseme]]:
        """
        Generate speech audio and visemes
        
        Args:
            text: Text to synthesize
        
        Returns:
            (audio_base64, visemes_list)
        """
        try:
            if self.engine is None:
                # Mock mode - return empty audio
                logger.warning("Using mock TTS - no audio generated")
                visemes = self._generate_visemes(text, len(text.split()) * 0.3)
                return "", visemes
            
            # Generate unique filename
            audio_id = str(uuid.uuid4())
            audio_path = self.temp_dir / f"{audio_id}.wav"
            
            # Synthesize speech
            self.engine.save_to_file(text, str(audio_path))
            self.engine.runAndWait()
            
            # Read and encode as base64
            if audio_path.exists():
                with open(audio_path, 'rb') as f:
                    audio_bytes = f.read()
                audio_b64 = base64.b64encode(audio_bytes).decode()
                
                # Estimate duration (rough estimate: ~150 words/minute)
                word_count = len(text.split())
                duration = word_count / 2.5  # ~150 wpm = 2.5 words/second
                
                # Generate visemes
                visemes = self._generate_visemes(text, duration)
                
                logger.info(f"Generated speech for '{text[:50]}...' ({duration:.1f}s, {len(visemes)} visemes)")
                
                # Clean up temp file
                audio_path.unlink()
                
                return audio_b64, visemes
            else:
                logger.error(f"Audio file not created: {audio_path}")
                visemes = self._generate_visemes(text, len(text.split()) * 0.3)
                return "", visemes
            
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            visemes = self._generate_visemes(text, len(text.split()) * 0.3)
            return "", visemes
    
    def _generate_visemes(self, text: str, duration: float) -> List[Viseme]:
        """
        Generate viseme timeline from text (simplified approach)
        """
        words = text.split()
        if not words:
            return [Viseme(time=0.0, viseme="sil")]
        
        visemes = [Viseme(time=0.0, viseme="sil")]
        
        # Estimate duration per word
        avg_word_duration = duration / len(words) if words else 1.0
        
        current_time = 0.1
        for word in words:
            # Simple vowel/consonant detection for viseme selection
            word_lower = word.lower()
            
            # Add visemes based on simple heuristics
            if any(v in word_lower for v in ['oo', 'ou']):
                visemes.append(Viseme(time=current_time, viseme="U"))
            elif any(v in word_lower for v in ['ee', 'ea']):
                visemes.append(Viseme(time=current_time, viseme="E"))
            elif any(v in word_lower for v in ['aa', 'ah']):
                visemes.append(Viseme(time=current_time, viseme="aa"))
            elif word_lower[0] in ['m', 'p', 'b']:
                visemes.append(Viseme(time=current_time, viseme="PP"))
            elif word_lower[0] in ['f', 'v']:
                visemes.append(Viseme(time=current_time, viseme="FF"))
            else:
                visemes.append(Viseme(time=current_time, viseme="aa"))  # Default open
            
            current_time += avg_word_duration
            
            # Add brief neutral between words
            if current_time < duration - 0.1:
                visemes.append(Viseme(time=current_time - 0.05, viseme="sil"))
        
        # End with silence
        visemes.append(Viseme(time=duration, viseme="sil"))
        
        return visemes

# Singleton instance
tts_service = TTSService()

# Singleton instance
tts_service = TTSService()
