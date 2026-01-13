from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from typing_extensions import Dict, Any, Optional, Final

READ_CURRENT_PLAYING_SCOPE: Final[str] = "user-read-currently-playing"


def create_spotify_client(
    client_id: str, client_secret: str, redirect_uri: str, scope: str
) -> Spotify:
    spotify_client: Spotify = Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            open_browser=False,
        )
    )
    return spotify_client


def get_current_playing_track_id(spotify_client: Spotify) -> Optional[str]:
    user_current_playing_track: Dict[str, Any] = (
        spotify_client.current_user_playing_track()
    )
    is_playing: bool = user_current_playing_track["is_playing"]
    print(f"is_playing: {is_playing}")
    if not is_playing:
        return None
    current_playing_track_id: str = user_current_playing_track["item"]["id"]
    print(f"current_playing_track_id: {current_playing_track_id}")
    return current_playing_track_id
