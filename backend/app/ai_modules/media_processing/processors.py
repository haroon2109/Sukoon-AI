import os
import openai
from PIL import Image
from ...core.logger import api_logger

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

class WhisperSTT:
    def __init__(self):
        # Assumes OPENAI_API_KEY is set in environment variables
        self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def transcribe(self, audio_file_path: str) -> str:
        """
        Calls the OpenAI Whisper API to transcribe multilingual audio files 
        (Hindi, Tamil, English) into text.
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcription.text
        except Exception as e:
            api_logger.error(f"Error transcribing audio with Whisper: {e}")
            raise RuntimeError(f"Audio transcription failed: {e}")

class VisionLanguageModel:
    def __init__(self):
        """
        Initializes the Salesforce BLIP model for image captioning/OCR.
        """
        self.processor = None
        self.model = None
        if HAS_TRANSFORMERS:
            try:
                self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
                self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            except Exception as e:
                api_logger.error(f"Error loading BLIP model: {e}")
                raise RuntimeError(f"Failed to load vision model: {e}")

    def process_image(self, image_input, prompt: str = None) -> str:
        """
        Processes an image to generate a text description or identify text (OCR).
        Accepts either a file path (str) or a PIL.Image object.
        """
        if not self.processor or not self.model:
            raise RuntimeError("Vision model is not loaded (requires transformers & torch).")
        
        try:
            if isinstance(image_input, str):
                raw_image = Image.open(image_input).convert('RGB')
            elif isinstance(image_input, Image.Image):
                raw_image = image_input.convert('RGB')
            else:
                raise ValueError("Invalid image input type.")
                
            if prompt:
                inputs = self.processor(raw_image, prompt, return_tensors="pt")
            else:
                inputs = self.processor(raw_image, return_tensors="pt")
            
            out = self.model.generate(**inputs, max_new_tokens=50)
            return self.processor.decode(out[0], skip_special_tokens=True)
        except Exception as e:
            api_logger.error(f"Error processing image with Vision Language Model: {e}")
            raise RuntimeError(f"Image processing failed: {e}")

class OCREngine:
    def extract_text(self, image_file_path: str) -> str:
        """
        Uses Tesseract OCR to extract text from images/video frames.
        """
        if not HAS_TESSERACT:
            api_logger.warning("pytesseract is not installed. Returning empty OCR string.")
            return ""
            
        try:
            image = Image.open(image_file_path)
            extracted_text = pytesseract.image_to_string(image)
            return extracted_text.strip()
        except Exception as e:
            api_logger.error(f"Error extracting text with OCR: {e}")
            raise RuntimeError(f"OCR extraction failed: {e}")

class VideoFrameAnalyzer:
    def __init__(self, vision_engine: VisionLanguageModel):
        self.vision_engine = vision_engine

    def analyze_video(self, video_file_path: str, prompt: str = None) -> list[str]:
        """
        Extracts frames from a video at 1 FPS and uses the VisionLanguageModel to describe them.
        """
        if not HAS_CV2:
            return ["Error: opencv-python is required for video frame analysis."]

        if not os.path.exists(video_file_path):
            return [f"Error: Video file not found: {video_file_path}"]

        descriptions = []
        try:
            cap = cv2.VideoCapture(video_file_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps == 0 or not fps:
                fps = 30 # fallback if OpenCV can't detect FPS

            frame_interval = int(round(fps)) # 1 FPS
            frame_count = 0
            seconds = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                if frame_count % frame_interval == 0:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(frame_rgb)
                    
                    # Process with BLIP
                    desc = self.vision_engine.process_image(pil_img, prompt)
                    descriptions.append(f"Second {seconds}: {desc}")
                    seconds += 1
                    
                frame_count += 1
                
            cap.release()
            return descriptions
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


whisper_engine = WhisperSTT()
vision_engine = VisionLanguageModel()
ocr_engine = OCREngine()
video_analyzer = VideoFrameAnalyzer(vision_engine)
omni_engine = OmniProcessor()

