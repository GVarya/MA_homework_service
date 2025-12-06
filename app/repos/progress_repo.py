from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.homework import HomeworkProgress
from app.schemas.proggress import StudentProgress as DBProgress
from app.schemas.solution import Solution as DBSolution
from app.models.solution import SolutionStatus

class ProgressRepo:
    def __init__(self) -> None:
        self.db: Session = next(get_db())

    def get_progress_by_student(self, student_id: UUID) -> HomeworkProgress:
        p = (
            self.db.query(DBProgress)
            .filter(DBProgress.student_id == student_id)
            .first()
        )
        if p is None:
            raise KeyError
        return HomeworkProgress.from_orm(p)

    def create_or_update_progress(
        self,
        student_id: UUID,
        course_id: UUID,
        total_homeworks: int,
        completed_homeworks: int,
        average_grade: float | None = None,
    ) -> HomeworkProgress:
        p = (
            self.db.query(DBProgress)
            .filter(DBProgress.student_id == student_id)
            .first()
        )
        if p is None:
            p = DBProgress(
                id=uuid4(),
                student_id=student_id,
                course_id=course_id,
                total_homeworks=total_homeworks,
                completed_homeworks=completed_homeworks,
                average_grade=average_grade,
            )
            self.db.add(p)
        else:
            p.total_homeworks = total_homeworks
            p.completed_homeworks = completed_homeworks
            p.average_grade = average_grade

        self.db.commit()
        self.db.refresh(p)
        return HomeworkProgress.from_orm(p)

    def update_progress_by_solution(self, student_id: UUID) -> HomeworkProgress:
        
        solutions = (
            self.db.query(DBSolution)
            .filter(DBSolution.student_id == student_id)
            .all()
        )

        completed = len([s for s in solutions if s.status == SolutionStatus.GRADED])
        total = len(solutions)
        
        grades = [s.grade for s in solutions if s.grade is not None]
        avg_grade = sum(grades) / len(grades) if grades else None

        p = (
            self.db.query(DBProgress)
            .filter(DBProgress.student_id == student_id)
            .first()
        )

        if p:
            p.completed_homeworks = completed
            p.average_grade = avg_grade
            self.db.commit()
            self.db.refresh(p)
            return HomeworkProgress.from_orm(p)

        raise KeyError
