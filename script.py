import csv

from challenge.api.groups import get_group_entries
from challenge.api.propositions import get_propositions
from challenge.score import (
    calculate_group_uniqueness_score,
    calculate_global_uniqueness_score,
    build_outcome_frequency,
)
from settings import CHALLENGE_ID, GROUP_ID

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
    "Total Score (global)",
    "R1 (global)",
    "R2 (global)",
    "R3 (global)",
    "R4 (global)",
    "R5 (global)",
    "R6 (global)",
]


def run():
    if GROUP_ID is None:
        print("GROUP_ID is not set. Please define it in a .env file.")
        exit(1)

    if CHALLENGE_ID is None:
        print("CHALLENGE_ID is not set. Please define it in a .env file.")
        exit(1)

    print(
        f"SCRIPT: Calculating uniqueness scores for group {GROUP_ID} in challenge {CHALLENGE_ID}"
    )
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
        group_score = calculate_group_uniqueness_score(
            entry, outcome_frequency, all_propositions
        )
        global_score = calculate_global_uniqueness_score(entry, all_propositions)
        output.append(
            [
                entry.name,
                round(sum(group_score.values()), 2),
                group_score[1],
                group_score[2],
                group_score[3],
                group_score[4],
                group_score[5],
                group_score[6],
                round(sum(global_score.values()), 2),
                global_score[1],
                global_score[2],
                global_score[3],
                global_score[4],
                global_score[5],
                global_score[6],
            ]
        )

    with open(output_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output)

    print(f"SCRIPT: Uniqueness scores written to {output_filename}")


if __name__ == "__main__":
    run()
