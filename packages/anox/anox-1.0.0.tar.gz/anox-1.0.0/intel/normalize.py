# intel/normalize.py
from intel.types import IntelPacket


class IntelNormalizer:
    def normalize(self, packet: IntelPacket) -> IntelPacket:
        normalized = {
            "data": packet.raw_content,
            "received_at": packet.collected_at.isoformat(),
        }

        return IntelPacket(
            **{**packet.__dict__, "normalized_content": normalized}
        )
