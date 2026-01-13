from spotipy import Spotify
from typing_extensions import Final, Optional
from datetime import timedelta, datetime
from time import sleep
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from libs.firewall import (
    Firewall,
    determine_firewall,
    open_firewall_ports,
    close_firewall_ports,
)
from libs.spotipy import (
    create_spotify_client,
    get_current_playing_track_id,
    READ_CURRENT_PLAYING_SCOPE,
)


class Settings(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", env_prefix="PORTify_"
    )

    CLIENT_ID: Final[str] = Field()
    CLIENT_SECRET: Final[str] = Field()
    REDIRECT_URI: Final[str] = Field()

    SECRET_OPEN_TRACK_ID: Final[str] = Field()
    SECRET_CLOSE_TRACK_ID: Final[str] = Field()

    OPEN_PORTS_TIMEOUT_MINUTES: Final[timedelta] = Field()
    PORTS_TO_MANAGE: Final[frozenset[int]] = Field()


def updated_closing_ports_countdown(timeout: timedelta) -> datetime:
    return datetime.now() + timeout


def maybe_close_ports_on_timeout(
    firewall: type[Firewall], ports: frozenset[int], time_to_remove_rules: datetime
) -> None:
    if datetime.now() > time_to_remove_rules:
        print("Timeout has reached, closing ports!")
        close_firewall_ports(firewall=firewall, ports=ports)


def main() -> None:
    settings: Final[Settings] = Settings()
    spotify_client: Spotify = create_spotify_client(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        redirect_uri=settings.REDIRECT_URI,
        scope=READ_CURRENT_PLAYING_SCOPE,
    )
    firewall: type[Firewall] = determine_firewall()

    time_to_remove_rules: datetime = datetime.now()

    while True:
        current_playing_track_id: Optional[str] = get_current_playing_track_id(
            spotify_client=spotify_client
        )
        if current_playing_track_id == settings.SECRET_OPEN_TRACK_ID:
            print("User is playing the secret open track - Opening firewall's ports")
            open_firewall_ports(firewall=firewall, ports=settings.PORTS_TO_MANAGE)
            time_to_remove_rules = updated_closing_ports_countdown(
                timeout=settings.OPEN_PORTS_TIMEOUT_MINUTES
            )
        elif current_playing_track_id == settings.SECRET_CLOSE_TRACK_ID:
            print("User is playing the secret close track - Closing firewall's ports")
            close_firewall_ports(firewall=firewall, ports=settings.PORTS_TO_MANAGE)
        else:
            maybe_close_ports_on_timeout(
                firewall=firewall,
                ports=settings.PORTS_TO_MANAGE,
                time_to_remove_rules=time_to_remove_rules,
            )
        sleep(1 * 10)


if __name__ == "__main__":
    main()
