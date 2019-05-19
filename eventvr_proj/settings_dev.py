import os

if os.getenv("DJANGO_SETTINGS_MODULE").endswith("dev"):
    from eventvr_proj.settings import *


# DEBUG
DEBUG = True

# ALLOWED_HOSTS
allowed_hosts = os.getenv("ALLOWED_HOSTS")
if allowed_hosts:
    ALLOWED_HOSTS += allowed_hosts.split(",")

# INSTALLED_APPS
INSTALLED_APPS += ["debug_toolbar", "django_extensions"]

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "eventvr_database",
        "USER": "eventvr_db_admin",
        "PASSWORD": os.getenv("PGPASSWORD"),
        "HOST": "localhost",
        "PORT": "",
    }
}

# Channels
if os.getenv("IN_MEMORY_CHANNEL_LAYER"):
    CHANNEL_LAYERS["default"] = {"BACKEND": "channels.layers.InMemoryChannelLayer"}

# Django debug toolbar
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}
SHELL_PLUS_PRINT_SQL = True
