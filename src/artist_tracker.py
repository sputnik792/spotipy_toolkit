from datetime import datetime, timedelta

def get_new_releases_since_last_check(sp, artist_id, last_checked_date):
    """Get only tracks released AFTER last_checked_date"""
    albums = []
    results = sp.artist_albums(artist_id, album_type=['album', 'single'], limit=50)
    
    while results:
        for album in results['items']:
            album_date = parse_date(album['release_date'])
            if album_date > last_checked_date:
                albums.append(album)
        results = sp.next(results) if results['next'] else None
    
    tracks = []
    for album in albums:
        for track in sp.album_tracks(album['id'])['items']:
            tracks.append({
                'uri': track['uri'],
                'name': track['name'],
                'album': album['name'],
                'release_date': album['release_date']
            })
    
    return tracks
