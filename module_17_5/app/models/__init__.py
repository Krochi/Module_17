# app/models/__init__.py

from app.backend.db import Base
from app.models.user import User  # Импорт модели User
from app.models.task import Task  # Импорт модели Task

__all__ = ["Base", "User", "Task"]  # Экспортируем все необходимые элементы

