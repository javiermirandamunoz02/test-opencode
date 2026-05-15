from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
SECRET_KEY = os.environ["SECRET_KEY"]
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

import re
match = re.match(r"postgres://(.+):(.+)@(.+):(\d+)/(.+)", os.environ["DATABASE_URL"])
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": match.group(5),
        "USER": match.group(1),
        "PASSWORD": match.group(2),
        "HOST": match.group(3),
        "PORT": match.group(4),
    }
}

STATIC_ROOT = BASE_DIR / "staticfiles"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
