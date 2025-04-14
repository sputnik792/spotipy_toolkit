import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler

def get_spotify_client():
    # Verify all required environment variables exist
    required_vars = [
        'SPOTIPY_CLIENT_ID',
        'SPOTIPY_CLIENT_SECRET',
        'SPOTIPY_REDIRECT_URI',
        'SPOTIPY_REFRESH_TOKEN'
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")

    # Initialize with pre-existing token only
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope='playlist-modify-private playlist-read-private',
        cache_handler=MemoryCacheHandler({
            'refresh_token': os.getenv('SPOTIPY_REFRESH_TOKEN'),
            'access_token': '',  # Will be auto-refreshed
            'expires_at': 0      # Forces immediate refresh
        }),
        open_browser=False,
        show_dialog=False
    ))
