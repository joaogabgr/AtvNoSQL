import redis

def get_redis_client():
    return redis.Redis(
        host='redis-12812.c8.us-east-1-3.ec2.redns.redis-cloud.com',
        port=12812,
        password='yC9rwjRaQSZglA2nQQLFUs23e5s0atZr'
    )
