"""
Main FastAPI Application
WebSocket server for real-time communication with Unreal Engine
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging
import asyncio
import time
import json
from pathlib import Path

from config import settings
from models.messages import (
    StudentQuestion, TeacherResponse, ErrorMessage, MessageType,
    ActionType, ActionTiming, TeacherAction
)
from services.stt_service import stt_service
from services.llm_service import llm_service
from services.rag_service import rag_service
from services.tts_service import tts_service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# CORS middleware for browser clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for web interface
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/ui", StaticFiles(directory=static_dir, html=True), name="static")

# Active WebSocket connections
active_connections = []

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info("=" * 60)
    logger.info(f"Ollama Model: {settings.OLLAMA_MODEL}")
    logger.info(f"Whisper Model: {settings.WHISPER_MODEL}")
    logger.info(f"Knowledge Base: {settings.KNOWLEDGE_BASE_DIR}")
    logger.info("=" * 60)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "app": settings.APP_NAME,
        "ollama_model": settings.OLLAMA_MODEL,
        "whisper_model": settings.WHISPER_MODEL
    }

@app.get("/slides")
async def get_slides():
    """Get all slides metadata"""
    slides_index_path = settings.SLIDES_DIR / "slides_index.json"
    if slides_index_path.exists():
        with open(slides_index_path) as f:
            return json.load(f)
    return {"error": "Slides not found"}

@app.get("/slides/{slide_id}")
async def get_slide(slide_id: int):
    """Get specific slide data"""
    slides_index_path = settings.SLIDES_DIR / "slides_index.json"
    if slides_index_path.exists():
        with open(slides_index_path) as f:
            data = json.load(f)
            for slide in data.get("slides", []):
                if slide["id"] == slide_id:
                    return slide
    return {"error": f"Slide {slide_id} not found"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for Unreal Engine communication
    """
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"WebSocket connected (total: {len(active_connections)})")
    
    try:
        while True:
            # Receive message from client (Unreal)
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message_type = message_data.get("type")
            
            logger.info(f"Received message type: {message_type}")
            
            if message_type == MessageType.STUDENT_QUESTION:
                # Handle student question
                await handle_student_question(websocket, message_data)
            
            elif message_type == MessageType.HEARTBEAT:
                # Respond to heartbeat
                await websocket.send_json({
                    "type": MessageType.HEARTBEAT,
                    "timestamp": time.time()
                })
            
            else:
                logger.warning(f"Unknown message type: {message_type}")
    
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected (total: {len(active_connections)})")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        active_connections.remove(websocket)

async def handle_student_question(websocket: WebSocket, message_data: dict):
    """Process student question and generate teacher response"""
    
    try:
        # Parse student question
        question_msg = StudentQuestion(**message_data)
        
        # Get question text
        if question_msg.text:
            question_text = question_msg.text
        elif question_msg.audio_data:
            # Transcribe audio
            logger.info("Transcribing audio...")
            stt_result = await asyncio.to_thread(
                stt_service.transcribe,
                question_msg.audio_data
            )
            question_text = stt_result["text"]
            logger.info(f"Transcribed: '{question_text}'")
        else:
            raise ValueError("No text or audio provided")
        
        if not question_text:
            raise ValueError("Empty question")
        
        # Get slide context
        slides_index_path = settings.SLIDES_DIR / "slides_index.json"
        slide_title = "Unknown"
        if slides_index_path.exists():
            with open(slides_index_path) as f:
                data = json.load(f)
                for slide in data.get("slides", []):
                    if slide["id"] == question_msg.current_slide_id:
                        slide_title = slide["title"]
                        break
        
        # RAG: Retrieve relevant context
        logger.info("Retrieving context...")
        retrieved_context = await asyncio.to_thread(
            rag_service.retrieve,
            question_text,
            question_msg.current_slide_id
        )
        
        # LLM: Generate answer
        logger.info("Generating answer...")
        llm_response = await asyncio.to_thread(
            llm_service.generate_answer,
            question_text,
            retrieved_context,
            question_msg.current_slide_id,
            slide_title
        )
        
        # TTS: Generate speech and visemes
        logger.info("Generating speech...")
        audio_b64, visemes = await asyncio.to_thread(
            tts_service.generate_speech,
            llm_response["answer_text"]
        )
        
        # Build response
        response = TeacherResponse(
            answer_text=llm_response["answer_text"],
            audio_data=audio_b64,
            visemes=visemes,
            actions=llm_response["actions"],
            citations=llm_response["citations"],
            confidence=llm_response["confidence"],
            timestamp=time.time()
        )
        
        # Send response
        await websocket.send_json(response.dict())
        logger.info(f"Sent response ({len(audio_b64)} bytes audio, {len(visemes)} visemes)")
    
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        
        # Send error response
        error_response = ErrorMessage(
            error_code="PROCESSING_ERROR",
            error_message=str(e),
            timestamp=time.time()
        )
        await websocket.send_json(error_response.dict())

@app.post("/refresh_knowledge_base")
async def refresh_knowledge_base():
    """Refresh knowledge base (useful after content updates)"""
    try:
        await asyncio.to_thread(rag_service.refresh_knowledge_base)
        return {"status": "success", "message": "Knowledge base refreshed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
