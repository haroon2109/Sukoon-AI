from celery import Celery, Task
from app.core.config import settings
from app.db.session import SessionLocal

class DatabaseTask(Task):
    """
    A Celery Task base class that safely handles SQLAlchemy session life cycles.
    Provides a shared thread-local session and automatically closes it upon task completion.
    """
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self._db is not None:
            try:
                self._db.close()
            except Exception as e:
                import logging
                logging.getLogger("celery").error(f"Error closing DB session in task after_return: {e}")
            finally:
                self._db = None

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
