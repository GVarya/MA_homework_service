# hw_service/app/models/requests.py
from uuid import UUID
from pydantic import BaseModel

class CreateHomeworkRequest(BaseModel):
    course_id: UUID
    title: str
    description: str

class PublishHomeworkRequest(BaseModel):
    """Опубликовать ДЗ (сделать активным для студентов)"""
    homework_id: UUID

class SubmitSolutionRequest(BaseModel):
    """Отправить решение на проверку"""
    homework_id: UUID
    student_id: UUID
    answer: str

class ReturnSolutionRequest(BaseModel):
    """Вернуть решение на доработку"""
    solution_id: UUID
    feedback: str

class GradeSolutionRequest(BaseModel):
    """Поставить оценку за ДЗ"""
    solution_id: UUID
    grade: int
    feedback: str | None = None
