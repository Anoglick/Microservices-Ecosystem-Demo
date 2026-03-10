import asyncio
from aio_pika import connect_robust

from src.settings.loggers.config import log
from src.settings.decorators.logs_decorators import debugs_decorator


class ConsumerRouter:
    def __init__(self, module):
        self.module = module
    
    async def consumer_process(self, rmq_url, queue_names):
        await Consumer(router=self, rmq_url=rmq_url).connection(queue_names=queue_names)
    
    async def consumer_callback(self, message, answer: bool = False):
        await self.module.consumer_callback(message=message, answer=answer)


class Consumer:
    def __init__(self, router, rmq_url):
        self.router = router
        self.rmq_url = rmq_url

    @debugs_decorator
    async def consume_queue(self, consumers_queue_name):
        try:
            connection = await connect_robust(self.rmq_url)
            log.info("Connected to RabbitMQ", rmq_url=self.rmq_url)

        except Exception as err:
            log.error("Failed to connect to RabbitMQ", RMQ=self.rmq_url, error=str(err))
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
                            log.info("The Discovery has been received a message", RMQ=self.rmq_url, queue=consumers_queue_name)

                            if consumers_queue_name == 'discovery':
                                await self.router.consumer_callback(message, answer=True)
                            else:
                                await self.router.consumer_callback(message)
                            

                    except Exception as err:
                        log.error("Unhandled exception", delivery_tag=message.delivery_tag, error=str(err))
                        raise

    async def connection(self, queue_names):
        await asyncio.gather(
            *[
                self.consume_queue(name)
                for name in queue_names
            ]
        )