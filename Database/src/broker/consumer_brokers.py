from aio_pika import connect_robust
from src.settings.loggers.config import log
from src.settings.decorators.logs_decorators import debugs_decorator


class ConsumerRouter:
    def __init__(self, module):
        self.module = module
        self.consumer = Consumer(self)
    
    async def consumer_process(self, rmq_url: str, queue_name: str):
        await self.consumer.connection(rmq_url=rmq_url, consumers_queue_name=queue_name)

    async def consumer_callback(self, message, channel=None):
        await self.module.consumer_callback(message=message, channel=channel, )


class Consumer:
    def __init__(self, router):
        self.router = router

    @debugs_decorator
    async def connection(self, rmq_url, consumers_queue_name):
        try:
            connection = await connect_robust(rmq_url)
            log.info("Connected to RabbitMQ", rmq_url=rmq_url)

        except Exception as err:
            log.error("Failed to connect to RabbitMQ", RMQ=rmq_url, error=str(err))
            raise

        async with connection:
            try:
                channel = await connection.channel()
                queue = await channel.declare_queue(consumers_queue_name, durable=True)
            
            except Exception as err:
                log.error("Failed to create channel or queue", queue_name=consumers_queue_name, error=str(err))
                raise

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:

                    try: 
                        async with message.process():
                            log.info("The Database-service has been received a message", RMQ=rmq_url, queue=consumers_queue_name)
                            await self.router.consumer_callback(message=message, channel=channel)
                            

                    except Exception as err:
                        log.error("Unhandled exception", RMQ=rmq_url, queue=consumers_queue_name, delivery_tag=message.delivery_tag, error=str(err))
                        raise