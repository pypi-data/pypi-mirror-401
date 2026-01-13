class IntelKillSwitch:
    def __init__(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def check(self):
        if not self.enabled:
            raise RuntimeError("Intel automation disabled by kill switch")
