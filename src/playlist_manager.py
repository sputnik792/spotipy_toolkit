from artist_tracker import get_new_tracks
from utils import parse_release_date

def get_managed_playlists(sp):
    """Find playlists with #auto-update in description"""
    playlists = []
    results = sp.current_user_playlists()
    
    while results:
        for playlist in results['items']:
            if playlist['description'] and "#auto-update" in playlist['description'].lower():
                artist_name = extract_artist_from_description(playlist['description'])
                if artist_name:
                    playlists.append({
                        'id': playlist['id'],
                        'name': playlist['name'],
                        'artist_name': artist_name
                    })
        results = sp.next(results) if results['next'] else None
    return playlists

def update_managed_playlists(sp):
    playlists = get_managed_playlists(sp)
    for playlist in playlists:
        update_playlist(sp, playlist)

def update_playlist(sp, playlist_id, artist_id):
    """
    Update playlist with new songs while preserving:
    1. Chronological order (newest first)
    2. Original album track order
    3. Existing song positions
    """
    # Get current playlist tracks (to avoid duplicates)
    existing_tracks = []
    results = sp.playlist_tracks(playlist_id)
    existing_tracks.extend([item['track']['uri'] for item in results['items']])
    
    while results['next']:
        results = sp.next(results)
        existing_tracks.extend([item['track']['uri'] for item in results['items']])

    # Get artist's new releases
    new_tracks = get_new_tracks(sp, artist_id)
    
    # Filter out duplicates and already existing tracks
    new_tracks = [t for t in new_tracks 
                 if t['uri'] not in existing_tracks]
    
    if not new_tracks:
        print(f"No new tracks found for playlist {playlist_id}")
        return

    # Group new tracks by album
    albums = {}
    for track in new_tracks:
        if track['album_uri'] not in albums:
            albums[track['album_uri']] = {
                'name': track['album_name'],
                'release_date': track['release_date'],
                'tracks': []
            }
        albums[track['album_uri']]['tracks'].append(track)

    # Sort albums by release date (newest first)
    sorted_albums = sorted(albums.values(), 
                          key=lambda x: parse_release_date(x['release_date']), 
                          reverse=True)

    # Prepare track batches to insert (maintaining album order)
    tracks_to_add = []
    for album in sorted_albums:
        # Sort tracks by their original album position
        album['tracks'].sort(key=lambda x: x['track_number'])
        tracks_to_add.extend([t['uri'] for t in album['tracks']])

    # Get current playlist details to determine insert position
    playlist = sp.playlist(playlist_id)
    current_snapshot = playlist['snapshot_id']

    # Add tracks at the top while preserving album groups
    sp.playlist_add_items(playlist_id, tracks_to_add, position=0)
    
    # Re-sort the entire playlist (your existing sorting logic)
    final_sort_playlist(sp, playlist_id)

    print(f"Added {len(tracks_to_add)} new tracks to playlist {playlist_id}")

def final_sort_playlist(sp, playlist_id):
    """Your existing sorting implementation"""
    # 1. Get all tracks with metadata
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    
    while results:
        tracks.extend([{
            'uri': item['track']['uri'],
            'name': item['track']['name'],
            'release_date': item['track']['album']['release_date'],
            'album_name': item['track']['album']['name'],
            'track_number': item['track']['track_number']
        } for item in results['items']])
        
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    
    # 2. Group by album and sort
    albums = {}
    for track in tracks:
        if track['album_name'] not in albums:
            albums[track['album_name']] = {
                'release_date': track['release_date'],
                'tracks': []
            }
        albums[track['album_name']]['tracks'].append(track)
    
    # Sort albums by release date (newest first)
    sorted_albums = sorted(albums.values(),
                          key=lambda x: parse_release_date(x['release_date']),
                          reverse=True)
    
    # Rebuild track order
    new_order = []
    for album in sorted_albums:
        album['tracks'].sort(key=lambda x: x['track_number'])
        new_order.extend([t['uri'] for t in album['tracks']])
    
    # 3. Reorder playlist
    sp.playlist_replace_items(playlist_id, new_order)
