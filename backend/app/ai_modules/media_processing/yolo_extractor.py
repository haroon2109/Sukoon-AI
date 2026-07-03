import os
try:
    from ultralytics import YOLO
except ImportError:
    pass

class YOLOExtractor:
    def __init__(self, model_version: str = "yolov8n.pt"):
        """
        Initializes the YOLO model for object and scene extraction.
        Defaults to the nano version (yolov8n.pt) for fast inference.
        """
        print(f"Initializing YOLO Object & Scene Extractor ({model_version})...")
        self.model = None
        try:
            # ultralytics automatically downloads the weights on first run
            self.model = YOLO(model_version)
        except Exception as e:
            print(f"Failed to load YOLO model {model_version}: {e}")

    def extract_objects(self, media_path: str, confidence_threshold: float = 0.25) -> dict:
        """
        Runs YOLO object detection on an image or video to extract detected items
        and context labels (e.g., 'person', 'car', 'fire').
        """
        if not self.model:
            return {"error": "YOLO model is not loaded (requires ultralytics)."}
            
        if not os.path.exists(media_path):
            return {"error": f"File not found: {media_path}"}
            
        results_data = {"detected_objects": {}, "context_labels": []}
        try:
            # The ultralytics predict method handles both images and videos
            results = self.model.predict(source=media_path, conf=confidence_threshold, verbose=False)
            
            # Aggregate detections across frames (if video) or single image
            unique_labels = set()
            for result in results:
                names = result.names
                boxes = result.boxes
                
                if boxes is not None:
                    for box in boxes:
                        cls_id = int(box.cls[0])
                        label = names[cls_id]
                        conf = float(box.conf[0])
                        
                        unique_labels.add(label)
                        
                        if label not in results_data["detected_objects"]:
                            results_data["detected_objects"][label] = []
                        results_data["detected_objects"][label].append(conf)
            
            results_data["context_labels"] = list(unique_labels)
            
            # Basic context aggregation heuristics
            if "person" in results_data["detected_objects"] and len(results_data["detected_objects"]["person"]) >= 5:
                if "crowd" not in results_data["context_labels"]:
                    results_data["context_labels"].append("crowd")
                    
        except Exception as e:
            results_data["error"] = f"YOLO extraction failed: {str(e)}"
            
        return results_data

# Example Usage:
# yolo_engine = YOLOExtractor()
# data = yolo_engine.extract_objects("flagged_video.mp4")
