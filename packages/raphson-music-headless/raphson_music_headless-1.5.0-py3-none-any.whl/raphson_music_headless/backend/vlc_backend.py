from collections.abc import Callable
import logging
from tempfile import NamedTemporaryFile
from typing import Any, cast

import vlc
from typing_extensions import override

from raphson_music_headless.backend import PlayerBackend

_LOGGER = logging.getLogger(__name__)  # noqa: F821


class VLCPlayerBackend(PlayerBackend):
    start_timestamp: int = 0
    temp_file: Any = None
    vlc_instance: vlc.Instance
    vlc_player: vlc.MediaPlayer
    vlc_events: vlc.EventManager

    def __init__(self, on_media_end: Callable[[], None]):
        super().__init__(on_media_end)

        self.vlc_instance = vlc.Instance(
            "--file-caching=0"
        )  # pyright: ignore[reportAttributeAccessIssue]
        if not self.vlc_instance:
            raise ValueError("Failed to create VLC instance")
        self.vlc_player = self.vlc_instance.media_player_new()
        self.vlc_events = self.vlc_player.event_manager()

    @override
    def setup(self):
        self.vlc_events.event_attach(
            vlc.EventType.MediaPlayerEndReached,  # pyright: ignore[reportAttributeAccessIssue, reportUnknownArgumentType]
            self._on_media_end,
        )

    @override
    def quit(self):
        pass

    @override
    def play(self):
        self.vlc_player.play()

    @override
    def pause(self) -> None:
        self.vlc_player.set_pause(True)

    @override
    def stop(self) -> None:
        try:
            self.vlc_player.stop()
            self.vlc_player.set_media(None)
        finally:
            if self.temp_file:
                self.temp_file.close()

    @override
    def set_media(self, media: bytes) -> None:
        temp_file = NamedTemporaryFile("wb", prefix="rmp-playback-server-")
        try:
            temp_file.write(media)

            media = self.vlc_instance.media_new(  # pyright: ignore[reportUnknownVariableType]
                temp_file.name
            )
            self.vlc_player.set_media(media)
            self.vlc_player.play()
        finally:
            # Remove old temp file
            if self.temp_file:
                self.temp_file.close()
            # Store current temp file so it can be removed later
            self.temp_file = temp_file

    @override
    def set_media_url(self, url: str):
        media = self.vlc_instance.media_new(url)  # pyright: ignore[reportUnknownVariableType]
        self.vlc_player.set_media(media)
        self.vlc_player.play()

    @override
    def has_media(self) -> bool:
        return self.vlc_player.get_media() is not None

    @override
    def get_media_title(self):
        media = cast(vlc.Media | None, self.vlc_player.get_media())
        if media is None:
            return None
        meta = cast(vlc.Meta, vlc.Meta.Title)  # pyright: ignore[reportAttributeAccessIssue]
        return cast(str | None, media.get_meta(meta))

    @override
    def is_playing(self) -> bool:
        return cast(int, self.vlc_player.is_playing()) == 1

    @override
    def position(self) -> int:
        return cast(int, self.vlc_player.get_time()) // 1000

    @override
    def duration(self) -> int:
        return cast(int, self.vlc_player.get_length()) // 1000

    @override
    def seek(self, position: float):
        _LOGGER.info("Seek to:", position)
        self.vlc_player.set_time(int(position * 1000))

    @override
    def get_volume(self) -> float:
        return cast(int, self.vlc_player.audio_get_volume() / 100)

    @override
    def set_volume(self, volume: float) -> None:
        self.vlc_player.audio_set_volume(int(volume * 100))
