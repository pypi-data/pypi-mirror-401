from dataclasses import dataclass
from typing import Optional
import aio_pika
import logging


@dataclass
class ConnectionParams:
    host: str = "127.0.0.1"
    port: int = 5672
    virtual_host: str = "/"
    username: str = "guest"
    password: str = "guest"
    heartbeat: int = 60
    timeout: int = 10


class ConnectionError(Exception):
    pass


logger = logging.getLogger(__name__)


class RabbitMQConnection:
    def __init__(self, params: ConnectionParams = None):
        self.params = params or ConnectionParams()
        self._connection: Optional[aio_pika.abc.AbstractRobustConnection] = None
        self._channel: Optional[aio_pika.Channel] = None

    @property
    def channel(self) -> aio_pika.Channel:
        if not self._channel or self._channel.is_closed:
            raise ConnectionError("Channel not available. Call connect() first.")
        return self._channel

    def _get_url(self) -> str:
        return (f"amqp://{self.params.username}:{self.params.password}"
                f"@{self.params.host}:{self.params.port}"
                f"/{self.params.virtual_host}")

    async def is_healthy(self) -> bool:
        return self._connection and not self._connection.is_closed

    async def connect(self) -> None:
        if self._connection and not self._connection.is_closed:
            logger.info("Connection is already open.")
            return
        try:
            self._connection = await aio_pika.connect_robust(
                self._get_url(),
                heartbeat=self.params.heartbeat,
                timeout=self.params.timeout
            )
            self._channel = await self._connection.channel()
            logger.info(f"Connected to RabbitMQ at {self.params.host}:{self.params.port}")
        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}")
            raise ConnectionError(f"Error connecting to RabbitMQ: {e}")

    async def reconnect(self) -> None:
        await self.close()
        await self.connect()

    async def close(self) -> None:
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            self._connection = None
            self._channel = None
            logger.info("Connection to RabbitMQ closed.")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
