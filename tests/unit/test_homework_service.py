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

"""Unit tests for HomeworkService with LocalRepo (no database)"""

import pytest
from app.models.homework import Homework, Solution, HomeworkStatus
from app.services.homework_service import HomeworkService
from app.repositories.local_repo import LocalHomeworkRepository


@pytest.fixture
def local_repo():
    """Fixture providing LocalRepo instance (in-memory, no DB)"""
    return LocalHomeworkRepository()


@pytest.fixture
def service(local_repo):
    """Fixture providing HomeworkService with LocalRepo"""
    return HomeworkService(repository=local_repo)


class TestHomeworkServiceBasics:
    """Basic HomeworkService operations with LocalRepo"""

    def test_create_homework(self, service):
        """Test creating homework in memory"""
        hw = service.create_homework(
            title="Math Basics",
            description="Linear equations",
            course_id="course_1"
        )
        assert hw is not None
        assert hw.title == "Math Basics"
        assert hw.course_id == "course_1"
        assert hw.status == HomeworkStatus.DRAFT

    def test_publish_homework(self, service):
        """Test publishing homework (status change)"""
        hw = service.create_homework(
            title="Math",
            description="Equations",
            course_id="course_1"
        )

        published_hw = service.publish_homework(hw.id)
        assert published_hw is not None
        assert published_hw.status == HomeworkStatus.PUBLISHED

    def test_publish_homework_wrong_status(self, service):
        """Test cannot publish already published homework"""
        hw = service.create_homework(
            title="Math",
            description="Equations",
            course_id="course_1"
        )
        service.publish_homework(hw.id)

        with pytest.raises(ValueError) as exc_info:
            service.publish_homework(hw.id)
        assert "already published" in str(exc_info.value).lower()

    def test_submit_solution(self, service):
        """Test submitting solution to homework"""
        hw = service.create_homework(
            title="Math",
            description="Equations",
            course_id="course_1"
        )
        service.publish_homework(hw.id)

        solution = service.submit_solution(
            homework_id=hw.id,
            student_id="student_1",
            answer="2x = 4, x = 2"
        )

        assert solution is not None
        assert solution.answer == "2x = 4, x = 2"
        assert solution.student_id == "student_1"


class TestHomeworkServiceValidation:
    """Validation tests"""

    def test_homework_requires_title(self, service):
        """Test homework requires title"""
        with pytest.raises((ValueError, TypeError)):
            service.create_homework(
                title="",
                description="Test",
                course_id="course_1"
            )

    def test_homework_requires_course_id(self, service):
        """Test homework requires course_id"""
        with pytest.raises((ValueError, TypeError)):
            service.create_homework(
                title="Test",
                description="Test",
                course_id=""
            )

    def test_solution_requires_answer(self, service):
        """Test solution requires answer"""
        hw = service.create_homework(
            title="Test",
            description="Test",
            course_id="course_1"
        )
        service.publish_homework(hw.id)

        with pytest.raises((ValueError, TypeError)):
            service.submit_solution(
                homework_id=hw.id,
                student_id="student_1",
                answer=""
            )