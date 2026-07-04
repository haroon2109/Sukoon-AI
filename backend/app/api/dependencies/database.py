from typing import Generator
from app.db.session import get_db  # noqa: F401 — explicit re-export for router dependencies

__all__ = ["get_db"]
