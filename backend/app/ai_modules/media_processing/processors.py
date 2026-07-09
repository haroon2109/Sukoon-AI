import os
import openai
from PIL import Image
from ...core.logger import api_logger

import importlib.util

HAS_CV2 = importlib.util.find_spec("cv2") is not None
HAS_TRANSFORMERS = importlib.util.find_spec("transformers") is not None

from ..services.vision_service import vision_service

_paddle_ocr = None

class OCREngine:
    def __init__(self):
        pass

    def extract_text(self, image_file_path: str) -> str:
        """
        Uses PaddleOCR to extract text from images/video frames. Falls back to EasyOCR.
        Loads models only during extraction and unloads them immediately to save memory.
        Resizes images >1920px to save memory.
        """
        import gc
        from PIL import Image
        import tempfile
        
        temp_path = None
        try:
            with Image.open(image_file_path) as img:
                max_dim = 1920
                if img.width > max_dim or img.height > max_dim:
                    img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                    fd, temp_path = tempfile.mkstemp(suffix=".jpg")
                    os.close(fd)
                    img.convert("RGB").save(temp_path, format="JPEG", quality=85)
                    image_file_path = temp_path
        except Exception as e:
            api_logger.warning(f"Failed to resize image before OCR: {e}")

        extracted_text = ""
        
        # 1. Try PaddleOCR first
        try:
            from paddleocr import PaddleOCR
            api_logger.info("Initializing PaddleOCR for current request...")
            paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en')
            
            result = paddle_ocr.ocr(image_file_path, cls=True)
            if result and result[0]:
                lines = []
                for line in result[0]:
                    text = line[1][0]
                    lines.append(text)
                
                from app.core.payload_optimizer import deduplicate_lines
                extracted_text = deduplicate_lines("\n".join(lines))
            
            # Explicitly delete and collect to free RAM
            del paddle_ocr
            gc.collect()
            
        except ImportError:
            api_logger.warning("PaddleOCR is not installed. Will rely entirely on EasyOCR fallback.")
        except Exception as e:
            api_logger.error(f"Error extracting text with PaddleOCR: {e}")
                
        # 2. Fallback to EasyOCR if PaddleOCR failed or found nothing
        if not extracted_text.strip():
            try:
                import easyocr
                api_logger.info("Initializing EasyOCR fallback for current request...")
                easy_reader = easyocr.Reader(['en'])
                
                result = easy_reader.readtext(image_file_path, detail=0)
                
                from app.core.payload_optimizer import deduplicate_lines
                extracted_text = deduplicate_lines("\n".join(result))
                
                # Explicitly delete and collect
                del easy_reader
                gc.collect()
            except ImportError:
                api_logger.warning("EasyOCR is not installed either. OCR will fail.")
            except Exception as e:
                api_logger.error(f"Error extracting text with EasyOCR: {e}")
                
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
                    
        return extracted_text

class VideoFrameAnalyzer:
    def analyze_video(self, video_file_path: str, prompt: str = None) -> list[str]:
        """
        Extracts frames from a video and uses the VisionService to describe them.
        """
        import asyncio
        if not HAS_CV2:
            return ["Error: opencv-python is required for video frame analysis."]

        if not os.path.exists(video_file_path):
            return [f"Error: Video file not found: {video_file_path}"]

        try:
            cap = cv2.VideoCapture(video_file_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps == 0 or not fps:
                fps = 30 # fallback if OpenCV can't detect FPS

            frame_interval = int(round(fps * 5)) # 1 frame every 5 seconds
            if frame_interval == 0:
                frame_interval = 1
            frame_count = 0
            
            frames_to_analyze = []
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                if frame_count % frame_interval == 0:
                    # Convert BGR to RGB
                    _, buffer = cv2.imencode('.jpg', frame)
                    frames_to_analyze.append(buffer.tobytes())
                    if len(frames_to_analyze) >= 6: # Limit to 6 frames (max 30s)
                        break
                    
                frame_count += 1
                
            cap.release()
            
            if not frames_to_analyze:
                return ["No frames extracted."]
                
            # Analyze all frames at once
            prompt_to_use = prompt or "What is happening in this video sequence?"
            loop = asyncio.get_event_loop()
            
            if loop.is_running():
                # We can't use await here because this is a synchronous function (historically)
                import nest_asyncio
                nest_asyncio.apply()
            
            result = loop.run_until_complete(vision_service.analyze_video_frames(frames_to_analyze, prompt_to_use))
            return [result]
            
        except Exception as e:
            print(f"Error analyzing video frames: {e}")
            return [f"Error processing video: {str(e)}"]

class OmniProcessor:
    def __init__(self):
        """
        Initializes a unified Omni model (e.g., Qwen2.5-Omni 3B or Gemma 4)
        for natively processing multiple modalities (text, image, audio) in a single pass.
        """
        self.processor = None
        self.model = None
        if HAS_TRANSFORMERS:
            try:
                # Placeholder for Qwen2.5-Omni / Gemma 4 Omni model loading.
                # In practice, this would use AutoProcessor and the specific Model class
                # based on the chosen open-weights model.
                from transformers import AutoProcessor, AutoModelForCausalLM
                
                # Using a generic Omni model path as placeholder based on user request
                model_id = "Qwen/Qwen2.5-Omni-3B-Instruct" 
                
                # self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
                # self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
                
                # Simulating load to avoid blocking on massive model downloads for now.
                print(f"Omni model {model_id} initialization simulated (would require substantial VRAM).")
            except Exception as e:
                print(f"Error initializing Omni model: {e}")

    def process_multimodal(self, prompt: str, image_paths: list[str] = None, audio_paths: list[str] = None) -> str:
        """
        Processes a combination of text, images, and audio natively in one inference pass.
        """
        if not HAS_TRANSFORMERS:
            return "Omni model is not loaded (requires transformers)."
        
        # Real implementation would format inputs according to the model's chat template
        # mapping image_paths and audio_paths into the context window.
        modalities = []
        if image_paths:
            modalities.append(f"{len(image_paths)} image(s)")
        if audio_paths:
            modalities.append(f"{len(audio_paths)} audio(s)")
            
        mods_str = ", ".join(modalities) if modalities else "text only"
        return f"Simulated Omni Output: Processed prompt '{prompt}' alongside {mods_str} successfully. Fake news likelihood: low."


# Lazy singletons — instantiated on first use to avoid blocking server startup
# and to avoid crashing when optional dependencies (OpenAI, BLIP) are missing.
_ocr_engine = None
_video_analyzer = None

def get_whisper_engine():
    from ..services.audio_transcriber import audio_transcriber
    return audio_transcriber

def get_vision_engine():
    from ..services.vision_service import vision_service
    return vision_service

def get_ocr_engine() -> OCREngine:
    global _ocr_engine
    if _ocr_engine is None:
        _ocr_engine = OCREngine()
    return _ocr_engine

def get_video_analyzer() -> VideoFrameAnalyzer:
    global _video_analyzer
    if _video_analyzer is None:
        _video_analyzer = VideoFrameAnalyzer()
    return _video_analyzer

whisper_engine = property(get_whisper_engine)
vision_engine = property(get_vision_engine)
ocr_engine = property(get_ocr_engine)
video_analyzer = property(get_video_analyzer)
