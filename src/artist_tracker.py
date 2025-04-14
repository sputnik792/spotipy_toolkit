from datetime import datetime

def get_artist_id(sp, artist_name):
    results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
    return results['artists']['items'][0]['id'] if results['artists']['items'] else None

def get_new_releases_since_last_check(sp, artist_id, last_checked_date):
    albums = []
    results = sp.artist_albums(artist_id, album_type=['album', 'single'])
    
    while results:
        for album in results['items']:
            if parse_date(album['release_date']) > last_checked_date:
                albums.append({
                    'id': album['id'],
                    'name': album['name'],
                    'uri': album['uri'],
                    'release_date': album['release_date']
                })
        results = sp.next(results) if results['next'] else None
    
    tracks = []
    for album in albums:
        for track in sp.album_tracks(album['id'])['items']:
            tracks.append({
                'uri': track['uri'],
                'name': track['name'],
                'album_name': album['name'],
                'album_uri': album['uri'],
                'release_date': album['release_date']
            })
    return tracks

def parse_date(date_str):
    parts = date_str.split('-')
    year = int(parts[0])
    month = int(parts[1]) if len(parts) > 1 else 1
    day = int(parts[2]) if len(parts) > 2 else 1
    return datetime(year, month, day)
