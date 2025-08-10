import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')
if ALLOWED_HOSTS is not None:
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')
    CSRF_TRUSTED_ORIGINS = ['https://' + x for x in ALLOWED_HOSTS]
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
else:
    del ALLOWED_HOSTS

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.oauth2',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'yaru': {
        'APP': {
            'client_id': os.getenv('OAUTH_CLIENT_ID'),
            'secret': os.getenv('OAUTH_CLIENT_SECRET'),
            'provider_class': 'core.provider.YaRuProvider',
        }
    },
    'google': {
        "APP": {
            "client_id": os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
            "secret": os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
        },
    }
}

ROOT_URLCONF = 'chatbot.urls'

# Auth Settings
LOGIN_URL = 'login/'
LOGIN_REDIRECT_URL = 'home'

# Required Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

# Database and Static Files
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('SQLITE_DB_PATH'),
    }
}

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
    }
]
