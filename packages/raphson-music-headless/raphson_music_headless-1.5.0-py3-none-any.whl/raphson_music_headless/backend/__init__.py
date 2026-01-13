from abc import ABC, abstractmethod
from collections.abc import Callable


class PlayerBackend(ABC):

    _on_media_end: Callable[[], None]

    def __init__(self, on_media_end: Callable[[], None]):
        self._on_media_end = on_media_end

    @abstractmethod
    def setup(self) -> None: ...

    @abstractmethod
    def quit(self) -> None: ...

    @abstractmethod
    def play(self) -> None: ...

    @abstractmethod
    def pause(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def set_media(self, media: bytes) -> None: ...

    @abstractmethod
    def set_media_url(self, url: str) -> None: ...

    @abstractmethod
    def has_media(self) -> bool: ...

    @abstractmethod
    def get_media_title(self) -> str | None: ...

    @abstractmethod
    def is_playing(self) -> bool: ...

    @abstractmethod
    def position(self) -> int: ...

    @abstractmethod
    def duration(self) -> int: ...

    @abstractmethod
    def seek(self, position: float) -> None: ...

    @abstractmethod
    def get_volume(self) -> float: ...

    @abstractmethod
    def set_volume(self, volume: float) -> None: ...
