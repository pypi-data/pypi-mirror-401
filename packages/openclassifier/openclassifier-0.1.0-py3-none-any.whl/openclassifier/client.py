from __future__ import annotations

import os
from typing import Any

from ._http import HTTPClient
from .classify import Classify


class OpenClassifier:
    """
    Client for the OpenClassifier API.

    Usage:
        client = OpenClassifier(api_key="sk_live_...")
        result = client.classify.text("Hello world", ["greeting", "question"])
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        """
        Initialize the OpenClassifier client.

        Args:
            api_key: Your OpenClassifier API key. If not provided, reads from
                     OPENCLASSIFIER_API_KEY environment variable.
            base_url: Override the default API base URL.
            timeout: Request timeout in seconds (default: 60).
        """
        resolved_key = api_key or os.environ.get("OPENCLASSIFIER_API_KEY")
        if not resolved_key:
            raise ValueError(
                "API key required. Set api_key or OPENCLASSIFIER_API_KEY env var."
            )

        self._http = HTTPClient(
            api_key=resolved_key,
            base_url=base_url,
            timeout=timeout,
        )
        self.classify = Classify(self._http)

    def close(self) -> None:
        """Close the client and release resources."""
        self._http.close()

    def __enter__(self) -> OpenClassifier:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
