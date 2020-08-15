from .base import *

# Base

SECRET_KEY = env('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Logging

LOGGING = {
    'version': 1, 
    'disable_existing_loggers': False,  
    'formatters': {
        'production': {
            'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d '
                      '%(pathname)s:%(lineno)d %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO', 
            'class': 'logging.handlers.TimedRotatingFileHandler', 
            'filename': '/django/log/app.log',
            'when': 'D',
            'interval': 30, 
            'formatter': 'production',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'], 
            'level': 'INFO', 
            'propagate': False,
        },
        'django': {
            'handlers': ['file'], 
            'level': 'INFO', 
            'propagate': False,
        },
    },
}