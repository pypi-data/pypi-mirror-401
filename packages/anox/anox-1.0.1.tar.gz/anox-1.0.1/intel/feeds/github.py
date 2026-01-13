from intel.feeds.base import IntelFeed


class GitHubFeed(IntelFeed):
    def __init__(self, query: str):
        self.query = query

    def fetch(self):
        return []

    def source(self) -> str:
        return f"github:{self.query}"

    def source_type(self) -> str:
        return "repo"
