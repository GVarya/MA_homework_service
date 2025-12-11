import asyncio
from fastapi import FastAPI
from app.endpoints.homework_router import router as homework_router
from app import rabbitmq
from app.database import init_db

app = FastAPI(title="Homework Service")

@app.on_event("startup")
async def startup():
    """Инициализация при запуске приложения"""
    # Инициализируем БД
    init_db()
    
    # Запускаем RabbitMQ consumer в фоне
    asyncio.create_task(rabbitmq.consume())

app.include_router(homework_router, prefix="/api")