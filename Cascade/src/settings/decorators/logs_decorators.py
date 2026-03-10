from functools import wraps
from src.settings.loggers.config import log


def debugs_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        log.debug("Calling function", func=func.__name__, kwargs=kwargs)
        try:
            output = await func(*args, **kwargs)
            log.debug("Function finished", func=func.__name__, output=output)
            return output
        except Exception:
            log.error("Unhandled exception", func=func.__name__, exc_info=True)
            raise
    return wrapper
