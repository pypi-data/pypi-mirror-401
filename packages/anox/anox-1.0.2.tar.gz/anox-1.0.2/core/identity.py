# core/identity.py
"""
Identity Resolution System

Responsibilities:
- Define identity structure
- Resolve identity from input
- Validate identity completeness
- Enforce identity immutability

Identity represents WHO is making a request.
Identity is separate from WHAT they want (intent).
Identity is immutable once resolved.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Identity:
    """
    Immutable identity representation.
    
    Fields:
    - source: Where the request originated (human | api | internal)
    - role: Permission level (developer | blue_team | red_team | observer)
    - subject_id: Optional unique identifier for the actor
    
    Frozen to prevent modification after creation.
    """
    source: str          # human | api | internal
    role: str            # developer | blue_team | red_team | observer
    subject_id: Optional[str] = None


class IdentityResolver:
    """
    Resolves identity from input parameters.
    
    Phase 1: Simple validation only
    Phase 2+: Add role validation against roles.yaml
    Phase 2+: Add authentication checks
    Phase 2+: Add session binding
    """
    
    # Allowed sources for identity
    ALLOWED_SOURCES = ["human", "api", "internal"]

    @staticmethod
    def resolve(
        source: str,
        role: str,
        subject_id: Optional[str] = None
    ) -> Identity:
        """
        Resolve identity from parameters.
        
        Validates:
        - source and role are provided
        - source is one of allowed sources
        - role is properly formatted
        
        Raises:
        - ValueError if validation fails
        """
        if not source or not role:
            raise ValueError("Identity resolution failed: source or role missing")

        # Validate source format
        source = source.strip().lower()
        if source not in IdentityResolver.ALLOWED_SOURCES:
            raise ValueError(f"Invalid source '{source}'. Must be one of: {', '.join(IdentityResolver.ALLOWED_SOURCES)}")
        
        # Validate role format
        role = role.strip().lower()
        if not role.replace("_", "").isalnum():
            raise ValueError(f"Invalid role format '{role}'. Must contain only alphanumeric characters and underscores")
        
        # Validate subject_id if provided
        if subject_id is not None:
            subject_id = subject_id.strip()
            if not subject_id:
                subject_id = None

        return Identity(
            source=source,
            role=role,
            subject_id=subject_id
        )

    @staticmethod
    def validate(identity: Identity) -> bool:
        """
        Validate an existing identity.
        
        Checks:
        - Identity object is properly formatted
        - Source and role are valid
        - Subject_id is properly formatted if present
        
        Returns:
        - True if identity is valid
        - False otherwise
        """
        if not identity:
            return False
        
        try:
            # Check required fields
            if not identity.source or not identity.role:
                return False
            
            # Validate source
            if identity.source not in IdentityResolver.ALLOWED_SOURCES:
                return False
            
            # Validate role format
            if not identity.role.replace("_", "").isalnum():
                return False
            
            # Validate subject_id format if present
            if identity.subject_id is not None:
                if not isinstance(identity.subject_id, str) or not identity.subject_id.strip():
                    return False
            
            return True
        except Exception:
            return False
