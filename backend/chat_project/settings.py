# Import Path to handle project directories
from pathlib import Path

# Base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY KEY (used by Django for cryptographic signing)
SECRET_KEY = 'dev-secret-key'

# Debug mode (True for development, should be False in production)
DEBUG = True

# Allowed hosts (empty for local development)
ALLOWED_HOSTS = []


# ---------------------------------------------------
# INSTALLED APPLICATIONS
# ---------------------------------------------------
INSTALLED_APPS = [

    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django REST Framework (for building APIs)
    'rest_framework',

    # Project applications
    'users',
    'channels_app',
    'messaging',
    'files',
    'notification',
]


# ---------------------------------------------------
# MIDDLEWARE
# Middleware processes request/response lifecycle
# ---------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # Protects against CSRF attacks
    'django.middleware.csrf.CsrfViewMiddleware',

    # Handles authentication of users
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Message framework
    'django.contrib.messages.middleware.MessageMiddleware',
]


# Root URL configuration
ROOT_URLCONF = 'chat_project.urls'


# ---------------------------------------------------
# TEMPLATES CONFIGURATION
# Used for rendering HTML templates
# ---------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Template directory (empty because project is API based)
        'DIRS': [],

        # Enables template loading inside apps
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [

                # Debug information
                'django.template.context_processors.debug',

                # Adds request object to templates
                'django.template.context_processors.request',

                # Authentication context
                'django.contrib.auth.context_processors.auth',

                # Message context
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ---------------------------------------------------
# DATABASE CONFIGURATION (PostgreSQL)
# ---------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',   # PostgreSQL database engine

        'NAME': 'chat_db',                            # Database name

        'USER': 'postgres',                           # PostgreSQL username

        'PASSWORD': 'postgres123',                    # Password set during installation

        'HOST': 'localhost',                          # Database host

        'PORT': '5432',                               # Default PostgreSQL port
    }
}


# ---------------------------------------------------
# STATIC FILES
# Used for CSS / JS / Images
# ---------------------------------------------------
STATIC_URL = 'static/'


# Default primary key type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------
# CUSTOM USER MODEL
# ---------------------------------------------------
# Tells Django to use our custom user model
AUTH_USER_MODEL = 'users.User'


# ---------------------------------------------------
# PASSWORD VALIDATION
# Ensures strong password policies
# ---------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [

    # Prevent passwords similar to username
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    # Minimum password length validator
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    # Prevent common passwords
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    # Prevent numeric-only passwords
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]