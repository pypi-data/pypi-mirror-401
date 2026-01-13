"""Random UID provider for production use."""

from __future__ import annotations

import secrets
import uuid
from datetime import datetime, timezone


class RandomUIDProvider:
    """
    Random UID provider for production.

    Generates unique IDs using timestamp + random hex suffix.
    Format: YYYYMMDDTHHMMSS.mmmZ-XXXX
    """

    def generate(self) -> str:
        """
        Generate a new unique UID.

        Returns:
            UID string in format "YYYYMMDDTHHMMSS.mmmZ-XXXX"

        Note: Uses current timestamp + cryptographic random suffix for uniqueness.
        """
        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y%m%dT%H%M%S")
        ms = now.microsecond // 1000
        # Generate random 4-char hex suffix (65536 possibilities)
        suffix = secrets.token_hex(2).upper()
        return f"{timestamp}.{ms:03d}Z-{suffix}"

    def generate_session_id(self) -> str:
        """
        Generate a new session ID.

        Returns:
            UUID-based session identifier
        """
        return str(uuid.uuid4())
