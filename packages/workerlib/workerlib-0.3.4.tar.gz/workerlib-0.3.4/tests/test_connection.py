from unittest.mock import AsyncMock, patch

import pytest
from workerlib.connection import RabbitMQConnection, ConnectionParams, ConnectionError


class TestConnectionParams:

    def test_default_values(self):
        params = ConnectionParams()
        assert params.host == "127.0.0.1"
        assert params.port == 5672
        assert params.username == "guest"
        assert params.password == "guest"
        assert params.virtual_host == "/"

    def test_custom_values(self):
        params = ConnectionParams(
            host="example.com",
            port=1234,
            username="admin",
            password="secret",
            virtual_host="/vhost"
        )
        assert params.host == "example.com"
        assert params.port == 1234
        assert params.username == "admin"
        assert params.password == "secret"
        assert params.virtual_host == "/vhost"


class TestRabbitMQConnection:

    @pytest.mark.asyncio
    async def test_get_url(self):
        params = ConnectionParams(
            host="test_host",
            port=1234,
            username="user",
            password="pass",
            virtual_host="/vhost"
        )
        connection = RabbitMQConnection(params)

        url = connection._get_url()
        assert "amqp://user:pass@test_host:1234" in url

    @pytest.mark.asyncio
    async def test_connect_success(self, mock_connection_params):
        with patch('aio_pika.connect_robust', AsyncMock()) as mock_connect:
            mock_connection = AsyncMock()
            mock_channel = AsyncMock()
            mock_connect.return_value = mock_connection
            mock_connection.channel = AsyncMock(return_value=mock_channel)

            connection = RabbitMQConnection(mock_connection_params)
            await connection.connect()

            mock_connect.assert_called_once()
            assert connection._connection == mock_connection
            assert connection._channel == mock_channel

    @pytest.mark.asyncio
    async def test_connect_already_connected(self, mock_rabbitmq_connection):
        connection = mock_rabbitmq_connection
        connection._connection.is_closed = False

        await connection.connect()
        connection.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_connect_failure(self, mock_connection_params):
        with patch('aio_pika.connect_robust', side_effect=ConnectionError("Test error")):
            connection = RabbitMQConnection(mock_connection_params)

            with pytest.raises(ConnectionError):
                await connection.connect()

    @pytest.mark.asyncio
    async def test_is_healthy(self, mock_rabbitmq_connection):
        connection = mock_rabbitmq_connection
        assert await connection.is_healthy() is True

    @pytest.mark.asyncio
    async def test_channel_property(self, mock_rabbitmq_connection):
        connection = mock_rabbitmq_connection
        assert connection.channel is not None

    @pytest.mark.asyncio
    async def test_reconnect(self):
        params = ConnectionParams()
        connection = RabbitMQConnection(params)

        mock_close = AsyncMock()
        mock_connect = AsyncMock()
        connection.close = mock_close
        connection.connect = mock_connect

        await connection.reconnect()

        mock_close.assert_called_once()
        mock_connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_close(self, mock_rabbitmq_connection):
        connection = mock_rabbitmq_connection
        await connection.close()
        connection.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_context_manager(self, mock_connection_params):
        connection = RabbitMQConnection(mock_connection_params)

        with patch.object(connection, 'connect', AsyncMock()) as mock_connect:
            with patch.object(connection, 'close', AsyncMock()) as mock_close:
                async with connection:
                    mock_connect.assert_called_once()
                mock_close.assert_called_once()
