# no-more-chalk
Tired of everyone in your March Madness group picking chalk for every matchup? Do you want to encourage
some wild and exciting upset picks in your group? Reward those more creative minds by having a "uniqueness" award in addition to a bracket winner!

This script calculates a "uniqueness" score for each bracket in your group - you score more points for picks that have fewer repeats within the group. However, you can't just pick underdogs for the sake of picking underdogs - if your predicted winner doesn't play in the matchup, you receive a half-score penalty.

The group uniqueness score is calculated as follows:
- A valid prediction is defined as one where your predicted winner is playing in the matchup.
- For each valid prediction you made, you receive 1/X points, where X is the number of entries that picked the same outcome as you in the group.
- For each invalid prediction you made, you receive 1/2X points.
- The uniqueness score of your bracket is the sum of your score for each matchup.

There is also a bonus global uniqueness score that compares your pick against the global pick percentage across all brackets.

The global uniqueness score is calculated as follows:
- A valid prediction is defined as one where your predicted winner is playing in the matchup.
- For each valid prediction you made, you receive 1-X points, where X is the percentage of entries that picked the same outcome as you in the world.
- For each invalid prediction you made, you receive (1-X)/2 points.
- The uniqueness score of your bracket is the sum of your score for each matchup.

## Usage
1. Install dependencies.
```
pip install -r requirements.txt
```
2. Populate challenge and group ID in an `.env` file:
```
GROUP_ID=...
CHALLENGE_ID=...
```
3. Run the script.
```
python script.py
```
This will output the results in csv format to `uniqueness_scores.csv`.