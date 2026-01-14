import json
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import amochka.client as client_module
from amochka import AmoCRMClient, CacheConfig, APIError, NotFoundError, RateLimitError


class FakeResponse:
    def __init__(self, status_code, json_data=None, text="", headers=None, raise_on_json=False):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text
        self.headers = headers or {}
        self._raise_on_json = raise_on_json

    def json(self):
        if self._raise_on_json:
            raise ValueError("invalid json")
        return self._json_data


def make_client(max_retries=0):
    token_data = {"access_token": "token", "expires_at": str(time.time() + 3600)}
    return AmoCRMClient(
        base_url="https://example.amocrm.ru",
        token_file=json.dumps(token_data),
        cache_config=CacheConfig.disabled(),
        disable_logging=True,
        max_retries=max_retries,
    )


def test_make_request_success_json(monkeypatch):
    client = make_client()

    def fake_request(*args, **kwargs):
        return FakeResponse(200, json_data={"ok": True})

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    assert client._make_request("GET", "/api/v4/leads") == {"ok": True}


def test_make_request_invalid_json_raises(monkeypatch):
    client = make_client()

    def fake_request(*args, **kwargs):
        return FakeResponse(200, text="not json", raise_on_json=True)

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    with pytest.raises(APIError) as excinfo:
        client._make_request("GET", "/api/v4/leads")
    assert "Invalid JSON response" in str(excinfo.value)


def test_make_request_204_returns_none(monkeypatch):
    client = make_client()

    def fake_request(*args, **kwargs):
        return FakeResponse(204)

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    assert client._make_request("DELETE", "/api/v4/leads/1") is None


def test_make_request_404_raises(monkeypatch):
    client = make_client()

    def fake_request(*args, **kwargs):
        return FakeResponse(404, text="not found")

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    with pytest.raises(NotFoundError):
        client._make_request("GET", "/api/v4/leads/404")


def test_make_request_bad_request_non_sensitive(monkeypatch):
    client = make_client()

    def fake_request(*args, **kwargs):
        return FakeResponse(400, text="bad request")

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    with pytest.raises(APIError) as excinfo:
        client._make_request("GET", "/api/v4/leads")
    assert "bad request" in str(excinfo.value)


def test_make_request_bad_request_sensitive(monkeypatch):
    client = make_client()

    def fake_request(*args, **kwargs):
        return FakeResponse(400, text="secret token")

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    with pytest.raises(APIError) as excinfo:
        client._make_request("POST", "/oauth2/access_token")
    assert "secret token" not in str(excinfo.value)


def test_rate_limit_error_includes_retry_after(monkeypatch):
    client = make_client(max_retries=0)

    def fake_request(*args, **kwargs):
        return FakeResponse(429, text="too many", headers={"Retry-After": "3"})

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    with pytest.raises(RateLimitError) as excinfo:
        client._make_request("GET", "/api/v4/leads")
    assert excinfo.value.retry_after == "3"
    assert "too many" in str(excinfo.value)


def test_rate_limit_sensitive_hides_body(monkeypatch):
    client = make_client(max_retries=0)

    def fake_request(*args, **kwargs):
        return FakeResponse(429, text="secret", headers={"Retry-After": "1"})

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    with pytest.raises(RateLimitError) as excinfo:
        client._make_request("GET", "/oauth2/access_token")
    assert "secret" not in str(excinfo.value)


def test_retries_then_succeeds(monkeypatch):
    client = make_client(max_retries=1)
    responses = [
        FakeResponse(500, text="server error"),
        FakeResponse(200, json_data={"ok": True}),
    ]
    calls = []

    def fake_request(*args, **kwargs):
        calls.append(1)
        return responses.pop(0)

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    monkeypatch.setattr(client_module.time, "sleep", lambda *_: None)
    assert client._make_request("GET", "/api/v4/leads") == {"ok": True}
    assert len(calls) == 2


def test_401_triggers_refresh(monkeypatch):
    client = make_client(max_retries=1)
    client.refresh_token = "refresh"
    client.client_id = "id"
    client.client_secret = "secret"
    client.redirect_uri = "https://example.amocrm.ru"

    responses = [
        FakeResponse(401, text="unauthorized"),
        FakeResponse(200, json_data={"ok": True}),
    ]
    refreshed = {"called": 0}

    def fake_request(*args, **kwargs):
        return responses.pop(0)

    def fake_refresh():
        refreshed["called"] += 1
        client.token = "new-token"

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    monkeypatch.setattr(client, "_refresh_access_token", fake_refresh)
    assert client._make_request("GET", "/api/v4/leads") == {"ok": True}
    assert refreshed["called"] == 1


def test_timeout_raises_api_error(monkeypatch):
    client = make_client(max_retries=0)

    def fake_request(*args, **kwargs):
        raise client_module.requests.exceptions.Timeout("timeout")

    monkeypatch.setattr(client_module.requests, "request", fake_request)
    with pytest.raises(APIError):
        client._make_request("GET", "/api/v4/leads")
