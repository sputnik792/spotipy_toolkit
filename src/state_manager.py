import json
from pathlib import Path
from datetime import datetime, timedelta

def get_last_checked(playlist_id):
    state_file = Path(f"state_{playlist_id}.json")
    try:
        data = json.loads(state_file.read_text())
        return datetime.fromisoformat(data['last_checked'])
    except:
        # Default to 30 days ago if no state exists
        return datetime.now() - timedelta(days=30)

def update_last_checked(playlist_id, artist_name, playlist_name):
    state_file = Path(f"state_{playlist_id}.json")
    state_file.write_text(json.dumps({
        'last_checked': datetime.now().isoformat(),
        'artist': artist_name,
        'playlist_name': playlist_name
    }))
