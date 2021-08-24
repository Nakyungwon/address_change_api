from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('172.21.0.2', 6379)],
            # "hosts": [('234.5t.02.2', 6379)],
        }, 
    },
}

STAGE = 'develop'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
