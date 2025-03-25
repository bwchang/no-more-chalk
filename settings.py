import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file into the environment

GROUP_ID = os.getenv("GROUP_ID")
CHALLENGE_ID = os.getenv("CHALLENGE_ID")
BASE_URL = "https://gambit-api.fantasy.espn.com/apis/v1"