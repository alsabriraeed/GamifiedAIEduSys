# AI Classroom System - Complete Implementation

This project implements an AI-powered virtual classroom with:
- **Unreal Engine 5** with MetaHuman teacher
- **Pixel Streaming** for browser-based student access
- **Local AI services** (Ollama, Whisper, Coqui TTS)
- **RAG system** with deep learning course content

## Project Structure

```
GamifiedAIEduSys/
├── backend/                    # Python AI services (COMPLETED)
│   ├── main.py                # FastAPI WebSocket server
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Dependencies
│   ├── services/              # AI services
│   │   ├── stt_service.py    # Faster Whisper STT
│   │   ├── tts_service.py    # Coqui TTS with visemes
│   │   ├── llm_service.py    # Ollama LLM
│   │   └── rag_service.py    # ChromaDB RAG
│   ├── models/
│   │   └── messages.py       # WebSocket message schemas
│   └── knowledge_base/
│       ├── slides/           # 12 deep learning slides + notes
│       └── documents/        # Syllabus + fundamentals guide
│
├── unreal_project/            # TO BE CREATED
│   └── AIClassroom/
│       ├── Content/
│       │   ├── Classroom/    # Scene, meshes, materials
│       │   ├── Teacher/      # MetaHuman + animations
│       │   ├── Slides/       # Slide display system
│       │   └── Communication/# WebSocket client
│       └── Plugins/
│           └── PixelStreaming/
│
└── pixel_streaming/           # TO BE CREATED
    ├── signaling_server/     # Node.js WebRTC server
    └── web_client/           # Browser interface
```

## What's Completed ✅

### Backend AI Services (Fully Functional)
- ✅ FastAPI WebSocket server
- ✅ RAG system with ChromaDB (vector search + retrieval)
- ✅ Ollama integration (llama3.3:latest)
- ✅ Faster Whisper STT (speech-to-text)
- ✅ Coqui TTS with viseme generation
- ✅ Message schemas for Unreal communication

### Course Content
- ✅ 12 slide outlines with metadata
- ✅ Detailed speaker notes for all slides
- ✅ Course syllabus
- ✅ Comprehensive deep learning reference document
- ✅ 2 generated slide images (slides 1-2)
- ⚠️ Slides 3-12 images need generation (use slide generator script)

## Quick Start

### 1. Set Up Backend

```bash
cd backend

# Install Ollama
# Visit https://ollama.ai and install for your system
ollama pull llama3.3:latest

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Server runs at `http://localhost:8000`
- WebSocket: `ws://localhost:8000/ws`
- API docs: `http://localhost:8000/docs`

### 2. Test Backend

```python
# test_backend.py
import websocket
import json
import time

ws = websocket.create_connection("ws://localhost:8000/ws")

question = {
    "type": "student_question",
    "text": "What is a neural network?",
    "current_slide_id": 1,
    "timestamp": time.time()
}

ws.send(json.dumps(question))
response = json.loads(ws.recv())

print(f"Answer: {response['answer_text']}")
print(f"Confidence: {response['confidence']}")
print(f"Citations: {len(response['citations'])}")
print(f"Audio bytes: {len(response['audio_data'])}")
print(f"Visemes: {len(response['visemes'])}")

ws.close()
```

## Next Steps (Unreal Engine Setup)

### Option 1: Full Unreal Implementation (Recommended)

1. **Install Unreal Engine 5.3+**
   - Download from Epic Games Launcher
   - Enable Pixel Streaming plugin

2. **Create MetaHuman**
   - Use MetaHuman Creator (free)
   - Import into Unreal project
   - Set up lip sync with visemes

3. **Build Classroom Scene**
   - Create room environment
   - Position MetaHuman at podium
   - Add screen mesh for slides

4. **Implement WebSocket Client (Blueprint or C++)**
   ```cpp
   // Connect to backend
   WebSocket->Connect("ws://localhost:8000/ws");
   
   // Send student question
   FString message = "{\"type\":\"student_question\",\"text\":\"...\"}";
   WebSocket->Send(message);
   
   // Receive response and parse
   // - Play audio
   // - Apply visemes to MetaHuman face rig
   // - Execute actions (goto_slide, point_to, etc.)
   ```

5. **Pixel Streaming Setup**
   - Configure signaling server (included with Unreal)
   - Build web client interface
   - Add microphone capture in browser

### Option 2: Simplified Prototype (Faster)

Use the backend as-is with a simple web interface:

1. **Web-based prototype** (no Unreal needed):
   - Build React/Vue app
   - Connect to WebSocket
   - Display slides as images
   - Use browser mic for questions
   - Play TTS audio responses
   - Show avatar as 2D animated character or video

