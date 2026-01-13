# core/intent.py
"""Rule-based intent classification for AXON Phase 1."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Sequence, Tuple

_TOKENIZER = re.compile(r"[^a-z0-9]+")


def _normalize_phrase(value: str) -> str:
    cleaned = _TOKENIZER.sub(" ", value.lower())
    return " ".join(cleaned.split())


def _slugify(value: str) -> str:
    return _normalize_phrase(value).replace(" ", "_")


def _tokenize(normalized: str) -> Tuple[str, ...]:
    return tuple(normalized.split())


def _normalize_term(term: str) -> str:
    normalized = _normalize_phrase(term)
    if not normalized:
        raise ValueError("term cannot be empty")
    if " " in normalized:
        raise ValueError("term must be a single token")
    return normalized


@dataclass(frozen=True)
class Intent:
    """Immutable, auditable intent representation."""

    domain: str
    action: str
    passive: bool
    confidence: str = "LOW"
    decision_trace: Tuple[str, ...] = ()


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"

    @property
    def weight(self) -> int:
        return {self.HIGH: 3, self.MEDIUM: 2}[self]


@dataclass(frozen=True)
class MatchResult:
    definition: "ActionDefinition"
    confidence: ConfidenceLevel
    rule: str


@dataclass(frozen=True)
class ActionDefinition:
    name: str
    domain: str
    passive: bool
    aliases: Tuple[str, ...] = tuple()
    term_sets: Tuple[Tuple[str, ...], ...] = tuple()

    def __post_init__(self) -> None:
        alias_slugs = tuple(_slugify(alias) for alias in (self.name, *self.aliases))
        term_sets = tuple(tuple(_normalize_term(term) for term in term_set) for term_set in self.term_sets)
        object.__setattr__(self, "aliases", alias_slugs)
        object.__setattr__(self, "term_sets", term_sets)

    def match(self, slug: str, token_set: Sequence[str]) -> MatchResult | None:
        if slug in self.aliases:
            return MatchResult(self, ConfidenceLevel.HIGH, f"alias:{slug}")
        if not token_set:
            return None
        token_lookup = set(token_set)
        for term_set in self.term_sets:
            if all(term in token_lookup for term in term_set):
                joined = "+".join(term_set)
                return MatchResult(self, ConfidenceLevel.MEDIUM, f"terms:{joined}")
        return None


ACTION_REGISTRY: Tuple[ActionDefinition, ...] = (
    ActionDefinition(
        name="code_generation",
        domain="dev",
        passive=False,
        aliases=("generate_code", "write_code"),
        term_sets=(
            ("generate", "code"),
            ("write", "code"),
            ("create", "script"),
            ("generate", "script"),
            ("write", "script"),
            ("create", "function"),
            ("write", "function"),
        ),
    ),
    ActionDefinition(
        name="code_refactoring",
        domain="dev",
        passive=False,
        aliases=("refactor_code",),
        term_sets=(("refactor", "code"), ("improve", "code")),
    ),
    ActionDefinition(
        name="architecture_design",
        domain="dev",
        passive=False,
        term_sets=(("architecture", "design"), ("system", "design")),
    ),
    ActionDefinition(
        name="documentation",
        domain="dev",
        passive=False,
        term_sets=(("write", "documentation"), ("update", "docs")),
    ),
    ActionDefinition(
        name="static_code_review",
        domain="dev",
        passive=True,
        aliases=("code_review", "analyze_code"),
        term_sets=(
            ("review", "code"),
            ("static", "analysis"),
            ("analyze", "code"),
            ("code", "analysis"),
            ("code", "quality"),
            ("review", "security"),
            ("security", "review"),
        ),
    ),
    ActionDefinition(
        name="defensive_security_analysis",
        domain="blue",
        passive=False,
        term_sets=(("defensive", "analysis"), ("blue", "analysis")),
    ),
    ActionDefinition(
        name="detection_and_monitoring_design",
        domain="blue",
        passive=False,
        term_sets=(("monitoring", "design"), ("detection", "design")),
    ),
    ActionDefinition(
        name="read_analysis",
        domain="read_only",
        passive=True,
        term_sets=(("read", "analysis"),),
    ),
    ActionDefinition(
        name="view_logs",
        domain="read_only",
        passive=True,
        term_sets=(("view", "logs"), ("read", "logs")),
    ),
    ActionDefinition(
        name="red_team_vulnerability_analysis",
        domain="red",
        passive=False,
        aliases=("vuln_analysis",),
        term_sets=(("vulnerability", "analysis"), ("red", "team")),
    ),
    ActionDefinition(
        name="exploit_patterns_non_operational",
        domain="red",
        passive=False,
        term_sets=(("exploit", "pattern"),),
    ),
    ActionDefinition(
        name="security_sensitive_code_generation",
        domain="dev",
        passive=False,
        term_sets=(
            ("generate", "security", "code"),
            ("write", "security", "code"),
            ("create", "authentication"),
            ("create", "encryption"),
        ),
    ),
    ActionDefinition(
        name="malware_structure_analysis_static",
        domain="malware",
        passive=True,
        term_sets=(("malware", "analysis"), ("static", "malware")),
    ),
    ActionDefinition(
        name="system_configuration_change",
        domain="cloud",
        passive=False,
        term_sets=(("configuration", "change"), ("system", "config")),
    ),
    ActionDefinition(
        name="auto_execute_attack",
        domain="red",
        passive=False,
        term_sets=(("auto", "attack"), ("automatic", "attack")),
    ),
    ActionDefinition(
        name="real_world_exploitation",
        domain="red",
        passive=False,
        term_sets=(("real", "exploitation"), ("real", "attack")),
    ),
    ActionDefinition(
        name="malware_execution",
        domain="malware",
        passive=False,
        term_sets=(("execute", "malware"),),
    ),
    ActionDefinition(
        name="bypass_authorization",
        domain="red",
        passive=False,
        term_sets=(("bypass", "authorization"),),
    ),
    ActionDefinition(
        name="disable_audit_logging",
        domain="dev",
        passive=False,
        term_sets=(("disable", "audit"), ("turn", "audit")),
    ),
    ActionDefinition(
        name="hidden_or_unaudited_actions",
        domain="dev",
        passive=False,
        term_sets=(("hidden", "action"), ("unaudited", "action")),
    ),
    ActionDefinition(
        name="self_modifying_policy",
        domain="dev",
        passive=False,
        term_sets=(("modify", "policy"), ("self", "policy")),
    ),
    
    # Conversational intents for general queries and natural language interaction
    ActionDefinition(
        name="general_query",
        domain="read_only",
        passive=True,
        aliases=("ask_question", "general_question"),
        term_sets=(
            ("what", "is"),
            ("what", "are"),
            ("how", "to"),
            ("how", "do"),
            ("how", "can"),
            ("how", "does"),
            ("why", "is"),
            ("why", "does"),
            ("why", "are"),
            ("when", "should"),
            ("when", "is"),
            ("where", "is"),
            ("where", "can"),
            ("who", "is"),
            ("can", "you"),
            ("could", "you"),
            ("will", "you"),
            ("would", "you"),
            ("tell", "me"),
            ("explain", "this"),
            ("explain", "how"),
            ("explain", "what"),
            ("explain", "why"),
        ),
    ),
    ActionDefinition(
        name="help_request",
        domain="read_only",
        passive=True,
        aliases=("get_help", "need_help"),
        term_sets=(("guide",), ("tutorial",), ("documentation",), ("need", "help")),
    ),
    ActionDefinition(
        name="general_conversation",
        domain="read_only",
        passive=True,
        aliases=("chat", "talk", "conversation"),
        term_sets=(
            ("hello",),
            ("hi",),
            ("hey",),
            ("thank", "you"),
            ("good", "morning"),
            ("good", "evening"),
        ),
    ),
)

_ACTION_LOOKUP = {definition.name: definition for definition in ACTION_REGISTRY}


class IntentClassifier:
    """Deterministic, audit-friendly intent classifier."""

    ACTIONS: Sequence[ActionDefinition] = ACTION_REGISTRY

    @classmethod
    def classify(cls, raw_input: str) -> Intent:
        normalized, slug, tokens, trace = cls._prepare_input(raw_input)
        match, match_trace = cls._determine_match(slug, tokens)
        trace.extend(match_trace)
        trace.append(f"selected:{match.definition.name}:{match.confidence.value}")
        trace.append(f"domain:{match.definition.domain}")
        return Intent(
            domain=match.definition.domain,
            action=match.definition.name,
            passive=match.definition.passive,
            confidence=match.confidence.value,
            decision_trace=tuple(trace),
        )

    @classmethod
    def classify_from_input(cls, user_input: str) -> Intent:
        return cls.classify(user_input)

    @classmethod
    def validate(cls, intent: Intent) -> bool:
        definition = _ACTION_LOOKUP.get(intent.action)
        if not definition:
            return False
        if definition.domain != intent.domain:
            return False
        if definition.passive != intent.passive:
            return False
        return True

    @staticmethod
    def _prepare_input(raw_input: str) -> Tuple[str, str, Tuple[str, ...], list[str]]:
        if not raw_input or not raw_input.strip():
            raise ValueError("Intent classification failed: empty input")
        normalized = _normalize_phrase(raw_input)
        if not normalized:
            raise ValueError("Intent classification failed: no valid tokens")
        slug = normalized.replace(" ", "_")
        tokens = _tokenize(normalized)
        trace = [
            f"raw:{raw_input}",
            f"normalized:{normalized}",
            f"slug:{slug}",
        ]
        return normalized, slug, tokens, trace

    @classmethod
    def _determine_match(
        cls,
        slug: str,
        tokens: Tuple[str, ...],
    ) -> Tuple[MatchResult, list[str]]:
        match_trace: list[str] = []
        matches: list[MatchResult] = []
        for definition in cls.ACTIONS:
            result = definition.match(slug, tokens)
            if result:
                matches.append(result)
                match_trace.append(
                    f"match:{definition.name}:{result.rule}:{result.confidence.value}"
                )
        if not matches:
            # Fallback to general_query instead of raising error
            match_trace.append("fallback:no_match:using_general_query")
            fallback_definition = _ACTION_LOOKUP.get("general_query")
            if not fallback_definition:
                raise ValueError("Intent classification failed: no matching actions and no fallback available")
            fallback_match = MatchResult(
                definition=fallback_definition,
                confidence=ConfidenceLevel.MEDIUM,
                rule="fallback"
            )
            return fallback_match, match_trace
        best_weight = max(match.confidence.weight for match in matches)
        best_matches = [m for m in matches if m.confidence.weight == best_weight]
        if len(best_matches) > 1:
            names = ", ".join(m.definition.name for m in best_matches)
            raise ValueError(f"Intent classification ambiguous: {names}")
        return best_matches[0], match_trace
