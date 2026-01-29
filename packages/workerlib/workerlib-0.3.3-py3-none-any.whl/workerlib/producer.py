import json
import logging
import asyncio
from typing import Any, Dict, List, Optional

import aio_pika
from aio_pika.exceptions import AMQPConnectionError

from .connection import RabbitMQConnection
from .mq_queue import RabbitMQQueue

logger = logging.getLogger(__name__)


class RabbitMQProducer:
    def __init__(
            self,
            connection: RabbitMQConnection,
            queue: RabbitMQQueue,
            send_retries: int = 3,
            retry_delay: float = 1.0,
            enable_auto_reconnect: bool = True
    ) -> None:
        self.connection = connection
        self.queue = queue
        self.send_retries = send_retries
        self.retry_delay = retry_delay
        self.enable_auto_reconnect = enable_auto_reconnect
        self.metrics = {
            "sent": 0,
            "failed": 0,
            "retried": 0
        }

    async def _ensure_connection(self) -> None:
        if not await self.connection.is_healthy():
            if self.enable_auto_reconnect:
                logger.warning("Connection lost, attempting to reconnect...")
                await self.connection.reconnect()
            else:
                raise ConnectionError("Connection is not available")

    async def send_with_retry(
            self,
            data: Dict[str, Any],
            max_retries: Optional[int] = None,
            retry_delay: Optional[float] = None,
            **kwargs
    ) -> bool:
        max_retries = max_retries or self.send_retries
        retry_delay = retry_delay or self.retry_delay
        last_exception = None

        for attempt in range(max_retries):
            try:
                await self.send(data, **kwargs)
                return True

            except (AMQPConnectionError, ConnectionError) as e:
                last_exception = e
                self.metrics["retried"] += 1

                if attempt == max_retries - 1:
                    logger.error(f"Failed to send after {max_retries} attempts: {e}")
                    break

                logger.warning(
                    f"Connection error on send attempt {attempt + 1}/{max_retries}. "
                    f"Retrying in {retry_delay}s... Error: {e}"
                )

                await asyncio.sleep(retry_delay)

                if self.enable_auto_reconnect:
                    try:
                        await self.connection.reconnect()
                        logger.info("Reconnected successfully")
                    except Exception as reconnect_error:
                        logger.error(f"Failed to reconnect: {reconnect_error}")

        self.metrics["failed"] += 1
        if last_exception:
            raise last_exception
        return False

    async def send(self, data: Dict[str, Any], **kwargs) -> None:
        await self._ensure_connection()

        try:
            queue_obj = await self.queue.get_queue()
            body = json.dumps(data).encode()

            message = aio_pika.Message(
                body=body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json",
                **kwargs
            )

            channel = self.connection.channel
            exchange = channel.default_exchange

            await exchange.publish(
                message,
                routing_key=queue_obj.name
            )

            self.metrics["sent"] += 1
            logger.debug(f"Message sent to queue {queue_obj.name}")

        except Exception as e:
            self.metrics["failed"] += 1
            logger.error(f"Failed to send message: {e}")
            raise

    async def send_raw(self, body: bytes, **kwargs) -> None:
        await self._ensure_connection()

        try:
            queue_obj = await self.queue.get_queue()
            message = aio_pika.Message(body=body, **kwargs)

            channel = self.connection.channel
            exchange = channel.default_exchange
            await exchange.publish(
                message,
                routing_key=queue_obj.name
            )

            self.metrics["sent"] += 1
            logger.debug(f"Raw message sent to queue {queue_obj.name}")

        except Exception as e:
            self.metrics["failed"] += 1
            logger.error(f"Failed to send raw message: {e}")
            raise

    async def send_batch(self, messages: List[Dict[str, Any]]) -> None:
        await self._ensure_connection()

        queue_obj = await self.queue.get_queue()
        channel = self.connection.channel
        exchange = channel.default_exchange
        sent_count = 0

        for data in messages:
            try:
                body = json.dumps(data).encode()
                message = aio_pika.Message(
                    body=body,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    content_type="application/json"
                )
                await exchange.publish(message, routing_key=queue_obj.name)
                sent_count += 1

            except Exception as e:
                logger.error(f"Failed to send message in batch: {e}")

        self.metrics["sent"] += sent_count
        logger.info(f"Sent {sent_count}/{len(messages)} messages to queue {queue_obj.name}")
