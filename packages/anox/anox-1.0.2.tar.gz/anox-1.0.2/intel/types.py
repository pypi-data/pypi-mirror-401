# intel/types.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional


@dataclass(frozen=True)
class IntelPacket:
    id: str
    source: str
    source_type: str
    collected_at: datetime

    raw_content: Any
    normalized_content: Optional[dict]

    tags: List[str]

    confidence_score: float
    risk_level: str

    verification_state: str
    quarantine: bool

    notes: Optional[str] = None
