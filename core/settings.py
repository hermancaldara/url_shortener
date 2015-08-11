import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('URL_SHORTENER_SECRET_KEY', 'secret_key')

DEBUG = int(os.environ.get('URL_SHORTENER_DEBUG', 1)) != 0

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'url_shortener'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % os.environ.get('URL_SHORTENER_DATABASES_ENGINE', 'sqlite3'),
        'NAME': os.environ.get('URL_SHORTENER_DATABASES_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('URL_SHORTENER_DATABASES_USER', ''),
        'PASSWORD': os.environ.get('URL_SHORTENER_DATABASES_PASSWORD', ''),
        'HOST': os.environ.get('URL_SHORTENER_DATABASES_HOST', ''),
        'PORT': os.environ.get('URL_SHORTENER_DATABASES_PORT', '')
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'core/templates'),
)

LOGIN_REDIRECT_URL = '/'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('URL_SHORTENER_CACHES_LOCATION', "redis://localhost:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
