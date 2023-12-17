import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'app_fossils.apps.AppFossilsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'debug_toolbar',
    'django_resized',
    'tinymce',
    'captcha',
    'axes',
    'formtools',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'axes.middleware.AxesMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'fossils.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates', 'allauth')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app_fossils.context_processors.user_species',
            ],
        },
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

WSGI_APPLICATION = 'fossils.wsgi.application'

TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'toolbar': "undo redo | styleselect | bold italic underline | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | fullscreen | fontselect | fontsizeselect | forecolor backcolor | subscript superscript | removeformat | table | hr",
    'menubar': True,
    'forced_root_block': 'div',
    'plugins': 'table hr image'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

AXES_FAILURE_LIMIT = 10

ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Shared Projects APP ⋮ '
DEFAULT_FROM_EMAIL = 'app@sharedprojects.co.uk'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.ionos.co.uk'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'app@sharedprojects.co.uk'
EMAIL_HOST_PASSWORD = config('IONOS_PASSWORD')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'PNG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'PNG': ".png"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'homepage'
LOGOUT_REDIRECT_URL = 'homepage'
