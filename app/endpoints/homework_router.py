from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.services.homework_service import HomeworkService
from app.models.homework import Homework, HomeworkProgress
from app.models.solution import Solution
from app.models.requests import (
    CreateHomeworkRequest,
    PublishHomeworkRequest,
    SubmitSolutionRequest,
    ReturnSolutionRequest,
    GradeSolutionRequest,
)

router = APIRouter(prefix="/homeworks", tags=["Homework"])

@router.get("/", response_model=list[Homework])
def get_homeworks(svc: HomeworkService = Depends()):
    return svc.get_homeworks()

@router.get("/course/{course_id}", response_model=list[Homework])
def get_homeworks_by_course(
    course_id: UUID,
    svc: HomeworkService = Depends(),
):
    return svc.get_homeworks_by_course(course_id)

@router.post("/", response_model=Homework)
def create_homework(
    dto: CreateHomeworkRequest,
    svc: HomeworkService = Depends(),
):
    try:
        return svc.create_homework(dto)
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/publish", response_model=Homework)
def publish_homework(
    dto: PublishHomeworkRequest,
    svc: HomeworkService = Depends(),
):
    try:
        return svc.publish_homework(dto)
    except KeyError:
        raise HTTPException(404, "Homework not found")
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/solutions/submit", response_model=Solution)
def submit_solution(
    dto: SubmitSolutionRequest,
    svc: HomeworkService = Depends(),
):
    try:
        return svc.submit_solution(dto)
    except KeyError:
        raise HTTPException(404, "Homework not found")
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/solutions/return", response_model=Solution)
def return_solution(
    dto: ReturnSolutionRequest,
    svc: HomeworkService = Depends(),
):
    try:
        return svc.return_solution(dto)
    except KeyError:
        raise HTTPException(404, "Solution not found")
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/solutions/grade", response_model=Solution)
def grade_solution(
    dto: GradeSolutionRequest,
    svc: HomeworkService = Depends(),
):
    try:
        return svc.grade_solution(dto)
    except KeyError:
        raise HTTPException(404, "Solution not found")
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/solutions/student/{student_id}", response_model=list[Solution])
def get_solutions_by_student(
    student_id: UUID,
    svc: HomeworkService = Depends(),
):
    return svc.get_solutions_by_student(student_id)

@router.get("/solutions/homework/{homework_id}", response_model=list[Solution])
def get_solutions_by_homework(
    homework_id: UUID,
    svc: HomeworkService = Depends(),
):
    return svc.get_solutions_by_homework(homework_id)

@router.get("/progress/student/{student_id}", response_model=HomeworkProgress)
def get_student_progress(
    student_id: UUID,
    svc: HomeworkService = Depends(),
):
    try:
        return svc.get_student_progress(student_id)
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.post("/progress/update/{student_id}", response_model=HomeworkProgress)
def update_progress(
    student_id: UUID,
    svc: HomeworkService = Depends(),
):
    try:
        return svc.update_progress(student_id)
    except KeyError:
        raise HTTPException(404, "Progress not found")
