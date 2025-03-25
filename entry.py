from pick import get_picks_from_entry

def get_entries_from_api_response(api_response):
    """Returns a list of Entry objects from the API response."""
    entries = []
    for entry in api_response["entries"]:
        entry_id = entry["id"]
        entry_name = entry["name"]
        entry_username = entry["member"]["displayName"]
        entry_picks = get_picks_from_entry(entry["picks"])
        entries.append(Entry(entry_id, entry_name, entry_username, entry_picks))
    return entries

class Entry:
    """Represents an entry by a user in the challenge."""
    def __init__(self, id, name, username, picks):
        self.id = id
        self.name = name
        self.username = username
        self.picks = picks

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
