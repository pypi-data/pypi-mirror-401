# intel/verify.py
from intel.types import IntelPacket


class IntelVerifier:
    def verify(self, packet: IntelPacket) -> IntelPacket:
        state = "PARTIAL"

        if packet.confidence_score < 0.2:
            state = "FAILED"

        return IntelPacket(
            **{**packet.__dict__, "verification_state": state}
        )
