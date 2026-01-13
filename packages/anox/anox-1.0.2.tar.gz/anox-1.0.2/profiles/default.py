"""Default profile definition for AXON Phase 0."""

PROFILE = {
    "name": "default",
    "version": "0.1",
    "identity": {
        "default_role": "developer",
        "default_source": "human",
        "subject_id": "local_cli"
    },
    "domain": {
        "active": "dev",
        "allowed": ["dev"],
    },
    "risk": {
        "ceiling": "MEDIUM",
        "require_confirmation_above": "MEDIUM"
    },
    "model": {
        "worker": {
            "type": "offline",
            "name": "axon-offline-mock"
        },
        "teacher": {
            "type": "offline",
            "enabled": False
        }
    },
    "session": {
        "max_duration_minutes": 60,
        "max_messages": 40,
        "context_size": 4096
    }
}
