from __future__ import annotations

from typing import Any

import httpx

from .exceptions import ConnectionError, TimeoutError, raise_for_error

DEFAULT_BASE_URL = "https://api.openclassifier.com"
DEFAULT_TIMEOUT = 60.0


def _convert_keys_to_camel_case(data: Any) -> Any:
    """Convert snake_case keys to camelCase for API compatibility."""
    if isinstance(data, dict):
        return {
            _to_camel_case(k): _convert_keys_to_camel_case(v) for k, v in data.items()
        }
    if isinstance(data, list):
        return [_convert_keys_to_camel_case(item) for item in data]
    return data


def _to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def _convert_keys_to_snake_case(data: Any) -> Any:
    """Convert camelCase keys to snake_case for Python convention."""
    if isinstance(data, dict):
        return {
            _to_snake_case(k): _convert_keys_to_snake_case(v) for k, v in data.items()
        }
    if isinstance(data, list):
        return [_convert_keys_to_snake_case(item) for item in data]
    return data


def _to_snake_case(camel_str: str) -> str:
    """Convert camelCase to snake_case."""
    result = []
    for i, char in enumerate(camel_str):
        if char.isupper() and i > 0:
            result.append("_")
        result.append(char.lower())
    return "".join(result)


class HTTPClient:
    """HTTP client for OpenClassifier API."""

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout or DEFAULT_TIMEOUT
        self._client: httpx.Client | None = None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                timeout=self._timeout,
            )
        return self._client

    def post(self, path: str, json: dict[str, Any]) -> dict[str, Any]:
        """Make a POST request to the API."""
        client = self._get_client()
        payload = _convert_keys_to_camel_case(json)

        try:
            response = client.post(path, json=payload)
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to API: {e}") from e
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}") from e

        body = response.json()

        if response.status_code >= 400:
            raise_for_error(response.status_code, body)

        return _convert_keys_to_snake_case(body)

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> HTTPClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
