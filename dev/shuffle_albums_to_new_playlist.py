### takes all the albums you've saved in library, shuffles them by album and places them into a new
### playlist. This retains the song order within each respective album

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Spotify API credentials
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = ''  # Must match the redirect URI in your Spotify Developer Dashboard

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-library-read playlist-modify-public playlist-modify-private'))

# Fetch all saved albums
def get_saved_albums():
    albums = []
    results = sp.current_user_saved_albums(limit=50)
    albums.extend(results['items'])
    
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    
    return albums

# Extract tracks from each album
def get_album_tracks(album):
    tracks = []
    results = sp.album_tracks(album['album']['id'])
    tracks.extend(results['items'])
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks

# Create a new playlist
def create_playlist(name):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, name, public=False)
    return playlist['id']

# Add tracks to the playlist in chunks
def add_tracks_to_playlist(playlist_id, track_uris):
    # Split track_uris into chunks of 100
    chunk_size = 100
    for i in range(0, len(track_uris), chunk_size):
        chunk = track_uris[i:i + chunk_size]
        sp.playlist_add_items(playlist_id, chunk)
        print(f"Added {len(chunk)} tracks to the playlist.")

# Main function
def main():
    # Get all saved albums
    albums = get_saved_albums()
    
    # Shuffle the albums
    random.shuffle(albums)
    
    # Extract tracks from each album in order
    track_uris = []
    for album in albums:
        tracks = get_album_tracks(album)
        track_uris.extend([track['uri'] for track in tracks])
    
    # Create a new playlist
    playlist_name = "All Albums Shuffled"
    playlist_id = create_playlist(playlist_name)
    
    # Add tracks to the playlist in chunks
    add_tracks_to_playlist(playlist_id, track_uris)
    
    print(f"Playlist '{playlist_name}' created with {len(track_uris)} tracks.")

if __name__ == "__main__":
    main()
