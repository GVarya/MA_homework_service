# tests/unit/test_homework_service.py

import pytest
from uuid import uuid4
from datetime import datetime

from app.services.homework_service import HomeworkService
from app.models.homework import HomeworkStatus
from app.models.requests import CreateHomeworkRequest, PublishHomeworkRequest, SubmitSolutionRequest


@pytest.fixture(scope='session')
def homework_service():
    """Фикстура с сервисом (используем локальные репозитории)"""
    return HomeworkService()


@pytest.fixture(scope='session')
def course_id():
    return uuid4()


@pytest.fixture(scope='session')
def student_id():
    return uuid4()


def test_create_homework(homework_service: HomeworkService, course_id):
    """Тест создания домашнего задания"""
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
    """Тест публикации домашнего задания"""
    # Создаём домашку
    create_req = CreateHomeworkRequest(
        course_id=course_id,
        title='Homework to Publish',
        description='Description'
    )
    homework = homework_service.create_homework(create_req)
    
    # Публикуем
    publish_req = PublishHomeworkRequest(homework_id=homework.id)
    published_hw = homework_service.publish_homework(publish_req)
    
    assert published_hw.status == HomeworkStatus.ACTIVE
    assert published_hw.published_at is not None


def test_publish_homework_wrong_status(homework_service: HomeworkService, course_id):
    """Тест ошибки при публикации уже опубликованной домашки"""
    create_req = CreateHomeworkRequest(
        course_id=course_id,
        title='Already Published',
        description='Desc'
    )
    homework = homework_service.create_homework(create_req)
    
    # Публикуем первый раз
    publish_req = PublishHomeworkRequest(homework_id=homework.id)
    homework_service.publish_homework(publish_req)
    
    # Пробуем опубликовать второй раз
    with pytest.raises(ValueError):
        homework_service.publish_homework(publish_req)


def test_submit_solution(homework_service: HomeworkService, course_id, student_id):
    """Тест отправки решения"""
    # Создаём и публикуем домашку
    create_req = CreateHomeworkRequest(
        course_id=course_id,
        title='Homework for Solution',
        description='Description'
    )
    homework = homework_service.create_homework(create_req)
    publish_req = PublishHomeworkRequest(homework_id=homework.id)
    homework_service.publish_homework(publish_req)
    
    # Отправляем решение
    solution_req = SubmitSolutionRequest(
        homework_id=homework.id,
        student_id=student_id,
        answer='My solution'
    )
    solution = homework_service.submit_solution(solution_req)
    
    assert solution.homework_id == homework.id
    assert solution.student_id == student_id
    assert solution.answer == 'My solution'


# """Unit tests for HomeworkService with full mocking"""

# import pytest
# from uuid import uuid4
# from datetime import datetime
# from unittest.mock import patch, MagicMock

# from app.models.homework import Homework, HomeworkStatus
# from app.models.solution import Solution, SolutionStatus
# from app.models.requests import (
#     CreateHomeworkRequest,
#     PublishHomeworkRequest,
#     SubmitSolutionRequest
# )
# from app.services.homework_service import HomeworkService


# class TestHomeworkServiceBasics:
#     """Basic HomeworkService operations with full mocking"""

#     @patch('app.services.homework_service.HomeworkService.hw_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.sol_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.prog_repo', new_callable=MagicMock)
#     def test_create_homework(self, mock_progress, mock_sol, mock_hw):
#         """Test creating homework"""
#         hw_id = uuid4()
#         course_id = uuid4()

#         mock_hw_obj = Homework(
#             id=hw_id,
#             course_id=course_id,
#             title="Math Basics",
#             description="Linear equations",
#             status=HomeworkStatus.CREATED,
#             created_at=datetime.utcnow()
#         )
#         mock_hw.create_homework.return_value = mock_hw_obj

#         service = HomeworkService()
#         service.hw_repo = mock_hw
#         service.sol_repo = mock_sol
#         service.prog_repo = mock_progress

