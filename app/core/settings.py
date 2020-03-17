import os

import databases
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

# Config will be read from environment variables and/or ".env" files.
config = Config(".env")

# Directories
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Mode
DEBUG = config("DEBUG", cast=bool, default=False)

# Security
SECRET_KEY = config("SECRET_KEY", cast=Secret)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings)

# Database
DATABASE_URL = config("DATABASE_URL", cast=databases.DatabaseURL)

# Caching
REDIS_URL = config("REDIS_URL")

app = Starlette(debug=DEBUG)