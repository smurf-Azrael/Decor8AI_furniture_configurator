from os import environ
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("DECOR8AI_API_KEY")
BASE_URL = os.environ.get("DECOR8AI_BASE_URL")

