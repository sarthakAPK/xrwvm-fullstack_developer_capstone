"""
Django settings for djangoproj project.
Final integrated configuration with static files fix
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# Security & Core Settings
# ========================
SECRET_KEY = 'django-insecure-ccow$tz_=9%dxu4(0%^(z%nx32#s@(zt9$ih@)5l54yny)wm-0'
DEBUG = True

# Host/Proxy Configuration (Wildcards for all variations)
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.proxy.cognitiveclass.ai',
    '.cognitiveclass.ai'
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.proxy.cognitiveclass.ai',
    'https://*.cognitiveclass.ai'
]

# =================
# Security Headers
# =================
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = 'same-origin'
USE_X_FORWARDED_HOST = True

# =================
# Application Definition
# =================
INSTALLED_APPS = [
    'djangoapp.apps.DjangoappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'djangoproj.urls'

# =============
# Templates
# =============
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend/static')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['django.templatetags.static'],
        },
    },
]

WSGI_APPLICATION = 'djangoproj.wsgi.application'

# =============
# Database
# =============
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===================
# Password Validation
# ===================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {'user_attributes': ('username', 'email'), 'max_similarity': 0.7}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =================
# Internationalization
# =================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# =================
# Static Files (FIXED)
# =================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Production collected files

# Development static directories (create these folders)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/static'),  # Your frontend assets
    # os.path.join(BASE_DIR, 'static'),  # Only uncomment if you create this folder
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =================
# Default primary key
# =================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =================
# Development Overrides
# =================
if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
    