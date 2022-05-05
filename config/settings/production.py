from .base import *

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = str(os.getenv("SECRET_KEY"))

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = [
    "adrianopc.pythonanywhere.com",
]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# email

EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_HOST = "smtp.gmail.com"

EMAIL_HOST_USER = str(os.getenv("EMAIL_HOST_USER"))

EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_HOST_PASSWORD"))

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# security

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
