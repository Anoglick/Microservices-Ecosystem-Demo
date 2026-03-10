import json
import asyncio
import uuid

from aio_pika import ExchangeType, IncomingMessage, connect_robust, Message
from src.settings.decorators.logs_decorators import debugs_decorator
from src.settings.loggers.config import log


class ProducerRouter:
    def __init__(self, module):
        self.module = module
        self.producer = Producer(self)
    
    async def producer_process(self, message, rmq_url, queue, action):
        if action == 'pull_request':
            method="rpc"
            message.update({method: True})
            return await self.producer.connection_queue(rmq_url=rmq_url, queue_name=queue.PRODUCERS_DATABASE_QUEUE, message=message, method=method)
        else:
            await self.producer.connection_queue(rmq_url=rmq_url, queue_name=queue.PRODUCERS_CACHE_QUEUE, message=message)


class Producer:
    def __init__(self, router):
        self.router = router
    
    @debugs_decorator
    async def rpc(self, message, rmq_url: str, queue_name: str, timeout: float = 5.0):
        try:
            connection = await connect_robust(rmq_url)
        
        except Exception as err:
            log.error("Failed to connect to RabbitMQ", RMQ=rmq_url, error=str(err))
            raise

        async with connection:
            try:
                channel = await connection.channel()
                callback_queue = await channel.declare_queue(
                    exclusive=True
                )
            except Exception as err:
                log.error("Failed to create channel or queue", RMQ=rmq_url, error=str(err))
                raise
            
            correlation_id = str(uuid.uuid4())
            future = asyncio.get_event_loop().create_future()

            async def on_response(msg: IncomingMessage):
                if msg.correlation_id == correlation_id:
                    try:
                        body = json.loads(msg.body.decode())
                        future.set_result(body)
                    except Exception as err:
                        log.error("Invalid response body", error=str(err))
                        raise
            
            await callback_queue.consume(on_response)

            msg = Message(
                body=json.dumps(message).encode(),
                reply_to=callback_queue.name,
                correlation_id=correlation_id
            )

            try:
                await channel.default_exchange.publish(
                    msg,
                    routing_key=queue_name
                )
                
                return await asyncio.wait_for(future, timeout=timeout)
            
            except asyncio.TimeoutError as err:
                log.error("RPC call timed out", correlation_id=correlation_id)
                raise
    
    @debugs_decorator
    async def default_queue(self, message, rmq_url: str, queue_name: str,):
        try:
            connection = await connect_robust(rmq_url)
        
        except Exception as err:
            log.error("Failed to connect to RabbitMQ", RMQ=rmq_url, error=str(err))
            raise

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
                log.error("Failed to create channel, exchange or queue", RMQ=rmq_url, queue_name=queue_name, error=str(err))
                raise
            
            message_body = Message(
                body=json.dumps(message).encode()
            )

            try:
                await queue.bind(exchange, routing_key=queue_name)
                await exchange.publish(
                    message_body,
                    routing_key=queue.name  
                )
            except:
                ...

    async def connection_queue(self, message, rmq_url, queue_name: str, method: str = 'default'):
        if method == 'rpc':
            return await self.rpc(
                rmq_url=rmq_url,
                message=message,
                queue_name=queue_name
            )
        
        await self.default_queue(
            rmq_url=rmq_url,
            message=message,
            queue_name=queue_name
        )