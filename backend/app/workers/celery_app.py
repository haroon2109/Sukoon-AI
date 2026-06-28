from celery import Celery

# Initialize Celery app with Redis broker and backend
# These values would typically be loaded from app.core.config
celery_app = Celery(
    "sukoon_ai_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Define our specific queue routing as per architecture
    task_routes={
        "app.workers.task_pipelines.process_audio": {"queue": "gpu_heavy"},
        "app.workers.task_pipelines.process_ocr": {"queue": "gpu_heavy"},
        "app.workers.task_pipelines.extract_claim": {"queue": "api_fast"},
        "app.workers.task_pipelines.verify_claim": {"queue": "api_fast"},
        "app.workers.task_pipelines.generate_truth_card": {"queue": "api_fast"},
    }
)
