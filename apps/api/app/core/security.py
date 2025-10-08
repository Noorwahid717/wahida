"""Security primitives such as rate limiting."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from time import monotonic


class RateLimitExceeded(Exception):
    """Raised when a caller exceeds the configured rate limit."""


@dataclass
class RateLimiter:
    """Simple in-memory fixed-window rate limiter."""

    limit: int
    window_seconds: int

    def __post_init__(self) -> None:
        self._calls: defaultdict[str, deque[float]] = defaultdict(deque)

    def hit(self, key: str) -> None:
        now = monotonic()
        window_start = now - self.window_seconds
        calls = self._calls[key]

        while calls and calls[0] < window_start:
            calls.popleft()

        if len(calls) >= self.limit:
            raise RateLimitExceeded("Rate limit exceeded. Please slow down.")

        calls.append(now)


__all__ = ["RateLimitExceeded", "RateLimiter"]
