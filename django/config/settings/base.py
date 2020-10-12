#from pathlib import Path
from django.contrib.messages import constants as messages
import os
import environ

# Base
# BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env = environ.Env()
env.read_env(os.path.join(BASE_DIR,'.env'))

# Application
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'blog.apps.BlogConfig',
    #'django_cleanup',
    'django_summernote',
    'bootstrap4',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'blog.middleware.IpRestrictMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.common',
                'blog.context_processors.is_debug',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Locales
LANGUAGE_CODE = env('LANGUAGE_CODE')
TIME_ZONE = env('TIME_ZONE')
USE_I18N = env('USE_I18N')
USE_L10N = env('USE_L10N')
USE_TZ = env('USE_TZ')

# Flash Message
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage' 
MESSAGE_TAGS = {
    messages.SUCCESS: 'alert alert-success',
}

# sites Framework
SITE_ID = env('SITE_ID')

# ClickJacking Protection
X_FRAME_OPTIONS = env('X_FRAME_OPTIONS')

# ALLOWD_IPS
ALLOWED_IPS = env.list('ALLOWED_IPS')

# django-summernote
SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': env('SUMMERNOTE_WIDTH'),
        'height': env('SUMMERNOTE_HEIGHT'),
    },
}

# Email
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env.get_value('EMAIL_USE_TLS', bool)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
STATIC_ROOT = '/static'

# Janome
JANOME_DICTIONARY_PATH = env('JANOME_DICTIONARY_PATH')
JANOME_STOPWORDS_PATH = env('JANOME_STOPWORDS_PATH')
JANOME_SYNONYM_PATH = env('JANOME_SYNONYM_PATH')

# Loop Count
WORD_CLOUD_COUNT = env.get_value('WORD_CLOUD_COUNT', int)