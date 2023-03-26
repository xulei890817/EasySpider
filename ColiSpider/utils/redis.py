import redis.asyncio as redis


def create_redis_client(_config):
    pool = redis.ConnectionPool(**_config)
    return redis.Redis(connection_pool=pool, decode_responses=True)
