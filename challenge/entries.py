class Entry:
    """Represents an entry by a user in the challenge."""

    def __init__(self, id, name, username, picks, score):
        self.id = id
        self.name = name
        self.username = username
        self.picks = picks
        self.score = score

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Pick:
    """Represents a pick made for a game."""

    def __init__(self, proposition_id, outcome_picked_id, outcome_picked_result):
        self.proposition_id = proposition_id
        self.outcome_picked_id = outcome_picked_id
        self.outcome_picked_result = outcome_picked_result
