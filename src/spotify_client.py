import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope='playlist-modify-private playlist-read-private',
        cache_handler=MemoryCacheHandler(
            token_info={
                'refresh_token': os.getenv('SPOTIPY_REFRESH_TOKEN')
            }
        ),
        open_browser=False
    ))
