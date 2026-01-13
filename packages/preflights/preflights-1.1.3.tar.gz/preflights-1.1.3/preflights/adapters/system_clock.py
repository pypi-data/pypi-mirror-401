"""System clock provider for production use."""

from __future__ import annotations

from datetime import datetime, timezone


class SystemClockProvider:
    """
    Real system clock provider.

    Uses actual system time for production environments.
    """

    def now_unix(self) -> float:
        """
        Get current time as Unix timestamp.

        Returns:
            Current time in seconds since epoch
        """
        return datetime.now(timezone.utc).timestamp()

    def now_utc_iso(self) -> str:
        """
        Get current time as ISO 8601 UTC string.

        Returns:
            Time string like "2025-01-06T12:00:00.000Z"
        """
        now = datetime.now(timezone.utc)
        # Format with milliseconds
        return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"