2. **Test full AI pipeline without 3D**

## System Architecture

```
┌─────────────────┐
│  Student Browser│
│  (Pixel Stream) │
└────────┬────────┘
         │ WebRTC video + audio
         ↓
┌─────────────────┐
│ Unreal Engine   │
│ (MetaHuman)     │◄────── Renders classroom
│                 │        Animates teacher
└────────┬────────┘        Displays slides
         │
         │ WebSocket (student questions)
         ↓
┌─────────────────┐
│ Python Backend  │
│ ┌─────────────┐ │
│ │ STT (Whisper)│ │◄────── Transcribes speech
│ └──────┬───────┘ │
│        ↓         │
│ ┌─────────────┐ │
│ │ RAG (Chroma) │ │◄────── Retrieves context
│ └──────┬───────┘ │
│        ↓         │
│ ┌─────────────┐ │
│ │ LLM (Ollama) │ │◄────── Generates answer
│ └──────┬───────┘ │
│        ↓         │
 │ ┌─────────────┐ │
│ │ TTS (Coqui)  │ │◄────── Synthesizes speech
│ └──────┬───────┘ │                 + visemes
└────────┼────────┘
         │
         └────► Returns to Unreal
```

## Technical Documentation

### Backend API

**Full documentation**: See `backend/README.md`

**WebSocket Message Format**:
- Student → Backend: `StudentQuestion` (text/audio + slide context)
- Backend → Student: `TeacherResponse` (answer + audio + visemes + actions)

**Actions** MetaHuman can perform:
- `goto_slide`: Navigate to specific slide
- `point_to`: Point at screen/object
- `highlight`: Highlight slide region
- `pause`: Pause for thinking time

### Course Content

**Slides** (12 total):
1. Welcome to Deep Learning
2. Neural Networks Basics
3. Building Multi-Layer Networks
4. Loss Functions
5. Backpropagation
6. Gradient Descent
7. Convolutional Neural Networks
8. Recurrent Neural Networks
9. Attention Mechanisms
10. Transformers
11. Regularization Techniques
12. Best Practices & Next Steps

Each slide has:
- Title + bullet points
- Detailed speaker notes (30-60 second scripts)
- Keywords for RAG
- Common Q&A scenarios

## Deployment Options

### Local Development
- Run backend locally
- Run Unreal locally
- Students connect via LAN (`http://192.168.x.x`)

### Remote Access (via Tunnel)
```bash
# Use ngrok or Cloudflare Tunnel
ngrok http 8000  # For backend
# Configure Pixel Streaming URL to point to ngrok
```

### Production Cloud (Not Recommended for Cost)
- Deploy Unreal to AWS/Azure with GPU instances
- $$$ expensive ($1-3/hour per instance)
- Only for large-scale deployment

## Performance Notes

**Backend Requirements**:
- CPU: 4+ cores
- RAM: 8GB minimum (16GB recommended)
- Storage: 2GB for models

**Unreal Requirements**:
- GPU: NVIDIA GTX 1060 or better
- RAM: 16GB minimum
- Storage: 50GB (Unreal + MetaHuman + assets)

**Latency Targets**:
- STT: <2 seconds
- RAG retrieval: <0.5 seconds
- LLM generation: <3 seconds (Ollama on CPU)
- TTS: <2 seconds
- **Total: ~5-7 seconds** (question → answer)

GPU acceleration reduces this to ~2-3 seconds total.

## Troubleshooting

**Backend won't start**:
```bash
# Check Ollama is running
ollama list
ollama serve

# Check Python dependencies
pip install -r requirements.txt
```

**Low LLM quality**:
- Try larger model: `ollama pull llama3:70b`
- Adjust temperature in `config.py`
- Review RAG retrieval quality

**Slow TTS**:
- Use GPU: Install CUDA-enabled torch
- Use faster model (quality tradeoff)

## Resources

- **Unreal Engine**: https://www.unrealengine.com
- **MetaHuman Creator**: https://www.unrealengine.com/metahuman
- **Pixel Streaming Docs**: https://docs.unrealengine.com/5.3/en-US/pixel-streaming-in-unreal-engine/
- **Ollama**: https://ollama.ai
- **Faster Whisper**: https://github.com/guillaumekln/faster-whisper
- **Coqui TTS**: https://github.com/coqui-ai/TTS

## License

MIT - Feel free to use for educational purposes

## Credits

- Deep Learning course content: Generated for demonstration
- Architecture inspired by modern AI classroom research
- Built with: FastAPI, Ollama, ChromaDB, Faster Whisper, Coqui TTS
