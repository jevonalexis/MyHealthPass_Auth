import redis
from app.config import REDIS_CONFIG
from json import dumps, loads

"""
    Proxy to redis client instance
"""


class RedisProxy:

    def __init__(self):
        #: redis client
        self.r = redis.Redis(**REDIS_CONFIG['conn'])

        #: default time to live for keys
        self.expiration_time = int((REDIS_CONFIG['options']['ttl']))

        #: prefix to be added to all keys
        self.prefix = REDIS_CONFIG['options']['prefix']

    def key_exists(self, key):
        """
        :param key name of key to check for
        :return: True is `key` exists in redis
        """
        return self.r.exists(f'{self.prefix}{key}')

    def get(self, key):
        """
        proxy to get() which return the value at key `key`, or None if the key doesn't exist
        """
        try:
            result = self.r.get(f"{self.prefix}{key}")
            if result is None:
                return None
            return loads(result)
        except Exception as e:
            print(str(e))
            print("Failed to connect to redis")
            raise e

    def set(self, key, value, expiration_time=None):
        """
        proxy to set() which stores `value` at key` in redis
        :param key:
        :param value:
        :param expiration_time: optionally set time to live in seconds
        """
        try:
            expiration_time = self.expiration_time if expiration_time is None else expiration_time
            self.r.set(f"{self.prefix}{key}", dumps(value))
            self.r.expire(f"{self.prefix}{key}", expiration_time)
        except Exception as e:
            print("Failed to connect to redis")
            raise e

    def hash_get(self, name, key):
        """proxy to hget() which returns the value of ``key`` within the hash ``name``"""
        try:
            value = self.r.hget(f"{self.prefix}{name}", key)
            if not value:
                return None
            return value.decode('utf-8')
        except Exception as e:
            print("Failed to connect to redis")
            raise e

    def hash_set(self, name, key, value, expiration_time=None):
        """
        proxy to hset() which sets ``key`` to ``value`` within hash ``name``
        :param name:
        :param key:
        :param value:
        :param expiration_time: optionally set the time to live for the set in seconds
        :return:
        """
        try:
            expiration_time = self.expiration_time if expiration_time is None else expiration_time
            self.r.hset(f"{self.prefix}{name}", key, value)
            self.r.expire(f"{self.prefix}{name}", expiration_time)
        except Exception as e:
            print("Failed to connect to redis")
            raise e

    def hashmap_set(self, name, map, expiration_time=None):
        """
        proxy to hmset() which sets key to value within hash ``name`` for each corresponding
        key and value from the ``mapping`` dict
        :param name:
        :param map:
        :param expiration_time:
        :return:
        """
        try:
            expiration_time = self.expiration_time if expiration_time is None else expiration_time
            self.r.hmset(f"{self.prefix}{name}", map)
            self.r.expire(f"{self.prefix}{name}", expiration_time)
        except Exception as e:
            print("Failed to connect to redis")
            raise e

    def hashmap_get(self, name):
        try:
            value = self.r.hmget(f"{self.prefix}{name}", key)

            return value
        except Exception as e:
            print("Failed to connect to redis")
            raise e

    def set_expiration(self, name, exp_time):
        self.r.expire(f"{self.prefix}{name}", exp_time)

    def set_expiring_key(self, name, value, exp_time):
        try:
            self.r.setex(f"{self.prefix}{name}", exp_time, value)
        except Exception as e:
            print("Failed to connect to redis")
            raise e


if __name__ == '__main__':
    r = RedisProxy()