#         request = CreateHomeworkRequest(
#             title="Math Basics",
#             description="Linear equations",
#             course_id=course_id
#         )
#         hw = service.create_homework(request)

#         assert hw is not None
#         assert hw.title == "Math Basics"
#         assert hw.status == HomeworkStatus.CREATED

#     @patch('app.services.homework_service.HomeworkService.hw_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.sol_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.prog_repo', new_callable=MagicMock)
#     def test_publish_homework(self, mock_progress, mock_sol, mock_hw):
#         """Test publishing homework"""
#         hw_id = uuid4()
#         course_id = uuid4()

#         mock_hw_obj = Homework(
#             id=hw_id,
#             course_id=course_id,
#             title="Math",
#             description="Equations",
#             status=HomeworkStatus.ACTIVE,
#             published_at=datetime.utcnow(),
#             created_at=datetime.utcnow()
#         )
#         mock_hw.get_homework_by_id.return_value = mock_hw_obj
#         mock_hw.publish_homework.return_value = mock_hw_obj

#         service = HomeworkService()
#         service.hw_repo = mock_hw
#         service.sol_repo = mock_sol
#         service.prog_repo = mock_progress

#         publish_req = PublishHomeworkRequest(homework_id=hw_id)
#         published_hw = service.publish_homework(publish_req)

#         assert published_hw is not None
#         assert published_hw.status == HomeworkStatus.ACTIVE

#     @patch('app.services.homework_service.HomeworkService.hw_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.sol_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.prog_repo', new_callable=MagicMock)
#     def test_list_homeworks(self, mock_progress, mock_sol, mock_hw):
#         """Test listing all homeworks"""
#         course_id = uuid4()

#         mock_homeworks = [
#             Homework(
#                 id=uuid4(),
#                 course_id=course_id,
#                 title="HW1",
#                 description="First",
#                 status=HomeworkStatus.CREATED,
#                 created_at=datetime.utcnow()
#             ),
#             Homework(
#                 id=uuid4(),
#                 course_id=uuid4(),
#                 title="HW2",
#                 description="Second",
#                 status=HomeworkStatus.CREATED,
#                 created_at=datetime.utcnow()
#             )
#         ]
#         mock_hw.get_homeworks.return_value = mock_homeworks

#         service = HomeworkService()
#         service.hw_repo = mock_hw
#         service.sol_repo = mock_sol
#         service.prog_repo = mock_progress

#         homeworks = service.get_homeworks()
#         assert len(homeworks) >= 2

#     @patch('app.services.homework_service.HomeworkService.hw_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.sol_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.prog_repo', new_callable=MagicMock)
#     def test_get_homeworks_by_course(self, mock_progress, mock_sol, mock_hw):
#         """Test retrieving homeworks by course"""
#         course_id = uuid4()

#         mock_homeworks = [
#             Homework(
#                 id=uuid4(),
#                 course_id=course_id,
#                 title=f"Test {i}",
#                 description=f"Test desc {i}",
#                 status=HomeworkStatus.CREATED,
#                 created_at=datetime.utcnow()
#             )
#             for i in range(2)
#         ]
#         mock_hw.get_homeworks_by_course.return_value = mock_homeworks

#         service = HomeworkService()
#         service.hw_repo = mock_hw
#         service.sol_repo = mock_sol
#         service.prog_repo = mock_progress

#         homeworks = service.get_homeworks_by_course(course_id)
#         assert len(homeworks) >= 2


# class TestHomeworkServiceValidation:
#     """Validation tests"""

#     def test_homework_requires_title(self):
#         """Test that homework requires title"""
#         with pytest.raises((ValueError, TypeError)):
#             request = CreateHomeworkRequest(
#                 title="",
#                 description="Test",
#                 course_id=uuid4()
#             )

#     def test_homework_requires_course_id(self):
#         """Test that homework requires course_id"""
#         with pytest.raises((ValueError, TypeError)):
#             request = CreateHomeworkRequest(
#                 title="Test",
#                 description="Test",
#                 course_id=None
#             )


