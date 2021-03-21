from .base import *

# Base
SECRET_KEY = env('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
#ALLOWED_HOSTS = ['*']

# SecurityMiddleware
SECURE_SSL_REDIRECT = env.get_value('SECURE_SSL_REDIRECT', bool)
#SECURE_SSL_REDIRECT = False

# Media Files
MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# django-cloudinary-storage
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
    'SECURE': env.get_value('CLOUDINARY_SECURE', bool),
}

# Google Analytics Reporting API
SERVICE_ACCOUNT_EMAIL = env('SERVICE_ACCOUNT_EMAIL')
VIEW_ID = env('VIEW_ID')
KEY_FILE_LOCATION = os.path.join(BASE_DIR, 'client_secrets.p12')

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