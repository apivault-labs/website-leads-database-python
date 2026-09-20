"""Thin synchronous client for the Shopify & Ecommerce Store Finder Apify Actor."""
from __future__ import annotations

import os
import time
from typing import Any, Mapping

import requests

from .exceptions import ActorRunError, ActorTimeoutError, AuthenticationError, WebsiteLeadsDatabaseError

ACTOR_ID = "apivault_labs~website-leads-database"
APIFY_API_BASE = "https://api.apify.com/v2"
TERMINAL_FAIL = {"FAILED", "TIMED-OUT", "ABORTED"}


class WebsiteLeadsDatabaseClient:
    """Run the hosted Actor and download its Dataset results."""

    def __init__(self, api_token: str | None = None, timeout: int = 600,
                 poll_interval: float = 3.0):
        token = api_token or os.environ.get("APIFY_API_TOKEN")
        if not token:
            raise AuthenticationError(
                "Pass api_token or set APIFY_API_TOKEN. Create a token at "
                "https://console.apify.com/account/integrations"
            )
        self.timeout = int(timeout)
        self.poll_interval = float(poll_interval)
        self.base_url = APIFY_API_BASE
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "website-leads-database-python/0.1.0",
        })

    def run(self, actor_input: Mapping[str, Any], *, actor_timeout_secs: int = 300) -> list[dict[str, Any]]:
        """Start one Actor run, wait for completion and return clean Dataset items."""
        if not isinstance(actor_input, Mapping):
            raise TypeError("actor_input must be a mapping")
        run_id = self._start(dict(actor_input), actor_timeout_secs)
        run = self._wait(run_id)
        dataset_id = run.get("defaultDatasetId")
        if not dataset_id:
            raise ActorRunError("Successful run did not expose a Dataset ID")
        return self._dataset(dataset_id)

    def run_one(self, actor_input: Mapping[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Return the first Dataset row, raising when no result was produced."""
        rows = self.run(actor_input, **kwargs)
        if not rows:
            raise ActorRunError("Actor completed but returned no Dataset rows")
        return rows[0]

    def count(self, actor_input: Mapping[str, Any], *, actor_timeout_secs: int = 300) -> dict[str, Any]:
        """Count a public audience segment without requesting paid lead rows."""
        payload = dict(actor_input)
        payload.update({"workflow": "count", "countOnly": True})
        run = self._run(payload, actor_timeout_secs)
        store_id = run.get("defaultKeyValueStoreId")
        if not store_id:
            raise ActorRunError("Successful count did not expose a result store")
        summary = self._record(store_id, "COUNT_SUMMARY")
        if not isinstance(summary, dict):
            raise ActorRunError("COUNT_SUMMARY was missing or invalid")
        return summary

    def run_page(self, actor_input: Mapping[str, Any], *, actor_timeout_secs: int = 300) -> dict[str, Any]:
        """Export one page and return rows plus the Actor's copy-ready continuation."""
        payload = dict(actor_input)
        payload.update({"workflow": "export", "countOnly": False})
        run = self._run(payload, actor_timeout_secs)
        dataset_id = run.get("defaultDatasetId")
        store_id = run.get("defaultKeyValueStoreId")
        if not dataset_id or not store_id:
            raise ActorRunError("Successful export did not expose its result stores")
        continuation = self._record(store_id, "EXPORT_CONTINUATION", required=False)
        return {
            "rows": self._dataset(dataset_id),
            "continuation": continuation if isinstance(continuation, dict) else None,
        }

    @staticmethod
    def estimate_cost(result_count: int, price_per_1000: float = 8.0) -> float:
        """Estimate result charges; actual tier pricing and platform usage may vary."""
        if result_count < 0:
            raise ValueError("result_count cannot be negative")
        return round(result_count * price_per_1000 / 1000, 6)

    def _start(self, payload: dict[str, Any], timeout_secs: int) -> str:
        try:
            response = self.session.post(
                f"{self.base_url}/acts/{ACTOR_ID}/runs",
                params={"timeout": int(timeout_secs)}, json=payload, timeout=30,
            )
        except requests.RequestException as exc:
            raise WebsiteLeadsDatabaseError(f"Could not start Actor run: {exc}") from exc
        if response.status_code == 401:
            raise AuthenticationError("Apify rejected the API token")
        if response.status_code >= 400:
            raise ActorRunError(f"Run start failed with HTTP {response.status_code}: {response.text[:300]}")
        run_id = (response.json().get("data") or {}).get("id")
        if not run_id:
            raise ActorRunError("Apify response did not contain a run ID")
        return run_id

    def _run(self, payload: dict[str, Any], timeout_secs: int) -> dict[str, Any]:
        return self._wait(self._start(payload, timeout_secs))

    def _wait(self, run_id: str) -> dict[str, Any]:
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                response = self.session.get(f"{self.base_url}/actor-runs/{run_id}", timeout=30)
            except requests.RequestException as exc:
                raise WebsiteLeadsDatabaseError(f"Could not poll Actor run: {exc}") from exc
            if response.status_code >= 400:
                raise ActorRunError(f"Run poll failed with HTTP {response.status_code}: {response.text[:300]}")
            run = response.json().get("data") or {}
            status = run.get("status")
            if status == "SUCCEEDED":
                return run
            if status in TERMINAL_FAIL:
                raise ActorRunError(f"Actor run ended with {status}: {run.get('statusMessage') or 'no details'}")
            if time.monotonic() >= deadline:
                raise ActorTimeoutError(f"Actor run {run_id} did not finish within {self.timeout} seconds")
            time.sleep(self.poll_interval)

    def _dataset(self, dataset_id: str) -> list[dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/datasets/{dataset_id}/items",
                params={"clean": "true", "format": "json"}, timeout=120,
            )
        except requests.RequestException as exc:
            raise WebsiteLeadsDatabaseError(f"Could not download Dataset: {exc}") from exc
        if response.status_code >= 400:
            raise ActorRunError(f"Dataset fetch failed with HTTP {response.status_code}: {response.text[:300]}")
        data = response.json()
        if not isinstance(data, list):
            raise ActorRunError("Unexpected Dataset response type")
        return data

    def _record(self, store_id: str, key: str, *, required: bool = True) -> Any:
        try:
            response = self.session.get(
                f"{self.base_url}/key-value-stores/{store_id}/records/{key}", timeout=30,
            )
        except requests.RequestException as exc:
            raise WebsiteLeadsDatabaseError(f"Could not download {key}: {exc}") from exc
        if response.status_code == 404 and not required:
            return None
        if response.status_code >= 400:
            raise ActorRunError(f"{key} fetch failed with HTTP {response.status_code}: {response.text[:300]}")
        try:
            return response.json()
        except ValueError as exc:
            raise ActorRunError(f"{key} response was not valid JSON") from exc
