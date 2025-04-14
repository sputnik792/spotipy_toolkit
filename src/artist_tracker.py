from datetime import datetime

def get_artist_id(sp, artist_name):
    results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
    return results['artists']['items'][0]['id'] if results['artists']['items'] else None

def get_new_tracks(sp, artist_id, days_back=60):
    cutoff = datetime.now() - timedelta(days=days_back)
    albums = []
    results = sp.artist_albums(artist_id, album_type=['album', 'single'])
    
    while results:
        albums.extend([
            album for album in results['items']
            if parse_date(album['release_date']) > cutoff
        ])
        results = sp.next(results) if results['next'] else None
    
    tracks = []
    for album in albums:
        tracks.extend([
            {
                'uri': track['uri'],
                'name': track['name'],
                'album': album['name'],
                'release_date': album['release_date']
            }
            for track in sp.album_tracks(album['id'])['items']
        ])
    
    return tracks

def parse_date(date_str):
    parts = date_str.split('-')
    year = int(parts[0])
    month = int(parts[1]) if len(parts) > 1 else 1
    day = int(parts[2]) if len(parts) > 2 else 1
    return datetime(year, month, day)
