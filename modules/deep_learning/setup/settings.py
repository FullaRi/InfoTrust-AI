import os
from dotenv import load_dotenv


load_dotenv(override=False)

DEBUG = True if os.getenv("DEBUG") == "True" else False
APP_PORT = os.getenv("APP_PORT")

MODEL_PATH = os.getenv("MODEL_PATH")
SECRET_KEY = os.getenv("SECRET_KEY")

