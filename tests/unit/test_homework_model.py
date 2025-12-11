# tests/unit/test_homework_model.py

import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from app.models.homework import Homework, HomeworkStatus
from app.models.solution import Solution, SolutionStatus


@pytest.fixture()
def sample_homework_data():
    return {
        'id': uuid4(),
        'course_id': uuid4(),
        'title': 'Test Homework',
        'description': 'Test Description',
        'created_at': datetime.utcnow(),
        'published_at': None,
        'status': HomeworkStatus.CREATED
    }


def test_homework_creation(sample_homework_data):
    """Тест создания домашнего задания"""
    homework = Homework(**sample_homework_data)
    assert homework.id == sample_homework_data['id']
    assert homework.title == sample_homework_data['title']
    assert homework.status == HomeworkStatus.CREATED


def test_homework_title_required():
    """Тест обязательности поля title"""
    with pytest.raises(ValidationError):
        Homework(
            id=uuid4(),
            course_id=uuid4(),
            description='desc',
            created_at=datetime.utcnow(),
            status=HomeworkStatus.CREATED
        )


def test_homework_course_id_required():
    """Тест обязательности поля course_id"""
    with pytest.raises(ValidationError):
        Homework(
            id=uuid4(),
            title='title',
            description='desc',
            created_at=datetime.utcnow(),
            status=HomeworkStatus.CREATED
        )


def test_solution_creation():
    """Тест создания решения"""
    solution = Solution(
        id=uuid4(),
        homework_id=uuid4(),
        student_id=uuid4(),
        answer='My answer',
        status=SolutionStatus.DRAFT,
        created_at=datetime.utcnow()
    )
    assert solution.status == SolutionStatus.DRAFT
    assert solution.answer == 'My answer'


def test_solution_answer_required():
    """Тест обязательности поля answer"""
    with pytest.raises(ValidationError):
        Solution(
            id=uuid4(),
            homework_id=uuid4(),
            student_id=uuid4(),
            status=SolutionStatus.DRAFT,
            created_at=datetime.utcnow()
        )