import os
import base64
import logging
import httpx
from PIL import Image
import io

logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
VISION_MODEL = os.getenv("VISION_MODEL", "qwen2.5-vl")

class VisionService:
    """
    Handles image understanding, meme analysis, and infographic data extraction 
    using Qwen2.5-VL via Ollama.
    """
    
    @staticmethod
    async def analyze_image(image_bytes: bytes, prompt: str = "Describe this image in detail.") -> str:
        """
        Sends an image to the local Qwen2.5-VL model to analyze.
        """
        try:
            # Convert image to base64
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            payload = {
                "model": VISION_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [base64_image]
                    }
                ],
                "stream": False
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_URL}/api/chat",
                    json=payload,
                    timeout=120.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "").strip()
                
        except Exception as e:
            logger.error(f"Error during Vision analysis: {e}")
            return f"Error analyzing image: {str(e)}"
            
    @staticmethod
    async def analyze_video_frames(frames: list[bytes], prompt: str = "What is happening in this video?") -> str:
        """
        Analyzes a sequence of frames by passing them to Qwen2.5-VL.
        For simplicity, we can pass multiple images to the model if it supports it,
        or analyze them iteratively and summarize.
        """
        base64_images = [base64.b64encode(f).decode('utf-8') for f in frames[:5]] # Limit to 5 frames to avoid blowing up context
        
        payload = {
            "model": VISION_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": base64_images
                }
            ],
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_URL}/api/chat",
                    json=payload,
                    timeout=120.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "").strip()
        except Exception as e:
            logger.error(f"Error during Video Frame analysis: {e}")
            return f"Error analyzing video frames: {str(e)}"

vision_service = VisionService()
