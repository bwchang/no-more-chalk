import requests

from settings import CHALLENGE_ID, BASE_URL
from challenge.propositions import PossibleOutcome, Proposition


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


def get_propositions_from_api_response(response):
    """Returns a list of Proposition objects from the API response."""
    propositions = []
    for proposition in response:
        id = proposition["id"]
        name = proposition["name"]
        scoring_period_id = proposition["scoringPeriodId"]
        scoring_period_matchup_id = proposition["scoringPeriodMatchupId"]
        status = proposition["status"]
        actual_outcome_ids = proposition.get("actualOutcomeIds")
        correct_outcome_id = proposition.get("correctOutcomes", [None])[0]
        possible_outcomes = [
            PossibleOutcome(
                outcome["id"],
                outcome["name"],
                outcome["choiceCounters"][0]["percentage"],
            )
            for outcome in proposition["possibleOutcomes"]
        ]
        propositions.append(
            Proposition(
                id,
                name,
                scoring_period_id,
                scoring_period_matchup_id,
                status,
                actual_outcome_ids,
                correct_outcome_id,
                possible_outcomes,
            )
        )
    return propositions
