from functools import wraps


def converter(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if args:
            params = func.__code__.co_varnames[:func.__code__.co_argcount]
            kwargs.update(zip(params, args))

        message = {key: value for key, value in kwargs.items()}
        kwargs["message"] = message
        
        return await func(self, **kwargs)
    return wrapper