from sqlalchemy import Column, String, DateTime, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.schemas.base_schema import Base
from app.models.solution import SolutionStatus

class Solution(Base):
    __tablename__ = "solutions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    homework_id = Column(UUID(as_uuid=True), nullable=False)
    student_id = Column(UUID(as_uuid=True), nullable=False)
    answer = Column(String, nullable=False)
    status = Column(Enum(SolutionStatus), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    grade = Column(Integer, nullable=True)
    feedback = Column(String, nullable=True)
