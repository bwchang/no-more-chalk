import requests

from settings import CHALLENGE_ID, GROUP_ID
from entry import get_entries_from_api_response
from propositions import get_propositions_from_api_response

BASE_URL = "https://gambit-api.fantasy.espn.com/apis/v1"

def get_group_entries_url():
    """Returns the URL to fetch the group data for this challenge."""
    return f"{BASE_URL}/challenges/{CHALLENGE_ID}/groups/{GROUP_ID}"

def get_group_entries():
    """Returns the group data for this challenge."""
    try:
        response = requests.get(get_group_entries_url()).json()
    except Exception as e:
        print(f"An error occurred fetching data from ESPN: {e}")
        return {"success": False}
    return {"success": True, "data": get_entries_from_api_response(response)}

def get_propositions_url():
    """Returns the URL to fetch the propositions for this challenge."""
    return f"{BASE_URL}/propositions"

def get_propositions():
    params = {
        "challengeId": CHALLENGE_ID,
    }
    try:
        response = requests.get(get_propositions_url(), params=params).json()
    except Exception as e:
        print(f"An error occurred fetching data from ESPN: {e}")
        return {"success": False}
    return {"success": True, "data": get_propositions_from_api_response(response)}