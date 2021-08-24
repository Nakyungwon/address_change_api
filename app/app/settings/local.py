from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

STAGE = 'local'