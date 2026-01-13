# intel/approval.py
class IntelApprovalGate:
    def request_approval(self, packet):
        raise RuntimeError(
            "Intel promotion requires explicit human approval."
        )
