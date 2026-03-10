from aio_pika import connect_robust

from src.settings.loggers.config import log
from src.settings.decorators.logs_decorators import debugs_decorator


class Router:
    def __init__(self, module):
        self.consumer = Consumer(self)
        self.module = module
        
    async def consumer_process(self, rmq_url: str, queue_name: str):
        await self.consumer.connection(rmq_url=rmq_url, queue_name=queue_name)

    async def consumer_callback(self, message):
        await self.module.consumer_callback(message=message)


class Consumer:
    def __init__(self, router):
        self.router = router
    
    @debugs_decorator
    async def connection(self, rmq_url: str, queue_name: str):
        try:
            connection = await connect_robust(rmq_url)
            log.info("Connected to RabbitMQ", rmq_url=rmq_url)

        except Exception as err:
            log.error("Failed to connect to RabbitMQ", RMQ=rmq_url, error=str(err))
            raise

        async with connection:
            try:
                channel = await connection.channel()
                exchange = await channel.declare_exchange(
                    queue_name, 
                    durable=True
                )
                queue = await channel.declare_queue(
                    queue_name,
                    durable=True    
                )
                log.info("Queue declared successfully", queue_name=queue_name)
            except Exception as err:
                log.error("Failed to create channel or queue", queue_name=queue_name, error=str(err))
                raise
            
            await queue.bind(exchange, routing_key=queue_name)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:

                    try:
                        async with message.process():
                            log.info("The Importer has been received a message", message=message.body.decode())
                            await self.router.consumer_callback(message=message.body.decode())
                            
                    except Exception as err:
                        log.error("Unhandled exception", message=message.body.decode(), delivery_tag=message.delivery_tag, error=str(err))
                        raise