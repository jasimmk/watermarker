# Logging Settings

from functools import wraps

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(name)s \
            %(process)d  %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'watermark': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}


def log_start(logger):
    """
    Debug functions
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug('Calling: %s with: args: %s, kwargs:%s' %
                         (func.__name__, args, kwargs))
            return func(*args, **kwargs)

        return wrapper

    return decorator
