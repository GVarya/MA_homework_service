from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.schemas.base_schema import Base
from app.models.homework import HomeworkStatus

class Homework(Base):
    __tablename__ = "homeworks"

    id = Column(UUID(as_uuid=True), primary_key=True)
    course_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    status = Column(Enum(HomeworkStatus), nullable=False)
