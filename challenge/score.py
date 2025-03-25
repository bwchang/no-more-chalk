UNDECIDED = "UNDECIDED"
CORRECT = "CORRECT"
INCORRECT = "INCORRECT"

def build_outcome_frequency(all_entries):
    """Returns a dictionary of outcome IDs and their frequency of being picked for each proposition."""
    outcome_frequency = {}
    for entry in all_entries:
        for pick in entry.picks:
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

def calculate_group_uniqueness_score(entry, outcome_frequency, all_propositions):
    """
    Returns the group uniqueness score for an entry.

    The group uniqueness score is calculated as follows:
    - A valid prediction is defined as one where your predicted winner is playing in the matchup.
    - For each valid prediction you made, you receive 1/X points,
      where X is the number of entries that picked the same outcome as you.
    - For each invalid prediction you made, you receive 1/2X points.
    """
    scores = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}
    for pick in entry.picks:
        # Skip picks that are still undecided
        if pick.outcome_picked_result == UNDECIDED:
            continue

        proposition = [prop for prop in all_propositions if prop.id == pick.proposition_id][0]
        # Skip future rounds
        if proposition.actual_outcome_ids is None or len(proposition.actual_outcome_ids) == 0:
            continue

        prop_frequencies = outcome_frequency.get(pick.proposition_id, {})
        outcome_frequency_for_proposition = prop_frequencies.get(pick.outcome_picked_id, 0)

        # Calculate the score for the pick
        pick_score = 1 / outcome_frequency_for_proposition
        if pick.outcome_picked_id not in proposition.actual_outcome_ids:
            # The pick is invalid
            pick_score = pick_score / 2

        # Add the rounded score to the total score for the scoring period
        scores[proposition.scoring_period_id] += pick_score

    # Round the total score to two decimal places
    for key in scores:
        scores[key] = round(scores[key], 2)

    return scores

def calculate_global_uniqueness_score(entry, all_propositions):
    """
    Returns the global uniqueness score for an entry.

    The global uniqueness score is calculated as follows:
    - A valid prediction is defined as one where your predicted winner is playing in the matchup.
    - For each valid prediction you made, you receive 1-X points,
      where X is the percentage of entries globally that picked the same outcome as you.
    - For each invalid prediction you made, you receive (1-X)/2 points.
    """
    scores = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}
    for pick in entry.picks:
        # Skip picks that are still undecided
        if pick.outcome_picked_result == UNDECIDED:
            continue

        proposition = [prop for prop in all_propositions if prop.id == pick.proposition_id][0]
        # Skip future rounds
        if proposition.actual_outcome_ids is None or len(proposition.actual_outcome_ids) == 0:
            continue

        # Calculate the score for the pick
        global_percentage_picked = proposition.get_percentage_for_outcome(pick.outcome_picked_id)
        pick_score = 1 - global_percentage_picked
        if pick.outcome_picked_id not in proposition.actual_outcome_ids:
            # The pick is invalid
            pick_score = pick_score / 2

        # Add the rounded score to the total score for the scoring period
        scores[proposition.scoring_period_id] += pick_score

    # Round the total score to two decimal places
    for key in scores:
        scores[key] = round(scores[key], 2)

    return scores
