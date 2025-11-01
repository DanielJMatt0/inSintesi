import os
from dotenv import load_dotenv


load_dotenv()

# Database configuration

DATABASE_URL = os.getenv("DATABASE_URL")

# Mistral API configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-medium-latest")