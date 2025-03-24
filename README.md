# no-more-chalk
Tired of everyone in your March Madness group picking chalk for every matchup? Do you want to encourage
some wild and exciting upset picks in your group? Reward those more creative minds by having a "uniqueness" award in addition to a bracket winner!

This script calculates a "uniqueness" score for each bracket in your group - you score more points for picks that have fewer repeats within the group.

## Usage
1. Install dependencies.
```
python -r requirements.txt
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