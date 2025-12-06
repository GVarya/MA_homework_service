from uuid import UUID, uuid4
from datetime import datetime

from app.models.homework import Homework, HomeworkStatus, HomeworkProgress
from app.models.solution import Solution, SolutionStatus
from app.models.requests import (
    CreateHomeworkRequest,
    PublishHomeworkRequest,
    SubmitSolutionRequest,
    ReturnSolutionRequest,
    GradeSolutionRequest,
)
from app.repos.homework_repo import HomeworkRepo
from app.repos.solution_repo import SolutionRepo
from app.repos.progress_repo import ProgressRepo

class HomeworkService:
    def __init__(self) -> None:
        self.hw_repo = HomeworkRepo()
        self.sol_repo = SolutionRepo()
        self.prog_repo = ProgressRepo()

    def publish_homework(self, dto: PublishHomeworkRequest) -> Homework:
        hw = self.hw_repo.get_homework_by_id(dto.homework_id)
        if hw.status != HomeworkStatus.CREATED:
            raise ValueError("Homework is not in CREATED status")
        return self.hw_repo.publish_homework(dto.homework_id)

    def submit_solution(self, dto: SubmitSolutionRequest) -> Solution:

        hw = self.hw_repo.get_homework_by_id(dto.homework_id)
        if hw.status != HomeworkStatus.ACTIVE:
            raise ValueError("Homework is not active")

        sol = Solution(
            id=uuid4(),
            homework_id=hw.id,
            student_id=dto.student_id,
            answer=dto.answer,
            status=SolutionStatus.DRAFT,
            created_at=datetime.utcnow(),
            submitted_at=None,
            grade=None,
            feedback=None,
        )
        created_sol = self.sol_repo.create_solution(sol)

        submitted_sol = self.sol_repo.submit_solution(created_sol.id)
        return submitted_sol

    def return_solution(self, dto: ReturnSolutionRequest) -> Solution:
        sol = self.sol_repo.get_solution_by_id(dto.solution_id)
        if sol.status not in [SolutionStatus.SUBMITTED, SolutionStatus.GRADED]:
            raise ValueError("Solution cannot be returned")
        return self.sol_repo.return_solution(dto.solution_id, dto.feedback)

    def grade_solution(self, dto: GradeSolutionRequest) -> Solution:
        sol = self.sol_repo.get_solution_by_id(dto.solution_id)
        if sol.status not in [SolutionStatus.SUBMITTED, SolutionStatus.RETURNED]:
            raise ValueError("Solution cannot be graded")

        graded_sol = self.sol_repo.grade_solution(
            dto.solution_id,
            dto.grade,
            dto.feedback,
        )

        try:
            self.prog_repo.update_progress_by_solution(graded_sol.student_id)
        except KeyError:
            pass  

        return graded_sol

    def get_student_progress(self, student_id: UUID) -> HomeworkProgress:
        try:
            return self.prog_repo.get_progress_by_student(student_id)
        except KeyError:
            raise ValueError("Progress not found")

    def update_progress(self, student_id: UUID) -> HomeworkProgress:
        return self.prog_repo.update_progress_by_solution(student_id)


    def create_homework(self, dto: CreateHomeworkRequest) -> Homework:
        hw = Homework(
            id=uuid4(),
            course_id=dto.course_id,
            title=dto.title,
            description=dto.description,
            created_at=datetime.utcnow(),
            published_at=None,
            status=HomeworkStatus.CREATED,
        )
        return self.hw_repo.create_homework(hw)

    def get_homeworks(self) -> list[Homework]:
        return self.hw_repo.get_homeworks()

    def get_homeworks_by_course(self, course_id: UUID) -> list[Homework]:
        return self.hw_repo.get_homeworks_by_course(course_id)

    def activate_homeworks_by_course(self, course_id: UUID) -> None:
        self.hw_repo.activate_by_course(course_id)

    def get_solutions_by_student(self, student_id: UUID) -> list[Solution]:
        return self.sol_repo.get_solutions_by_student(student_id)

    def get_solutions_by_homework(self, homework_id: UUID) -> list[Solution]:
        return self.sol_repo.get_solutions_by_homework(homework_id)
