import logging
from dataclasses import dataclass
from typing import Optional

import aio_pika

from .connection import RabbitMQConnection


@dataclass
class QueueConfig:
    name: str
    durable: bool = True
    exclusive: bool = False
    auto_delete: bool = False
    arguments: Optional[dict] = None
    prefetch_count: int = 1


logger = logging.getLogger(__name__)


class RabbitMQQueue:
    def __init__(self, connection: RabbitMQConnection, config: QueueConfig):
        self.connection = connection
        self.config = config
        self._queue = None

    @property
    def queue_name(self) -> str:
        return self.config.name

    async def get_queue(self) -> aio_pika.Queue:
        if not self._queue:
            await self.connection.connect()
            channel = self.connection.channel
            await channel.set_qos(prefetch_count=self.config.prefetch_count)
            self._queue = await channel.declare_queue(
                self.config.name,
                durable=self.config.durable,
                exclusive=self.config.exclusive,
                auto_delete=self.config.auto_delete,
                arguments=self.config.arguments or {}
            )
            logger.info(f"Queue declared: {self.config.name}")
        return self._queue
