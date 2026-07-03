import os
try:
    import easyocr
except ImportError:
    pass

class EasyOCREngine:
    def __init__(self, languages: list = None):
        """
        Initializes the EasyOCR reader. 
        Defaults to English ('en') and Hindi ('hi') to handle regional Indian content.
        """
        if languages is None:
            languages = ['en', 'hi']
            
        print(f"Initializing EasyOCR Engine for languages: {languages}...")
        self.reader = None
        try:
            # Setting gpu=False as a safe default, though production environments 
            # with PyTorch/CUDA should toggle this to True for maximum speed.
            self.reader = easyocr.Reader(languages, gpu=False)
        except Exception as e:
            print(f"Failed to load EasyOCR: {e}")

    def extract_text(self, image_path: str) -> str:
        """
        Extracts embedded text from a meme or screenshot using EasyOCR before 
        sending the payload to a LLM for semantic verification.
        """
        if not self.reader:
            return "OCR engine is not loaded (requires easyocr)."
            
        if not os.path.exists(image_path):
            return f"Error: File not found: {image_path}"
            
        try:
            # detail=0 returns just the raw text strings, stripping out bounding boxes and confidences
            results = self.reader.readtext(image_path, detail=0)
            
            # Combine the extracted text fragments into a single contiguous string
            extracted_text = " ".join(results).strip()
            return extracted_text
            
        except Exception as e:
            error_msg = f"EasyOCR extraction failed: {str(e)}"
            print(error_msg)
            return error_msg

# Example Usage:
# ocr = EasyOCREngine()
# text = ocr.extract_text("suspicious_whatsapp_forward.jpg")
