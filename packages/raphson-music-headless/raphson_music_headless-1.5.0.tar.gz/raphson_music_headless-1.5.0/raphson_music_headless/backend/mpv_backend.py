from collections.abc import Callable
import logging
from typing import cast
from typing_extensions import override
import mpv

from raphson_music_headless.backend import PlayerBackend


_LOGGER = logging.getLogger(__name__)  # noqa: F821


class MPVPlayerBackend(PlayerBackend):
    """
    https://pypi.org/project/python-mpv
    https://mpv.io/manual/master/#command-interface
    """

    player: mpv.MPV

    def __init__(
        self, on_media_end: Callable[[], None], mpv_opts: dict[str, str]
    ):
        super().__init__(on_media_end)
        self.player = mpv.MPV()
        for k, v in mpv_opts.items():
            self.player[k] = v

    @override
    def setup(self):
        # https://mpv.io/manual/master/#command-interface-end-file
        @self.player.event_callback("end_file")
        def on_media_end(event: mpv.MpvEvent):  # pyright: ignore[reportUnusedFunction]
            data = cast(mpv.MpvEventEndFile, event.data)
            # only call on_media_end if the cause is EOF (not in case of an error or deliberate stop)
            if data.reason == mpv.MpvEventEndFile.EOF:
                self._on_media_end()

    @override
    def quit(self):
        self.player.quit()

    @override
    def stop(self) -> None:
        self.player.stop()

    @override
    def pause(self) -> None:
        self.player.pause = True

    @override
    def play(self):
        self.player.pause = False

    @override
    def set_media(self, media: bytes):
        self.player.pause = False
        self.player.play_bytes(media)
        try:
            self.player.wait_until_playing(timeout=1)
        except TimeoutError:
            _LOGGER.warning(
                "wait_until_playing reached timeout, the track is probably corrupt"
            )

    @override
    def set_media_url(self, url: str):
        self.player.play(url)
        self.player.pause = False

    @override
    def get_media_title(self):
        meta = cast(dict[str, str] | None, self.player.metadata)
        if meta is None:
            return None
        name = meta.get("icy-name")
        title = meta.get("icy-title", meta.get("StreamTitle"))
        if title and name:
            return f"{name}: {title}"
        elif title:
            return title
        elif name:
            return name
        return cast(str | None, self.player.media_title)

    @override
    def has_media(self) -> bool:
        return cast(float | None, self.player.duration) is not None

    @override
    def is_playing(self) -> bool:
        return self.has_media() and not cast(bool, self.player.pause)

    @override
    def position(self) -> int:
        position = cast(float | None, self.player.time_pos)
        if position:
            return int(position)
        else:
            return 0

    @override
    def duration(self) -> int:
        duration = cast(float | None, self.player.duration)
        if duration:
            return int(duration)
        else:
            return 0

    @override
    def seek(self, position: float):
        duration = cast(float | None, self.player.duration)
        if duration:
            self.player.seek(int(min(position, duration)), reference="absolute")
            self.player.wait_for_event("seek", timeout=1)

    @override
    def get_volume(self) -> float:
        try:
            volume = cast(float | None, self.player.ao_volume)
            if volume:
                return volume / 100
        except RuntimeError:
            pass
        return 0

    @override
    def set_volume(self, volume: float) -> None:
        try:
            self.player.ao_volume = volume * 100
        except RuntimeError:
            pass
