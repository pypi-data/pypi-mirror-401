import asyncio
import logging
from asyncio import Task
from typing import Optional, Dict, Callable, Any, Awaitable

from .connection import RabbitMQConnection, ConnectionParams
from .mq_queue import RabbitMQQueue, QueueConfig
from .consumer import RabbitMQConsumer, ErrorHandlingStrategy
from .producer import RabbitMQProducer
from .retry import RetryConfig

logger = logging.getLogger(__name__)


class WorkerPool:
    def __init__(
            self,
            connection_params: Optional[ConnectionParams] = None,
            auto_start: bool = True
    ):
        self.connection_params = connection_params or ConnectionParams()
        self.connection: Optional[RabbitMQConnection] = None
        self.workers: Dict[str, RabbitMQConsumer] = {}
        self.producers: Dict[str, RabbitMQProducer] = {}
        self.tasks: Dict[str, Task] = {}
        self._auto_start = auto_start

    async def __aenter__(self):
        if self._auto_start:
            await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    async def start(self):
        if self.connection and await self.connection.is_healthy():
            logger.info("WorkerPool already started")
            return

        self.connection = RabbitMQConnection(self.connection_params)
        await self.connection.connect()
        logger.info("WorkerPool started")

    async def stop(self):
        for task_name, task in self.tasks.items():
            task.cancel()
            logger.debug(f"Cancelled task: {task_name}")

        if self.tasks:
            await asyncio.gather(*self.tasks.values(), return_exceptions=True)
            self.tasks.clear()

        if self.connection:
            await self.connection.close()
            self.connection = None

        self.workers.clear()
        self.producers.clear()
        logger.info("WorkerPool stopped")

    def add_worker(
            self,
            queue_name: str,
            handler: Callable[[Dict[str, Any]], Awaitable[bool]],
            prefetch_count: int = 1,
            error_strategy: ErrorHandlingStrategy = ErrorHandlingStrategy.DLQ,
            retry_config: Optional[RetryConfig] = None,
            dlq_enabled: bool = True,
            auto_start: bool = True
    ):
        if queue_name in self.workers:
            raise KeyError(f"Worker for queue '{queue_name}' already exists")

        if not self.connection:
            raise RuntimeError("Connection not established. Call start() first or set auto_start=True")

        queue_config = QueueConfig(
            name=queue_name,
            prefetch_count=prefetch_count
        )

        queue = RabbitMQQueue(self.connection, queue_config)

        consumer = RabbitMQConsumer(
            queue=queue,
            handler=handler,
            error_strategy=error_strategy,
            retry_config=retry_config,
            dlq_enabled=dlq_enabled
        )

        producer = RabbitMQProducer(
            connection=self.connection,
            queue=queue,
            send_retries=3
        )

        self.workers[queue_name] = consumer
        self.producers[queue_name] = producer

        if auto_start:
            task = asyncio.create_task(consumer.consume())
            self.tasks[queue_name] = task
            logger.info(f"Worker for queue '{queue_name}' started")
        else:
            logger.info(f"Worker for queue '{queue_name}' added (not started)")

    async def send(
            self,
            queue_name: str,
            data: Dict[str, Any],
            with_retry: bool = True,
            **kwargs
    ):
        if queue_name not in self.producers:
            raise ValueError(f"No producer for queue '{queue_name}'")

        producer = self.producers[queue_name]

        if with_retry:
            await producer.send_with_retry(data, **kwargs)
        else:
            await producer.send(data, **kwargs)

    async def send_raw(self, queue_name: str, body: bytes, **kwargs):
        if queue_name not in self.producers:
            raise ValueError(f"No producer for queue '{queue_name}'")

        producer = self.producers[queue_name]
        await producer.send_raw(body, **kwargs)

    def get_metrics(self, queue_name: Optional[str] = None) -> Dict[str, Any]:
        if queue_name:
            if queue_name not in self.workers:
                raise ValueError(f"No worker for queue '{queue_name}'")

            consumer_metrics = self.workers[queue_name].metrics.copy()
            producer_metrics = self.producers[queue_name].metrics.copy()

            return {
                "consumer": consumer_metrics,
                "producer": producer_metrics,
                "queue": queue_name
            }
        else:
            all_metrics = {
                "total_queues": len(self.workers),
                "queues": {}
            }

            for q_name in self.workers:
                all_metrics["queues"][q_name] = self.get_metrics(q_name)

            return all_metrics

    async def restart_worker(self, queue_name: str):
        if queue_name not in self.tasks:
            raise ValueError(f"No running worker for queue '{queue_name}'")

        old_task = self.tasks[queue_name]
        old_task.cancel()
        try:
            await old_task
        except asyncio.CancelledError:
            pass

        consumer = self.workers[queue_name]
        new_task = asyncio.create_task(consumer.consume())
        self.tasks[queue_name] = new_task

        logger.info(f"Worker for queue '{queue_name}' restarted")
