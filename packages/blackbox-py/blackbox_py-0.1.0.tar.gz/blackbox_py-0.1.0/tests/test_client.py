import io
from urllib import error
from unittest import mock

import pytest

from blackbox_py import BlackBoxClient, BlackBoxError


class FakeResponse:
    def __init__(self, status: int, body: bytes, headers=None, reason: str = "OK"):
        self.status = status
        self._body = body
        self.headers = headers or {}
        self.reason = reason

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_build_base_url_and_query():
    client = BlackBoxClient(url="http://127.0.0.1/", port=8080)
    assert client.base_url == "http://127.0.0.1:8080"
    assert client._to_query({"a": 1, "b": None, "c": ["x", "y"]}) == "?a=1&c=x&c=y"


@mock.patch("urllib.request.urlopen")
def test_request_success_json(mock_urlopen):
    mock_urlopen.return_value = FakeResponse(
        status=200,
        body=b'{"status":"ok","data":{"uptime":1}}',
        headers={"Content-Type": "application/json"},
    )
    client = BlackBoxClient(url="http://example.com", port=None)
    payload = client._request("/v1/health")
    assert payload["status"] == "ok"
    assert payload["data"]["uptime"] == 1


@mock.patch("urllib.request.urlopen")
def test_request_http_error(mock_urlopen):
    http_error = error.HTTPError(
        url="http://example.com/v1/health",
        code=400,
        msg="Bad Request",
        hdrs={},
        fp=io.BytesIO(b'{"error":{"message":"boom"}}'),
    )
    mock_urlopen.side_effect = http_error
    client = BlackBoxClient(url="http://example.com", port=None)
    with pytest.raises(BlackBoxError) as exc:
        client._request("/v1/health")
    assert exc.value.status == 400
    assert "boom" in str(exc.value)


@mock.patch("urllib.request.urlopen")
def test_request_url_error(mock_urlopen):
    mock_urlopen.side_effect = error.URLError(reason="connection refused")
    client = BlackBoxClient(url="http://example.com", port=None)
    with pytest.raises(BlackBoxError) as exc:
        client._request("/v1/health")
    assert exc.value.status == -1
    assert "connection refused" in str(exc.value)
