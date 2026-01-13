from intel.feeds.base import IntelFeed


class RSSFeed(IntelFeed):
    def __init__(self, url: str):
        self.url = url

    def fetch(self):
        # Phase 3: skeleton only
        # Real network logic added later with limits
        return []

    def source(self) -> str:
        return self.url

    def source_type(self) -> str:
        return "rss"
