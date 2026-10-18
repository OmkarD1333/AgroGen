from fastapi import APIRouter, Depends, UploadFile, File
from app.dependencies.db import get_current_user
from app.database.models import User
from app.schemas.agriculture import VoiceTTSRequest, VoiceTTSResponse
from app.services.voice_service import synthesize_speech
from app.services.chat_service import answer_farmer_query

voice_router = APIRouter(prefix="/voice", tags=["voice"])


@voice_router.post("/tts", response_model=VoiceTTSResponse)
@voice_router.post("/synthesize", response_model=VoiceTTSResponse)
async def generate_speech(
    req: VoiceTTSRequest,
    current_user: User = Depends(get_current_user),
):
    audio_path = synthesize_speech(text=req.text, language=req.language or "mr")
    return VoiceTTSResponse(
        audio_url=audio_path,
        language=req.language or "mr",
        duration_seconds=3.5,
    )


@voice_router.post("/chat")
async def voice_chat_endpoint(
    req: VoiceTTSRequest,
    current_user: User = Depends(get_current_user),
):
    # Process text query from voice transcription, synthesize response
    reply_text = answer_farmer_query(req.text, language=req.language or "mr")
    audio_url = synthesize_speech(reply_text, language=req.language or "mr")
    return {
        "text": reply_text,
        "audio_url": audio_url,
        "language": req.language or "mr",
    }


@voice_router.post("/upload")
async def voice_audio_upload(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    # Simulated voice speech-to-text response
    return {
        "transcribed_text": "सोयाबीन पिकावरील किडीवर कोणता उपाय करावा?",
        "language": "mr",
    }
