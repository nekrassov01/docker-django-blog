from .base import *

# Base

SECRET_KEY = env('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ['*']

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
            'level': 'DEBUG', 
            'class': 'logging.StreamHandler', 
            'formatter': 'develop',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'], 
            'level': 'DEBUG', 
            'propagate': False,
        },
        'django': {
            'handlers': ['console'], 
            'level': 'INFO', 
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'], 
            'level': 'DEBUG', 
            'propagate': False,
        },
    },
}

# django-debug-toolbar

if DEBUG:
    def show_toolbar(request):
        return True
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': show_toolbar,}