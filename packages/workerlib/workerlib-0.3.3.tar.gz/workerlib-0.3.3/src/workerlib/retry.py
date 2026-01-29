import asyncio
import logging
from dataclasses import dataclass
from typing import Optional, Any, Callable, Awaitable

logger = logging.getLogger(__name__)


@dataclass
class RetryConfig:
    max_attempts: int = 3
    initial_delay: float = 1.0
    backoff_factor: float = 2.0
    max_delay: float = 60.0

    def get_delay(self, attempt: int) -> float:
        delay = self.initial_delay * (self.backoff_factor ** (attempt - 1))
        return min(delay, self.max_delay)


async def retry_on_failure(
        func: Callable[..., Awaitable[Any]],
        *args,
        config: Optional[RetryConfig] = None,
        **kwargs
) -> Any:
    retry_config = config or RetryConfig()
    last_error: Optional[Exception] = None

    for attempt in range(1, retry_config.max_attempts + 1):
        try:
            result = await func(*args, **kwargs)
            if attempt > 1:
                logger.info(f"Success after {attempt} attempts")
            return result
        except Exception as e:
            last_error = e
            if attempt == retry_config.max_attempts:
                logger.error(f"Max retries exceeded: {attempt}")
                break

            delay = retry_config.get_delay(attempt)
            logger.warning(
                f"Attempt {attempt}/{retry_config.max_attempts} failed. "
                f"Retrying in {delay:.1f}s. Error: {e}"
            )
            await asyncio.sleep(delay)

    raise last_error or Exception("Unknown error")
