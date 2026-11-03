"""
Speech-to-Text Service using Faster Whisper
Handles audio transcription from student microphone input
"""

from faster_whisper import WhisperModel
from config import settings
import logging
import base64
import io
import soundfile as sf
import numpy as np

logger = logging.getLogger(__name__)

class STTService:
    def __init__(self):
        logger.info(f"Loading Whisper model: {settings.WHISPER_MODEL}")
        self.model = WhisperModel(
            settings.WHISPER_MODEL,
            device=settings.WHISPER_DEVICE,
            compute_type=settings.WHISPER_COMPUTE_TYPE
        )
        logger.info("Whisper model loaded successfully")
    
    def transcribe(self, audio_data: str) -> dict:
        """
        Transcribe audio from base64 encoded data
        
        Args:
            audio_data: Base64 encoded audio (WAV, MP3, etc.)
        
        Returns:
            {
                "text": str,
                "language": str,
                "confidence": float
            }
        """
        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_data)
            
            # Load audio using soundfile
            audio_array, sample_rate = sf.read(io.BytesIO(audio_bytes))
            
            # Convert to float32 mono if needed
            if audio_array.ndim > 1:
                audio_array = audio_array.mean(axis=1)
            audio_array = audio_array.astype(np.float32)
            
            # Transcribe
            segments, info = self.model.transcribe(
                audio_array,
                beam_size=5,
                language="en",
                condition_on_previous_text=False
            )
            
            # Collect all segments
            text_parts = []
            total_confidence = 0
            segment_count = 0
            
            for segment in segments:
                text_parts.append(segment.text)
                if hasattr(segment, 'avg_logprob'):
                    total_confidence += np.exp(segment.avg_logprob)
                    segment_count += 1
            
            transcribed_text = " ".join(text_parts).strip()
            avg_confidence = total_confidence / max(segment_count, 1)
            
            logger.info(f"Transcribed: '{transcribed_text[:50]}...' (confidence: {avg_confidence:.2f})")
            
            return {
                "text": transcribed_text,
                "language": info.language,
                "confidence": float(avg_confidence)
            }
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return {
                "text": "",
                "language": "en",
                "confidence": 0.0
            }
    
    def transcribe_stream(self, audio_chunks: list) -> str:
        """
        Transcribe streaming audio chunks
        (For future implementation with real-time streaming)
        """
        # Concatenate chunks
        combined_audio = b"".join(audio_chunks)
        audio_b64 = base64.b64encode(combined_audio).decode()
        result = self.transcribe(audio_b64)
        return result["text"]

# Singleton instance
stt_service = STTService()
