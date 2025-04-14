from spotify_client import get_spotify_client
from playlist_manager import update_managed_playlists

def main():
    sp = get_spotify_client()
    update_managed_playlists(sp)

if __name__ == "__main__":
    main()
