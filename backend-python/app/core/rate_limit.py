from __future__ import annotations

from collections import defaultdict, deque
from threading import Lock
from time import time

from fastapi import HTTPException, Request, status

from app.core.config import get_settings


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._storage: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str) -> None:
        settings = get_settings()
        current_time = time()
        window = settings.rate_limit_window_seconds

        with self._lock:
            bucket = self._storage[key]
            while bucket and bucket[0] <= current_time - window:
                bucket.popleft()

            if len(bucket) >= settings.rate_limit_max_attempts:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Demasiados intentos. Espera un momento e intenta de nuevo.",
                )

            bucket.append(current_time)


rate_limiter = InMemoryRateLimiter()


def rate_limit_auth_requests(request: Request) -> None:
    client_host = request.client.host if request.client else "anonymous"
    route_key = f"{client_host}:{request.url.path}"
    rate_limiter.check(route_key)
