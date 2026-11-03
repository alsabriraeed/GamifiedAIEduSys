import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "AI Classroom Backend"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent
    KNOWLEDGE_BASE_DIR: Path = BASE_DIR / "knowledge_base"
    SLIDES_DIR: Path = KNOWLEDGE_BASE_DIR / "slides"
    DOCUMENTS_DIR: Path = KNOWLEDGE_BASE_DIR / "documents"
    VECTOR_STORE_DIR: Path = KNOWLEDGE_BASE_DIR / "vector_store"
    
    # Ollama settings
    OLLAMA_MODEL: str = "llama3.2:latest"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_TEMPERATURE: float = 0.7
    OLLAMA_MAX_TOKENS: int = 512
    
    # STT settings (Faster Whisper)
    WHISPER_MODEL: str = "base"  # tiny, base, small, medium, large
    WHISPER_DEVICE: str = "cpu"  # cuda if GPU available
    WHISPER_COMPUTE_TYPE: str = "int8"  # int8, float16, float32
    
    # TTS settings (Coqui TTS)
    TTS_MODEL: str = "tts_models/en/ljspeech/tacotron2-DDC"
    TTS_VOCODER: str = "vocoder_models/en/ljspeech/hifigan_v2"
    TTS_SPEAKER_WAV: Optional[str] = None  # Path to voice clone sample if using
    
    # RAG settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 300
    CHUNK_OVERLAP: int = 50
    TOP_K_RETRIEVAL: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    
    # WebSocket settings
    WS_HEARTBEAT_INTERVAL: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create required directories
settings.VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
