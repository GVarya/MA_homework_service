# hw_service/app/repositories/homework_repo.py
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.homework import Homework, HomeworkStatus
from app.schemas.homework import Homework as DBHomework

class HomeworkRepo:
    def __init__(self) -> None:
        self.db: Session = next(get_db())

    def get_homeworks(self) -> list[Homework]:
        return [Homework.from_orm(h) for h in self.db.query(DBHomework).all()]

    def get_homeworks_by_course(self, course_id: UUID) -> list[Homework]:
        return [
            Homework.from_orm(h)
            for h in self.db.query(DBHomework)
            .filter(DBHomework.course_id == course_id)
            .all()
        ]

    def get_homework_by_id(self, id: UUID) -> Homework:
        h = (
            self.db.query(DBHomework)
            .filter(DBHomework.id == id)
            .first()
        )
        if h is None:
            raise KeyError
        return Homework.from_orm(h)

    def create_homework(self, homework: Homework) -> Homework:
        db_obj = DBHomework(
            id=homework.id,
            course_id=homework.course_id,
            title=homework.title,
            description=homework.description,
            created_at=homework.created_at,
            published_at=homework.published_at,
            status=homework.status,
        )
        self.db.add(db_obj)
        self.db.commit()
        return homework

    def set_status(self, id: UUID, status: HomeworkStatus) -> Homework:
        db_obj = (
            self.db.query(DBHomework)
            .filter(DBHomework.id == id)
            .first()
        )
        if db_obj is None:
            raise KeyError
        db_obj.status = status
        self.db.commit()
        self.db.refresh(db_obj)
        return Homework.from_orm(db_obj)

    def publish_homework(self, id: UUID) -> Homework:
        db_obj = (
            self.db.query(DBHomework)
            .filter(DBHomework.id == id)
            .first()
        )
        if db_obj is None:
            raise KeyError
        db_obj.status = HomeworkStatus.ACTIVE
        db_obj.published_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_obj)
        return Homework.from_orm(db_obj)

    def activate_by_course(self, course_id: UUID) -> list[Homework]:
        homeworks = (
            self.db.query(DBHomework)
            .filter(DBHomework.course_id == course_id)
            .filter(DBHomework.status == HomeworkStatus.CREATED)
            .all()
        )
        for hw in homeworks:
            hw.status = HomeworkStatus.ACTIVE
            hw.published_at = datetime.utcnow()
        self.db.commit()
        return [Homework.from_orm(h) for h in homeworks]
