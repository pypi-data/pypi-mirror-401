# models/context.py

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ModelContext:
    task_id: str
    role: str
    constraints: Dict[str, Any]
