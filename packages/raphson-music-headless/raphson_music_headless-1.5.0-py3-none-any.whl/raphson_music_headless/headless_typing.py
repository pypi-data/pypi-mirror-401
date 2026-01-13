from typing import NotRequired, TypedDict

from raphson_mp.common.typing import TrackDict


class StateDictPlaylist(TypedDict):
    all: list[str]
    enabled: list[str]


class StateDictPlayer(TypedDict):
    has_media: bool
    is_playing: bool
    position: int
    duration: int
    volume: int
    title: NotRequired[str | None]
    stream_url: NotRequired[str | None]


class StateDict(TypedDict):
    name: str | None
    playlists: StateDictPlaylist
    player: StateDictPlayer
    currently_playing: TrackDict | None

class StreamInfoDict(TypedDict):
    url: str
    retry: NotRequired[bool]
