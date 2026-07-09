import os
import exifread


class DeepfakeDetector:
    def __init__(self):
        print("Initializing Deepfake & Anomaly Detection Framework...")
        # Models are lazy-loaded by DeepFace

    def extract_metadata(self, image_path: str) -> dict:
        """
        Extracts EXIF metadata from an image and checks for suspicious artifact 
        signatures (e.g. Photoshop or other editing software metadata).
        """
        results = {"metadata": {}, "suspicion_level": "low", "flags": []}
        try:
            with open(image_path, "rb") as f:
                tags = exifread.process_file(f)
                
            for tag in tags.keys():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                    results["metadata"][tag] = str(tags[tag])
                    
                    # Basic manipulation checks
                    val_lower = str(tags[tag]).lower()
                    if any(kw in val_lower for kw in ['photoshop', 'gimp', 'lightroom', 'ai generated', 'midjourney', 'dall-e', 'stable diffusion']):
                        results["flags"].append(f"Suspicious metadata tag found: {tag} = {tags[tag]}")
                        results["suspicion_level"] = "high"
        except Exception as e:
            results["error"] = f"Failed to extract metadata: {str(e)}"
            
        return results

    def analyze_faces(self, image_path: str) -> dict:
        """
        Uses DeepFace to analyze faces in the image. DeepFace can be used as a precursor
        to detecting swapped faces (e.g. checking face embeddings or facial artifacts).
        """
        results = {"faces_detected": 0, "analysis": [], "error": None}
        try:
            # We can use DeepFace to extract faces or perform attribute analysis
            # For deepfake detection, usually one would use a specific deepfake classifier (like MesoNet).
            # Here we use DeepFace's face extraction as a foundational check for facial anomalies.
            from deepface import DeepFace
            faces = DeepFace.extract_faces(img_path=image_path, enforce_detection=False)
            results["faces_detected"] = len(faces)
            
            # Simulated artifact check based on facial alignment confidence
            for face in faces:
                confidence = face.get("confidence", 1.0)
                if confidence < 0.85:
                    results["analysis"].append({
                        "status": "suspicious", 
                        "confidence": confidence, 
                        "note": "Low facial alignment confidence may indicate manipulation or face-swapping."
                    })
                else:
                    results["analysis"].append({"status": "normal", "confidence": confidence})
                    
        except Exception as e:
            results["error"] = f"Face analysis failed: {str(e)}"
            
        return results

    def run_full_scan(self, image_path: str) -> dict:
        """
        Runs both metadata extraction and facial anomaly detection on an image.
        """
        if not os.path.exists(image_path):
            return {"error": f"File not found: {image_path}"}
            
        return {
            "metadata_scan": self.extract_metadata(image_path),
            "facial_analysis": self.analyze_faces(image_path)
        }

# Example Usage:
# detector = DeepfakeDetector()
# report = detector.run_full_scan("suspicious_image.jpg")
