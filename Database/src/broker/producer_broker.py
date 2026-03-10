import json

from aio_pika import connect_robust, Message, IncomingMessage

from src.settings.loggers.config import log
from src.settings.decorators.logs_decorators import debugs_decorator


class ProducerRouter:
    def __init__(self, module):
        self.module = module
        self.producer = Producer(router=self)

    async def producer_process(self, rmq_url, message, queue_name):
        await self.producer.connection_cache(rmq_url=rmq_url, message=message, queue_name=queue_name)

    async def producer_reply(self, channel, message, message_reply):
        await self.producer.connection_reply(channel=channel, message=message, message_reply=message_reply)


class Producer:
    def __init__(self, router):
        self.router = router

    @debugs_decorator
    async def connection_cache(self, rmq_url, message, queue_name: str):
        try:
            connection = await connect_robust(rmq_url)
            log.info("Connected to RabbitMQ", rmq_url=rmq_url)

        except Exception as err:
            log.error("Failed to connect to RabbitMQ", RMQ=rmq_url, error=str(err))
            raise

        async with connection:
            try:
                channel = await connection.channel()
                queue = await channel.declare_exchange(
                    queue_name, 
                    durable=True
                )
            
            except Exception as err:
                log.error("Failed to create channel or queue", queue_name=queue_name, error=str(err))
                raise

            message_body = Message(
                body=json.dumps(message).encode()
            )
            
            try:
                await queue.publish(
                    message_body,
                    routing_key=queue_name   
                )

            except Exception as err:
                log.error("Unhandled exception", msg=message_body, error=str(err))
                raise
        
    @debugs_decorator
    async def connection_reply(self, message, message_reply: IncomingMessage, channel):
            try:
                exchange = channel.default_exchange

            except Exception as err:
                log.error("Failed to create exchange", queue_name=exchange.name, error=str(err))
                raise
            
            response = Message(
                body=json.dumps(message).encode(),
                correlation_id=message_reply.correlation_id
            )

            try:
                await exchange.publish(
                    response,
                    routing_key=message_reply.reply_to
                )

            except Exception as err:
                log.error("Unhandled exception", msg=response, error=str(err))
                raise
