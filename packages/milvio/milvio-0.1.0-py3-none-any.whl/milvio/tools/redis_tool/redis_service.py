import redis.asyncio as redis
import redis as sync_redis
import json
import logging
from typing import Optional, Any, Union

logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        self.sync_redis: Optional[sync_redis.Redis] = None
        self.redis_url = None
        self.app_slug = None
        self.environment = None
        self._connected = False
        
    async def connect(self, redis_url: str, app_slug: str, environment: str):
        """Connect to Redis"""
        self.redis_url = redis_url
        self.app_slug = app_slug
        self.environment = environment
        try:
            self.redis = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                health_check_interval=30
            )
            
            # Initialize synchronous client
            self.sync_redis = sync_redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                health_check_interval=30
            )
            
            # Test the connection
            await self.redis.ping()
            self.sync_redis.ping()
            
            self._connected = True
            logger.info(f"Successfully connected to Redis at {self.redis_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.aclose()
        
        if self.sync_redis:
            self.sync_redis.close()
            
        self._connected = False
        logger.info("Disconnected from Redis")
    
    def _check_connection(self):
        """Check if Redis is connected"""
        if not self._connected or not self.redis:
            raise RuntimeError("Redis not connected. Call connect() first.")
    
    def _check_sync_connection(self):
        """Check if synchronous Redis is connected"""
        if not self._connected or not self.sync_redis:
            raise RuntimeError("Redis not connected. Call connect() first.")

    def _get_prefixed_key(self, key: str) -> str:
        """Get key with app slug and environment prefix"""
        if not self.app_slug or not self.environment:
             raise RuntimeError("RedisService not properly initialized. app_slug and environment are missing.")
        return f"{self.app_slug}_{self.environment}_{key}"
    
    async def set_async(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set a key-value pair in Redis asynchronously"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            # print(f"Setting key: {prefixed_key} with value: xxxxx and expire: {expire}")
            self._check_connection()
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            if expire:
                await self.redis.setex(prefixed_key, expire, value)  # type: ignore
            else:
                await self.redis.set(prefixed_key, value)  # type: ignore
            return True
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set a key-value pair in Redis synchronously"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            # print(f"Setting key: {prefixed_key} with value: xxxxx and expire: {expire}")

            self._check_sync_connection()
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            if expire:
                self.sync_redis.setex(prefixed_key, expire, value)  # type: ignore
            else:
                self.sync_redis.set(prefixed_key, value)  # type: ignore
            return True
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False

    async def get_async(self, key: str) -> Optional[Any]:
        """Get a value from Redis asynchronously"""
                
        try:
            prefixed_key = self._get_prefixed_key(key)
            # print(f"Getting key: {prefixed_key}")
            self._check_connection()
            #print connection status
            value = await self.redis.get(prefixed_key)  # type: ignore
            if value is None:
                return None
            
            # Try to parse as JSON, fall back to string
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None

    def get(self, key: str) -> Optional[Any]:
        """Get a value from Redis synchronously"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            # print(f"Getting key: {prefixed_key}")

            self._check_sync_connection()
            value = self.sync_redis.get(prefixed_key)  # type: ignore
            if value is None:
                return None
            
            # Try to parse as JSON, fall back to string
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None
    
    async def delete_async(self, key: str) -> bool:
        """Delete a key from Redis asynchronously"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            result = await self.redis.delete(prefixed_key)  # type: ignore
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete a key from Redis synchronously"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_sync_connection()
            result = self.sync_redis.delete(prefixed_key)  # type: ignore
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in Redis"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            return await self.redis.exists(prefixed_key)  # type: ignore
        except Exception as e:
            logger.error(f"Error checking key existence {key}: {e}")
            return False
    
    async def expire_async(self, key: str, seconds: int) -> bool:
        """Set expiration for a key asynchronously"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            return await self.redis.expire(prefixed_key, seconds)  # type: ignore
        except Exception as e:
            logger.error(f"Error setting expiration for key {key}: {e}")
            return False

    def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for a key synchronously"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_sync_connection()
            return self.sync_redis.expire(prefixed_key, seconds)  # type: ignore
        except Exception as e:
            logger.error(f"Error setting expiration for key {key}: {e}")
            return False
    
    async def ttl(self, key: str) -> int:
        """Get time to live for a key"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            return await self.redis.ttl(prefixed_key)  # type: ignore
        except Exception as e:
            logger.error(f"Error getting TTL for key {key}: {e}")
            return -1
    
    async def hset(self, name: str, key: str, value: Any) -> bool:
        """Set a hash field"""
        try:
            self._check_connection()
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            result = await self.redis.hset(name, key, value)  # type: ignore
            return result >= 0
        except Exception as e:
            logger.error(f"Error setting hash field {name}.{key}: {e}")
            return False
    
    async def hget(self, name: str, key: str) -> Optional[Any]:
        """Get a hash field"""
        try:
            self._check_connection()
            value = await self.redis.hget(name, key)  # type: ignore
            if value is None:
                return None
            
            # Try to parse as JSON, fall back to string
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            logger.error(f"Error getting hash field {name}.{key}: {e}")
            return None
    
    async def hgetall(self, name: str) -> dict:
        """Get all hash fields"""
        try:
            self._check_connection()
            result = await self.redis.hgetall(name)  # type: ignore
            # Try to parse JSON values
            parsed_result = {}
            for k, v in result.items():
                try:
                    parsed_result[k] = json.loads(v)
                except (json.JSONDecodeError, TypeError):
                    parsed_result[k] = v
            return parsed_result
        except Exception as e:
            logger.error(f"Error getting all hash fields for {name}: {e}")
            return {}
    
    async def hdel(self, name: str, key: str) -> bool:
        """Delete a hash field"""
        try:
            self._check_connection()
            result = await self.redis.hdel(name, key)  # type: ignore
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting hash field {name}.{key}: {e}")
            return False
    
    async def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment a key's value"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            if amount == 1:
                return await self.redis.incr(prefixed_key)  # type: ignore
            else:
                return await self.redis.incrby(prefixed_key, amount)  # type: ignore
        except Exception as e:
            logger.error(f"Error incrementing key {key}: {e}")
            return None
    
    async def decr(self, key: str, amount: int = 1) -> Optional[int]:
        """Decrement a key's value"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            if amount == 1:
                return await self.redis.decr(prefixed_key)  # type: ignore
            else:
                return await self.redis.decrby(prefixed_key, amount)  # type: ignore
        except Exception as e:
            logger.error(f"Error decrementing key {key}: {e}")
            return None
    
    async def flushdb(self) -> bool:
        """Flush current database"""
        try:
            self._check_connection()
            await self.redis.flushdb()  # type: ignore
            return True
        except Exception as e:
            logger.error(f"Error flushing database: {e}")
            return False
    
    async def keys(self, pattern: str = "*") -> list:
        """Get keys matching pattern"""
        try:
            self._check_connection()
            # Add prefix to pattern
            prefixed_pattern = self._get_prefixed_key(pattern)
            keys = await self.redis.keys(prefixed_pattern)  # type: ignore
            
            # Strip prefix from keys
            prefix = self._get_prefixed_key("")
            prefix_len = len(prefix)
            
            return [k[prefix_len:] for k in keys if k.startswith(prefix)]
        except Exception as e:
            logger.error(f"Error getting keys with pattern {pattern}: {e}")
            return []

    def keys_sync(self, pattern: str = "*") -> list:
        """Get keys matching pattern synchronously"""
        try:
            self._check_sync_connection()
            # Add prefix to pattern
            prefixed_pattern = self._get_prefixed_key(pattern)
            keys = self.sync_redis.keys(prefixed_pattern)  # type: ignore
            
            # Strip prefix from keys
            prefix = self._get_prefixed_key("")
            prefix_len = len(prefix)
            
            return [k[prefix_len:] for k in keys if k.startswith(prefix)]
        except Exception as e:
            logger.error(f"Error getting keys with pattern {pattern}: {e}")
            return []
    
    async def sadd(self, key: str, *values: Any) -> int:
        """Add members to a set"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            # Convert complex objects to JSON strings
            json_values = []
            for value in values:
                if isinstance(value, (dict, list)):
                    json_values.append(json.dumps(value))
                else:
                    json_values.append(value)
            return await self.redis.sadd(prefixed_key, *json_values)  # type: ignore
        except Exception as e:
            logger.error(f"Error adding to set {key}: {e}")
            return 0
    
    async def srem(self, key: str, *values: Any) -> int:
        """Remove members from a set"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            # Convert complex objects to JSON strings
            json_values = []
            for value in values:
                if isinstance(value, (dict, list)):
                    json_values.append(json.dumps(value))
                else:
                    json_values.append(value)
            return await self.redis.srem(prefixed_key, *json_values)  # type: ignore
        except Exception as e:
            logger.error(f"Error removing from set {key}: {e}")
            return 0
    
    async def smembers(self, key: str) -> set:
        """Get all members of a set"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            members = await self.redis.smembers(prefixed_key)  # type: ignore
            # Try to parse JSON values
            parsed_members = set()
            for member in members:
                try:
                    parsed_members.add(json.loads(member))
                except (json.JSONDecodeError, TypeError):
                    parsed_members.add(member)
            return parsed_members
        except Exception as e:
            logger.error(f"Error getting set members for {key}: {e}")
            return set()
    
    async def sismember(self, key: str, value: Any) -> bool:
        """Check if value is a member of set"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return await self.redis.sismember(prefixed_key, value)  # type: ignore
        except Exception as e:
            logger.error(f"Error checking set membership for {key}: {e}")
            return False
    
    async def lpush(self, key: str, *values: Any) -> int:
        """Push values to the left of a list"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            # Convert complex objects to JSON strings
            json_values = []
            for value in values:
                if isinstance(value, (dict, list)):
                    json_values.append(json.dumps(value))
                else:
                    json_values.append(value)
            return await self.redis.lpush(prefixed_key, *json_values)  # type: ignore
        except Exception as e:
            logger.error(f"Error pushing to list {key}: {e}")
            return 0
    
    async def rpush(self, key: str, *values: Any) -> int:
        """Push values to the right of a list"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            # Convert complex objects to JSON strings
            json_values = []
            for value in values:
                if isinstance(value, (dict, list)):
                    json_values.append(json.dumps(value))
                else:
                    json_values.append(value)
            return await self.redis.rpush(prefixed_key, *json_values)  # type: ignore
        except Exception as e:
            logger.error(f"Error pushing to list {key}: {e}")
            return 0
    
    async def lpop(self, key: str) -> Optional[Any]:
        """Pop value from the left of a list"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            value = await self.redis.lpop(prefixed_key)  # type: ignore
            if value is None:
                return None
            
            # Try to parse as JSON, fall back to string
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            logger.error(f"Error popping from list {key}: {e}")
            return None
    
    async def rpop(self, key: str) -> Optional[Any]:
        """Pop value from the right of a list"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            value = await self.redis.rpop(prefixed_key)  # type: ignore
            if value is None:
                return None
            
            # Try to parse as JSON, fall back to string
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            logger.error(f"Error popping from list {key}: {e}")
            return None
    
    async def llen(self, key: str) -> int:
        """Get the length of a list"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            return await self.redis.llen(prefixed_key)  # type: ignore
        except Exception as e:
            logger.error(f"Error getting list length for {key}: {e}")
            return 0
    
    async def lrange(self, key: str, start: int = 0, end: int = -1) -> list:
        """Get a range of elements from a list"""
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            values = await self.redis.lrange(prefixed_key, start, end)  # type: ignore
            # Try to parse JSON values
            parsed_values = []
            for value in values:
                try:
                    parsed_values.append(json.loads(value))
                except (json.JSONDecodeError, TypeError):
                    parsed_values.append(value)
            return parsed_values
        except Exception as e:
            logger.error(f"Error getting list range for {key}: {e}")
            return []

    async def geo_add_async(self, key: str, values: list, expire: Optional[int] = None) -> int:
        """
        Add geospatial items to a sorted set asynchronously
        values: list of [longitude, latitude, member]
        """
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()
            
            # Process values to handle JSON serialization of members
            processed_values = []
            for item in values:
                if len(item) == 3:
                    lon, lat, member = item
                    if isinstance(member, (dict, list)):
                        member = json.dumps(member)
                    processed_values.extend([lon, lat, member])
                else:
                    # If item is already flat or something else, we might have issues if mixed.
                    # But assuming input is list of [lon, lat, member]
                    if isinstance(item, (list, tuple)):
                         processed_values.extend(item)
                    else:
                         processed_values.append(item)
            
            result = await self.redis.geoadd(prefixed_key, processed_values)
            if expire:
                await self.expire_async(key, expire)
            return result
        except Exception as e:
            logger.error(f"Error adding geo items to {key}: {e}")
            return 0

    def geo_add(self, key: str, values: list, expire: Optional[int] = None) -> int:
        """
        Add geospatial items to a sorted set synchronously
        values: list of [longitude, latitude, member]
        """
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_sync_connection()
            
            # Process values to handle JSON serialization of members
            processed_values = []
            for item in values:
                if len(item) == 3:
                    lon, lat, member = item
                    if isinstance(member, (dict, list)):
                        member = json.dumps(member)
                    processed_values.extend([lon, lat, member])
                else:
                    # If item is already flat or something else, we might have issues if mixed.
                    # But assuming input is list of [lon, lat, member]
                    if isinstance(item, (list, tuple)):
                         processed_values.extend(item)
                    else:
                         processed_values.append(item)
            
            result = self.sync_redis.geoadd(prefixed_key, processed_values)
            if expire:
                self.expire(key, expire)
            return result
        except Exception as e:
            logger.error(f"Error adding geo items to {key}: {e}")
            return 0

    async def geo_search_async(self, key: str, longitude: float, latitude: float, radius: float = 100, unit: str = "km", count: int | None = None) -> list:
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_connection()

            members = await self.redis.georadius(
                prefixed_key,
                longitude,
                latitude,
                radius,
                unit=unit,
                withdist=True,
                sort="ASC",
                count=count
            )

            parsed_members = []
            for member, dist in members:
                try:
                    parsed = json.loads(member)
                except (json.JSONDecodeError, TypeError):
                    parsed = member

                parsed_members.append(parsed)

            return parsed_members

        except Exception as e:
            print(e)
            logger.error(f"Error getting geo radius for {key}: {e}")
            return []

    def geo_search(self, key: str, longitude: float, latitude: float, radius: float = 100, unit: str = "km", count: int | None = None) -> list:
        try:
            prefixed_key = self._get_prefixed_key(key)
            self._check_sync_connection()

            members = self.sync_redis.georadius(
                prefixed_key,
                longitude,
                latitude,
                radius,
                unit=unit,
                withdist=True,
                sort="ASC",
                count=count
            )

            parsed_members = []
            for member, dist in members:
                try:
                    parsed = json.loads(member)
                except (json.JSONDecodeError, TypeError):
                    parsed = member

                parsed_members.append(parsed)

            return parsed_members

        except Exception as e:
            logger.error(f"Error getting geo radius for {key}: {e}")
            return []

# Create a global Redis service instance
redis_service = RedisService()
