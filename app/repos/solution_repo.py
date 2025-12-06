from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.solution import Solution, SolutionStatus
from app.schemas.solution import Solution as DBSolution

class SolutionRepo:
    def __init__(self) -> None:
        self.db: Session = next(get_db())

    def create_solution(self, solution: Solution) -> Solution:
        db_obj = DBSolution(
            id=solution.id,
            homework_id=solution.homework_id,
            student_id=solution.student_id,
            answer=solution.answer,
            status=solution.status,
            created_at=solution.created_at,
            submitted_at=solution.submitted_at,
            grade=solution.grade,
            feedback=solution.feedback,
        )
        self.db.add(db_obj)
        self.db.commit()
        return solution

    def get_solution_by_id(self, id: UUID) -> Solution:
        s = (
            self.db.query(DBSolution)
            .filter(DBSolution.id == id)
            .first()
        )
        if s is None:
            raise KeyError
        return Solution.from_orm(s)

    def get_solutions_by_homework(self, homework_id: UUID) -> list[Solution]:
        return [
            Solution.from_orm(s)
            for s in self.db.query(DBSolution)
            .filter(DBSolution.homework_id == homework_id)
            .all()
        ]

    def get_solutions_by_student(self, student_id: UUID) -> list[Solution]:
        return [
            Solution.from_orm(s)
            for s in self.db.query(DBSolution)
            .filter(DBSolution.student_id == student_id)
            .all()
        ]

    def set_status(self, id: UUID, status: SolutionStatus) -> Solution:
        s = (
            self.db.query(DBSolution)
            .filter(DBSolution.id == id)
            .first()
        )
        if s is None:
            raise KeyError
        s.status = status
        self.db.commit()
        self.db.refresh(s)
        return Solution.from_orm(s)

    def submit_solution(self, id: UUID) -> Solution:
        s = (
            self.db.query(DBSolution)
            .filter(DBSolution.id == id)
            .first()
        )
        if s is None:
            raise KeyError
        s.status = SolutionStatus.SUBMITTED
        s.submitted_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(s)
        return Solution.from_orm(s)

    def return_solution(self, id: UUID, feedback: str) -> Solution:
        s = (
            self.db.query(DBSolution)
            .filter(DBSolution.id == id)
            .first()
        )
        if s is None:
            raise KeyError
        s.status = SolutionStatus.RETURNED
        s.feedback = feedback
        self.db.commit()
        self.db.refresh(s)
        return Solution.from_orm(s)

    def grade_solution(self, id: UUID, grade: int, feedback: str | None = None) -> Solution:
        s = (
            self.db.query(DBSolution)
            .filter(DBSolution.id == id)
            .first()
        )
        if s is None:
            raise KeyError
        s.status = SolutionStatus.GRADED
        s.grade = grade
        if feedback:
            s.feedback = feedback
        self.db.commit()
        self.db.refresh(s)
        return Solution.from_orm(s)
