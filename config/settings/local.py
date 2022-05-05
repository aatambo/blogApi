from .base import *

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = str(os.getenv("SECRET_KEY"))

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(os.getenv("db_NAME")),
        "USER": str(os.getenv("db_USER")),
        "PASSWORD": str(os.getenv("db_PASSWORD")),
        "HOST": str(os.getenv("db_HOST")),
        "PORT": "",
    }
}

# email


EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_HOST = "smtp.gmail.com"

EMAIL_HOST_USER = str(os.getenv("EMAIL_HOST_USER"))

EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_HOST_PASSWORD"))

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
