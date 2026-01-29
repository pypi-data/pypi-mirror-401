import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from workerlib.consumer import ErrorHandlingStrategy
from workerlib.pool import WorkerPool


class TestWorkerPool:

    @pytest.mark.asyncio
    async def test_init_default(self):
        pool = WorkerPool()

        assert pool.connection is None
        assert pool.workers == {}
        assert pool.producers == {}
        assert pool.tasks == {}
        assert pool._auto_start is True

    @pytest.mark.asyncio
    async def test_init_with_params(self, mock_connection_params):
        pool = WorkerPool(connection_params=mock_connection_params, auto_start=False)

        assert pool.connection_params == mock_connection_params
        assert pool._auto_start is False

    @pytest.mark.asyncio
    async def test_start(self, mock_connection_params):
        pool = WorkerPool(connection_params=mock_connection_params, auto_start=False)

        mock_connection = AsyncMock()
        mock_connection.connect = AsyncMock()
        mock_connection.is_healthy = AsyncMock(return_value=False)

        with patch('workerlib.pool.RabbitMQConnection', return_value=mock_connection):
            await pool.start()

        assert pool.connection == mock_connection
        mock_connection.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_already_started(self, mock_connection_params):
        pool = WorkerPool(connection_params=mock_connection_params, auto_start=False)

        mock_connection = AsyncMock()
        mock_connection.connect = AsyncMock()
        mock_connection.is_healthy = AsyncMock(return_value=True)
        pool.connection = mock_connection

        await pool.start()

        mock_connection.connect.assert_not_called()

    @pytest.mark.asyncio
    async def test_stop(self):
        pool = WorkerPool()

        mock_task1 = AsyncMock()
        mock_task1.cancel = Mock()

        mock_task2 = AsyncMock()
        mock_task2.cancel = Mock()

        pool.tasks = {"task1": mock_task1, "task2": mock_task2}

        mock_connection = AsyncMock()
        mock_connection.close = AsyncMock()
        pool.connection = mock_connection

        with patch('asyncio.gather', AsyncMock(return_value=[])):
            await pool.stop()

        mock_task1.cancel.assert_called_once()
        mock_task2.cancel.assert_called_once()
        mock_connection.close.assert_called_once()
        assert pool.workers == {}
        assert pool.producers == {}
        assert pool.tasks == {}

    @pytest.mark.asyncio
    async def test_stop_no_connection(self):
        pool = WorkerPool()
        pool.connection = None

        await pool.stop()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        pool = WorkerPool()

        pool.start = AsyncMock()
        pool.stop = AsyncMock()

        async with pool:
            pool.start.assert_called_once()

        pool.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_worker(self, mock_rabbitmq_connection):
        pool = WorkerPool()
        pool.connection = mock_rabbitmq_connection

        async def mock_handler(data):
            return True

        pool.add_worker(
            queue_name="test_queue",
            handler=mock_handler,
            error_strategy=ErrorHandlingStrategy.IGNORE,
            prefetch_count=5,
            auto_start=True
        )

        assert "test_queue" in pool.workers
        assert "test_queue" in pool.producers
        assert "test_queue" in pool.tasks

        worker = pool.workers["test_queue"]
        assert worker.handler == mock_handler
        assert worker.error_strategy == ErrorHandlingStrategy.IGNORE

    @pytest.mark.asyncio
    async def test_add_worker_duplicate(self, mock_rabbitmq_connection):
        pool = WorkerPool()
        pool.connection = mock_rabbitmq_connection

        async def mock_handler(data):
            return True

        pool.add_worker("test_queue", mock_handler)

        with pytest.raises(KeyError):
            pool.add_worker("test_queue", mock_handler)

    @pytest.mark.asyncio
    async def test_add_worker_no_connection(self):
        pool = WorkerPool(auto_start=False)

        async def mock_handler(data):
            return True

        with pytest.raises(RuntimeError):
            pool.add_worker("test_queue", mock_handler)

    @pytest.mark.asyncio
    async def test_send(self):
        pool = WorkerPool()

        mock_producer = AsyncMock()
        mock_producer.send = AsyncMock()
        pool.producers = {"test_queue": mock_producer}

        test_data = {"id": 1, "data": "test"}

        await pool.send("test_queue", test_data, with_retry=False)

        mock_producer.send.assert_called_once_with(test_data)

    @pytest.mark.asyncio
    async def test_send_with_retry(self):
        pool = WorkerPool()

        mock_producer = AsyncMock()
        mock_producer.send_with_retry = AsyncMock()
        pool.producers = {"test_queue": mock_producer}

        test_data = {"id": 1, "data": "test"}

        await pool.send("test_queue", test_data, with_retry=True)

        mock_producer.send_with_retry.assert_called_once_with(test_data)

    @pytest.mark.asyncio
    async def test_send_no_producer(self):
        pool = WorkerPool()

        with pytest.raises(ValueError):
            await pool.send("nonexistent_queue", {"test": "data"})

    @pytest.mark.asyncio
    async def test_send_raw(self):
        pool = WorkerPool()

        mock_producer = AsyncMock()
        mock_producer.send_raw = AsyncMock()
        pool.producers = {"test_queue": mock_producer}

        test_body = b"raw data"

        await pool.send_raw("test_queue", test_body, content_type="text/plain")

        mock_producer.send_raw.assert_called_once_with(test_body, content_type="text/plain")

    @pytest.mark.asyncio
    async def test_get_metrics_single_queue(self):
        pool = WorkerPool()

        mock_worker = Mock()
        mock_worker.metrics = {"processed": 10, "failed": 2}

        mock_producer = Mock()
        mock_producer.metrics = {"sent": 15, "retried": 3}

        pool.workers = {"test_queue": mock_worker}
        pool.producers = {"test_queue": mock_producer}

        metrics = pool.get_metrics("test_queue")

        assert metrics["queue"] == "test_queue"
        assert metrics["consumer"] == {"processed": 10, "failed": 2}
        assert metrics["producer"] == {"sent": 15, "retried": 3}

    @pytest.mark.asyncio
    async def test_get_metrics_all_queues(self):
        pool = WorkerPool()

        mock_worker1 = Mock()
        mock_worker1.metrics = {"processed": 10}

        mock_producer1 = Mock()
        mock_producer1.metrics = {"sent": 15}

        mock_worker2 = Mock()
        mock_worker2.metrics = {"processed": 5}

        mock_producer2 = Mock()
        mock_producer2.metrics = {"sent": 8}

        pool.workers = {
            "queue1": mock_worker1,
            "queue2": mock_worker2
        }

        pool.producers = {
            "queue1": mock_producer1,
            "queue2": mock_producer2
        }

        metrics = pool.get_metrics()

        assert metrics["total_queues"] == 2
        assert "queue1" in metrics["queues"]
        assert "queue2" in metrics["queues"]
        assert metrics["queues"]["queue1"]["consumer"]["processed"] == 10
        assert metrics["queues"]["queue2"]["consumer"]["processed"] == 5

    @pytest.mark.asyncio
    async def test_get_metrics_no_queue(self):
        pool = WorkerPool()

        with pytest.raises(ValueError):
            pool.get_metrics("nonexistent_queue")

    @pytest.mark.asyncio
    async def test_restart_worker(self):
        pool = WorkerPool()

        async def mock_coroutine():
            await asyncio.sleep(0)

        mock_task = asyncio.create_task(mock_coroutine())

        mock_worker = Mock()
        mock_worker.consume = AsyncMock()

        pool.tasks = {"test_queue": mock_task}
        pool.workers = {"test_queue": mock_worker}

        new_task = asyncio.create_task(mock_coroutine())

        with patch('asyncio.create_task', return_value=new_task):
            await pool.restart_worker("test_queue")

        assert pool.tasks["test_queue"] == new_task

        mock_task.cancel()
        new_task.cancel()
        try:
            await mock_task
            await new_task
        except asyncio.CancelledError:
            pass

    @pytest.mark.asyncio
    async def test_restart_worker_not_found(self):
        pool = WorkerPool()

        with pytest.raises(ValueError):
            await pool.restart_worker("nonexistent_queue")
