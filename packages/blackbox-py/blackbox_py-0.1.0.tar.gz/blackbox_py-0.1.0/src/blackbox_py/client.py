"""
Minimal Python client for the BlackBox HTTP API.
Mirrors the endpoints exposed by the reference JS client.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, Mapping, Optional
from urllib import error, parse, request


class BlackBoxError(Exception):
    """Represents HTTP or network failures when talking to BlackBox."""

    def __init__(self, status: int, message: str):
        super().__init__(f"HTTP {status}: {message}")
        self.status = status
        self.message = message


class BlackBoxClient:
    """
    Lightweight HTTP client for BlackBox DB.

    Example:
        client = BlackBoxClient(url="http://127.0.0.1", port=8080)
        print(client.health())
        client.create_index({"name": "demo", "schema": {"fields": {"title": "text"}}})
        client.index_document("demo", {"title": "hello"})
        hits = client.search("demo", {"q": "hello"})
    """

    def __init__(self, url: str = "http://127.0.0.1", port: Optional[int] = 8080, timeout: float = 10.0):
        self.base_url = self._build_base_url(url, port)
        self.timeout = timeout

    def _build_base_url(self, url: str, port: Optional[int]) -> str:
        if not url:
            raise ValueError("url is required")
        normalized = url.rstrip("/")
        return f"{normalized}:{port}" if port else normalized

    def _to_query(self, params: Optional[Mapping[str, Any]]) -> str:
        if not params:
            return ""
        filtered = {k: v for k, v in params.items() if v is not None}
        if not filtered:
            return ""
        return f"?{parse.urlencode(filtered, doseq=True)}"

    def _extract_error(self, payload: Any, status_text: str) -> str:
        if isinstance(payload, dict):
            if isinstance(payload.get("error"), dict) and "message" in payload["error"]:
                return str(payload["error"]["message"])
            if "message" in payload:
                return str(payload["message"])
        if isinstance(payload, str) and payload:
            return payload
        return status_text or "Request failed"

    def _request(
        self,
        path: str,
        method: str = "GET",
        *,
        headers: Optional[Mapping[str, str]] = None,
        body: Optional[Any] = None,
    ) -> Any:
        endpoint = f"{self.base_url}{path}"
        final_headers: Dict[str, str] = {"Accept": "application/json"}
        if headers:
            final_headers.update(headers)

        data_bytes = None
        if body is not None:
            if not isinstance(body, (str, bytes)):
                body = json.dumps(body)
            if isinstance(body, str):
                body = body.encode("utf-8")
            data_bytes = body
            final_headers.setdefault("Content-Type", "application/json")

        req = request.Request(endpoint, data=data_bytes, method=method, headers=final_headers)
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                status = resp.status
                content_type = resp.headers.get("Content-Type", "")
                raw = resp.read()
                payload: Any
                if "application/json" in content_type:
                    payload = json.loads(raw.decode("utf-8") or "null")
                else:
                    payload = raw.decode("utf-8")

                if status >= 400:
                    message = self._extract_error(payload, resp.reason)
                    raise BlackBoxError(status, message)
                return payload
        except error.HTTPError as exc:
            raw_body = exc.read().decode("utf-8")
            try:
                payload = json.loads(raw_body) if raw_body else None
            except json.JSONDecodeError:
                payload = raw_body
            message = self._extract_error(payload, exc.reason)
            raise BlackBoxError(exc.code, message) from None
        except error.URLError as exc:
            raise BlackBoxError(-1, str(exc.reason)) from None

    # Health & config
    def health(self) -> Any:
        return self._request("/v1/health")

    def metrics(self) -> Any:
        return self._request("/v1/metrics")

    def prometheus_metrics(self) -> Any:
        return self._request("/metrics", headers={"Accept": "text/plain"})

    def config(self) -> Any:
        return self._request("/v1/config")

    # Index management
    def create_index(self, body: Mapping[str, Any]) -> Any:
        return self._request("/v1/indexes", method="POST", body=body)

    def list_indexes(self) -> Any:
        return self._request("/v1/indexes")

    # Snapshots / shipping
    def save_snapshot(self, path: Optional[str] = None) -> Any:
        qs = self._to_query({"path": path} if path else None)
        return self._request(f"/v1/snapshot{qs}", method="POST")

    def load_snapshot(self, path: Optional[str] = None) -> Any:
        qs = self._to_query({"path": path} if path else None)
        return self._request(f"/v1/snapshot/load{qs}", method="POST")

    def ship_plan(self) -> Any:
        return self._request("/v1/ship")

    def ship_apply(self, path: str) -> Any:
        if not path:
            raise ValueError("path is required")
        qs = self._to_query({"path": path})
        return self._request(f"/v1/ship/apply{qs}", method="POST")

    def ship_fetch_apply(self, base: str) -> Any:
        if not base:
            raise ValueError("base is required")
        qs = self._to_query({"base": base})
        return self._request(f"/v1/ship/fetch_apply{qs}", method="POST")

    # Documents
    def index_document(self, index: str, doc: Mapping[str, Any]) -> Any:
        if not index:
            raise ValueError("index is required")
        encoded = parse.quote(index, safe="")
        return self._request(f"/v1/{encoded}/doc", method="POST", body=doc)

    def bulk_index(self, index: str, docs: Iterable[Mapping[str, Any]], *, continue_on_error: bool = True) -> Any:
        if not index:
            raise ValueError("index is required")
        encoded = parse.quote(index, safe="")
        body = list(docs)
        qs = self._to_query({"continue_on_error": str(continue_on_error).lower()})
        return self._request(f"/v1/{encoded}/_bulk{qs}", method="POST", body=body)

    def get_document(self, index: str, doc_id: Any) -> Any:
        if not index or doc_id is None:
            raise ValueError("index and id are required")
        encoded_index = parse.quote(index, safe="")
        encoded_id = parse.quote(str(doc_id), safe="")
        return self._request(f"/v1/{encoded_index}/doc/{encoded_id}")

    def replace_document(self, index: str, doc_id: Any, doc: Mapping[str, Any]) -> Any:
        if not index or doc_id is None:
            raise ValueError("index and id are required")
        encoded_index = parse.quote(index, safe="")
        encoded_id = parse.quote(str(doc_id), safe="")
        return self._request(f"/v1/{encoded_index}/doc/{encoded_id}", method="PUT", body=doc)

    def update_document(self, index: str, doc_id: Any, doc: Mapping[str, Any]) -> Any:
        if not index or doc_id is None:
            raise ValueError("index and id are required")
        encoded_index = parse.quote(index, safe="")
        encoded_id = parse.quote(str(doc_id), safe="")
        return self._request(f"/v1/{encoded_index}/doc/{encoded_id}", method="PATCH", body=doc)

    def delete_document(self, index: str, doc_id: Any) -> Any:
        if not index or doc_id is None:
            raise ValueError("index and id are required")
        encoded_index = parse.quote(index, safe="")
        encoded_id = parse.quote(str(doc_id), safe="")
        return self._request(f"/v1/{encoded_index}/doc/{encoded_id}", method="DELETE")

    def stored_match(self, index: str, *, field: str, value: Any) -> Any:
        if not index:
            raise ValueError("index is required")
        if not field:
            raise ValueError("field is required")
        if value is None:
            raise ValueError("value is required")
        encoded_index = parse.quote(index, safe="")
        qs = self._to_query({"field": field, "value": value})
        return self._request(f"/v1/{encoded_index}/stored_match{qs}")

    def search(self, index: str, params: Optional[Mapping[str, Any]] = None) -> Any:
        if not index:
            raise ValueError("index is required")
        encoded_index = parse.quote(index, safe="")
        qs = self._to_query(params)
        return self._request(f"/v1/{encoded_index}/search{qs}")

    # Custom templates
    def list_custom_templates(self) -> Any:
        return self._request("/v1/custom")

    def get_custom_template(self, name: str) -> Any:
        if not name:
            raise ValueError("name is required")
        encoded = parse.quote(name, safe="")
        return self._request(f"/v1/custom/{encoded}")

    def put_custom_template(self, name: str, template: Mapping[str, Any]) -> Any:
        if not name:
            raise ValueError("name is required")
        encoded = parse.quote(name, safe="")
        return self._request(f"/v1/custom/{encoded}", method="PUT", body=template)

    def execute_custom_template(self, name: str, params: Optional[Mapping[str, Any]] = None) -> Any:
        if not name:
            raise ValueError("name is required")
        encoded = parse.quote(name, safe="")
        return self._request(f"/v1/custom/{encoded}", method="POST", body=params or {})


__all__ = ["BlackBoxClient", "BlackBoxError"]
