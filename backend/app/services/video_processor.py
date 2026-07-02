import os
import cv2
import tempfile
import logging
import ffmpeg
from app.services.audio_transcriber import audio_transcriber

logger = logging.getLogger(__name__)

class VideoProcessor:
    """
    Processes video files locally to extract semantic components.
    Uses FFmpeg for audio extraction and OpenCV for keyframe extraction.
    """
    
    @staticmethod
    async def extract_audio_and_transcribe(video_bytes: bytes, filename: str) -> str:
        """
        Extracts the audio track from the video bytes and transcribes it using Whisper.
        Returns the transcribed text claim.
        """
        if not video_bytes:
            return ""

        audio_text = ""
        temp_video_path = ""
        temp_audio_path = ""
        
        try:
            # 1. Save video bytes to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                temp_video.write(video_bytes)
                temp_video_path = temp_video.name
                
            # 2. Extract audio to a temporary MP3 file using ffmpeg
            temp_audio_path = temp_video_path + "_audio.mp3"
            
            logger.info(f"Extracting audio from {filename} using FFmpeg...")
            (
                ffmpeg
                .input(temp_video_path)
                .output(temp_audio_path, format="mp3", acodec="libmp3lame", ac=1, ar="16k")
                .overwrite_output()
                .run(quiet=True)
            )
            
            # 3. Read the extracted audio bytes
            if os.path.exists(temp_audio_path):
                with open(temp_audio_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                
                # 4. Send the audio bytes to Whisper
                logger.info(f"Transcribing extracted audio from {filename}...")
                audio_filename = f"{filename}_extracted.mp3"
                audio_text = await audio_transcriber.transcribe(audio_bytes, audio_filename)
            
        except ffmpeg.Error as e:
            logger.warning(f"FFmpeg failed to extract audio from {filename}: {e.stderr.decode() if e.stderr else str(e)}")
        except Exception as e:
            logger.error(f"Error during video audio extraction for {filename}: {e}")
        finally:
            # Cleanup temp files
            if temp_video_path and os.path.exists(temp_video_path):
                os.remove(temp_video_path)
            if temp_audio_path and os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                
        return audio_text

    @staticmethod
    def extract_keyframes(video_bytes: bytes, max_frames: int = 5) -> list[bytes]:
        """
        Extracts evenly spaced keyframes from the video using OpenCV.
        Returns a list of JPEG encoded frame bytes.
        """
        if not video_bytes:
            return []
            
        temp_video_path = ""
        frames = []
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                temp_video.write(video_bytes)
                temp_video_path = temp_video.name
                
            logger.info("Extracting keyframes using OpenCV...")
            cap = cv2.VideoCapture(temp_video_path)
            
            if not cap.isOpened():
                logger.error("Failed to open video file with OpenCV.")
                return frames
                
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            if total_frames <= 0 or fps <= 0:
                logger.warning("Invalid video properties detected by OpenCV.")
                return frames
                
            # Calculate frame indices to extract (evenly spaced)
            step = max(1, total_frames // max_frames)
            target_frames = [i * step for i in range(max_frames)]
            
            current_frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                if current_frame_idx in target_frames:
                    # Encode frame to JPEG bytes
                    success, buffer = cv2.imencode('.jpg', frame)
                    if success:
                        frames.append(buffer.tobytes())
                        
                current_frame_idx += 1
                if current_frame_idx > max(target_frames):
                    break
                    
            cap.release()
            
        except Exception as e:
            logger.error(f"Error during keyframe extraction: {e}")
        finally:
            if temp_video_path and os.path.exists(temp_video_path):
                os.remove(temp_video_path)
                
        return frames

video_processor = VideoProcessor()
