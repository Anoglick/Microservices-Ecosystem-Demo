from datetime import timedelta
import json

import redis.asyncio as redis


class Cachevaluer:
    def __init__(self, manager):
        self.manager = manager

    async def process(self, action: str, *, key: str, value: str, host: str, port: int, db: int, ttl: int | timedelta):
        if action == 'create':
            cache = await CacheHandler(host=host, port=port, db=db, ttl=ttl).save(key=key, value=value)
            return cache
        elif action == 'get':
            cache = await CacheHandler(host=host, port=port, db=db, ttl=ttl).get(key=key)
            return cache
        elif action == 'update':
            cache = await CacheHandler(host=host, port=port, db=db, ttl=ttl).update(key=key, value=value)
            return cache
        elif action == 'delete':
            cache = await CacheHandler(host=host, port=port, db=db, ttl=ttl).delete(key=key)
            return cache
    
    async def _callback(self):
        pass

class CacheHandler:
    def __init__(self, *, host: str, port: int, db: int, ttl: int | timedelta):
        self.saveloader = SaveLoadCache(host=host, port=port, db=db, ttl=ttl)
        
    async def save(self, key: str, value: dict = None):
        return await self.saveloader.save_cache(key, value)

    async def get(self, key: str):
        return await self.saveloader.load_cache(key)
    
    async def update(self, key: str, value: str):
        return await self.saveloader.update_cache(key=key, value=value)
    
    async def delete(self, key: str):
        return await self.saveloader.delete_cache(key=key)

class SaveLoadCache:
    def __init__(self, host: str, port: int, db: int, ttl: int | timedelta):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True, db=db)
        self.ttl = ttl
    
    async def save_cache(self, key: str, value: dict):
        get_value = await self.redis.get(key)

        if get_value is not None:
            await self.redis.expire(key, self.ttl)
            return "User exists"
        else:
            convert_value = json.dumps(value)
            await self.redis.setex(key, self.ttl, convert_value)
        
        return await self.load_cache(key)
    
    async def load_cache(self, key: str):
        value = await self.redis.get(key)

        if value is None:
            return None
        
        await self.redis.expire(key, self.ttl)
        return json.loads(value)
    
    async def update_cache(self, key: str, value: dict):
        cache = await self.redis.get(key)

        if not cache:
            return {
                "status": 404,
                "message": "user not found"
            }

        await self.redis.setex(key, self.ttl, json.dumps(value))
        return value
    
    async def delete_cache(self, key: str):
        cache = await self.redis.get(key)

        if not cache:
            return {
                "status": 404,
                "message": "user not found"
            }
        
        await self.redis.delete(key)
        return {
                "status": 200,
                "message": "user deleted"
            }
