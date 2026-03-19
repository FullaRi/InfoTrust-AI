import os
from dotenv import load_dotenv


load_dotenv(override=False)

DEBUG = True if os.getenv("DEBUG") == "True" else False

SECRET_KEY = os.getenv("SECRET_KEY")
APP_PORT = os.getenv("APP_PORT")

AGENT_WEIGHT_SCORE = 0.8
DEEP_LEARNING_WEIGHT_SCORE = 0.2

FACT_CHECK_LOG_PATH = os.getenv("FACT_CHECK_LOG_PATH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")
AI_AGENT_API_URL = os.getenv("AI_AGENT_API_URL")
DEEP_LEARNING_API_URL = os.getenv("DEEP_LEARNING_API_URL")

