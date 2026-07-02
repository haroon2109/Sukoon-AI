import os
import io
import logging
from fastapi import UploadFile
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

groq_api_key = os.getenv("GROQ_API_KEY")
client = AsyncGroq(api_key=groq_api_key) if groq_api_key else None

class AudioTranscriber:
    """
    Uses Groq's blazing fast whisper-large-v3 model to transcribe audio files.
    """
    
    @staticmethod
    async def transcribe(file_bytes: bytes, filename: str) -> str:
        if not client:
            logger.error("GROQ_API_KEY not configured. Cannot transcribe audio.")
            return ""
            
        try:
            # We must pass a file-like object to the Groq API.
            # Groq's API accepts a tuple of (filename, file_data)
            file_tuple = (filename, file_bytes)
            
            logger.info(f"Transcribing {filename} via Groq Whisper...")
            
            transcription = await client.audio.transcriptions.create(
                file=file_tuple,
                model="whisper-large-v3",
                prompt="Specify context or leave empty",  # Optional
                response_format="json",
                language="en", 
                temperature=0.0
            )
            
            logger.info("Audio transcription completed successfully.")
            return transcription.text
            
        except Exception as e:
            logger.error(f"Error during audio transcription: {e}")
            return ""

audio_transcriber = AudioTranscriber()
