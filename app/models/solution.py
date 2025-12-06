# hw_service/app/models/solution.py
import enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SolutionStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    RETURNED = "returned"
    GRADED = "graded"

class Solution(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    homework_id: UUID
    student_id: UUID
    answer: str
    status: SolutionStatus
    created_at: datetime
    submitted_at: datetime | None = None
    grade: int | None = None
    feedback: str | None = None
