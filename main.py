"""
Buyvia Voice API
FastAPI server for voice command processing with Ghanaian accent support
Powered by Google Speech Recognition as per PRD requirements
"""

import os
import io
import sys
import tempfile
from typing import Optional

# Fix for Python 3.13+ where aifc was removed (for local development)
if sys.version_info >= (3, 13):
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # Create stub modules for removed audio modules
    import types
    for mod_name in ['aifc', 'audioop', 'chunk', 'sndhdr', 'sunau']:
        if mod_name not in sys.modules:
            sys.modules[mod_name] = types.ModuleType(mod_name)

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Import speech_recognition after the Python 3.13 fix
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

from utils.accent_mapper import (
    normalize_accent, 
    ACCENT_MAP, 
    LEARNED_MAPPINGS,
    get_unknown_words,
    add_learned_mapping,
    load_learned_mappings
)
from utils.audio_processor import AudioProcessor
from models.command_parser import parse_command, get_command_help

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Buyvia Voice API",
    description="Voice command processing API with Ghanaian accent support",
    version="1.0.0"
)

# CORS middleware for React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Google Speech Recognition (if available)
recognizer = None
if SPEECH_RECOGNITION_AVAILABLE and sr:
    recognizer = sr.Recognizer()
    # Configure recognizer for better accuracy with Ghanaian accents
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8


class TranscriptionResponse(BaseModel):
    """Response model for transcription endpoint."""
    success: bool
    raw_text: Optional[str] = None
    normalized_text: Optional[str] = None
    command: Optional[dict] = None
    error: Optional[str] = None


class TextCommandRequest(BaseModel):
    """Request model for text-based command parsing."""
    text: str


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Buyvia Voice API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "/transcribe": "POST - Transcribe audio to command",
            "/parse": "POST - Parse text to command",
            "/health": "GET - Health check",
            "/commands": "GET - List available commands"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "buyvia-voice-api"}


@app.get("/commands")
async def list_commands():
    """List all available voice commands with examples."""
    return {
        "success": True,
        "commands": get_command_help(),
        "total_commands": "100+",
        "accent_mappings": len(ACCENT_MAP)
    }


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio file to text using Google Speech Recognition.
    
    Accepts audio files in formats: wav, mp3, m4a, ogg, flac, webm
    Returns normalized text with Ghanaian accent corrections and parsed command.
    
    This is the primary endpoint for voice commands as per PRD requirements.
    """
    # Check if speech recognition is available
    if not SPEECH_RECOGNITION_AVAILABLE or not recognizer:
        return TranscriptionResponse(
            success=False,
            error="Speech recognition not available on Python 3.13+. Use /parse endpoint with text instead, or deploy to Render (Python 3.11)."
        )
    
    temp_wav_path = None
    
    try:
        # Validate file type
        filename = file.filename or "audio.m4a"
        file_ext = filename.split('.')[-1].lower()
        
        if file_ext not in AudioProcessor.SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio format. Supported: {AudioProcessor.SUPPORTED_FORMATS}"
            )
        
        # Read audio data
        audio_data = await file.read()
        
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Convert to WAV if needed
        if file_ext != 'wav':
            wav_bytes, temp_wav_path = AudioProcessor.convert_to_wav(audio_data, file_ext)
        else:
            # Write WAV to temp file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_wav_path = temp_file.name
        
        # Transcribe with Google Speech Recognition
        with sr.AudioFile(temp_wav_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)
        
        # Try Google Speech Recognition first
        try:
            raw_text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return TranscriptionResponse(
                success=False,
                error="Could not understand audio. Please speak clearly and try again."
            )
        except sr.RequestError as e:
            return TranscriptionResponse(
                success=False,
                error=f"Speech recognition service unavailable: {str(e)}"
            )
        
        # Apply Ghanaian accent normalization
        normalized_text = normalize_accent(raw_text)
        
        # Parse command from normalized text
        command = parse_command(normalized_text)
        
        return TranscriptionResponse(
            success=True,
            raw_text=raw_text,
            normalized_text=normalized_text,
            command=command
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return TranscriptionResponse(
            success=False,
            error=f"Transcription failed: {str(e)}"
        )
    finally:
        # Cleanup temp file
        if temp_wav_path:
            AudioProcessor.cleanup_temp_file(temp_wav_path)


@app.post("/parse", response_model=TranscriptionResponse)
async def parse_text_command(request: TextCommandRequest):
    """
    Parse text directly to command (for testing or text input).
    Applies accent normalization before parsing.
    """
    try:
        if not request.text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Apply accent normalization
        normalized_text = normalize_accent(request.text)
        
        # Parse command
        command = parse_command(normalized_text)
        
        return TranscriptionResponse(
            success=True,
            raw_text=request.text,
            normalized_text=normalized_text,
            command=command
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return TranscriptionResponse(
            success=False,
            error=f"Parsing failed: {str(e)}"
        )


@app.get("/accent-map")
async def get_accent_map():
    """Get the full accent mapping dictionary."""
    return {
        "success": True,
        "mappings": ACCENT_MAP,
        "count": len(ACCENT_MAP)
    }


@app.post("/normalize")
async def normalize_text(request: TextCommandRequest):
    """Normalize text with Ghanaian accent mappings."""
    try:
        normalized = normalize_accent(request.text)
        return {
            "success": True,
            "original": request.text,
            "normalized": normalized
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============== Self-Learning Endpoints (Admin) ==============

class LearnedMappingRequest(BaseModel):
    """Request model for adding learned mappings."""
    ghanaian: str
    standard: str


@app.get("/admin/unknown-words")
async def get_unknown_words_list():
    """
    Get list of unknown words logged for admin review.
    These are potential new accent mappings to add.
    """
    unknown = get_unknown_words()
    return {
        "success": True,
        "unknown_words": unknown,
        "count": len(unknown)
    }


@app.post("/admin/add-mapping")
async def add_new_mapping(request: LearnedMappingRequest):
    """
    Add a new learned accent mapping (admin approved).
    This enables the model to learn from user interactions.
    """
    try:
        add_learned_mapping(request.ghanaian, request.standard)
        return {
            "success": True,
            "message": f"Added mapping: '{request.ghanaian}' -> '{request.standard}'",
            "total_learned": len(LEARNED_MAPPINGS)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/admin/learned-mappings")
async def get_learned_mappings():
    """Get all learned mappings (added via admin approval)."""
    return {
        "success": True,
        "learned_mappings": LEARNED_MAPPINGS,
        "count": len(LEARNED_MAPPINGS)
    }


@app.get("/admin/stats")
async def get_learning_stats():
    """Get statistics about the accent learning system."""
    return {
        "success": True,
        "static_mappings": len(ACCENT_MAP),
        "learned_mappings": len(LEARNED_MAPPINGS),
        "total_mappings": len(ACCENT_MAP) + len(LEARNED_MAPPINGS),
        "pending_review": len(get_unknown_words())
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
