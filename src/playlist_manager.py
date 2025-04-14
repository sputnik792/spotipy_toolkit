import json
from datetime import datetime, timedelta
from src.artist_tracker import get_artist_id, get_new_releases_since_last_check

def update_managed_playlists(sp):
    for playlist in get_managed_playlists(sp):
        update_playlist(sp, playlist)

def get_managed_playlists(sp):
    playlists = []
    results = sp.current_user_playlists()
    
    while results:
        for item in results['items']:
            desc = item.get('description', '')
            if "#auto-update" in desc.lower():
                artist = extract_artist(desc)
                if artist:
                    playlists.append({
                        'id': item['id'],
                        'name': item['name'],
                        'artist': artist
                    })
        results = sp.next(results) if results['next'] else None
    return playlists

def update_playlist(sp, playlist):
    artist_id = get_artist_id(sp, playlist['artist'])
    if not artist_id:
        print(f"❌ Artist {playlist['artist']} not found")
        return

    last_checked = get_last_checked(playlist['id'])
    new_tracks = get_new_releases_since_last_check(sp, artist_id, last_checked)
    existing = get_existing_tracks(sp, playlist['id'])
    
    to_add = [t for t in new_tracks if t['uri'] not in existing]
    
    if to_add:
        sp.playlist_add_items(playlist['id'], [t['uri'] for t in to_add], position=0)
        print(f"➕ Added {len(to_add)} tracks to {playlist['name']}")
    
    update_last_checked(playlist['id'], playlist['artist'], playlist['name'])

def get_last_checked(playlist_id):
    try:
        with open(f"state_{playlist_id}.json") as f:
            return datetime.fromisoformat(json.load(f)['last_checked'])
    except:
        return datetime.now() - timedelta(days=30)

def update_last_checked(playlist_id, artist, name):
    with open(f"state_{playlist_id}.json", 'w') as f:
        json.dump({
            'last_checked': datetime.now().isoformat(),
            'artist': artist,
            'playlist_name': name
        }, f)

def extract_artist(desc):
    parts = desc.split('@')
    return parts[-1].strip() if len(parts) > 1 else None

def get_existing_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        tracks.extend(item['track']['uri'] for item in results['items'])
        results = sp.next(results) if results['next'] else None
    return tracks
