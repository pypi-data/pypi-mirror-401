# domains/_enforcer.py
"""Domain Enforcement System (Phase 1 rule-based implementation)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml

from domains._boundary import BoundaryValidator, BoundaryViolation, CrossDomainRequest


@dataclass(frozen=True)
class DomainPolicySet:
    forbidden: Tuple[str, ...]
    conditional: Tuple[str, ...]
    allowed: Tuple[str, ...]
    default_decision: str = "REFUSE"

    def decision_for(self, action: str) -> Tuple[str, str]:
        if action in self.forbidden:
            return "REFUSE", "domain_policy:forbidden"
        if action in self.conditional:
            return "REQUIRE_CONFIRMATION", "domain_policy:conditional"
        if action in self.allowed:
            return "ALLOW", "domain_policy:allowed"
        return self.default_decision, "domain_policy:default"


@dataclass(frozen=True)
class DomainManifest:
    domain_id: str
    version: str
    description: str
    allowed_roles: Tuple[str, ...]
    forbidden_roles: Tuple[str, ...]
    tools: Tuple[str, ...]
    knowledge_sources: Tuple[str, ...]
    constraints: Dict[str, Any]
    policy: DomainPolicySet


@dataclass(frozen=True)
class DomainDecision:
    decision: str
    reason: str
    trace: Tuple[str, ...]

    @property
    def requires_confirmation(self) -> bool:
        return self.decision == "REQUIRE_CONFIRMATION"


class DomainEnforcer:
    """Deterministic domain enforcement engine."""

    def __init__(
        self,
        domains_path: Path,
        boundary_validator: BoundaryValidator,
    ) -> None:
        self.domains_path = domains_path
        self.boundary_validator = boundary_validator
        self._manifests: Dict[str, DomainManifest] = {}

    def load_domain(self, domain_id: str) -> DomainManifest:
        manifest_path = self._manifest_path(domain_id)
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found for domain '{domain_id}'")
        raw_manifest = self._load_yaml(manifest_path)
        policy = self._load_domain_policy(manifest_path, raw_manifest)
        manifest = self._build_manifest(domain_id, raw_manifest, policy)
        self._manifests[domain_id] = manifest
        return manifest

    def evaluate_action(self, domain_id: str, role: str, action: str) -> DomainDecision:
        trace: List[str] = [f"domain:{domain_id}", f"role:{role}", f"action:{action}"]
        try:
            manifest = self.get_manifest(domain_id)
            if manifest is None:
                manifest = self.load_domain(domain_id)
        except FileNotFoundError:
            trace.append("manifest:missing")
            return DomainDecision("REFUSE", "domain.manifest_missing", tuple(trace))

        if not self.boundary_validator.validate_access(domain_id, role):
            trace.append("boundary_validator:denied")
            return DomainDecision("REFUSE", "Boundary validator denied access", tuple(trace))
        trace.append("boundary_validator:allowed")

        if manifest.forbidden_roles and role in manifest.forbidden_roles:
            trace.append("role:forbidden")
            return DomainDecision("REFUSE", "Role forbidden in domain", tuple(trace))

        if manifest.allowed_roles and role not in manifest.allowed_roles:
            trace.append("role:not_allowed")
            return DomainDecision("REFUSE", "Role not allowed in domain", tuple(trace))

        decision, reason = manifest.policy.decision_for(action)
        trace.append(reason)
        return DomainDecision(decision, reason, tuple(trace))

    def enforce_access(self, domain_id: str, role: str, action: str) -> DomainDecision:
        decision = self.evaluate_action(domain_id, role, action)
        if decision.decision == "REFUSE":
            raise BoundaryViolation(domain_id=domain_id, role=role, reason=decision.reason)
        return decision

    def enforce_cross_domain(
        self,
        source_domain: str,
        target_domain: str,
        role: str,
        action: str,
    ) -> None:
        from domains._boundary import CrossDomainViolation

        request = CrossDomainRequest(
            source_domain=source_domain,
            target_domain=target_domain,
            role=role,
            action=action,
        )
        if not self.boundary_validator.validate_cross_domain(request):
            raise CrossDomainViolation(
                source_domain=source_domain,
                target_domain=target_domain,
                reason="Cross-domain access not permitted",
            )

    def check_tool_permission(self, domain_id: str, role: str, tool_id: str) -> bool:
        manifest = self.get_manifest(domain_id)
        if manifest is None:
            try:
                manifest = self.load_domain(domain_id)
            except FileNotFoundError:
                return False

        if manifest.allowed_roles and role not in manifest.allowed_roles:
            return False
        if manifest.forbidden_roles and role in manifest.forbidden_roles:
            return False
        if not tool_id:
            return True
        return tool_id in manifest.tools

    def get_available_tools(self, domain_id: str, role: str) -> List[str]:
        manifest = self.get_manifest(domain_id)
        if manifest is None:
            try:
                manifest = self.load_domain(domain_id)
            except FileNotFoundError:
                return []

        if manifest.allowed_roles and role not in manifest.allowed_roles:
            return []
        if manifest.forbidden_roles and role in manifest.forbidden_roles:
            return []
        return list(manifest.tools)

    def check_knowledge_access(self, domain_id: str, role: str, knowledge_source: str) -> bool:
        manifest = self.get_manifest(domain_id)
        if manifest is None:
            try:
                manifest = self.load_domain(domain_id)
            except FileNotFoundError:
                return False

        if manifest.allowed_roles and role not in manifest.allowed_roles:
            return False
        if manifest.forbidden_roles and role in manifest.forbidden_roles:
            return False
        return knowledge_source in manifest.knowledge_sources

    def get_domain_constraints(self, domain_id: str) -> Dict[str, Any]:
        manifest = self.get_manifest(domain_id)
        if manifest is None:
            try:
                manifest = self.load_domain(domain_id)
            except FileNotFoundError:
                return {}
        return dict(manifest.constraints)

    def validate_manifest(self, manifest_path: Path) -> bool:
        try:
            raw = self._load_yaml(manifest_path)
        except (FileNotFoundError, ValueError):
            return False
        required_fields = ("domain", "version", "description", "roles")
        for field in required_fields:
            if field not in raw:
                return False
        roles_section = raw.get("roles", {}) or {}
        if "allowed" not in roles_section:
            return False
        return True

    def list_domains(self) -> List[str]:
        if not self.domains_path.exists():
            return []
        domains: List[str] = []
        for path in self.domains_path.iterdir():
            manifest_path = path / "manifest.yaml"
            if manifest_path.exists():
                domains.append(path.name)
        return sorted(domains)

    def get_manifest(self, domain_id: str) -> Optional[DomainManifest]:
        return self._manifests.get(domain_id)

    def reload_domain(self, domain_id: str) -> None:
        self._manifests.pop(domain_id, None)
        self.load_domain(domain_id)

    def _manifest_path(self, domain_id: str) -> Path:
        return self.domains_path / domain_id / "manifest.yaml"

    @staticmethod
    def _load_yaml(path: Path) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if data is None:
            raise ValueError(f"YAML file is empty: {path}")
        return data

    def _resolve_policy_path(self, manifest_path: Path, reference: str) -> Path:
        ref_path = Path(reference)
        if ref_path.is_absolute():
            return ref_path
        if reference.startswith("domains/"):
            return Path(reference)
        return manifest_path.parent / ref_path

    def _load_domain_policy(self, manifest_path: Path, raw_manifest: Dict[str, Any]) -> DomainPolicySet:
        policy_ref = (raw_manifest.get("policies") or {}).get("path")
        if not policy_ref:
            return DomainPolicySet((), (), (), "REFUSE")
        policy_path = self._resolve_policy_path(manifest_path, policy_ref)
        policy_data = self._load_yaml(policy_path)
        policies = policy_data.get("domain_policies", {}) or {}
        forbidden = tuple(sorted({*(policies.get("forbidden") or [])}))
        conditional = tuple(sorted({*(policies.get("conditional") or [])}))
        allowed = tuple(sorted({*(policies.get("allowed") or [])}))
        default_decision = policy_data.get("rules", {}).get("default_action", "REFUSE")
        return DomainPolicySet(
            forbidden=forbidden,
            conditional=conditional,
            allowed=allowed,
            default_decision=default_decision,
        )

    def _build_manifest(
        self,
        domain_id: str,
        raw: Dict[str, Any],
        policy: DomainPolicySet,
    ) -> DomainManifest:
        roles_section = raw.get("roles", {}) or {}
        allowed_roles = tuple(roles_section.get("allowed") or ())
        forbidden_roles = tuple(roles_section.get("forbidden") or ())

        knowledge_sources = tuple(
            source.get("path")
            for source in (raw.get("knowledge_sources") or [])
            if isinstance(source, dict) and source.get("path")
        )

        constraints = dict(raw.get("constraints", {}) or {})

        return DomainManifest(
            domain_id=domain_id,
            version=str(raw.get("version", "0")),
            description=str(raw.get("description", "")),
            allowed_roles=allowed_roles,
            forbidden_roles=forbidden_roles,
            tools=tuple(raw.get("tools") or ()),
            knowledge_sources=knowledge_sources,
            constraints=constraints,
            policy=policy,
        )


class DomainEnforcementError(Exception):
    def __init__(self, domain_id: str, reason: str) -> None:
        self.domain_id = domain_id
        self.reason = reason
        super().__init__(f"Domain enforcement error in '{domain_id}': {reason}")
