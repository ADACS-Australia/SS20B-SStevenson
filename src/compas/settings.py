"""
Django settings for compas project.

Generated by 'django-admin startproject' using Django 2.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ

# env = environ.Env(DEBUG=(bool, False),)
# environ.Env.read_env(".env")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env("DEBUG")

DEBUG = os.environ.get("DEBUG", False)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "_ph%7&w0q+p7ab^hztsuy)z-i1^461j4hfry4h87y6ia^t+4#h"

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "compas",
    "compasweb",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "compas.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "compas.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    # }
    'default': {
        'ENGINE': os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
        'NAME': os.environ.get("MYSQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        'USER': os.environ.get("MYSQL_USER", "user"),
        'PASSWORD': os.environ.get("MYSQL_PASSWORD", "password"),
        'HOST': os.environ.get("MYSQL_HOST", "localhost"),
        'PORT': os.environ.get("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Australia/Melbourne"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# ROOT_SUBDIRECTORY_PATH = env("ROOT_SUBDIRECTORY_PATH", default="")
ROOT_SUBDIRECTORY_PATH = os.environ.get("ROOT_SUBDIRECTORY_PATH", "")

STATIC_URL = os.path.join("/", ROOT_SUBDIRECTORY_PATH, "static/")

STATIC_ROOT = os.path.join(BASE_DIR, "static-files/")

MEDIA_ROOT = os.path.join(BASE_DIR, "../files/")

MEDIA_URL = os.path.join("/", ROOT_SUBDIRECTORY_PATH, "files/")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
    os.path.join(BASE_DIR, "compasweb/static/"),
]

FIXTURE_DIRS = (os.path.join(BASE_DIR, "compasweb/fixtures/"),)

# Bokeh server configuration. If not specified, assume a default local server which means the COMPAS_HOST needs to be empty
COMPAS_HOST = os.environ.get("COMPAS_HOST", default="")
if COMPAS_HOST:
    BOKEH_SERVER = os.path.join(COMPAS_HOST, ROOT_SUBDIRECTORY_PATH, "bokeh/compas_hexbinplot")
else:
    # assume local development
    BOKEH_SERVER = "http://localhost:5006/compas_hexbinplot"

# Celery broker
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
CELERYD_SOFT_TIME_LIMIT = 10
CELERYD_TIME_LIMIT = 15

COMPAS_EXECUTABLE_PATH = os.environ.get('COMPAS_EXECUTABLE_PATH')
COMPAS_INPUT_DIR_PATH = os.environ.get('COMPAS_INPUT_DIR_PATH')
COMPAS_LOGS_OUTPUT_DIR_PATH = os.environ.get('COMPAS_LOGS_OUTPUT_DIR_PATH')

COMPAS_IO_PATH = (
    COMPAS_LOGS_OUTPUT_DIR_PATH if COMPAS_LOGS_OUTPUT_DIR_PATH != '' else os.path.join(MEDIA_ROOT, 'jobs/')
)
