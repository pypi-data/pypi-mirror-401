# domains/_boundary.py
"""
Domain Boundary System

Responsibilities:
- Define domain boundary structure
- Validate cross-domain access requests
- Enforce domain isolation rules
- Track domain access patterns

Domain boundaries are architectural, not optional.
Cross-domain access is exceptional, not default.
Violation results in immediate refusal.
"""

from typing import Optional, List, Set
from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass(frozen=True)
class DomainBoundary:
    """
    Immutable domain boundary definition.
    
    Fields:
    - domain_id: Domain identifier
    - allowed_roles: Roles that can access this domain
    - forbidden_roles: Roles explicitly forbidden
    - isolation_level: STRICT | MODERATE | PERMISSIVE
    - cross_domain_allowed: Other domains that can be accessed from here
    """
    domain_id: str
    allowed_roles: Set[str]
    forbidden_roles: Set[str]
    isolation_level: str
    cross_domain_allowed: Set[str]


@dataclass
class CrossDomainRequest:
    """
    Cross-domain access request.
    
    Fields:
    - source_domain: Originating domain
    - target_domain: Target domain
    - role: Role making the request
    - action: Action to be performed
    - reason: Justification for cross-domain access
    """
    source_domain: str
    target_domain: str
    role: str
    action: str
    reason: Optional[str] = None


class BoundaryValidator:
    """
    Validates domain boundary access.
    
    Phase 1: Basic role and domain checks
    Phase 2+: Cross-domain policy evaluation
    Phase 2+: Access pattern analysis
    Phase 2+: Audit trail integration
    """

    def __init__(self, domains_path: Path):
        """
        Initialize boundary validator.
        
        Args:
        - domains_path: Path to domains directory
        """
        self.domains_path = domains_path
        self._boundaries: dict[str, DomainBoundary] = {}
        self._load_boundaries()

    def _load_boundaries(self) -> None:
        """
        Load domain boundaries from manifests.
        
        Phase 1: Stub
        Phase 2+: Load all domain manifests
        Phase 2+: Build boundary registry
        Phase 2+: Validate boundary definitions
        """
        # TODO: Phase 2 - Scan domains directory
        # TODO: Phase 2 - Load each manifest.yaml
        # TODO: Phase 2 - Extract boundary rules
        # TODO: Phase 2 - Build boundaries dict
        # TODO: Phase 2 - Validate no conflicts
        pass

    def validate_access(
        self,
        domain_id: str,
        role: str
    ) -> bool:
        """
        Validate role has access to domain.
        
        Phase 1: Stub (always returns True)
        Phase 2+: Check role against domain manifest
        Phase 2+: Check forbidden list first
        Phase 2+: Check allowed list
        Phase 2+: Log access validation
        
        Returns:
        - True: Access allowed
        - False: Access denied
        """
        # TODO: Phase 2 - Load domain boundary
        # TODO: Phase 2 - Check forbidden_roles first
        # TODO: Phase 2 - Check allowed_roles
        # TODO: Phase 2 - Log validation result
        
        return True

    def validate_cross_domain(
        self,
        request: CrossDomainRequest
    ) -> bool:
        """
        Validate cross-domain access request.
        
        Phase 2+: Check source domain allows target
        Phase 2+: Check target domain allows source role
        Phase 2+: Verify action is permitted cross-domain
        Phase 2+: Log cross-domain request
        
        Returns:
        - True: Cross-domain access allowed
        - False: Cross-domain access denied
        """
        # TODO: Phase 2 - Load source boundary
        # TODO: Phase 2 - Check target in cross_domain_allowed
        # TODO: Phase 2 - Validate role access to target
        # TODO: Phase 2 - Check action permissions
        # TODO: Phase 2 - Log cross-domain attempt
        
        # Default: deny cross-domain access
        return False

    def get_boundary(self, domain_id: str) -> Optional[DomainBoundary]:
        """
        Get boundary definition for a domain.
        
        Phase 2+: Return loaded boundary
        
        Returns:
        - DomainBoundary if exists
        - None if domain not found
        """
        return self._boundaries.get(domain_id)

    def get_allowed_domains_for_role(self, role: str) -> List[str]:
        """
        Get list of domains accessible by role.
        
        Phase 2+: Query all boundaries
        Phase 2+: Filter by role access
        Phase 2+: Return sorted list
        
        Returns:
        - List of domain IDs
        """
        # TODO: Phase 2 - Iterate all boundaries
        # TODO: Phase 2 - Check role in allowed_roles
        # TODO: Phase 2 - Exclude forbidden_roles
        # TODO: Phase 2 - Return filtered list
        
        return []

    def get_cross_domain_targets(self, source_domain: str) -> List[str]:
        """
        Get list of domains accessible from source domain.
        
        Phase 2+: Load source boundary
        Phase 2+: Return cross_domain_allowed set
        
        Returns:
        - List of accessible domain IDs
        """
        # TODO: Phase 2 - Load boundary for source_domain
        # TODO: Phase 2 - Return cross_domain_allowed as list
        
        return []

    def check_isolation_level(self, domain_id: str) -> str:
        """
        Get isolation level for domain.
        
        Phase 2+: Load domain boundary
        Phase 2+: Return isolation_level
        
        Returns:
        - Isolation level: STRICT | MODERATE | PERMISSIVE
        """
        # TODO: Phase 2 - Load boundary
        # TODO: Phase 2 - Return isolation_level
        
        return "STRICT"


class BoundaryViolation(Exception):
    """
    Exception raised when domain boundary is violated.
    
    Contains:
    - domain_id: Domain that was accessed
    - role: Role that attempted access
    - reason: Why access was denied
    """
    def __init__(self, domain_id: str, role: str, reason: str):
        self.domain_id = domain_id
        self.role = role
        self.reason = reason
        super().__init__(
            f"Domain boundary violation: Role '{role}' cannot access domain '{domain_id}' - {reason}"
        )


class CrossDomainViolation(Exception):
    """
    Exception raised when cross-domain access is violated.
    
    Contains:
    - source_domain: Source domain
    - target_domain: Target domain
    - reason: Why cross-domain access was denied
    """
    def __init__(self, source_domain: str, target_domain: str, reason: str):
        self.source_domain = source_domain
        self.target_domain = target_domain
        self.reason = reason
        super().__init__(
            f"Cross-domain violation: '{source_domain}' → '{target_domain}' - {reason}"
        )
