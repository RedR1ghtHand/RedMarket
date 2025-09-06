import logging
import time
from functools import wraps
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class QueryTimer:
    def __init__(self, operation_name: str = "Database Operation", log_level: int = logging.INFO):
        self.operation_name = operation_name
        self.log_level = log_level
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            result = func(*args, **kwargs)
            
            duration = (time.time() - start_time) * 1000
            
            message = f"{self.operation_name} - Duration: {duration:.2f}ms"
            print(message)
            logger.log(self.log_level, message)
            
            return result
        return wrapper


class DetailedQueryTimer:
    def __init__(self, operation_name: str = "Query Operation", include_breakdown: bool = True):
        self.operation_name = operation_name
        self.include_breakdown = include_breakdown
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            result = func(*args, **kwargs)
            
            duration = (time.time() - start_time) * 1000
            
            if self.include_breakdown:
                items_count = ""
                if hasattr(result, '__len__'):
                    try:
                        items_count = f" | Items: {len(result)}"
                    except:
                        pass
                
                message = f"{self.operation_name} - Duration: {duration:.2f}ms{items_count}"
            else:
                message = f"{self.operation_name} - Duration: {duration:.2f}ms"
            
            print(message)
            logger.info(message)
            
            return result
        return wrapper


def time_queries(operation_name: str = "Database Operation", log_level: int = logging.INFO):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = (time.time() - start_time) * 1000
            
            message = f"{operation_name} - Duration: {duration:.2f}ms"
            print(message)
            logger.log(log_level, message)
            
            return result
        return wrapper
    return decorator
