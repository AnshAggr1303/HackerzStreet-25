# app/main.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import AudioResponse, TextResponse, QueryRequest  
from app.services.rag_service import RAGService
from app.services.llm_service import LlamaService
from app.services.speech_service import SpeechService
from app.services.translation_service import TranslationService
from app.utils.helpers import handle_error, timer_decorator, validate_language_code
from app.config import settings
from app.services.booking_system import process_booking
import logging
import base64

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Updated CORS middleware configuration with explicit allowed origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
translation_service = TranslationService()
rag_service = RAGService()
llm_service = LlamaService()
speech_service = SpeechService()

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)
    
@app.post("/api/upload", response_model=AudioResponse)
@handle_error
@timer_decorator
async def process_audio_upload(
    file: UploadFile = File(...)
):
    """Process audio upload from frontend"""
    logger.info(f"Received audio upload: {file.filename}")
    
    # Validate file type
    valid_audio_types = ['audio/mpeg', 'audio/mp3', 'audio/wav']
    if file.content_type not in valid_audio_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only MP3/WAV files are accepted."
        )
    
    try:
        # Read audio content
        audio_content = await file.read()
        file_size = len(audio_content)
        
        # Basic file size validation (e.g., max 10MB)
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=400,
                detail="File size too large. Maximum size is 10MB."
            )
        
        # Convert speech to text
        transcript = await speech_service.speech_to_text(audio_content)
        if not transcript:
            raise HTTPException(
                status_code=400,
                detail="Could not transcribe audio. Please ensure clear audio quality."
            )
        logger.info(f"Transcribed text: {transcript[:100]}...")
        
        # Detect language
        source_lang = translation_service.detect_language(transcript)
        if not validate_language_code(source_lang):
            raise HTTPException(
                status_code=400,
                detail=f"Language {source_lang} is not supported"
            )
        
        # Process query
        english_prompt = translation_service.translate_to_english(
            transcript, source_lang
        )
        context = rag_service.get_relevant_context(english_prompt)
        english_response = await llm_service.generate_response(english_prompt, context)
        final_response = translation_service.translate_from_english(
            english_response, source_lang
        )
        
        # Convert response to speech (raw bytes)
        audio_response = await speech_service.text_to_speech(
            final_response, source_lang
        )
        
        if not audio_response:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate audio response"
            )
        
        # Convert the raw audio bytes to a base64 encoded string to avoid UTF-8 errors.
        encoded_audio = base64.b64encode(audio_response).decode('utf-8')
        
        return AudioResponse(
            audio_content=encoded_audio,
            detected_language=source_lang,
            question=transcript,            # new field with original question
            llm_response=final_response       # new field with text response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing audio: {str(e)}"
        )
    
@app.post("/api/query", response_model=TextResponse)
@handle_error
@timer_decorator
async def process_text_query(request: QueryRequest):
    """Process text query"""
    if not request.prompt:
        raise HTTPException(
            status_code=400,
            detail="Text prompt is required"
        )
    
    logger.info(f"Received text query: {request.prompt[:100]}...")
    
    if "book" in request.prompt.lower():
        # If the prompt is exactly "yes" or "no", treat it as a confirmation response.
        if request.prompt.lower().strip() in ["yes", "no"]:
            # Call the booking function with the confirmation provided
            booking_response = process_booking(request.prompt, confirmation=request.prompt.lower().strip())
        else:
            # Initial booking request – no confirmation yet.
            booking_response = process_booking(request.prompt)
        return TextResponse(
            response=booking_response,
            detected_language="en"  # Adjust as needed if you want to detect/translate the language
        )

    # Detect language
    source_lang = translation_service.detect_language(request.prompt)
    
    # Translate to English if needed
    english_prompt = translation_service.translate_to_english(
        request.prompt, source_lang
    )
    
    # Get relevant context using RAG
    context = rag_service.get_relevant_context(english_prompt)
    
    # Generate response using Llama
    english_response = await llm_service.generate_response(
        english_prompt, context
    )
    
    # Translate response back if needed
    final_response = translation_service.translate_from_english(
        english_response, source_lang
    )
    
    return TextResponse(
        response=final_response,
        detected_language=source_lang
    )

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }