from .connection import RabbitMQConnection, ConnectionParams, ConnectionError
from .mq_queue import RabbitMQQueue, QueueConfig
from .consumer import RabbitMQConsumer, ErrorHandlingStrategy
from .pool import WorkerPool
from .producer import RabbitMQProducer
from .retry import RetryConfig, retry_on_failure

__version__ = "0.3.3"

__all__ = [
    'WorkerPool',
    'RabbitMQConnection',
    'ConnectionParams',
    'ConnectionError',
    'RabbitMQQueue',
    'QueueConfig',
    'RabbitMQConsumer',
    'ErrorHandlingStrategy',
    'RabbitMQProducer',
    'RetryConfig',
    'retry_on_failure'
]
