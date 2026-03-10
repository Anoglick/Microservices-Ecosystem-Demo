import json

from src.settings.decorators.logs_decorators import debugs_decorator


class Router:
    def __init__(self, manager):
        self.manager = manager
        self.correlation_id = None
        self.reply_to = None
    
    async def process(self, msg, answer):
        value = await self.redirect_method(msg=msg, answer=answer)
        action, message = value.get('action', None), value
        return action, message

    @debugs_decorator
    async def redirect_method(self, msg, answer):
        message = json.loads(msg.body.decode())

        if msg.correlation_id and msg.reply_to:
            self.correlation_id = msg.correlation_id
            self.reply_to = msg.reply_to
        
        if answer:
            return {
                "value": message,
                "correlation_id": self.correlation_id,
                "reply_to": self.reply_to
            }

        else:
            return {
                "action": message.get('method', None),
                "value": message.get('request', None),
                "tag": message.get('tag', None),
                "route": message.get('route', None)
            }