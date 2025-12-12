# # tests/unit/test_homework_service.py

# import pytest
# from uuid import uuid4
# from datetime import datetime

# from app.services.homework_service import HomeworkService
# from app.models.homework import HomeworkStatus
# from app.models.requests import CreateHomeworkRequest, PublishHomeworkRequest, SubmitSolutionRequest


# @pytest.fixture(scope='session')
# def homework_service():
#     """Фикстура с сервисом (используем локальные репозитории)"""
#     return HomeworkService()


# @pytest.fixture(scope='session')
# def course_id():
#     return uuid4()


# @pytest.fixture(scope='session')
# def student_id():
#     return uuid4()


# def test_create_homework(homework_service: HomeworkService, course_id):
#     """Тест создания домашнего задания"""
#     request = CreateHomeworkRequest(
#         course_id=course_id,
#         title='Test Homework',
#         description='Test Description'
#     )
#     homework = homework_service.create_homework(request)
    
#     assert homework.title == 'Test Homework'
#     assert homework.course_id == course_id
#     assert homework.status == HomeworkStatus.CREATED


# def test_publish_homework(homework_service: HomeworkService, course_id):
#     """Тест публикации домашнего задания"""
#     # Создаём домашку
#     create_req = CreateHomeworkRequest(
#         course_id=course_id,
#         title='Homework to Publish',
#         description='Description'
#     )
#     homework = homework_service.create_homework(create_req)
    
#     # Публикуем
#     publish_req = PublishHomeworkRequest(homework_id=homework.id)
#     published_hw = homework_service.publish_homework(publish_req)
    
#     assert published_hw.status == HomeworkStatus.ACTIVE
#     assert published_hw.published_at is not None


# def test_publish_homework_wrong_status(homework_service: HomeworkService, course_id):
#     """Тест ошибки при публикации уже опубликованной домашки"""
#     create_req = CreateHomeworkRequest(
#         course_id=course_id,
#         title='Already Published',
#         description='Desc'
#     )
#     homework = homework_service.create_homework(create_req)
    
#     # Публикуем первый раз
#     publish_req = PublishHomeworkRequest(homework_id=homework.id)
#     homework_service.publish_homework(publish_req)
    
#     # Пробуем опубликовать второй раз
#     with pytest.raises(ValueError):
#         homework_service.publish_homework(publish_req)


# def test_submit_solution(homework_service: HomeworkService, course_id, student_id):
#     """Тест отправки решения"""
#     # Создаём и публикуем домашку
#     create_req = CreateHomeworkRequest(
#         course_id=course_id,
#         title='Homework for Solution',
#         description='Description'
#     )
#     homework = homework_service.create_homework(create_req)
#     publish_req = PublishHomeworkRequest(homework_id=homework.id)
#     homework_service.publish_homework(publish_req)
    
#     # Отправляем решение
#     solution_req = SubmitSolutionRequest(
#         homework_id=homework.id,
#         student_id=student_id,
#         answer='My solution'
#     )
#     solution = homework_service.submit_solution(solution_req)
    
#     assert solution.homework_id == homework.id
#     assert solution.student_id == student_id
#     assert solution.answer == 'My solution'

# tests/unit/test_homework_service.py
"""Unit tests for HomeworkService with in-memory repositories"""

import pytest
from uuid import uuid4
from datetime import datetime

from app.services.homework_service import HomeworkService
from app.models.homework import Homework, HomeworkStatus
from app.models.solution import Solution, SolutionStatus
from app.models.requests import CreateHomeworkRequest, PublishHomeworkRequest, SubmitSolutionRequest


class LocalHomeworkRepo:
    def __init__(self):
        self.homeworks = {} 

    def create_homework(self, hw: Homework) -> Homework:
        self.homeworks[hw.id] = hw
        return hw

    def get_homework_by_id(self, hw_id: str) -> Homework:
        return self.homeworks.get(hw_id)

    def get_homeworks(self) -> list:
        return list(self.homeworks.values())

    def get_homeworks_by_course(self, course_id: str) -> list:
        return [hw for hw in self.homeworks.values() if hw.course_id == course_id]

    def publish_homework(self, homework_id: str) -> Homework:
        hw = self.homeworks.get(homework_id)
        if hw:
            hw.status = HomeworkStatus.ACTIVE
            from datetime import datetime
            hw.published_at = datetime.utcnow()
            self.homeworks[homework_id] = hw
        return hw

class LocalSolutionRepo:
    def __init__(self):
        self.solutions = {}

    def submit_solution(self, solution_id: str) -> Solution:
        sol = self.solutions.get(solution_id)
        if sol:
            sol.status = SolutionStatus.SUBMITTED
        return sol

    def get_solutions_by_homework(self, hw_id: str) -> list:
        return [sol for sol in self.solutions.values() if sol.homework_id == hw_id]
    
    def create_solution(self, sol: Solution) -> Solution: 
        self.solutions[sol.id] = sol
        return sol


class LocalProgressRepo:
    def __init__(self):
        self.progress = {}


@pytest.fixture(scope='session')
def homework_service():
    service = HomeworkService()
    service.hw_repo = LocalHomeworkRepo()
    service.sol_repo = LocalSolutionRepo()
    service.prog_repo = LocalProgressRepo()
    return service


@pytest.fixture(scope='session')
def course_id():
    return uuid4()


@pytest.fixture(scope='session')
def student_id():
    return uuid4()

def test_create_homework(homework_service: HomeworkService, course_id):
    request = CreateHomeworkRequest(
        course_id=course_id,
        title='Test Homework',
        description='Test Description'
    )
    homework = homework_service.create_homework(request)
    assert homework.title == 'Test Homework'
    assert homework.course_id == course_id
    assert homework.status == HomeworkStatus.CREATED


def test_publish_homework(homework_service: HomeworkService, course_id):
    create_req = CreateHomeworkRequest(
        course_id=course_id,
        title='Homework to Publish',
        description='Description'
    )
    homework = homework_service.create_homework(create_req)

    publish_req = PublishHomeworkRequest(homework_id=homework.id)
    published_hw = homework_service.publish_homework(publish_req)

    assert published_hw.status == HomeworkStatus.ACTIVE
    assert published_hw.published_at is not None


def test_publish_homework_wrong_status(homework_service: HomeworkService, course_id):
    create_req = CreateHomeworkRequest(
        course_id=course_id,
        title='Already Published',
        description='Desc'
    )
    homework = homework_service.create_homework(create_req)

    publish_req = PublishHomeworkRequest(homework_id=homework.id)
    homework_service.publish_homework(publish_req)

    with pytest.raises(ValueError):
        homework_service.publish_homework(publish_req)


def test_submit_solution(homework_service: HomeworkService, course_id, student_id):
    create_req = CreateHomeworkRequest(
        course_id=course_id,
        title='Homework for Solution',
        description='Description'
    )
    homework = homework_service.create_homework(create_req)

    publish_req = PublishHomeworkRequest(homework_id=homework.id)
    homework_service.publish_homework(publish_req)

    solution_req = SubmitSolutionRequest(
        homework_id=homework.id,
        student_id=student_id,
        answer='My solution'
    )
    solution = homework_service.submit_solution(solution_req)

    assert solution.homework_id == homework.id
    assert solution.student_id == student_id
    assert solution.answer == 'My solution'