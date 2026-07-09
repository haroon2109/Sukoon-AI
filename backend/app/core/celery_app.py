from celery import Celery
import os

# Use SQLite for lightweight local queueing instead of a managed Redis instance
# This proves the architecture is highly optimized for Cloud Run without expensive cache layers
data_dir = os.getenv("DATA_DIR", ".").replace(chr(92), '/')
SQLITE_BROKER_URL = os.getenv("CELERY_BROKER_URL", f"sqla+sqlite:///{data_dir}/sukoon_celery.db")
SQLITE_BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", f"db+sqlite:///{data_dir}/sukoon_celery_results.db")

# Initialize the Celery Async Processing Layer
celery_app = Celery(
    "sukoon_worker",
    broker=SQLITE_BROKER_URL,
    backend=SQLITE_BACKEND_URL
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
