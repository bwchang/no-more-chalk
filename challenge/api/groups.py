import requests

from settings import CHALLENGE_ID, GROUP_ID, BASE_URL
from challenge.entries import Entry, Pick


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


def get_entries_from_api_response(api_response):
    """Returns a list of Entry objects from the API response."""
    entries = []
    for entry in api_response["entries"]:
        entry_id = entry["id"]
        entry_name = entry["name"]
        entry_username = entry["member"]["displayName"]
        entry_picks = get_picks_from_entry(entry["picks"])
        entry_score = entry["score"]["overallScore"]
        entries.append(Entry(entry_id, entry_name, entry_username, entry_picks, entry_score))
    return entries


def get_picks_from_entry(api_response_picks):
    """Returns a list of Pick objects from the API response entry's picks."""
    picks = []
    for pick in api_response_picks:
        proposition_id = pick["propositionId"]
        outcome_picked = pick["outcomesPicked"][0]
        outcome_picked_id = outcome_picked["outcomeId"]
        outcome_picked_result = outcome_picked["result"]
        picks.append(Pick(proposition_id, outcome_picked_id, outcome_picked_result))
    return picks
