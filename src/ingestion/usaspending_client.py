"""
Phase 3 — USAspending API client
================================

Reusable HTTP client for USAspending with timeout, retries, and pagination.
"""

from __future__ import annotations

import time
from typing import Any, Iterator

import httpx

from src.config.logging import get_logger
from src.config.settings import get_settings

logger = get_logger(__name__)

_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class USASpendingClient:
    """HTTP client for api.usaspending.gov."""

    def __init__(self, timeout: float = 60.0, max_retries: int = 3) -> None:
        settings = get_settings()
        self.base_url = settings.usaspending_base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        # trust_env=False avoids broken corporate/proxy env interfering with public API calls
        self.client = httpx.Client(timeout=self.timeout, trust_env=False)

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "USASpendingClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POST JSON and return parsed response body."""
        url = f"{self.base_url}{path}"
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.post(url, json=payload)
                if response.status_code in _RETRYABLE_STATUS:
                    logger.warning(
                        "Retryable USAspending status %s on POST %s (attempt %s/%s)",
                        response.status_code,
                        path,
                        attempt,
                        self.max_retries,
                    )
                    time.sleep(2**attempt)
                    continue
                response.raise_for_status()
                return response.json()
            except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as exc:
                last_error = exc
                logger.warning(
                    "USAspending POST failed on %s (attempt %s/%s): %s",
                    path,
                    attempt,
                    self.max_retries,
                    exc,
                )
                if attempt < self.max_retries:
                    time.sleep(2**attempt)
                    continue
                raise

        raise RuntimeError(f"USAspending POST failed after retries: {path}") from last_error

    def get_json(self, path: str) -> dict[str, Any]:
        """GET JSON and return parsed response body."""
        url = f"{self.base_url}{path}"
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.get(url)
                if response.status_code in _RETRYABLE_STATUS:
                    logger.warning(
                        "Retryable USAspending status %s on GET %s (attempt %s/%s)",
                        response.status_code,
                        path,
                        attempt,
                        self.max_retries,
                    )
                    time.sleep(2**attempt)
                    continue
                response.raise_for_status()
                return response.json()
            except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as exc:
                last_error = exc
                logger.warning(
                    "USAspending GET failed on %s (attempt %s/%s): %s",
                    path,
                    attempt,
                    self.max_retries,
                    exc,
                )
                if attempt < self.max_retries:
                    time.sleep(2**attempt)
                    continue
                raise

        raise RuntimeError(f"USAspending GET failed after retries: {path}") from last_error

    def iter_award_pages(
        self,
        base_payload: dict[str, Any],
        start_page: int = 1,
    ) -> Iterator[dict[str, Any]]:
        """Yield spending_by_award pages until results are empty or hasNext is false."""
        page = start_page
        while True:
            payload = {**base_payload, "page": page}
            data = self.post_json("/api/v2/search/spending_by_award/", payload)
            results = data.get("results") or []
            if not results:
                break
            yield data

            page_metadata = data.get("page_metadata") or {}
            has_next = page_metadata.get("hasNext")
            if has_next is False:
                break
            # Some responses omit page_metadata; stop if we got fewer than requested limit
            limit = payload.get("limit") or data.get("limit")
            if has_next is None and limit and len(results) < int(limit):
                break

            page += 1
