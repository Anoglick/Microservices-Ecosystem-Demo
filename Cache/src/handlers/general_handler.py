import json

from src.settings.decorators.logs_decorators import debugs_decorator


class Router:
    def __init__(self, module):
        self.module = module

    async def process(self, request):
        return await unpacking(request=request)

@debugs_decorator
async def unpacking(request: dict):
    message = json.loads(request.body.decode())

    action = message['action']
    value = message.get('value', None)
    key = value['tag'].upper() if value is not None else message['tag']
    route = value['route'] if value is not None else message['route']

    return {
        "action": action,
        "key": key,
        "route": route,
        "value": value
    }