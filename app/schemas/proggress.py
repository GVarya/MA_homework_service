from sqlalchemy import Column, Float, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.base_schema import Base

class StudentProgress(Base):
    __tablename__ = "student_progress"

    id = Column(UUID(as_uuid=True), primary_key=True)
    student_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    course_id = Column(UUID(as_uuid=True), nullable=False)
    total_homeworks = Column(Integer, nullable=False, default=0)
    completed_homeworks = Column(Integer, nullable=False, default=0)
    average_grade = Column(Float, nullable=True)
