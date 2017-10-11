from .default import *

DEBUG = True

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')],
        },
        "ROUTING": "hawkeye.routing.channel_routing",
    },
}

REDIS_CONN_STR = 'redis://127.0.0.1:6379'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CONN_STR,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
            }
        }
    }
}
