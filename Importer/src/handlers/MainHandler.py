import httpx

from ..settings.decorators.logs_decorators import debugs_decorator
from ..settings.loggers.config import log


TYPE_MAPPING = {
    "string": str,
    "integer": int,
    "boolean": bool,
    "number": float,
    "object": dict,
    "array": list
}

class Router:
    def __init__(self, module):
        self.module = module
        self.handler = HandlerManager(self)

    async def process(self, url, cascade_url):
        values = await self.handler.get_response_values(url=url.strip())
        await self.handler.process(cascade_url=cascade_url, values=values['response'])
    
    async def _callback(self, http_method: str, url: str, prefix: str = None, values = None):
        return await self.module._callback(http_method=http_method, url=url, prefix=prefix, values=values)


class HandlerManager:
    def __init__(self, router):
        self.router = router
        self.handler = HandlerViewer()

        self.original_values = None
        self.cascade_url = None

    @debugs_decorator
    async def get_response_values(self, url: str, values: dict = None):
        callback_values = await self.router._callback(http_method='POST', url=url, prefix='/register-microservice', values=values)
        return callback_values

    @debugs_decorator
    async def process(self, cascade_url, values):
        self.original_values = values
        self.cascade_url = cascade_url

        method=values['method']
        body=[
            {
                "action": "concatenation",
                "items": [values["microservice_url"], values['tag'].lower(), values["route"]]
            },
            {
                "action": "validation_schema",
                "items": [values["microservice_schema"]]
            },
            {
                "action": "validation",
                "items": [values["microservice_schema"], values["test_data"]]
            }
        ]
        

        try:
            await self.importer_values(values=body, method=method)

        except Exception as err:
            log.error('The importers handlers encountered an unexpected error', values=body, method=method, error=str(err))
            raise
    
    @debugs_decorator
    async def importer_values(self, values: list[dict], method: str):
        for value in values:
            try:
                action, items = value['action'], value['items']
                test_values = await self.handler.actions[action](*items)

                if not test_values:
                    log.warning("Invalid value", action=action, items=items)
                    return False
                
            except:
                log.warning('Invalid value', value=value)
                continue
        
        log.info(
            "Calling the callback method",
            url=self.handler.url,
            http_method=method,  
            values=self.handler.test_data
        )
        try:
            response = await self.router._callback(
                url=self.handler.url, 
                http_method=method, 
                values=self.handler.test_data
            )

        except Exception as err:
            log.error(
                'The callback method returned error',
                url=self.handler.url, 
                http_method=method, 
                values=self.handler.test_data,
                error=str(err)   
            )

        if not response['response']:
            log.warning(
                'Invalid the callback response',
                url=self.handler.url,
                http_method=method, 
                values=self.handler.test_data    
            )
            return False
        
        try:
            await self.router._callback(
                url=self.cascade_url, 
                http_method=method, 
                values=self.original_values
            )
        except Exception as err:
            log.error(
                'The callback method returned error', 
                cascade_url=self.cascade_url,
                method=method,
                values=self.original_values,
                err=str(err)
            )

class HandlerViewer:
    def __init__(self):
        self.callback_data = []
        self.actions = {
            "concatenation": self.concatenation,
            "validation_schema": self.validation_schema,
            "validation": self.validation
        }
        self.url = None
        self.test_data = None

    @debugs_decorator
    async def validation_schema(self, schema: dict):
        properties, required = schema["properties"], schema["required"]
        return set(required).issubset(properties)

    @debugs_decorator
    async def validation(self, schema, test_data):
        key_type, required = schema["properties"], schema["required"]

        for data in test_data:
            for key, items in key_type.items():
                expected_type = TYPE_MAPPING.get(items["type"])
                if (key not in data and key not in required):
                    continue
                if expected_type and isinstance(data[key], expected_type):
                    continue
                else:
                    return False
                
        self.test_data = test_data
        return True

    @debugs_decorator
    async def concatenation(self, var_1, var_2, var_3):
        var_2 = var_2.lstrip('/')
        self.url = var_1 + '/' + var_2 + var_3

        return True