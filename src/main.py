from src.spotify_client import get_spotify_client
from src.playlist_manager import update_all_playlists

def main():
    print("Starting playlist update...")
    sp = get_spotify_client()
    update_all_playlists(sp)
    print("Update complete!")

if __name__ == "__main__":
    main()
