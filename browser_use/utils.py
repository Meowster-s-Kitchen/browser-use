import logging
import time
from functools import wraps
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

logger = logging.getLogger(__name__)


# Define generic type variables for return type and parameters
R = TypeVar('R')
P = ParamSpec('P')


def time_execution_sync(additional_text: str = '') -> Callable[[Callable[P, R]], Callable[P, R]]:
	def decorator(func: Callable[P, R]) -> Callable[P, R]:
		@wraps(func)
		def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
			start_time = time.time()
			result = func(*args, **kwargs)
			execution_time = time.time() - start_time
			logger.debug(f'{additional_text} Execution time: {execution_time:.2f} seconds')
			return result

		return wrapper

	return decorator


def time_execution_async(
	additional_text: str = '',
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
	def decorator(func: Callable[P, Coroutine[Any, Any, R]]) -> Callable[P, Coroutine[Any, Any, R]]:
		@wraps(func)
		async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
			start_time = time.time()
			result = await func(*args, **kwargs)
			execution_time = time.time() - start_time
			logger.debug(f'{additional_text} Execution time: {execution_time:.2f} seconds')
			return result

		return wrapper

	return decorator


def singleton(cls):
	instance = [None]

	def wrapper(*args, **kwargs):
		if instance[0] is None:
			instance[0] = cls(*args, **kwargs)
		return instance[0]

	return wrapper


from typing import Literal, Union, Optional
def print_color(text, color:Literal['red','green','blue','yellow','purple','cyan','white','reset'] = 'white'):

    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'blue': '\033[94m',
        'yellow': '\033[93m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m' 
    }
    
    print(f"{colors.get(color, '')}{text}{colors['reset']}")
