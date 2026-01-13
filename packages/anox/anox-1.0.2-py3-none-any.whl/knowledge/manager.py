"""Knowledge manager skeleton aligning with knowledge_sync.md."""

from __future__ import annotations

from typing import List, Dict, Any


class KnowledgeManager:
    """Coordinates intake → normalize → verify → approve → index."""

    def intake(self, payload: Dict[str, Any]) -> None:
        """Receive raw knowledge payload (Phase 1 stub)."""
        raise NotImplementedError

    def query(self, domain: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Query the indexed knowledge base (Phase 1 stub)."""
        raise NotImplementedError
