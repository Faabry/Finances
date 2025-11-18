"""
Django settings for finance_portal project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url  # New import for easy cloud database configuration

# Load environment variables from .env file
# This should be the very first thing that happens
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE SECURITY AND DEBUG SETTINGS ---
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-insecure-key-for-local-only')

# Use environment variable for DEBUG, defaulting to False for safety
# If DEBUG=True is set in .env, it runs in development mode.
DEBUG = True

# Allow all hosts (*) for initial deployment setup, but restrict in production.
# This variable is loaded from the environment (e.g., ALLOWED_HOSTS="app.example.com,127.0.0.1")
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# --- APPLICATION DEFINITION ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # Your app
    'widget_tweaks',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# ... (Rest of MIDDLEWARE, ROOT_URLCONF, TEMPLATES, WSGI_APPLICATION sections remain the same) ...

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add whitenoise only if you are serving static files through it
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'finance_portal.urls'

# ... (TEMPLATES and WSGI_APPLICATION sections) ...


# --- DATABASE CONFIGURATION (Simplified via dj-database-url) ---

# 1. Get the DATABASE_URL from the environment.
#    In local development, this variable can hold a SQLite path, 
#    or the full Supabase connection string.
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Use dj_database_url to parse the Supabase connection string
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            # REQUIRE SSL for production/Supabase connections
            # This is automatically handled correctly by dj-database-url 
            # if the URL specifies `sslmode=require` or if DEBUG is False.
            ssl_require=not DEBUG
        )
    }
else:
    # Fallback to local SQLite for simple local development if DATABASE_URL is not set
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# --- Password validation (remains the same) ---

# ... (AUTH_PASSWORD_VALIDATORS, I18N, TIME_ZONE, USE_I18N, USE_TZ sections remain the same) ...


# --- STATIC FILES CONFIGURATION ---

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []

# --- DEFAULT PRIMARY KEY FIELD TYPE (remains the same) ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'