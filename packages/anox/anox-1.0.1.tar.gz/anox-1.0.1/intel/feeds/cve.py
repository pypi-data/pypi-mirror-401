from intel.feeds.base import IntelFeed


class CVEFeed(IntelFeed):
    def fetch(self):
        return []

    def source(self) -> str:
        return "cve-database"

    def source_type(self) -> str:
        return "advisory"
