import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler

def get_spotify_client():
    # Get the refresh token from environment
    refresh_token = os.getenv('SPOTIPY_REFRESH_TOKEN')
    if not refresh_token:
        raise ValueError("Missing SPOTIPY_REFRESH_TOKEN in environment")
    
    # Initialize with pre-existing token
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope='playlist-modify-private playlist-read-private',
        cache_handler=MemoryCacheHandler({
            'refresh_token': refresh_token,
            'access_token': os.getenv('SPOTIPY_ACCESS_TOKEN', ''),
            'expires_at': int(os.getenv('SPOTIPY_EXPIRES_AT', '0'))
        }),
        open_browser=False
    ))
