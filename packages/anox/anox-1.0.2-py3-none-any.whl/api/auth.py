"""API authentication helpers."""

from __future__ import annotations

from typing import Optional

from control.auth.key_store import KeyStore


class APIAuthenticator:
    """Validates incoming API credentials (Phase 1 stub)."""

    def __init__(self, key_store: KeyStore) -> None:
        self._keys = key_store

    def authenticate(self, token: str) -> Optional[str]:
        """Return subject_id if token is valid, else None.
        
        Validates API tokens against stored keys.
        Returns the subject_id if valid, None otherwise.
        
        Note: Phase 1 implementation uses simple string comparison.
        Phase 2+ should implement:
        - Constant-time comparison to prevent timing attacks
        - Cryptographic token validation (JWT, etc.)
        - Token expiration and refresh
        - Rate limiting
        """
        if not token or not isinstance(token, str):
            return None
        
        # Validate token format (basic check)
        token = token.strip()
        if len(token) < 16:  # Minimum reasonable token length
            return None
        
        # Check token against key store
        # Note: In Phase 1, this is a basic implementation
        # Phase 2+ will add proper token validation with expiry, etc.
        try:
            # For now, we just verify the token exists in key store
            stored_key = self._keys.get_key("api_key")
            if stored_key and stored_key == token:
                # Return a placeholder subject_id
                return "authenticated_user"
            return None
        except Exception:
            # Log the error but don't expose details
            return None
