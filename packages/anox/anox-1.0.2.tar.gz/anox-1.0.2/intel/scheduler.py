from intel.intake import IntelIntake
from intel.feeds.base import IntelFeed
from audit.log import AuditLogger


class IntelScheduler:
    """
    Phase 3 Scheduler:
    - Explicit trigger only
    - No infinite loops
    """

    def __init__(self, intake: IntelIntake, audit: AuditLogger):
        self.intake = intake
        self.audit = audit

    def run_feed(self, feed: IntelFeed):
        self.audit.log({
            "event": "FEED_RUN_START",
            "source": feed.source(),
            "actor": "system",
        })

        for item in feed.fetch():
            self.intake.collect(
                source=feed.source(),
                content=item,
            )

        self.audit.log({
            "event": "FEED_RUN_END",
            "source": feed.source(),
            "actor": "system",
        })
