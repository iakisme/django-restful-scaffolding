
from django.conf import settings

import redis as redis_module

redis = redis_module.StrictRedis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT,
            #password=settings.REDIS_PASSWORD,
            decode_responses=True,
            charset='utf-8'
        )
pubsub = redis.pubsub(ignore_subscribe_messages=True)