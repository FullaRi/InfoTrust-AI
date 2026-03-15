import os
from dotenv import load_dotenv


load_dotenv(override=False)

DEBUG = True if os.getenv("DEBUG") == "True" else False

MODEL_PATH = os.getenv("MODEL_PATH")
SECRET_KEY = os.getenv("SECRET_KEY")

