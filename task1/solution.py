import inspect
from functools import wraps

def strict(func):
    signature = inspect.signature(func)
    annotations = func.__annotations__

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        
        for name, value in bound.arguments.items():
            if name in annotations:
                expected_type = annotations[name]
                if not isinstance(value, expected_type):
                    raise TypeError(f"Argument '{name}' must be of type {expected_type.__name__}, got {type(value).__name__}")
        
        return func(*args, **kwargs)
    
    return wrapper
