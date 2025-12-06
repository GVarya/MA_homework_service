# hw_service/app/models/homework.py
import enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class HomeworkStatus(str, enum.Enum):
    CREATED = "created"
    ACTIVE = "active"
    CLOSED = "closed"

class Homework(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    title: str
    description: str
    created_at: datetime
    published_at: datetime | None = None
    status: HomeworkStatus

class HomeworkProgress(BaseModel):
    """Прогресс студента по ДЗ"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    student_id: UUID
    course_id: UUID
    total_homeworks: int
    completed_homeworks: int
    average_grade: float | None = None
