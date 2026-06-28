class WhisperSTT:
    def transcribe(self, audio_file_path: str) -> str:
        """
        Simulates calling the OpenAI Whisper API or local model to transcribe 
        multilingual audio files (Hindi, Tamil, English) into text.
        """
        return "Simulated transcription: This video shows violence in Chennai today."

class OCREngine:
    def extract_text(self, image_file_path: str) -> str:
        """
        Simulates Tesseract OCR or Google Vision extraction from images/video frames.
        """
        return "Simulated OCR output: BREAKING NEWS - RIOTS"

whisper_engine = WhisperSTT()
ocr_engine = OCREngine()
