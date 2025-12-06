import asyncio
from fastapi import FastAPI

from app.endpoints.homework_router import router as homework_router
from app import rabbitmq

app = FastAPI(title="Homework Service")

@app.on_event("startup")
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))

app.include_router(homework_router, prefix="/api")

