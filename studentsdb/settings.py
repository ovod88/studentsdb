"""
Django settings for studentsdb project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from .db import DATABASES
from django.contrib.messages import constants as messages

ADMIN_EMAIL = 'admin@studentsdb.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'upworkem@gmail.com'
EMAIL_HOST_PASSWORD = '0RYD9IC1P4dDLimctL8Y'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

MANAGERS=(('Vova Khrystenko', 'ovod88@bigmir.net'),)

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(jk_lx661t8(-9r60^kz@m$=2rk&c*h5w@mxu&aagqf1^ms(fy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'students'
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

ROOT_URLCONF = 'studentsdb.urls'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'students.templates.mama.testing',
                'studentsdb.custom_context_processor.students_proc',
                'students.groups_context.groups_context_processor',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'studentsdb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

LOG_FILE = os.path.join(BASE_DIR, 'studentsdb.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level'     : 'INFO',
            'class'     : 'logging.StreamHandler',
            'formatter' : 'verbose'
        },
        'file': {
            'level'     : 'INFO',
            'class'     : 'logging.FileHandler',
            'filename'  : LOG_FILE,
            'formatter' : 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers'  : ['console'],
            'propagate' : True,
            'level'     : 'INFO',
            'formatter' : 'simple',
        },
        'students.signals': {
            'handlers' : ['console', 'file'],
            'level'    : 'INFO',
        },
        'students.views.contact_admin': {
            'handlers' : ['console', 'file'],
            'level'    : 'INFO',
        }
    }
}
