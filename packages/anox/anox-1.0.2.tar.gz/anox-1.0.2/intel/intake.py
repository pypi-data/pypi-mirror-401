from datetime import datetime
from typing import Any
from intel.types import IntelPacket
from audit.log import AuditLogger


class IntelIntake:
    def __init__(self, audit: AuditLogger):
        self.audit = audit

    def collect(self, source: str, content: Any) -> IntelPacket:
        if not source or content is None:
            raise ValueError("Invalid intel intake payload")

        packet = IntelPacket(
            id=f"intel-{abs(hash(source))}",
            source=source,
            source_type="unknown",
            collected_at=datetime.utcnow(),
            raw_content=content,
            normalized_content=None,
            tags=[],
            confidence_score=0.0,
            risk_level="LOW",
            verification_state="UNVERIFIED",
            quarantine=True,
            notes=None,
        )

        # 🔒 Audit boundary: metadata only
        self.audit.log({
            "event": "INTAKE",
            "intel_id": packet.id,
            "actor": "system",
            "source": source,
            "state": "RAW_COLLECTED",
        })

        return packet
