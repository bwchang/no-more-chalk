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

class Proposition:
    """Represents a matchup in the tournament."""
    def __init__(
        self,
        id,
        name,
        scoring_period_id,
        scoring_period_matchup_id,
        status,
        actual_outcome_ids,
        correct_outcome_id,
        possible_outcomes,
    ):
        self.id = id
        self.name = name
        self.scoring_period_id = scoring_period_id
        self.scoring_period_matchup_id = scoring_period_matchup_id
        self.status = status
        self.actual_outcome_ids = actual_outcome_ids
        self.correct_outcome_id = correct_outcome_id
        self.possible_outcomes = possible_outcomes

    def is_complete(self):
        return self.status == "COMPLETE"

    def get_possible_outcomes(self):
        return self.possible_outcomes

    def get_correct_outcome(self):
        if self.correct_outcome_id is None:
            return None
        return [outcome for outcome in self.get_possible_outcomes() if outcome.id == self.correct_outcome_id][0]

    def get_percentage_for_outcome(self, outcome_id):
        outcome = [outcome for outcome in self.get_possible_outcomes() if outcome.id == outcome_id][0]
        if outcome is None:
            return 0.0
        return outcome.percentage

    def __str__(self):
        res = f"Round {self.scoring_period_id} Game {self.scoring_period_matchup_id}: {self.name}"
        if self.status == "COMPLETE" and self.get_correct_outcome() is not None:
            res += f" (Winner: {self.get_correct_outcome().name})"
        return res

    def __repr__(self):
        return str(self)

class PossibleOutcome:
    """Represents a possible outcome for a matchup."""
    def __init__(self, id, name, percentage):
        self.id = id
        self.name = name
        self.percentage = percentage