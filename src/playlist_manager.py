import json
from pathlib import Path

def update_playlist(sp, playlist):
    # Load last checked date
    state_file = Path(f"state_{playlist['id']}.json")
    try:
        last_checked = datetime.fromisoformat(json.loads(state_file.read_text())['last_checked'])
    except:
        last_checked = datetime.now() - timedelta(days=60)  # Default: check last 60 days
    
    artist_id = get_artist_id(sp, playlist['artist'])
    if not artist_id:
        return

    # Get only NEW releases since last check
    new_tracks = get_new_releases_since_last_check(sp, artist_id, last_checked)
    existing_tracks = get_existing_tracks(sp, playlist['id'])
    
    # Filter out duplicates
    to_add = [t for t in new_tracks if t['uri'] not in existing_tracks]
    
    if to_add:
        # Add new tracks at top
        sp.playlist_add_items(playlist['id'], [t['uri'] for t in to_add], position=0)
        print(f"Added {len(to_add)} new tracks to {playlist['name']}")
    
    # Update checkpoint
    state_file.write_text(json.dumps({
        'last_checked': datetime.now().isoformat(),
        'artist': playlist['artist'],
        'playlist_name': playlist['name']
    }))
