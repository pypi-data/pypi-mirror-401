from dataclasses import dataclass
from typing import cast
from aiohttp import BaseConnector, ClientSession, ClientTimeout
from raphson_mp.client.track import Track
from raphson_mp.common.typing import TrackDict
from raphson_mp.common.util import urlencode

from raphson_music_headless.headless_typing import StateDict


@dataclass
class PlayerState:
    name: str | None
    all_playlists: list[str]
    enabled_playlists: list[str]
    has_media: bool
    is_playing: bool
    position: int
    duration: int
    volume: float
    title: str | None
    stream_url: str | None
    track: Track | None


class HeadlessPlayerClient:
    base_url: str
    _session: ClientSession

    def __init__(self, *, base_url: str, connector: BaseConnector):
        self.base_url = base_url
        self._session = ClientSession(
            connector=connector,
            base_url=base_url,
            timeout=ClientTimeout(connect=5, total=60),
            raise_for_status=True,
        )

    async def close(self):
        await self._session.close()

    async def state(self) -> PlayerState:
        response = await self._session.get("/state")
        json = cast(StateDict, await response.json())
        return PlayerState(
            json.get("name"),
            json["playlists"]["all"],
            json["playlists"]["enabled"],
            json["player"]["has_media"],
            json["player"]["is_playing"],
            json["player"]["position"],
            json["player"]["duration"],
            json["player"]["volume"] / 100,
            json["player"].get("title"),
            json["player"].get("stream_url"),
            (
                Track.from_dict(json["currently_playing"])
                if json["currently_playing"] is not None
                else None
            ),
        )

    async def list_tracks(self, playlist: str) -> list[Track]:
        async with self._session.get(
            "/list_tracks", params={"playlist": playlist}
        ) as response:
            response_json = await response.json()
        return [
            Track.from_dict(data)
            for data in cast(list[TrackDict], response_json["tracks"])
        ]

    async def stop(self) -> None:
        async with self._session.post("/stop"):
            pass

    async def pause(self) -> None:
        async with self._session.post("/pause"):
            pass

    async def play(self) -> None:
        async with self._session.post("/play"):
            pass

    async def previous(self) -> None:
        async with self._session.post("/previous"):
            pass

    async def next(self) -> None:
        async with self._session.post("/next"):
            pass

    async def play_news(self) -> None:
        async with self._session.post("/play_news"):
            pass

    async def seek(self, position: int) -> None:
        async with self._session.post("/seek", data=str(position)):
            pass

    async def set_volume(self, volume: float) -> None:
        async with self._session.post("/volume", data=str(int(volume * 100))):
            pass

    async def set_enabled_playlists(self, playlists: list[str]) -> None:
        async with self._session.post("/playlists", json=playlists):
            pass

    async def enqueue(self, track: str | Track) -> None:
        if isinstance(track, Track):
            track = track.path
        async with self._session.post("/enqueue", data=track):
            pass

    async def play_track(self, track: str | Track) -> None:
        if isinstance(track, Track):
            track = track.path
        async with self._session.post("/play_track", data=track):
            pass

    async def play_url(self, url: str, retry: bool = False) -> None:
        async with self._session.post(url="/play_url", json={"url": url, "retry": retry}):
            pass

    def cover_url(self, track: str | Track):
        if isinstance(track, Track):
            track = track.path
        return f"/cover?track={urlencode(track)}"

    async def cover(self, track: str | Track):
        async with self._session.get(self.cover_url(track)) as response:
            return await response.read()
