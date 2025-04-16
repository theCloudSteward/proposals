"""
Django settings for cloud_steward_proposals project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import logging
logging.disable(logging.INFO) # You can re‑enable later with logging.disable(logging.NOTSET)

# BASE_DIR explicitly defined
BASE_DIR = Path(__file__).resolve().parent.parent

# Load your environment variables from the .env file
load_dotenv("/root/proposal.thecloudsteward/.env")

# Fetch Stripe keys safely
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

if not STRIPE_SECRET_KEY:
    raise ValueError("STRIPE_SECRET_KEY is missing! Check your .env file.")

if not STRIPE_PUBLISHABLE_KEY:
    raise ValueError("STRIPE_PUBLISHABLE_KEY is missing! Check your .env file.")

# Django SECRET_KEY & DEBUG settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-insecure-key')
DEBUG = (os.getenv('DJANGO_DEBUG', 'False') == 'True')

# Allowed hosts clearly listed
ALLOWED_HOSTS = [
    "137.184.196.174",
    "proposals.thecloudsteward.com",
    "www.proposals.thecloudsteward.com"
]

# Installed apps
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'proposals',
]

# CRITICAL: Correct Middleware Order
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',              # FIRST
    'django.middleware.security.SecurityMiddleware',      # Next
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS/CSRF Settings clearly set
CORS_ALLOWED_ORIGINS = [
    "https://proposals.thecloudsteward.com",
    "https://www.proposals.thecloudsteward.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://proposals.thecloudsteward.com",
    "https://www.proposals.thecloudsteward.com",
]

ROOT_URLCONF = 'cloud_steward_proposals.urls'

# Template settings (React integration)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / '../frontend/build'],  # React build folder
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

WSGI_APPLICATION = 'cloud_steward_proposals.wsgi.application'

# SQLite database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = '/var/www/proposals_static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / '../frontend/build/static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

######################################
# LOGGING CONFIGURATION
######################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # The main Django logger
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Always show debug in logs
            'propagate': True,
        },
        # Your own app's loggers (adjust if your files are in a different package)
        'proposals': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cloud_steward_proposals': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Catch-all for any other loggers
        # This is optional but can help if your logger name is something else
        # '__main__': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
    },
}
