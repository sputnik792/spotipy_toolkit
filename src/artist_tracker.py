from utils import parse_release_date

def get_artist_id(sp, artist_name):
    results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
    return results['artists']['items'][0]['id'] if results['artists']['items'] else None

def get_new_tracks(artist_id, last_checked_date):
    """Get tracks released after last_checked_date"""
    albums = []
    results = sp.artist_albums(artist_id, album_type=['album', 'single', 'compilation'])
    albums.extend(results['items'])
    
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    
    new_tracks = []
    for album in albums:
        album_date = parse_release_date(album['release_date'])
        if album_date > last_checked_date:
            tracks = sp.album_tracks(album['id'])['items']
            for track in tracks:
                new_tracks.append({
                    'uri': track['uri'],
                    'name': track['name'],
                    'release_date': album['release_date'],
                    'album_name': album['name']
                })
    
    return new_tracks
