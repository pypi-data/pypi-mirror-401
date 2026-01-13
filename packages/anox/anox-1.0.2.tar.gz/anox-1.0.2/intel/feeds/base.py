from typing import Iterable, Any


class IntelFeed:
    """
    Base class for intel feeds.

    Feeds:
    - collect raw data only
    - NO analysis
    - NO scoring
    - NO memory access
    """

    def fetch(self) -> Iterable[Any]:
        raise NotImplementedError

    def source(self) -> str:
        raise NotImplementedError

    def source_type(self) -> str:
        raise NotImplementedError
