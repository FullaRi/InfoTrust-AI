import os
from dotenv import load_dotenv


load_dotenv(override=False)

DEBUG = True if os.getenv("DEBUG") == "True" else False

SECRET_KEY = os.getenv("SECRET_KEY")
CONTACT_REQUEST_DST_EMAIL = os.getenv("CONTACT_REQUEST_DST_EMAIL")
API_URL = os.getenv("API_URL")

MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USE_TLS = True if os.getenv("MAIL_USE_TLS") == "True" else False
MAIL_USE_SSL = True if os.getenv("MAIL_USE_SSL") == "True" else False
MAIL_DEBUG = True if os.getenv("MAIL_DEBUG") == "True" else False

