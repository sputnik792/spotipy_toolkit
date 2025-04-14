from datetime import datetime
from artist_tracker import get_artist_id, get_new_tracks

def update_all_playlists(sp):
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
        print(f"Artist {playlist['artist']} not found")
        return

    existing = get_existing_tracks(sp, playlist['id'])
    new_tracks = get_new_tracks(sp, artist_id)
    
    # Filter duplicates
    to_add = [t for t in new_tracks if t['uri'] not in existing]
    
    if to_add:
        # Add new tracks at top
        sp.playlist_add_items(playlist['id'], [t['uri'] for t in to_add], position=0)
        print(f"Added {len(to_add)} tracks to {playlist['name']}")
    else:
        print(f"No new tracks for {playlist['name']}")

def get_existing_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    
    while results:
        tracks.extend(item['track']['uri'] for item in results['items'])
        results = sp.next(results) if results['next'] else None
    
    return tracks

def extract_artist(desc):
    # Format: "#auto-update @Artist"
    parts = desc.split('@')
    return parts[-1].strip() if len(parts) > 1 else None
