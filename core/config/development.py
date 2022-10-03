from core.config.base import * #noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0"]


THIRD_PARTY_APPS += []

# Middleware Definition
MIDDLEWARE += []


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}