from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test-secret-key"

DEBUG = True

ALLOWED_HOSTS = []

#adding django channels to installed apps
INSTALLED_APPS = [
    "daphne",
    "channels",
    "users",
    "channels_app",
    "messaging",
]

MIDDLEWARE = [] 
ROOT_URLCONF = "chat_project.urls"
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
