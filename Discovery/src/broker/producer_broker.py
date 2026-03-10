import json
from aio_pika import connect_robust, Message, ExchangeType

from src.settings.loggers.config import log
from src.settings.decorators.logs_decorators import debugs_decorator


class ProducerRouter:
    def __init__(self, module):
        self.module = module
        self.producer = Producer()
    
    async def producer_load(self, rmq_url, message, queue_name):
        await self.producer.discovery_connect(rmq_url=rmq_url, queue_name=queue_name, message=message)
    
    async def producer_save(self, rmq_url, message, queue_name):
        await self.producer.discovery_connect(rmq_url=rmq_url, queue_name=queue_name, message=message)

    async def producer_response(self, rmq_url, message):
        await self.producer.discovery_connect(rmq_url=rmq_url, message=message['value'], correlation_id=message['correlation_id'], reply_to=message['reply_to'], rpc=True)


class Producer:
    async def get_connection(self, rmq_url):
        try:
            return await connect_robust(rmq_url)
        
        except Exception as err:
            log.error("Failed to connect to RabbitMQ", RMQ=rmq_url, error=str(err))
            raise

    @debugs_decorator
    async def send_message(self, rmq_url, queue_name: str, message: dict):
        connection = await self.get_connection(rmq_url=rmq_url)

        async with connection:
            try: 
                channel = await connection.channel()
                exchange = await channel.declare_exchange(
                    queue_name,
                    ExchangeType.DIRECT,
                    durable=True
                )
                queue = await channel.declare_queue(
                    queue_name,
                    durable=True
                )

            except Exception as err:
                log.error("Failed to create channel, exchange or queue", RMQ=self.rmq_url, queue_name=queue_name, error=str(err))
                raise
            

            message_body = Message(
                body=json.dumps(message).encode()
            )

            try:
                await queue.bind(
                    exchange, 
                    routing_key=queue_name
                )
                log.info("Queue was linked to the exchange", exchange=exchange.name)

                await exchange.publish(
                    message_body,
                    routing_key=queue.name  
                )
                log.info("Queue was linked to the exchange", exchange=exchange.name, routing_key=queue_name)
            except Exception as err:
                log.error("Exchange cannot send the message", RMQ=self.rmq_url, queue_name=queue_name, error=str(err))
                raise
    
    @debugs_decorator
    async def send_answer(self, rmq_url, message, correlation_id, reply_to):
        connection = await self.get_connection(rmq_url=rmq_url)
        
        async with connection:
            try:
                channel = await connection.channel()
                exchange = channel.default_exchange

            except Exception as err:
                log.error("Failed to create channel or exchange", RMQ=self.rmq_url, error=str(err))
                raise

            response = Message(
                body=json.dumps(message).encode(),
                correlation_id=correlation_id
            )

            try:
                await exchange.publish(
                    response,
                    routing_key=reply_to
                )

            except Exception as err:
                log.error("Exchange cannot send the message", RMQ=self.rmq_url, routing_key=reply_to, error=str(err))
                raise

    async def discovery_connect(self, rmq_url: str, message: dict, queue_name: str = None, correlation_id = None, reply_to = None, rpc: bool = False):
        if rpc:
            await self.send_answer(
                rmq_url=rmq_url,
                message=message,
                correlation_id=correlation_id,
                reply_to=reply_to
            )
            
        else:
            await self.send_message(
                rmq_url=rmq_url,
                queue_name=queue_name, 
                message=message
            )