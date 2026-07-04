from celery import Celery
from app.core.config import settings

# Initialize Celery app with SQLite broker and backend for lightweight Cloud Run deployment
celery_app = Celery(
    "sukoon_ai_tasks",
    broker=settings.DATABASE_URL or "sqla+sqlite:///celery_broker.sqlite",
    backend=settings.DATABASE_URL or "db+sqlite:///celery_backend.sqlite"
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
