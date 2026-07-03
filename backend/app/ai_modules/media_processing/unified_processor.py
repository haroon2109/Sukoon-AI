import os
import cv2
try:
    import librosa
except ImportError:
    pass
from PIL import Image
from transformers import pipeline

class SukoonMultimodalProcessor:
    def __init__(self):
        print("Initializing Free Open-Source Multi-Modal Engines...")
        # 1. Image Captioning Engine
        try:
            self.image_analyzer = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        except Exception as e:
            print(f"Failed to load image analyzer: {e}")
            self.image_analyzer = None
            
        # 2. Audio Transcription Engine
        try:
            self.audio_transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base")
        except Exception as e:
            print(f"Failed to load audio transcriber: {e}")
            self.audio_transcriber = None

    def process_image(self, image_path: str) -> str:
        """Extracts visual text context from an uploaded image/meme."""
        if not self.image_analyzer:
            return "Image analyzer pipeline is not available."
        try:
            image = Image.open(image_path)
            result = self.image_analyzer(image)
            return result[0]["generated_text"]
        except Exception as e:
            return f"Image processing failed: {str(e)}"

    def process_audio(self, audio_path: str) -> str:
        """Transcribes incoming voice notes or audio clips to scan for verbal rumors."""
        if not self.audio_transcriber:
            return "Audio transcriber pipeline is not available."
        try:
            # Resample audio natively using librosa for Whisper compatibility
            audio_data, sampling_rate = librosa.load(audio_path, sr=16000)
            result = self.audio_transcriber({"raw": audio_data, "sampling_rate": sampling_rate})
            return result["text"]
        except Exception as e:
            return f"Audio transcription failed: {str(e)}"

    def process_video(self, video_path: str, output_audio_path: str = "temp_audio.wav") -> dict:
        """
        Deconstructs video into 1 FPS frames for visual analysis 
        and extracts audio for deep transcription.
        """
        results = {"visual_keyframes": [], "transcript": ""}
        
        # 1. Video-to-Text: Sample frames using OpenCV
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_id = 0
        
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            
            # Sample exactly 1 frame per second to stay within container limits
            if fps > 0 and frame_id % int(fps) == 0:
                temp_frame_path = f"frame_{frame_id}.jpg"
                cv2.imwrite(temp_frame_path, frame)
                
                # Analyze frame context
                frame_description = self.process_image(temp_frame_path)
                results["visual_keyframes"].append({"timestamp_sec": frame_id // int(fps), "description": frame_description})
                
                # Clean up local frame file
                if os.path.exists(temp_frame_path):
                    os.remove(temp_frame_path)
                
            frame_id += 1
        video.release()
        
        # 2. Video-to-Audio: Extract audio track for transcription
        # Note: In production, use os.system(f"ffmpeg -i {video_path} -vn {output_audio_path}")
        if os.path.exists(output_audio_path):
            results["transcript"] = self.process_audio(output_audio_path)
            
        return results

# Example Usage for Sukoon AI Ingestion:
# processor = SukoonMultimodalProcessor()
# data = processor.process_video("suspicious_whatsapp_video.mp4")
