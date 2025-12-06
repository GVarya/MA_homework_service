import json
import traceback
from asyncio import AbstractEventLoop

from aio_pika import connect_robust, IncomingMessage
from aio_pika.abc import AbstractRobustConnection

from app.settings import settings
from app.services.homework_service import HomeworkService

async def process_payment_success(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        course_id = data["course_id"]
        student_id = data["student_id"]
        
        service = HomeworkService()
        
        service.activate_homeworks_by_course(course_id)
        
        print(f"Activated homeworks for course {course_id}, student {student_id}")
        
        await msg.ack()
    except Exception as e:
        print(f"Error processing payment: {e}")
        traceback.print_exc()
        await msg.ack()

async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    queue = await channel.declare_queue(
        "payment_success_queue",
        durable=True,
    )
    await queue.consume(process_payment_success)
    print("Started RabbitMQ consuming for Homework Service")

    return connection
