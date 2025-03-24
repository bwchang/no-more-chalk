import os
from dotenv import load_dotenv
import requests

from entry import get_entries_from_api_response
    
load_dotenv()  # Load variables from .env file into the environment

GROUP_ID = os.getenv("GROUP_ID")
CHALLENGE_ID = os.getenv("CHALLENGE_ID")
BASE_URL = "https://gambit-api.fantasy.espn.com/apis/v1"

UNDECIDED = "UNDECIDED"
CORRECT = "CORRECT"
INCORRECT = "INCORRECT"


def get_url():
    """Returns the URL to fetch the group data for this challenge."""
    return f"{BASE_URL}/challenges/{CHALLENGE_ID}/groups/{GROUP_ID}"

def build_outcome_frequency(all_entries):
    """Returns a dictionary of outcome IDs and their frequency of being picked for each proposition."""
    outcome_frequency = {}
    for entry in all_entries:
        for pick in entry.get_picks():
            # If the proposition ID is not in the dictionary, add it
            if pick.proposition_id not in outcome_frequency:
                outcome_frequency[pick.proposition_id] = {}

            proposition = outcome_frequency[pick.proposition_id]

            # If the outcome ID is not in the dictionary, add it
            if pick.outcome_picked_id not in proposition:
                proposition[pick.outcome_picked_id] = 0

            # Increment the count for the outcome ID
            proposition[pick.outcome_picked_id] += 1
    return outcome_frequency

def calculate_uniqueness_score(entry, outcome_frequency, entries_count):
    """
    Returns the uniqueness score for an entry.

    The uniqueness score is calculated as follows:
    - A valid prediction is defined as one where your predicted winner is playing in the matchup.
    - For each valid prediction you made, you receive N-X points,
      where N is the total number of entries
      and X is the number of entries that picked the same outcome as you.
    - For each invalid prediction you made, you receive (N-X)/2 points.
    """
    score = 0
    for pick in entry.get_picks():
        # Skip picks that are still undecided
        if pick.get_outcome_picked_result() == UNDECIDED:
            continue

        proposition = outcome_frequency.get(pick.get_proposition_id(), {})
        outcome_frequency_for_proposition = proposition.get(pick.get_outcome_picked_id(), 0)

        # Calculate the score for the pick and add it to the entry's total score
        score += entries_count - outcome_frequency_for_proposition
    return score

def run():
    if GROUP_ID is None:
        print("GROUP_ID is not set. Please define it in a .env file.")
        exit(1)

    if CHALLENGE_ID is None:
        print("CHALLENGE_ID is not set. Please define it in a .env file.")
        exit(1)

    try:
        api_response = requests.get(get_url()).json()
    except Exception as e:
        print(f"An error occurred fetching data from ESPN: {e}")
        exit(1)

    all_entries = get_entries_from_api_response(api_response)
    entries_count = len(all_entries)

    outcome_frequency = build_outcome_frequency(all_entries)
    for entry in all_entries:
        print(f"{entry}: {calculate_uniqueness_score(entry, outcome_frequency, entries_count)}")

if __name__ == "__main__":
    run()
