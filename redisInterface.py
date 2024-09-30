import redis.asyncio as redis

class RedisInterface:  
    def __init__(self, url, port, db):  
        self.url = url  
        self.port = port  
        self.db = db  
        self.rac = None  
    # redis operations and functions
    async def initialize_redis(self):  
        try:  
            self.rac = await redis.from_url(f"redis://{self.url}:{self.port}/{self.db}", decode_responses=True)   
        except Exception as e:  
            #logging.error(f"Redis connection error: {e}")  
            self.rac = None  # Bağlantı hatası durumunda rac'yi None olarak ayarlıyoruz  

    async def close_redis(self):  
        if self.rac:  
            try:  
                await self.rac.aclose()  
            except Exception as e:  
                print()#logging.error(f"Error closing Redis connection: {e}")  

    async def set_kfv(self, hash_key, field, value):  
        if self.rac:  
            try:  
                await self.rac.hset(hash_key, field, value)  
            except Exception as e:  
                print()#logging.error(f"Error setting key, field value in Redis: {e}")  

    async def get_kf(self, hash_key, field):  
        if self.rac:  
            try:  
                return await self.rac.hget(hash_key, field)  
            except Exception as e:  
                #logging.error(f"Error getting value from Redis: {e}")  
                return None  

    async def get_all(self, hash_key):  
        if self.rac:  
            try:  
                return await self.rac.hgetall(hash_key)  
            except Exception as e:  
                #logging.error(f"Error getting all values from Redis: {e}")  
                return None  

    async def set(self, hash_key, value):  
        if self.rac:  
            try:  
                await self.rac.set(hash_key, value)  
            except Exception as e:  
                print()#logging.error(f"Error setting value in Redis: {e}")  

    async def get(self, hash_key):  
        if self.rac:  
            try:  
                return await self.rac.get(hash_key)  
            except Exception as e:  
                #logging.error(f"Error getting value from Redis: {e}")  
                return None  

    async def delete(self, hash_key):  
        if self.rac:  
            try:  
                await self.rac.delete(hash_key)  
            except Exception as e:  
                print()#logging.error(f"Error deleting key from Redis: {e}")  

    async def delete_kf(self, hash_key, field):  
        if self.rac:  
            try:  
                await self.rac.hdel(hash_key, field)  
            except Exception as e:  
                print()#logging.error(f"Error deleting key, field from Redis: {e}")  