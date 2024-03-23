import os
from datetime import datetime
from pathlib import Path

now = datetime.now()
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.app.WebAppConfig'
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

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'unit_tests/db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    "app/static"
]

# =============================================================================================================
# Environment Variables
# =============================================================================================================
APPLICATION_NAME = os.environ.get("APPLICATION_NAME", "WaverAlert")
INSTANCE_NAME = os.environ.get("INSTANCE_NAME", "Local")
TELEGRAM_BOT_API_key = os.environ.get("TELEGRAM_BOT_API_KEY", "")
SECRET_KEY = os.environ.get("SECRET_KEY", 'django-insecure-76p^^_#tp0v)$kgy(r2^m^12j@j-mp%a#6^cbc))0tb#pe-4&=')
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(";")
# =============================================================================================================

IS_LOCAL_INSTANCE = INSTANCE_NAME == "Local"
DEBUG = IS_LOCAL_INSTANCE
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

__author__ = "Amin Aghaee"
__copyright__ = f"Copyright {now.year}, {APPLICATION_NAME}"
