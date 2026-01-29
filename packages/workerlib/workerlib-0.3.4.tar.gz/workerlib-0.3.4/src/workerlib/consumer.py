import asyncio
import json
import logging
import time
from enum import Enum
from typing import Callable, Awaitable, Optional, Dict, Any

import aio_pika
from aiormq.exceptions import AMQPConnectionError

from .mq_queue import RabbitMQQueue
from .retry import retry_on_failure, RetryConfig

logger = logging.getLogger(__name__)


class ErrorHandlingStrategy(Enum):
    IGNORE = "ignore"
    REQUEUE_END = "requeue_end"
    REQUEUE_FRONT = "requeue_front"
    DLQ = "dlq"


class RabbitMQConsumer:
    def __init__(
            self,
            queue: RabbitMQQueue,
            handler: Callable[[Dict[str, Any]], Awaitable[bool]],
            error_strategy: ErrorHandlingStrategy = ErrorHandlingStrategy.DLQ,
            retry_config: Optional[RetryConfig] = None,
            dlq_enabled: bool = True,
            requeue_delay: float = 5.0
    ) -> None:
        self.queue = queue
        self.handler = handler
        self.error_strategy = error_strategy
        self.retry_config = retry_config or RetryConfig()
        self.dlq_enabled = dlq_enabled
        self.requeue_delay = requeue_delay

        self.metrics = {
            "processed": 0,
            "failed": 0,
            "requeued": 0,
            "dlq_moved": 0,
            "ignored": 0,
            "ack_failed": 0,
            "nack_failed": 0
        }

    async def _safe_ack(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        try:
            await message.ack()
        except AMQPConnectionError:
            self.metrics["ack_failed"] += 1
            logger.warning("Connection lost during ack, ignoring")

    async def _safe_nack(self, message: aio_pika.abc.AbstractIncomingMessage, *, requeue: bool = True) -> None:
        try:
            await message.nack(requeue=requeue)
        except AMQPConnectionError:
            self.metrics["nack_failed"] += 1
            logger.warning("Connection lost during nack, ignoring")

    async def _requeue_with_delay(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        try:
            channel = message.channel
            delay_queue_name = f"{self.queue.config.name}.delayed"

            await channel.declare_queue(
                delay_queue_name,
                durable=True,
                arguments={
                    "x-dead-letter-exchange": "",
                    "x-dead-letter-routing-key": self.queue.config.name,
                    "x-message-ttl": int(self.requeue_delay * 1000)
                }
            )

            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=message.body,
                    headers=message.headers,
                    delivery_mode=message.delivery_mode
                ),
                routing_key=delay_queue_name
            )

            self.metrics["requeued"] += 1
            logger.info(f"Message requeued with {self.requeue_delay}s delay")

        except Exception as e:
            logger.error(f"Failed to requeue message: {e}")
            await self._safe_nack(message, requeue=True)

    async def _move_to_dlq(self, message: aio_pika.abc.AbstractIncomingMessage, error_msg: str = None) -> bool:
        if not self.dlq_enabled:
            return False

        try:
            dlq_name = f"{self.queue.config.name}.dlq"

            channel = self.queue.connection.channel

            await channel.declare_queue(
                dlq_name,
                durable=True,
                arguments={"x-queue-mode": "lazy"}
            )

            headers = message.headers or {}
            headers.update({
                "x-failure-reason": error_msg or "Unknown error",
                "x-original-queue": self.queue.config.name,
                "x-failed-at": time.time()
            })

            exchange = channel.default_exchange
            await exchange.publish(
                aio_pika.Message(
                    body=message.body,
                    headers=headers,
                    delivery_mode=message.delivery_mode,
                    content_type=message.content_type
                ),
                routing_key=dlq_name
            )

            self.metrics["dlq_moved"] += 1
            logger.info(f"Message moved to DLQ: {dlq_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to move message to DLQ: {e}")
            return False

    async def _handle_with_retry(self, data: Dict[str, Any]) -> bool:

        async def attempt_handler():
            return await self.handler(data)

        try:
            if self.retry_config.max_attempts > 1:
                return await retry_on_failure(attempt_handler, config=self.retry_config)
            else:
                return await self.handler(data)
        except Exception as e:
            logger.error(f"Handler failed after retries: {e}")
            return False

    async def _handle_error(self, message: aio_pika.abc.AbstractIncomingMessage,
                            data: Optional[Dict[str, Any]] = None,
                            error_msg: str = None) -> None:
        if self.error_strategy == ErrorHandlingStrategy.IGNORE:
            await self._safe_ack(message)
            self.metrics["ignored"] += 1
            logger.warning(f"Ignored failed message: {error_msg}")

        elif self.error_strategy == ErrorHandlingStrategy.REQUEUE_END:
            await self._requeue_with_delay(message)
            await self._safe_ack(message)
            self.metrics["failed"] += 1

        elif self.error_strategy == ErrorHandlingStrategy.REQUEUE_FRONT:
            await self._safe_nack(message, requeue=True)
            self.metrics["failed"] += 1
            logger.info("Message requeued to front")

        elif self.error_strategy == ErrorHandlingStrategy.DLQ:
            moved = await self._move_to_dlq(message, error_msg)
            await self._safe_ack(message)
            self.metrics["failed"] += 1
            if not moved:
                logger.error("Failed to move to DLQ, message acknowledged anyway")

    async def process_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        try:
            data = json.loads(message.body.decode())

            success = await self._handle_with_retry(data)
            if success:
                await self._safe_ack(message)
                self.metrics["processed"] += 1
                logger.info("Message processed successfully")
            else:
                await self._handle_error(message, data, "Handler returned False")

        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON: {e}"
            logger.error(error_msg)
            await self._handle_error(message, None, error_msg)

        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(error_msg)
            await self._handle_error(message, None, error_msg)

    async def consume(self, stop_event: Optional[asyncio.Event] = None) -> None:
        queue = await self.queue.get_queue()

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                if stop_event and stop_event.is_set():
                    logger.info("Stop event received, stopping consumer")
                    break

                logger.debug(f"Received message: {message.message_id}")
                await self.process_message(message)

        logger.info("Consumer stopped")
