from core.config.base import * #noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ["127.0.0.1"]