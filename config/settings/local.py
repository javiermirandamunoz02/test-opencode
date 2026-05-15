from .base import *

DEBUG = True

DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://school:school_pass@localhost:5432/school_db")
import re
match = re.match(r"postgres://(.+):(.+)@(.+):(\d+)/(.+)", DATABASE_URL)
if match:
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
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
