import os
import io
import tempfile
import logging
import gc

logger = logging.getLogger(__name__)

# Use tiny or base for extreme memory constraint
MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "tiny")

class AudioTranscriber:
    """
    Uses faster-whisper to transcribe audio files locally.
    Implements extreme memory optimization by loading models only when needed.
    """
    
    @staticmethod
    async def transcribe(file_bytes: bytes, filename: str) -> str:
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            logger.error("faster-whisper is not installed. Cannot transcribe.")
            return ""
            
        try:
            from pydub import AudioSegment
        except ImportError:
            logger.error("pydub is not installed. Cannot chunk audio.")
            return ""

        try:
            logger.info(f"Loading WhisperModel ({MODEL_SIZE}) for current request...")
            # Use 'cpu' and 'int8' for strict memory constrained environments
            whisper_model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
            
            logger.info(f"Chunking {filename} and transcribing via faster-whisper...")
            try:
                audio = AudioSegment.from_file(io.BytesIO(file_bytes))
            except Exception as e:
                logger.error(f"Failed to read audio with pydub: {e}")
                return ""
                
            chunk_length_ms = 30000 # 30 seconds
            chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
            transcription_parts = []
            
            for idx, chunk in enumerate(chunks):
                logger.info(f"Transcribing chunk {idx+1}/{len(chunks)}...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    chunk.export(tmp_file.name, format="wav")
                    tmp_path = tmp_file.name
                    
                try:
                    segments, info = whisper_model.transcribe(tmp_path, beam_size=1)
                    transcription_parts.append("".join([segment.text for segment in segments]))
                finally:
                    os.unlink(tmp_path)
                    gc.collect() # aggressively clear temp tensors per chunk
                    
            return " ".join(transcription_parts).strip()
            
        except Exception as e:
            logger.error(f"Error during audio transcription: {e}")
            return ""
            
        finally:
            # Aggressively release model memory when totally done
            if 'whisper_model' in locals():
                del whisper_model
            gc.collect()

audio_transcriber = AudioTranscriber()
