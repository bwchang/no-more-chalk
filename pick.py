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

class Pick:
    """Represents a pick made for a game."""
    def __init__(self, proposition_id, outcome_picked_id, outcome_picked_result):
        self.proposition_id = proposition_id
        self.outcome_picked_id = outcome_picked_id
        self.outcome_picked_result = outcome_picked_result

    def get_proposition_id(self):
        return self.proposition_id

    def get_outcome_picked_id(self):
        return self.outcome_picked_id

    def get_outcome_picked_result(self):
        return self.outcome_picked_result