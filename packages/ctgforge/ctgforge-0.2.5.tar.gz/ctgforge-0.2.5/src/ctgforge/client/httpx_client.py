from typing import Any, Optional

import httpx

from ctgforge.client.ctg_client import CTGClient, CTGTransportError, RetryConfig


class CTGHttpxClient(CTGClient):
    """
    Httpx-based thin HTTP transport for ClinicalTrials.gov v2.
    """

    def __init__(
        self,
        *,
        timeout: float = 30.0,
        headers: Optional[dict[str, str]] = None,
        retry: Optional[RetryConfig] = None,
        client: Optional[httpx.Client] = None,
    ) -> None:
        super().__init__(
            headers=headers,
            retry=retry,
            client=client,
        )

        self._client = client or httpx.Client(
            base_url=self.BASE_URL,
            timeout=httpx.Timeout(timeout),
            headers=self._headers,
            follow_redirects=True,
        )

    # ------ Implementation of abstract methods ------

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Any = None,
    ) -> dict[str, Any]:
        last_exc: Optional[Exception] = None

        # Convert dict-type params to httpx's QueryParams to keep "+" unescaped
        str_params = []
        if params is not None:
            for k, v in params.items():
                str_params.append(f"{k}={v}")
        qp = httpx.QueryParams("&".join(str_params))

        for attempt in range(self._retry.max_retries + 1):
            try:
                resp = self._client.request(
                    method,
                    path,
                    params=qp,
                    json=json,
                )
                if resp.status_code in self._retry.retry_statuses:
                    self._sleep_backoff(attempt, resp.headers.get("Retry-After"))
                    continue

                resp.raise_for_status()
                data = resp.json()
                if not isinstance(data, dict):
                    raise CTGTransportError(f"Expected JSON object, got: {type(data)}")
                return data

            except (httpx.TimeoutException, httpx.NetworkError) as e:
                last_exc = e
                self._sleep_backoff(attempt, None)
                continue
            except httpx.HTTPStatusError as e:
                # Non-retryable HTTP error
                raise CTGTransportError(
                    f"HTTP error: {e.response.status_code} calling {path}: {e.response.text[:300]}"
                ) from e
            except ValueError as e:
                # JSON decoding errors
                raise CTGTransportError(f"Invalid JSON response from {path}") from e

        raise CTGTransportError(f"Exhausted retries calling {path}") from last_exc
