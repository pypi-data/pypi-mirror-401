import asyncio
from collections.abc import Awaitable
from dataclasses import dataclass
import logging
import time
from typing import final

from raphson_mp.client import RaphsonMusicClient
from raphson_mp.client.track import DownloadedTrack, Track
from raphson_mp.common.control import (
    ClientState,
    ServerCommand,
    ServerNext,
    ServerPause,
    ServerPlay,
    ServerPrevious,
    ServerSeek,
    ServerSetPlaying,
    ServerSetPlaylists,
    ServerSetQueue,
)
from raphson_mp.common.typing import QueuedTrackDict

from raphson_music_headless.backend import PlayerBackend
from raphson_music_headless.config import Config
from raphson_music_headless.downloader import Downloader

_LOGGER = logging.getLogger(__name__)


@dataclass
class StreamInfo:
    url: str
    retry: bool


class AudioPlayer:
    client: RaphsonMusicClient
    downloader: Downloader
    config: Config
    backend: PlayerBackend

    currently_playing: DownloadedTrack | None = None
    queue: list[DownloadedTrack]
    history: list[DownloadedTrack]
    start_timestamp: int = 0
    last_news: int
    stream_info: StreamInfo | None = None
    _state_submitter_task: asyncio.Task[None] | None = None
    _stop_timer: asyncio.TimerHandle | None = None
    _loop: asyncio.AbstractEventLoop | None = None

    def __init__(self, client: RaphsonMusicClient, downloader: Downloader, config: Config):
        self.client = client
        self.downloader = downloader
        self.config = config

        def on_media_end():
            assert self._loop
            asyncio.run_coroutine_threadsafe(self._on_media_end(), self._loop)

        if config.player == "mpv":
            from raphson_music_headless.backend.mpv_backend import MPVPlayerBackend

            self.backend = MPVPlayerBackend(on_media_end, config.mpv_opts)
        elif config.player == "vlc":
            from raphson_music_headless.backend.vlc_backend import VLCPlayerBackend

            self.backend = VLCPlayerBackend(on_media_end)
        else:
            raise ValueError("invalid backend: ", config.player)

        self.last_news = int(time.time())  # do not queue news right after starting
        self.queue = []
        self.history = []

    async def setup(self):
        self._loop = asyncio.get_running_loop()
        if self.config.control:
            self.client.control_start(self.control_handler)
        self.backend.setup()
        self._state_submitter_task = asyncio.create_task(self._state_submitter())

    def quit(self):
        self.backend.quit()

    def has_media(self):
        return self.backend.has_media()

    def is_playing(self):
        return self.backend.is_playing()

    def position(self):
        return self.backend.position()

    def duration(self):
        return self.backend.position()

    def get_volume(self):
        return self.backend.get_volume()

    def set_volume(self, volume: float):
        return self.backend.set_volume(volume)

    def get_media_title(self):
        return self.backend.get_media_title()

    async def play(self) -> None:
        _LOGGER.info("play")
        if self._stop_timer:
            self._stop_timer.cancel()

        if self.backend.has_media():
            self.backend.play()
            await self.submit_state()
        else:
            await self.next(retry=True)

    @final
    async def play_url(self, stream_info: StreamInfo) -> None:
        _LOGGER.info("play url: %s", stream_info.url)
        self.currently_playing = None
        self.stream_info = stream_info
        self.backend.set_media_url(stream_info.url)

    @final
    async def pause(self) -> None:
        _LOGGER.info("pause")
        self.backend.pause()
        await self.submit_state()
        if self.config.stop_timeout > 0:
            loop = asyncio.get_running_loop()
            self._stop_timer = loop.call_later(
                self.config.stop_timeout,
                lambda: asyncio.run_coroutine_threadsafe(self.stop(), loop),
            )

    @final
    async def stop(self) -> None:
        _LOGGER.info("stop")
        self.stream_info = None
        self.currently_playing = None
        self.backend.stop()
        await self.submit_state()

    @final
    async def previous(self):
        try:
            track = self.history.pop()
        except IndexError:
            return

        # add current track to start of queue
        if self.currently_playing is not None:
            self.queue.insert(0, self.currently_playing)

        await self.play_track(track)

    @final
    async def next(self, *, retry: bool) -> None:
        self.stream_info = None

        if self.queue:
            next_track = self.queue.pop(0)
        else:
            next_track = self.downloader.get_track()

            if next_track is None:
                if retry:
                    _LOGGER.warning("no cached track available, trying again")
                    await asyncio.sleep(1)
                    return await self.next(retry=retry)
                else:
                    raise ValueError("no cached track available")

        if self.currently_playing is not None:
            self.history = [*self.history[-5:], self.currently_playing]

        await self.play_track(next_track)

    @final
    async def play_track(self, track: DownloadedTrack):
        _LOGGER.info("play track: %s", track.track.path)
        self.currently_playing = track
        self.start_timestamp = int(time.time())
        self.backend.set_media(track.audio)
        asyncio.create_task(self.submit_state())

    @final
    async def seek(self, position: float) -> None:
        if self.stream_info is not None:
            _LOGGER.warning("ignoring seek for stream")
            return
        self.backend.seek(position)
        asyncio.create_task(self.submit_state())

    async def enqueue(self, track_path: str, front: bool = False) -> None:
        track = await self.client.get_track(track_path)
        download = await track.download(self.client)
        if front:
            self.queue.insert(0, download)
        else:
            self.queue.append(download)

    async def control_handler(self, command: ServerCommand):
        if isinstance(command, ServerPlay):
            await self.play()
        elif isinstance(command, ServerPause):
            await self.pause()
        elif isinstance(command, ServerPrevious):
            await self.previous()
        elif isinstance(command, ServerNext):
            await self.next(retry=False)
        elif isinstance(command, ServerSeek):
            await self.seek(command.position)
        elif isinstance(command, ServerSetPlaylists):
            self.downloader.enabled_playlists = command.playlists
        elif isinstance(command, ServerSetPlaying):
            _LOGGER.info("download: %s", command.track["path"])
            track = Track.from_dict(command.track)
            downloaded = await track.download(self.client)
            await self.play_track(downloaded)
        elif isinstance(command, ServerSetQueue):
            new_queue: list[DownloadedTrack] = []

            for queuedtrack_dict in command.tracks:
                # try to reuse already downloaded track
                for old_track in self.queue:
                    if queuedtrack_dict["track"]["path"] == old_track.track.path:
                        new_queue.append(old_track)
                        break
                else:
                    # download new track
                    track = Track.from_dict(queuedtrack_dict["track"])
                    new_queue.append(await track.download(self.client))

            self.queue = new_queue

    async def submit_state(self):
        queue: list[QueuedTrackDict] = [
            {"track": track.track.to_dict(), "manual": True} for track in self.queue
        ]

        try:
            await self.client.control_send(
                ClientState(
                    track=self.currently_playing.track.to_dict() if self.currently_playing else None,
                    paused=not self.backend.is_playing(),
                    position=self.backend.position(),
                    duration=self.backend.duration(),
                    volume=self.backend.get_volume(),
                    control=self.config.control,
                    player_name=self.config.name,
                    queue=queue,
                    playlists=self.downloader.enabled_playlists,
                )
            )
        except Exception:
            _LOGGER.warning("failed to send state to server")

    async def _state_submitter(self):
        while True:
            try:
                await self.submit_state()
                if self.currently_playing is not None:
                    await asyncio.sleep(10)
                else:
                    await asyncio.sleep(30)
            except Exception:
                _LOGGER.warning("failed to submit now playing info", exc_info=True)
                await asyncio.sleep(30)

    async def _on_media_end(self) -> None:
        if self.stream_info is not None and self.stream_info.retry:
            _LOGGER.info("stream ended, restarting stream in 10 seconds")
            await asyncio.sleep(10)
            if (
                self.stream_info is not None  # pyright: ignore[reportUnnecessaryComparison]
                and self.stream_info.retry
            ):
                self.backend.set_media_url(self.stream_info.url)
            return

        tasks: list[Awaitable[None]] = []
        # save current info before it is replaced by the next track
        if self.currently_playing:
            path = self.currently_playing.track.path
            start_timestamp = self.start_timestamp
            if self.config.history:
                tasks.append(self.client.submit_played(path, timestamp=start_timestamp))
        tasks.append(self.next(retry=True))
        await asyncio.gather(*tasks)