# class TestHomeworkServiceWorkflow:
#     """End-to-end workflow tests with mocks"""

#     @patch('app.services.homework_service.HomeworkService.hw_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.sol_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.prog_repo', new_callable=MagicMock)
#     def test_complete_homework_workflow(self, mock_progress, mock_sol, mock_hw):
#         """Test complete workflow: create → publish → submit"""
#         course_id = uuid4()
#         student_id = uuid4()
#         hw_id = uuid4()

#         # Mock create
#         mock_hw_create = Homework(
#             id=hw_id,
#             course_id=course_id,
#             title="Python Basics",
#             description="Write a function",
#             status=HomeworkStatus.CREATED,
#             created_at=datetime.utcnow()
#         )
#         mock_hw.create_homework.return_value = mock_hw_create

#         service = HomeworkService()
#         service.hw_repo = mock_hw
#         service.sol_repo = mock_sol
#         service.prog_repo = mock_progress

#         create_req = CreateHomeworkRequest(
#             title="Python Basics",
#             description="Write a function",
#             course_id=course_id
#         )
#         hw = service.create_homework(create_req)
#         assert hw.status == HomeworkStatus.CREATED

#         # Mock publish
#         published_hw = Homework(
#             id=hw_id,
#             course_id=course_id,
#             title="Python Basics",
#             description="Write a function",
#             status=HomeworkStatus.ACTIVE,
#             published_at=datetime.utcnow(),
#             created_at=datetime.utcnow()
#         )
#         mock_hw.get_homework_by_id.return_value = published_hw
#         mock_hw.publish_homework.return_value = published_hw

#         publish_req = PublishHomeworkRequest(homework_id=hw_id)
#         published = service.publish_homework(publish_req)
#         assert published.status == HomeworkStatus.ACTIVE

#         # Mock submit solution
#         mock_solution = Solution(
#             id=uuid4(),
#             homework_id=hw_id,
#             student_id=student_id,
#             answer="def hello(): return 'Hello'",
#             status=SolutionStatus.SUBMITTED,
#             created_at=datetime.utcnow()
#         )
#         mock_sol.submit_solution.return_value = mock_solution

#         solution_req = SubmitSolutionRequest(
#             homework_id=hw_id,
#             student_id=student_id,
#             answer="def hello(): return 'Hello'"
#         )
#         solution = service.submit_solution(solution_req)
#         assert solution.homework_id == hw_id

#     @patch('app.services.homework_service.HomeworkService.hw_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.sol_repo', new_callable=MagicMock)
#     @patch('app.services.homework_service.HomeworkService.prog_repo', new_callable=MagicMock)
#     def test_multiple_homeworks_independence(self, mock_progress, mock_sol, mock_hw):
#         """Test that multiple homeworks are independent"""
#         course1_id = uuid4()
#         course2_id = uuid4()

#         hw1 = Homework(
#             id=uuid4(),
#             course_id=course1_id,
#             title="HW1",
#             description="First",
#             status=HomeworkStatus.ACTIVE,
#             published_at=datetime.utcnow(),
#             created_at=datetime.utcnow()
#         )
#         hw2 = Homework(
#             id=uuid4(),
#             course_id=course2_id,
#             title="HW2",
#             description="Second",
#             status=HomeworkStatus.CREATED,
#             created_at=datetime.utcnow()
#         )
#         mock_hw.get_homeworks.return_value = [hw1, hw2]

#         service = HomeworkService()
#         service.hw_repo = mock_hw
#         service.sol_repo = mock_sol
#         service.prog_repo = mock_progress

#         homeworks = service.get_homeworks()

#         hw2_retrieved = next((h for h in homeworks if h.id == hw2.id), None)
#         assert hw2_retrieved is not None
#         assert hw2_retrieved.status == HomeworkStatus.CREATED