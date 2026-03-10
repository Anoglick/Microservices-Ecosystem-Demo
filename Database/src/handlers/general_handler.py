import json
from src.database.schemas.models_schemas import RequestDict
from src.settings.decorators.logs_decorators import debugs_decorator

class Router:
    def __init__(self, module, message):
        self.module = module
        self.message = message

    async def process(self):
        message = json.loads(self.message.body.decode())
        unpacked = await RequestUnpacker().get_data(message)
        msg = await unpacking(message=unpacked, message_reply=self.message)

        if msg['tag'] is not None:
            msg['tag'] = msg['tag'].upper()
        return msg

class RequestUnpacker:
    @debugs_decorator
    async def get_data(self, body: RequestDict):
        if isinstance(body, dict):
            unpacked = body['request'] if body.get('request', None) is not None else body
        else:
            unpacked = body.model_dump()
        return unpacked

@debugs_decorator
async def unpacking(message: dict, message_reply):
    action = message.get('action', 'get')
    value = message.get('value', None)
    key = (value or {}).get('tag') or (message or {}).get('tag')
    route = (value or {}).get('route') or (message or {}).get('route')
    rpc = message.get('rpc', False)

    return {
        "action": action,
        "tag": key,
        "route": route,
        "value": value,
        "rpc": rpc,
        "message": message_reply
    }