import redis

def get_redis_client():
    return redis.Redis(
        host='redis-19376.c276.us-east-1-2.ec2.redns.redis-cloud.com',
        port=19376,
        password='GxiBZcYf4x7owUSoIjsMrZWKhp17gRNX')
