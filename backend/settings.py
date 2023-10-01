from os import environ, getenv
from os.path import join, dirname
from pathlib import Path
from dotenv import dotenv_values

# get flask env
flask_env = environ.get("ENV", "development")
FLASK_ENV = flask_env

# get the .env.{env-name} configs
dirname = dirname(__file__)
filename = join(dirname, f"../.env.{flask_env}")
configs = dotenv_values(dotenv_path=filename, verbose=True)

# settings - flask
DEBUG = configs.get("FLASK_DEBUG", 0)
FLASK_APP = "main.py"

# settings - sql alchemy configs
SQLALCHEMY_DATABASE_URI = configs.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# settings - TCG Player
TCG_API_BEARER_KEY = ""