import json
from typing import Any
import uuid

import asyncio
from aio_pika import (
    IncomingMessage, 
    Message, 
    ExchangeType, 
    DeliveryMode,
    connect_robust
)

from src.settings.decorators.handlers_decorators import converter
from src.settings.decorators.logs_decorators import debugs_decorator
from src.settings.loggers.config import log
from src.settings.schemas.models_schemas import RequestDict


class ProducerRouter:
    def __init__(self, module):
        self.producer = Producer()
        self.module = module
    
    async def request_importer(self, queue_name: str, rmq_url: str, url: str):
        return await self.producer.connection_importer(queue_name=queue_name, rmq_url=rmq_url, url=url)

    @converter
    async def request_discovery(
        self, 
        method: str, 
        request: RequestDict, 
        tag: str, 
        route: str, 
        queue_name: str, 
        rmq_url: str, 
        timeout: int | float,
        message: dict = None
    ):
        return await self.producer.connection_discovery(
            message=message, 
            queue_name=queue_name, 
            rmq_url=rmq_url, 
            timeout=timeout
        )

class Producer:
    @debugs_decorator
    async def connection_importer(self, queue_name: str, rmq_url: str, url: str):
        try:
            connection = await connect_robust(rmq_url)
            log.info("Connected to RabbitMQ", rmq_url=rmq_url)

        except Exception as err:
            log.error("Failed to connect to RabbitMQ", RMQ_URL=rmq_url, error=str(err))
            raise

        async with connection:
            try:
                channel = await connection.channel()
                exchange = await channel.declare_exchange(
                    queue_name,
                    ExchangeType.DIRECT,
                    durable=True
                )

            except Exception as err:
                log.error("Failed to create channel or queue", queue_name=queue_name, error=str(err))
                raise

            msg = Message(
                body=url.encode(),
                delivery_mode=DeliveryMode.PERSISTENT
            )

            try:
                await exchange.publish(
                    msg,
                    routing_key=queue_name   
                )

            except Exception as err:
                log.error("Unhandled exception", msg=msg, error=str(err))
                raise
            
            return {
                "message": f"Request for {url} sent",
                "status": 200
            }

    @debugs_decorator
    async def connection_discovery(self, message: Any, queue_name: str, rmq_url: str, timeout: int | float):
        try:
            connection = await connect_robust(rmq_url)
            log.info("Connected to RabbitMQ", rmq_url=rmq_url)

        except Exception as err:
            log.error("Failed to connect to RabbitMQ", RMQ=rmq_url, error=str(err))
            raise


        async with connection:
            try:
                channel = await connection.channel()
                callback_queue = await channel.declare_queue(
                    durable=True,
                    exclusive=True
                )

            except Exception as err:
                log.error("Failed to create channel or queue", error=str(err))
                raise
            
            correlation_id = str(uuid.uuid4())
            future = asyncio.get_event_loop().create_future()

            async def on_response(msg: IncomingMessage):
                if msg.correlation_id == correlation_id:
                    try:
                        body = json.loads(msg.body.decode())
                        future.set_result(body)
                        
                    except Exception as err:
                        log.error("Invalid response body", error=str(err), raw=msg.body)
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