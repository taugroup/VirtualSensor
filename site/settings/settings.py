"""
Django settings for Compliance project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

SITE_ID = 2

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-11t4i2mst=6j-3f)u0f4v^4fe5ot(z9qva4ic2=4j#*e1lr&&0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DJANGO_SUPERUSER_USERNAME = 'jtao'
DJANGO_SUPERUSER_PASSWORD = 't'
DJANGO_SUPERUSER_EMAIL = 'jtao@tamu.edu'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'django_q',
    'apps.core',
    'apps.account',
    'apps.sensor',
    # 'apps.input',
    'apps.file',
    # 'apps.task',
    'apps.home',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = BASE_DIR / "media"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'account.User'
LOGIN_REDIRECT_URL = "/sensor/list"
LOGIN_URL = "/account/login/"
LOGOUT_REDIRECT_URL = "/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'retry': 120,
    'compress': True,
    'cpu_affinity': 1,
    'save_limit': 250,
    'queue_limit': 8,
    'catch_up': False, # catch up runs for scheduled jobs after the server is down.
    'label': 'Django Q',
    'orm': 'default',
    # 'redis': {
    #     'host': 'localhost',
    #     'port': 6379,
    #     'db': 0,
    #     'password': None,
    #     'socket_timeout': None,
    #     'charset': 'utf-8',
    #     'errors': 'strict',
    #     'unix_socket_path': None
    # }
    ## Or simply with a redis URL
    # 'redis': 'redis://h:asdfqwer1234asdf@ec2-111-1-1-1.compute-1.amazonaws.com:111'
}

#gmail_send/settings.py
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'simulocean@gmail.com'
EMAIL_HOST_PASSWORD = 'YdpmvVbR22' #past the key or password app here
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'

# Portal Settings
PORTAL_MAX_NUMBER_TASKS = 1
PORTAL_MAX_NUMBER_INPUTS = 4
PORTAL_MAX_NUMBER_FILES_PER_INPUT = 2
