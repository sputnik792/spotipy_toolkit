from state_manager import get_last_checked, update_last_checked
from artist_tracker import get_artist_id, get_new_releases_since_last_check

def update_playlist(sp, playlist):
    artist_id = get_artist_id(sp, playlist['artist'])
    if not artist_id:
        print(f"Artist {playlist['artist']} not found")
        return

    last_checked = get_last_checked(playlist['id'])
    new_tracks = get_new_releases_since_last_check(sp, artist_id, last_checked)
    existing_tracks = get_existing_tracks(sp, playlist['id'])
    
    # Filter out duplicates
    to_add = [t for t in new_tracks if t['uri'] not in existing_tracks]
    
    if to_add:
        # Add new tracks at top while preserving album order
        add_tracks_to_playlist(sp, playlist['id'], to_add)
        print(f"Added {len(to_add)} new tracks to {playlist['name']}")
    else:
        print(f"No new tracks found for {playlist['name']}")
    
    # Update checkpoint even if no new tracks were found
    update_last_checked(playlist['id'], playlist['artist'], playlist['name'])

def add_tracks_to_playlist(sp, playlist_id, tracks):
    # Group by album and maintain order
    albums = {}
    for track in tracks:
        if track['album_uri'] not in albums:
            albums[track['album_uri']] = []
        albums[track['album_uri']].append(track)
    
    # Add album by album to maintain track order
    for album_uri, album_tracks in albums.items():
        sp.playlist_add_items(playlist_id, [t['uri'] for t in album_tracks], position=0)
