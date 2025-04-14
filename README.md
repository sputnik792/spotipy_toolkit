# Spotify Playlist Auto-Updater

Automatically updates playlists with new releases from specified artists.

## Setup
1. Create a Spotify Developer App
2. Add these GitHub Secrets:
   - `SPOTIPY_CLIENT_ID`
   - `SPOTIPY_CLIENT_SECRET` 
   - `SPOTIPY_REDIRECT_URI`
   - `SPOTIPY_REFRESH_TOKEN`

3. Tag playlists in Spotify with:
   ```
   #auto-update @ArtistName
   ```

## How It Works
- Runs every 48 hours via GitHub Actions
- Preserves album order while sorting chronologically
- Skips duplicate tracks
