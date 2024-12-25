import os
from datetime import timedelta
from pathlib import Path
from logging.handlers import RotatingFileHandler

from configs import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.django_config.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # FOR DEBUG MODE

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ["https://127.0.0.1"]
ROOT_URLCONF = 'drf_warehouse.urls'
WSGI_APPLICATION = 'drf_warehouse.wsgi.application'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition

INSTALLED_APPS = [
    'django_extensions',
    # 'django.contrib.admin', # FOR DEBUG MODE
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles', # FOR DEBUG MODE
    'django_filters',
    'storages',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'authentication_app',
    'warehouse_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'drf_warehouse.middleware.APILoggingMiddleware'
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication', # FOR DEBUG MODE
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer', # FOR DEBUG MODE
    ),

    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.UserRateThrottle',
    #     'rest_framework.throttling.AnonRateThrottle',
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'user': '60/minute',
    #     'anon': '60/minute',
    # }

}


# TEMPLATES = [ # FOR DEBUG MODE
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates']
#         ,
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

TEMPLATES = []

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Минимальная длина пароля
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'authentication_app.validators.SpecialCharacterValidator'
    },
    {
        'NAME': 'authentication_app.validators.UppercaseValidator',
    },
    {
        'NAME': 'authentication_app.validators.LowercaseValidator',
    },
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.db.db_name,
        'USER': config.db.db_user,
        'PASSWORD': config.db.db_pass,
        'HOST': config.db.db_host,
        'PORT': config.db.db_port
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://:{config.redis.redis_pass}@{config.redis.redis_host}:{config.redis.redis_port}/{config.redis.redis_db}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# STATIC_URL = 'static/'
MEDIA_URL = 'storage/'
DEFAULT_FILE_STORAGE = 'warehouse_app.custom_storage.MediaStorage'

MINIO_STORAGE_ENDPOINT = config.minio.minio_endpoint
MINIO_STORAGE_ACCESS_KEY = config.minio.minio_access_key
MINIO_STORAGE_SECRET_KEY = config.minio.minio_secret_key
MINIO_STORAGE_MEDIA_BUCKET_NAME = config.minio.minio_media_bucket

AWS_S3_ENDPOINT_URL = f"http://{MINIO_STORAGE_ENDPOINT}"
AWS_S3_CUSTOM_DOMAIN = f'{config.django_config.domain}/storage'
# AWS_S3_ENDPOINT_URL = f"https://{config.django_config.domain}" # FOR DEBUG MODE
AWS_ACCESS_KEY_ID = MINIO_STORAGE_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_STORAGE_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = MINIO_STORAGE_MEDIA_BUCKET_NAME
AWS_QUERYSTRING_AUTH = True
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_USE_SSL = True
AWS_S3_VERIFY = False


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True


LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Не отключать существующие логгеры
    'formatters': {
        'request_format': {
            'format': '{levelname} {asctime} {message} User: {user} IP: {ip} Method: {method} Path: {path}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'action_format': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'api_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/', 'api_requests.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'request_format',
            'encoding': 'utf8',
        },
        'action_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/', 'action_logs.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'action_format',
            'encoding': 'utf8',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'action_format',  # Или 'action_format', в зависимости от логгера
        },
    },
    'loggers': {
        'api_requests': {
            'handlers': ['api_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['action_file', 'console'],
            # 'handlers': ['action_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


