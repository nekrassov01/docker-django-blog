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
        'develop': {
            'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d '
                      '%(pathname)s:%(lineno)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO', 
            'class': 'logging.StreamHandler', 
            'formatter': 'develop',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'], 
            'level': 'INFO', 
            'propagate': False,
        },
        'django': {
            'handlers': ['console'], 
            'level': 'INFO', 
            'propagate': False,
        },
    },
}