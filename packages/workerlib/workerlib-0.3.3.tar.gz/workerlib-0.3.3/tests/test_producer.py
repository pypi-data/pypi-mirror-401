import json
from unittest.mock import AsyncMock, patch

import pytest
from workerlib.producer import RabbitMQProducer


class TestRabbitMQProducer:
    @pytest.mark.asyncio
    async def test_init(self, mock_rabbitmq_connection, mock_queue):
        producer = RabbitMQProducer(
            connection=mock_rabbitmq_connection,
            queue=mock_queue,
            send_retries=3,
            retry_delay=1.0,
            enable_auto_reconnect=True
        )

        assert producer.connection == mock_rabbitmq_connection
        assert producer.queue == mock_queue
        assert producer.send_retries == 3
        assert producer.retry_delay == 1.0
        assert producer.enable_auto_reconnect is True
        assert producer.metrics["sent"] == 0

    @pytest.mark.asyncio
    async def test_send_success(self, mock_rabbitmq_connection, mock_queue):
        producer = RabbitMQProducer(mock_rabbitmq_connection, mock_queue)

        mock_queue_obj = AsyncMock()
        mock_queue_obj.name = "test_queue"
        mock_queue.get_queue = AsyncMock(return_value=mock_queue_obj)

        mock_exchange = AsyncMock()
        mock_rabbitmq_connection.channel.default_exchange = mock_exchange

        test_data = {"id": 1, "message": "test"}

        await producer.send(test_data)

        mock_exchange.publish.assert_called_once()

        call_args = mock_exchange.publish.call_args
        message = call_args[0][0]
        assert json.loads(message.body.decode()) == test_data
        assert message.delivery_mode == 2
        assert message.content_type == "application/json"
        assert call_args[1]["routing_key"] == "test_queue"
        assert producer.metrics["sent"] == 1

    @pytest.mark.asyncio
    async def test_send_with_kwargs(self, mock_rabbitmq_connection, mock_queue):
        producer = RabbitMQProducer(mock_rabbitmq_connection, mock_queue)

        mock_exchange = AsyncMock()
        mock_rabbitmq_connection.channel.default_exchange = mock_exchange

        mock_queue_obj = AsyncMock()
        mock_queue_obj.name = "test_queue"
        mock_queue.get_queue = AsyncMock(return_value=mock_queue_obj)

        await producer.send(
            {"test": "data"},
            priority=5,
            correlation_id="123",
            expiration="60000"
        )

        call_args = mock_exchange.publish.call_args
        message = call_args[0][0]

        assert message.priority == 5
        assert message.correlation_id == "123"
        assert message.expiration == "60000"

    @pytest.mark.asyncio
    async def test_send_connection_error(self, mock_rabbitmq_connection, mock_queue):
        producer = RabbitMQProducer(mock_rabbitmq_connection, mock_queue)

        assert producer.metrics["failed"] == 0

        mock_rabbitmq_connection.is_healthy = AsyncMock(return_value=False)
        mock_rabbitmq_connection.reconnect = AsyncMock(side_effect=ConnectionError("Test"))

        with pytest.raises(ConnectionError):
            await producer.send({"test": "data"})

        assert True

    @pytest.mark.asyncio
    async def test_send_raw(self, mock_rabbitmq_connection, mock_queue):
        producer = RabbitMQProducer(mock_rabbitmq_connection, mock_queue)

        mock_exchange = AsyncMock()
        mock_rabbitmq_connection.channel.default_exchange = mock_exchange

        mock_queue_obj = AsyncMock()
        mock_queue_obj.name = "test_queue"
        mock_queue.get_queue = AsyncMock(return_value=mock_queue_obj)

        test_body = b"raw binary data"

        await producer.send_raw(test_body, content_type="application/octet-stream")

        call_args = mock_exchange.publish.call_args
        message = call_args[0][0]

        assert message.body == test_body
        assert message.content_type == "application/octet-stream"
        assert producer.metrics["sent"] == 1

    @pytest.mark.asyncio
    async def test_send_batch(self, mock_rabbitmq_connection, mock_queue):
        producer = RabbitMQProducer(mock_rabbitmq_connection, mock_queue)

        mock_exchange = AsyncMock()
        mock_rabbitmq_connection.channel.default_exchange = mock_exchange

        mock_queue_obj = AsyncMock()
        mock_queue_obj.name = "test_queue"
        mock_queue.get_queue = AsyncMock(return_value=mock_queue_obj)

        test_messages = [
            {"id": 1, "msg": "first"},
            {"id": 2, "msg": "second"},
            {"id": 3, "msg": "third"},
        ]

        await producer.send_batch(test_messages)

        assert mock_exchange.publish.call_count == 3
        assert producer.metrics["sent"] == 3

    @pytest.mark.asyncio
    async def test_send_batch_with_error(self, mock_rabbitmq_connection, mock_queue):
        producer = RabbitMQProducer(mock_rabbitmq_connection, mock_queue)

        mock_exchange = AsyncMock()
        mock_rabbitmq_connection.channel.default_exchange = mock_exchange

        call_count = 0

        async def mock_publish(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise Exception("Test error")

        mock_exchange.publish = AsyncMock(side_effect=mock_publish)

        mock_queue_obj = AsyncMock()
        mock_queue_obj.name = "test_queue"
        mock_queue.get_queue = AsyncMock(return_value=mock_queue_obj)

        test_messages = [
            {"id": 1, "msg": "first"},
            {"id": 2, "msg": "second"},
            {"id": 3, "msg": "third"},
        ]

        await producer.send_batch(test_messages)

        assert mock_exchange.publish.call_count == 3
        assert producer.metrics["sent"] == 2

    @pytest.mark.asyncio
    async def test_send_with_retry_success(self, mock_rabbitmq_connection, mock_queue):
        producer = RabbitMQProducer(
            mock_rabbitmq_connection,
            mock_queue,
            send_retries=3,
            retry_delay=0.01
        )

        attempt = 0

        async def mock_send(*args, **kwargs):
            nonlocal attempt
            attempt += 1
            if attempt == 1:
                raise ConnectionError("First attempt failed")

        producer.send = AsyncMock(side_effect=mock_send)
        producer._ensure_connection = AsyncMock()

        with patch.object(producer, 'send', AsyncMock(side_effect=[ConnectionError("Test"), None])):
            with patch('asyncio.sleep', AsyncMock()):
                result = await producer.send_with_retry({"test": "data"})

        assert result is True

    @pytest.mark.asyncio
    async def test_send_with_retry_failure(self, mock_rabbitmq_connection, mock_queue):
        producer = RabbitMQProducer(
            mock_rabbitmq_connection,
            mock_queue,
            send_retries=2,
            retry_delay=0.01
        )

        with patch.object(producer, 'send', AsyncMock(side_effect=ConnectionError("Test"))):
            with patch('asyncio.sleep', AsyncMock()):
                with pytest.raises(ConnectionError):
                    await producer.send_with_retry({"test": "data"})

        assert producer.metrics["failed"] == 1
