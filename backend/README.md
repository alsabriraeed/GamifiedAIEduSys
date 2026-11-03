# AI Classroom Backend

AI-powered virtual classroom backend with local AI services (Ollama, Faster Whisper, Coqui TTS) for real-time student-teacher interaction.

## Features

- **RAG (Retrieval-Augmented Generation)**: Grounded answers from course materials
- **Local LLM**: Ollama with llama3.3:latest (no API costs)
- **Speech-to-Text**: Faster Whisper for student questions
- **Text-to-Speech**: Coqui TTS with viseme generation for lip sync
- **WebSocket Server**: Real-time communication with Unreal Engine
- **Knowledge Base**: Deep learning course with 12 slides + comprehensive materials

## Prerequisites

1. **Python 3.10+**
2. **Ollama** with llama3.3:latest model installed
   ```bash
   # Install Ollama: https://ollama.ai
   ollama pull llama3.3:latest
   ```

3. **CUDA** (optional, for GPU acceleration with Whisper and TTS)

## Installation

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config.py` or create `.env` file:

```env
# Ollama
OLLAMA_MODEL=llama3.3:latest
OLLAMA_BASE_URL=http://localhost:11434

# Whisper
WHISPER_MODEL=base  # tiny, base, small, medium, large
WHISPER_DEVICE=cpu  # or cuda
WHISPER_COMPUTE_TYPE=int8

# TTS
TTS_MODEL=tts_models/en/ljspeech/tacotron2-DDC

# RAG
CHUNK_SIZE=300
TOP_K_RETRIEVAL=5
```

## Running the Server

```bash
python main.py
```

Server starts at `http://localhost:8000`

- WebSocket endpoint: `ws://localhost:8000/ws`
- Health check: `http://localhost:8000`
- Get slides: `http://localhost:8000/slides`

## API Endpoints

### HTTP Endpoints

- `GET /` - Health check
- `GET /slides` - Get all slides metadata
- `GET /slides/{slide_id}` - Get specific slide
- `POST /refresh_knowledge_base` - Re-index knowledge base

### WebSocket Messages

**Student Question (Client → Server):**
```json
{
  "type": "student_question",
  "text": "What is backpropagation?",
  "current_slide_id": 5,
  "timestamp": 1234567890.123
}
```

**Teacher Response (Server → Client):**
```json
{
  "type": "teacher_response",
  "answer_text": "Backpropagation is...",
  "audio_data": "base64_encoded_wav",
  "visemes": [
    {"time": 0.0, "viseme": "sil"},
    {"time": 0.2, "viseme": "PP"},
    ...
  ],
  "actions": [
    {
      "type": "point_to",
      "target": "screen",
      "timing": "during_speech",
      "at_word": 15
    }
  ],
  "citations": [
    {"source": "slide_05", "confidence": 0.95}
  ],
  "confidence": 0.88,
  "timestamp": 1234567890.456
}
```

## Project Structure

```
backend/
├── main.py                  # FastAPI app with WebSocket
├── config.py                # Configuration
├── requirements.txt         # Dependencies
├── models/
│   └── messages.py          # Pydantic message schemas
├── services/
│   ├── stt_service.py       # Faster Whisper STT
│   ├── tts_service.py       # Coqui TTS with visemes
│   ├── llm_service.py       # Ollama LLM integration
│   └── rag_service.py       # ChromaDB RAG system
└── knowledge_base/
    ├── slides/
    │   ├── slides_index.json
    │   ├── slide_XX.png
    │   └── speaker_notes/
    ├── documents/
    │   ├── syllabus.md
    │   └── dl_fundamentals.md
    └── vector_store/         # ChromaDB data
```

## Development

### Testing the Backend

```python
# Test script
import json
import websocket

ws = websocket.create_connection("ws://localhost:8000/ws")

# Send question
question = {
    "type": "student_question",
    "text": "What is a neural network?",
    "current_slide_id": 1,
    "timestamp": 1234567890.0
}
ws.send(json.dumps(question))

# Receive response
response = json.loads(ws.recv())
print(response["answer_text"])
print(f"Confidence: {response['confidence']}")

ws.close()
```

### Refresh Knowledge Base

After updating slides or documents:

```bash
curl -X POST http://localhost:8000/refresh_knowledge_base
```

## Troubleshooting

**Ollama not connecting:**
```bash
# Check Ollama is running
ollama list
ollama serve  # If not running
```

**Whisper model download:**
First run will download Whisper models (~150MB for base model)

**TTS model download:**
First run will download Coqui TTS models (~100MB)

**ChromaDB errors:**
Delete `knowledge_base/vector_store/` and restart (will re-index)

## Performance Tips

- Use GPU: Set `WHISPER_DEVICE=cuda` and `WHISPER_COMPUTE_TYPE=float16`
- Smaller Whisper model: `WHISPER_MODEL=tiny` (faster, less accurate)
- Adjust chunk size: Larger = slower retrieval, better context

## Next Steps

1. **Unreal Engine Integration**: Connect MetaHuman to this WebSocket server
2. **Pixel Streaming**: Set up for browser-based student access
3. **Slide Generation**: Create visual slide images (currently placeholders)
4. **Advanced TTS**: Use phoneme-aligned visemes for better lip sync
5. **Streaming STT**: Implement real-time partial transcripts

## License

MIT
