import asyncio
import logging
from aio_pika import connect_robust
from app.settings import settings

logger = logging.getLogger(__name__)

async def consume():
    """Подключится к RabbitMQ с retry логикой"""
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to RabbitMQ (attempt {attempt + 1}/{max_retries})...")
            
            loop = asyncio.get_event_loop()
            connection = await connect_robust(
                settings.amqp_url, 
                loop=loop,
                timeout=10
            )
            
            async with connection:
                channel = await connection.channel()
                logger.info("✅ Successfully connected to RabbitMQ")
                
                # Здесь твой код обработки очередей
                # exchange = await channel.get_exchange('homework_exchange')
                # queue = await channel.get_queue('homework_queue')
                # Пример слушания очереди:
                # async with queue.iterator() as queue_iter:
                #     async for message in queue_iter:
                #         print(f"Message: {message}")
                
                # Просто слушаем бесконечно
                await asyncio.sleep(999999)
                
        except Exception as e:
            logger.error(f"❌ RabbitMQ connection error: {e}")
            
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("Max retries reached. RabbitMQ consumer will not start.")
                break


def start_rabbitmq_consumer():
    """Запустить RabbitMQ consumer в фоне"""
    import asyncio
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(consume())
        logger.info("Started RabbitMQ consuming for Homework Service")
    except Exception as e:
        logger.error(f"Failed to start RabbitMQ consumer: {e}")
