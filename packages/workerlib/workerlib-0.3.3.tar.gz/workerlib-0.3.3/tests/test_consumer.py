import json
from unittest.mock import AsyncMock

import pytest
from workerlib.consumer import RabbitMQConsumer, ErrorHandlingStrategy
from workerlib.retry import RetryConfig


class TestRabbitMQConsumer:

    @pytest.fixture
    def mock_message(self):
        message = AsyncMock()
        message.body = json.dumps({"test": "data"}).encode()
        message.headers = {}
        message.delivery_mode = 2
        message.content_type = "application/json"
        message.ack = AsyncMock()
        message.nack = AsyncMock()
        message.channel = AsyncMock()
        return message

    @pytest.mark.asyncio
    async def test_init(self, mock_queue, success_handler):
        consumer = RabbitMQConsumer(
            queue=mock_queue,
            handler=success_handler,
            error_strategy=ErrorHandlingStrategy.IGNORE
        )

        assert consumer.queue == mock_queue
        assert consumer.handler == success_handler
        assert consumer.error_strategy == ErrorHandlingStrategy.IGNORE
        assert consumer.dlq_enabled is True
        assert consumer.metrics["processed"] == 0
        assert consumer.metrics["failed"] == 0

    @pytest.mark.asyncio
    async def test_process_message_success(self, mock_queue, success_handler, mock_message):
        consumer = RabbitMQConsumer(mock_queue, success_handler, ErrorHandlingStrategy.IGNORE)

        consumer._handle_error = AsyncMock()

        await consumer.process_message(mock_message)

        consumer._handle_error.assert_not_called()

    @pytest.mark.asyncio
    async def test_process_message_json_error(self, mock_queue, success_handler, mock_message):
        consumer = RabbitMQConsumer(mock_queue, success_handler, ErrorHandlingStrategy.IGNORE)

        message = AsyncMock()
        message.body = b"invalid json"
        message.ack = AsyncMock()
        message.nack = AsyncMock()

        consumer._handle_error = AsyncMock()

        await consumer.process_message(message)

        consumer._handle_error.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_message_handler_exception(self, mock_queue, mock_message):
        async def failing_handler(data):
            raise ValueError("Test error")

        consumer = RabbitMQConsumer(mock_queue, failing_handler, ErrorHandlingStrategy.IGNORE)

        consumer._handle_error = AsyncMock()

        await consumer.process_message(mock_message)

        consumer._handle_error.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_error_ignore(self, mock_queue, success_handler, mock_message):
        consumer = RabbitMQConsumer(
            queue=mock_queue,
            handler=success_handler,
            error_strategy=ErrorHandlingStrategy.IGNORE
        )

        await consumer._handle_error(mock_message, {"test": "data"}, "Test error")

        mock_message.ack.assert_called_once()
        assert consumer.metrics["ignored"] == 1

    @pytest.mark.asyncio
    async def test_handle_error_requeue_front(self, mock_queue, success_handler, mock_message):
        consumer = RabbitMQConsumer(
            queue=mock_queue,
            handler=success_handler,
            error_strategy=ErrorHandlingStrategy.REQUEUE_FRONT
        )

        await consumer._handle_error(mock_message, {"test": "data"}, "Test error")

        mock_message.nack.assert_called_once_with(requeue=True)
        assert consumer.metrics["failed"] == 1

    @pytest.mark.asyncio
    async def test_handle_error_dlq(self, mock_queue, success_handler, mock_message):
        consumer = RabbitMQConsumer(
            queue=mock_queue,
            handler=success_handler,
            error_strategy=ErrorHandlingStrategy.DLQ
        )

        consumer._move_to_dlq = AsyncMock(return_value=True)

        await consumer._handle_error(mock_message, {"test": "data"}, "Test error")

        consumer._move_to_dlq.assert_called_once_with(mock_message, "Test error")
        mock_message.ack.assert_called_once()
        assert consumer.metrics["failed"] == 1

    @pytest.mark.asyncio
    async def test_move_to_dlq_disabled(self, mock_queue, mock_message):
        consumer = RabbitMQConsumer(
            queue=mock_queue,
            handler=lambda x: True,
            error_strategy=ErrorHandlingStrategy.DLQ,
            dlq_enabled=False
        )

        result = await consumer._move_to_dlq(mock_message, "Test error")

        assert result is False

    @pytest.mark.asyncio
    async def test_move_to_dlq_failure(self, mock_queue, mock_message):
        consumer = RabbitMQConsumer(mock_queue, lambda x: True, ErrorHandlingStrategy.DLQ)

        mock_queue.connection.channel.declare_queue = AsyncMock(side_effect=Exception("Test"))

        result = await consumer._move_to_dlq(mock_message, "Test error")

        assert result is False
