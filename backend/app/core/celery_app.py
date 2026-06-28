from celery import Celery
import os

# Read Redis URL from environment or fallback to localhost for development
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize the Celery Async Processing Layer
celery_app = Celery(
    "sukoon_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    # Routing tasks to specific queues if needed for scale (e.g., heavy deepfake models on GPU workers)
    task_routes={
        "app.tasks.pipelines.process_video_deepfake": {"queue": "gpu_tasks"},
        "app.tasks.pipelines.*": {"queue": "cpu_tasks"},
    }
)
