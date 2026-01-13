# intel/assess.py
from intel.types import IntelPacket


class IntelAssessor:
    def assess(self, packet: IntelPacket) -> IntelPacket:
        score = 0.0
        notes = []

        if packet.source_type in ["vendor", "advisory"]:
            score += 0.3
            notes.append("trusted_source")

        score = min(score, 1.0)

        return IntelPacket(
            **{
                **packet.__dict__,
                "confidence_score": score,
                "risk_level": self._risk(score),
                "notes": ", ".join(notes),
            }
        )

    def _risk(self, score: float) -> str:
        if score > 0.7:
            return "HIGH"
        if score > 0.4:
            return "MEDIUM"
        return "LOW"
