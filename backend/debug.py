import logging
import sys
import asyncio
from functools import wraps
import time
from typing import Any, Callable

# Configure debug logger
debug_logger = logging.getLogger("debug")
debug_logger.setLevel(logging.DEBUG)

# Create console handler with custom formatting
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '\n%(asctime)s - %(name)s - %(levelname)s\n'
    'File: %(filename)s:%(lineno)d\n'
    'Function: %(funcName)s\n'
    'Message: %(message)s\n'
)
console_handler.setFormatter(formatter)
debug_logger.addHandler(console_handler)

def debug_log(func: Callable) -> Callable:
    """
    Decorator to log function entry, exit, arguments, and execution time.
    """
    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        debug_logger.debug(
            f"Entering {func.__name__}\n"
            f"Args: {args}\n"
            f"Kwargs: {kwargs}"
        )
        try:
            result = await func(*args, **kwargs)
            debug_logger.debug(
                f"Exiting {func.__name__}\n"
                f"Result: {result}\n"
                f"Execution time: {time.time() - start_time:.2f}s"
            )
            return result
        except Exception as e:
            debug_logger.exception(
                f"Exception in {func.__name__}\n"
                f"Error: {str(e)}\n"
                f"Execution time: {time.time() - start_time:.2f}s"
            )
            raise

    @wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        debug_logger.debug(
            f"Entering {func.__name__}\n"
            f"Args: {args}\n"
            f"Kwargs: {kwargs}"
        )
        try:
            result = func(*args, **kwargs)
            debug_logger.debug(
                f"Exiting {func.__name__}\n"
                f"Result: {result}\n"
                f"Execution time: {time.time() - start_time:.2f}s"
            )
            return result
        except Exception as e:
            debug_logger.exception(
                f"Exception in {func.__name__}\n"
                f"Error: {str(e)}\n"
                f"Execution time: {time.time() - start_time:.2f}s"
            )
            raise

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

def log_debug(message: str, *args: Any, **kwargs: Any) -> None:
    """
    Helper function to log debug messages with additional context.
    """
    debug_logger.debug(message, *args, **kwargs)

def setup_debug_mode() -> None:
    """
    Configure additional debug settings for the application.
    """
    # Set debug logging for key libraries
    logging.getLogger("uvicorn").setLevel(logging.DEBUG)
    logging.getLogger("fastapi").setLevel(logging.DEBUG)
    
    # Log debug mode initialization
    debug_logger.debug("Debug mode initialized") 