import csv

from api import get_group_entries, get_propositions
from settings import CHALLENGE_ID, GROUP_ID
    
UNDECIDED = "UNDECIDED"
CORRECT = "CORRECT"
INCORRECT = "INCORRECT"

output_filename = "uniqueness_scores.csv"
row_headers = [
    "Entry Name",
    "Total Score (group)",
    "R1 (group)",
    "R2 (group)",
    "R3 (group)",
    "R4 (group)",
    "R5 (group)",
    "R6 (group)",
]

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

def calculate_uniqueness_score(entry, outcome_frequency, all_propositions):
    """
    Returns the uniqueness score for an entry.

    The uniqueness score is calculated as follows:
    - A valid prediction is defined as one where your predicted winner is playing in the matchup.
    - For each valid prediction you made, you receive 1/X points,
      where X is the number of entries that picked the same outcome as you.
    - For each invalid prediction you made, you receive 1/2X points.
    """
    score = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}
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
        score[proposition.scoring_period_id] += pick_score

    # Round the total score to two decimal places
    for key in score:
        score[key] = round(score[key], 2)

    return score

def run():
    if GROUP_ID is None:
        print("GROUP_ID is not set. Please define it in a .env file.")
        exit(1)

    if CHALLENGE_ID is None:
        print("CHALLENGE_ID is not set. Please define it in a .env file.")
        exit(1)

    print(f"SCRIPT: Calculating uniqueness scores for group {GROUP_ID} in challenge {CHALLENGE_ID}")
    print("SCRIPT: Fetching data from ESPN...")

    group_response = get_group_entries()
    if not group_response["success"]:
        print("An error occurred fetching data from ESPN.")
        exit(1)

    all_entries = group_response["data"]
    print(f"SCRIPT: Found {len(all_entries)} entries in group {GROUP_ID}")

    outcome_frequency = build_outcome_frequency(all_entries)

    propositions_response = get_propositions()
    if not propositions_response["success"]:
        print("An error occurred fetching data from ESPN.")
        exit(1)

    all_propositions = propositions_response["data"]

    output = [row_headers]

    for entry in all_entries:
        score = calculate_uniqueness_score(entry, outcome_frequency, all_propositions)
        output.append([
            entry.name,
            round(sum(score.values()), 2),
            score[1],
            score[2],
            score[3],
            score[4],
            score[5],
            score[6],
        ])

    with open(output_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output)

    print(f"SCRIPT: Uniqueness scores written to {output_filename}")

if __name__ == "__main__":
    run()
