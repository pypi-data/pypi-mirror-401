# models/online_adapter.py

from models.base import BaseModel


class OnlineModelAdapter(BaseModel):
    def generate(self, prompt: str, context: dict) -> str:
        raise NotImplementedError("Online model used as validator only (Phase 1 stub)")

    def health_check(self) -> bool:
        return True
