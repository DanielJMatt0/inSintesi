import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///insintesi.db")

# Mistral API configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-medium-latest")

if not MISTRAL_API_KEY:
    raise ValueError("Missing MISTRAL_API_KEY in environment variables.")
