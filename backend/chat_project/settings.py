# Import Path to handle project directories
from pathlib import Path

# Base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test-secret-key"

DEBUG = True

ALLOWED_HOSTS = []

#adding django channels to installed apps
INSTALLED_APPS = [

    # Project applications
    "daphne",
    "channels",
    "users",
    "channels_app",
    "messaging",
    'files',
   # 'notification'

     # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

     # Django REST Framework (for building APIs)
    'rest_framework'
]

# Middleware processes request/response lifecycle
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

#Root URL configuration
ROOT_URLCONF = "chat_project.urls"

#template configuration
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

#database configuration
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
#static files 
STATIC_URL = 'static/'

# Default primary key type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tells Django to use our custom user model
AUTH_USER_MODEL = 'users.User'

#password validation
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

#defining ASGI as django uses WSGI
ASGI_APPLICATION = "chat_project.asgi.application"

#configuring redis as message broker
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

#logging configuration 
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    #formatters
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },

    #defining handlers
    "handlers": {
        #for connection events
        "websocket_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/websocket.log",
            "formatter": "verbose",
        },
        #for message flow
        "message_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/messages.log",
            "formatter": "verbose",
        },
        #for failures
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "logs/errors.log",
            "formatter": "verbose",
        },
    },

    "loggers": {
        "websocket": {
            "handlers": ["websocket_file"],
            "level": "INFO",
            "propagate": True,
        },

        "messaging": {
            "handlers": ["message_file"],
            "level": "INFO",
            "propagate": True,
        },

        "django": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
