import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
    GEMINI_MODEL = os.environ['GEMINI_MODEL']


settings = Settings()
