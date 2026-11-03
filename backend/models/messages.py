from pydantic import BaseModel
from typing import List, Dict, Optional, Literal
from enum import Enum

# ============= Message Types =============

class MessageType(str, Enum):
    STUDENT_QUESTION = "student_question"
    TEACHER_RESPONSE = "teacher_response"
    LECTURE_SEGMENT = "lecture_segment"
    ERROR = "error"
    HEARTBEAT = "heartbeat"

# ============= Student Messages =============

class StudentQuestion(BaseModel):
    """Message from student asking a question"""
    type: Literal[MessageType.STUDENT_QUESTION] = MessageType.STUDENT_QUESTION
    audio_data: Optional[str] = None  # Base64 encoded audio
    text: Optional[str] = None  # Transcribed or typed text
    current_slide_id: int
    timestamp: float

# ============= Teacher Response =============

class ActionType(str, Enum):
    GOTO_SLIDE = "goto_slide"
    POINT_TO = "point_to"
    HIGHLIGHT = "highlight"
    PAUSE = "pause"

class ActionTiming(str, Enum):
    BEFORE_SPEECH = "before_speech"
    DURING_SPEECH = "during_speech"
    AFTER_SPEECH = "after_speech"

class TeacherAction(BaseModel):
    """Action for MetaHuman to perform"""
    type: ActionType
    timing: ActionTiming = ActionTiming.DURING_SPEECH
    at_word: Optional[int] = None  # Word index for during_speech timing
    
    # Action-specific parameters
    slide_id: Optional[int] = None  # For goto_slide
    target: Optional[str] = None  # For point_to (e.g., "screen", "student")
    region: Optional[str] = None  # For highlight (e.g., "top_right")

class Viseme(BaseModel):
    """Viseme for lip sync"""
    time: float  # Timestamp in seconds
    viseme: str  # Viseme name (e.g., "PP", "sil", "aa")

class Citation(BaseModel):
    """Source citation for answer"""
    source: str  # Slide ID or document name
    confidence: float
    snippet: Optional[str] = None

class TeacherResponse(BaseModel):
    """Response from AI teacher"""
    type: Literal[MessageType.TEACHER_RESPONSE] = MessageType.TEACHER_RESPONSE
    answer_text: str
    audio_url: Optional[str] = None  # URL to generated TTS audio
    audio_data: Optional[str] = None  # Or base64 encoded audio
    visemes: List[Viseme] = []
    actions: List[TeacherAction] = []
    citations: List[Citation] = []
    confidence: float  # Overall confidence in answer
    timestamp: float

# ============= Lecture Mode =============

class LectureSegmentType(str, Enum):
    SUMMARY = "summary"
    EXPLANATION = "explanation"
    EXAMPLE = "example"
    TRANSITION = "transition"

class LectureSegment(BaseModel):
    """Single segment of a lecture"""
    type: LectureSegmentType
    text: str
    audio_url: Optional[str] = None
    audio_data: Optional[str] = None
    visemes: List[Viseme] = []

class LectureMessage(BaseModel):
    """Full lecture for a slide"""
    type: Literal[MessageType.LECTURE_SEGMENT] = MessageType.LECTURE_SEGMENT
    slide_id: int
    segments: List[LectureSegment]
    check_understanding_question: Optional[str] = None
    timestamp: float

# ============= Errors =============

class ErrorMessage(BaseModel):
    """Error response"""
    type: Literal[MessageType.ERROR] = MessageType.ERROR
    error_code: str
    error_message: str
    timestamp: float

# ============= Heartbeat =============

class HeartbeatMessage(BaseModel):
    """Keep-alive ping"""
    type: Literal[MessageType.HEARTBEAT] = MessageType.HEARTBEAT
    timestamp: float
