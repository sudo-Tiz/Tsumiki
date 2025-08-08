from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

# Create a shared thread pool
_executor = ThreadPoolExecutor(max_workers=4)


def thread(target: Callable, *args, **kwargs):
    """
    Submit the given function to the thread pool.
    Returns a Future instead of a Thread.
    """
    return _executor.submit(target, *args, **kwargs)


def run_in_thread(func: Callable) -> Callable:
    """
    Decorator to run the decorated function in the thread pool.
    """

    def wrapper(*args, **kwargs):
        return thread(func, *args, **kwargs)

    return wrapper
