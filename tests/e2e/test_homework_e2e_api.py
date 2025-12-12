import pytest
import requests
from uuid import uuid4

BASE_URL = "http://localhost:8000/api"

@pytest.fixture(scope="session")
def course_id():
    return str(uuid4())

@pytest.fixture(scope="session")
def student_id():
    return str(uuid4())


def test_get_homeworks_list():
    """Список домашних заданий возвращается и это список."""
    resp = requests.get(f"{BASE_URL}/homeworks/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_create_homework(course_id):
    """Создание домашнего задания."""
    payload = {
        "course_id": course_id,
        "title": "E2E Homework",
        "description": "Created from e2e test",
    }
    resp = requests.post(f"{BASE_URL}/homeworks/", json=payload)
    # роутер не задаёт явный статус-код, FastAPI по умолчанию вернёт 200
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["course_id"] == course_id
    assert data["status"].lower() == "created"



def test_publish_homework(course_id):
    """Публикация домашки меняет статус на active."""
    # 1. создаём
    payload = {
        "course_id": course_id,
        "title": "To publish",
        "description": "Publish me",
    }
    create_resp = requests.post(f"{BASE_URL}/homeworks/", json=payload)
    assert create_resp.status_code in (200, 201)
    hw = create_resp.json()
    hw_id = hw["id"]

    # 2. публикуем
    pub_resp = requests.post(
        f"{BASE_URL}/homeworks/publish",
        json={"homework_id": hw_id},
    )
    assert pub_resp.status_code == 200
    published = pub_resp.json()
    assert published["id"] == hw_id
    assert published["status"].lower() == "active"
    assert published["published_at"] is not None


def test_submit_solution(course_id, student_id):
    """Отправка решения по опубликованной домашке."""
    # 1. создаём и публикуем домашку
    payload = {
        "course_id": course_id,
        "title": "Homework with solution",
        "description": "Desc",
    }
    create_resp = requests.post(f"{BASE_URL}/homeworks/", json=payload)
    assert create_resp.status_code in (200, 201)
    hw_id = create_resp.json()["id"]

    pub_resp = requests.post(
        f"{BASE_URL}/homeworks/publish",
        json={"homework_id": hw_id},
    )
    assert pub_resp.status_code == 200

    # 2. отправляем решение
    sol_payload = {
        "homework_id": hw_id,
        "student_id": student_id,
        "answer": "My e2e solution",
    }
    sol_resp = requests.post(
        f"{BASE_URL}/homeworks/solutions/submit",
        json=sol_payload,
    )
    assert sol_resp.status_code in (200, 201)
    sol = sol_resp.json()
    assert str(sol["homework_id"]) == hw_id or sol["homework_id"] == hw_id
    assert str(sol["student_id"]) == student_id or sol["student_id"] == student_id
    assert sol["answer"] == sol_payload["answer"]


def test_get_solutions_by_homework(course_id, student_id):
    """Получение всех решений по домашке."""
    # 1. создаём и публикуем домашку
    payload = {
        "course_id": course_id,
        "title": "Homework for solutions list",
        "description": "Desc",
    }
    create_resp = requests.post(f"{BASE_URL}/homeworks/", json=payload)
    assert create_resp.status_code in (200, 201)
    hw_id = create_resp.json()["id"]

    pub_resp = requests.post(
        f"{BASE_URL}/homeworks/publish",
        json={"homework_id": hw_id},
    )
    assert pub_resp.status_code == 200

    # 2. отправляем хотя бы одно решение
    sol_payload = {
        "homework_id": hw_id,
        "student_id": student_id,
        "answer": "Solution for list",
    }
    sol_resp = requests.post(
        f"{BASE_URL}/homeworks/solutions/submit",
        json=sol_payload,
    )
    assert sol_resp.status_code in (200, 201)

    # 3. забираем решения
    list_resp = requests.get(
        f"{BASE_URL}/homeworks/solutions/homework/{hw_id}"
    )
    assert list_resp.status_code == 200
    sols = list_resp.json()
    assert isinstance(sols, list)
    assert any(s["answer"] == "Solution for list" for s in sols)
