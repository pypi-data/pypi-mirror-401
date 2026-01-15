import json
import os
import sys
import time

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import amochka.client as client_module
from amochka import AmoCRMClient, CacheConfig, AuthenticationError


class FakeResponse:
    def __init__(self, status_code, json_data=None, text="", headers=None):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text
        self.headers = headers or {}

    def json(self):
        return self._json_data


def _token_payload(expires_at):
    return {
        "access_token": "token",
        "refresh_token": "refresh",
        "expires_at": expires_at,
        "client_id": "client-id",
        "client_secret": "client-secret",
        "redirect_uri": "https://example.amocrm.ru",
    }


def test_validate_base_url_accepts_allowed_domains():
    assert AmoCRMClient._validate_base_url("https://example.amocrm.ru/") == "https://example.amocrm.ru"
    assert AmoCRMClient._validate_base_url("https://sub.amocrm.com") == "https://sub.amocrm.com"
    assert AmoCRMClient._validate_base_url("https://demo.kommo.com/") == "https://demo.kommo.com"


def test_validate_base_url_rejects_invalid():
    with pytest.raises(ValueError):
        AmoCRMClient._validate_base_url("http://example.amocrm.ru")
    with pytest.raises(ValueError):
        AmoCRMClient._validate_base_url("https://example.com")
    with pytest.raises(ValueError):
        AmoCRMClient._validate_base_url("https://example.amocrm.ru:8443")


def test_mask_sensitive():
    assert AmoCRMClient._mask_sensitive(None) == "***"
    assert AmoCRMClient._mask_sensitive("abcd") == "***"
    assert AmoCRMClient._mask_sensitive("abcdefghijkl") == "abcd...ijkl"


def test_env_token_overrides_file(monkeypatch, tmp_path):
    token_path = tmp_path / "token.json"
    token_path.write_text(json.dumps(_token_payload(time.time() + 3600)))

    monkeypatch.delenv("AMOCRM_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("AMOCRM_EXPIRES_AT", raising=False)
    monkeypatch.setenv("AMOCRM_ACCESS_TOKEN", "env-token")
    monkeypatch.setenv("AMOCRM_EXPIRES_AT", str(time.time() + 3600))

    client = AmoCRMClient(
        base_url="https://example.amocrm.ru",
        token_file=str(token_path),
        cache_config=CacheConfig.disabled(),
        disable_logging=True,
    )
    assert client.token == "env-token"


def test_load_token_from_json_string():
    payload = _token_payload(time.time() + 3600)
    client = AmoCRMClient(
        base_url="https://example.amocrm.ru",
        token_file=json.dumps(payload),
        cache_config=CacheConfig.disabled(),
        disable_logging=True,
    )
    assert client.token == "token"


def test_invalid_token_string_raises():
    with pytest.raises(AuthenticationError):
        AmoCRMClient(
            base_url="https://example.amocrm.ru",
            token_file="{bad json",
            cache_config=CacheConfig.disabled(),
            disable_logging=True,
        )


def test_missing_token_file_and_env_raises():
    with pytest.raises(AuthenticationError):
        AmoCRMClient(
            base_url="https://example.amocrm.ru",
            token_file=None,
            cache_config=CacheConfig.disabled(),
            disable_logging=True,
        )


def test_refresh_access_token_success(monkeypatch, tmp_path):
    token_path = tmp_path / "token.json"
    token_path.write_text(json.dumps(_token_payload(time.time() - 10)))

    def fake_post(*args, **kwargs):
        return FakeResponse(
            200,
            json_data={
                "access_token": "new-token",
                "refresh_token": "new-refresh",
                "expires_in": 3600,
            },
        )

    monkeypatch.setattr(client_module.requests, "post", fake_post)

    client = AmoCRMClient(
        base_url="https://example.amocrm.ru",
        token_file=str(token_path),
        cache_config=CacheConfig.disabled(),
        disable_logging=True,
    )

    assert client.token == "new-token"
    saved = json.loads(token_path.read_text())
    assert saved["access_token"] == "new-token"


def test_refresh_access_token_failure(monkeypatch, tmp_path):
    token_path = tmp_path / "token.json"
    token_path.write_text(json.dumps(_token_payload(time.time() - 10)))

    def fake_post(*args, **kwargs):
        return FakeResponse(400, text="bad")

    monkeypatch.setattr(client_module.requests, "post", fake_post)

    with pytest.raises(AuthenticationError):
        AmoCRMClient(
            base_url="https://example.amocrm.ru",
            token_file=str(token_path),
            cache_config=CacheConfig.disabled(),
            disable_logging=True,
        )


def test_refresh_access_token_invalid_json(monkeypatch, tmp_path):
    token_path = tmp_path / "token.json"
    token_path.write_text(json.dumps(_token_payload(time.time() - 10)))

    class BadJsonResponse:
        status_code = 200
        text = "not json"

        def json(self):
            raise ValueError("invalid json")

    monkeypatch.setattr(client_module.requests, "post", lambda *args, **kwargs: BadJsonResponse())

    with pytest.raises(AuthenticationError):
        AmoCRMClient(
            base_url="https://example.amocrm.ru",
            token_file=str(token_path),
            cache_config=CacheConfig.disabled(),
            disable_logging=True,
        )


def test_cache_path_validation():
    with pytest.raises(ValueError):
        CacheConfig._validate_path("../secret", "base_dir")
    with pytest.raises(ValueError):
        CacheConfig._validate_path("", "file")


def test_cache_file_path_stays_in_base_dir(tmp_path):
    token_path = tmp_path / "acct..name.json"
    token_path.write_text(json.dumps(_token_payload(time.time() + 3600)))
    cache_dir = tmp_path / "cache"
    cache_config = CacheConfig.file_cache(base_dir=str(cache_dir))

    client = AmoCRMClient(
        base_url="https://example.amocrm.ru",
        token_file=str(token_path),
        cache_config=cache_config,
        disable_logging=True,
    )

    cache_path = client._get_cache_file_path("users")
    assert os.path.realpath(cache_path).startswith(os.path.realpath(str(cache_dir)))
    assert ".." not in os.path.basename(cache_path)


def test_extract_account_name_from_token_file(tmp_path):
    token_path = tmp_path / "accounts" / "bneginskogo_eng.json"
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(json.dumps(_token_payload(time.time() + 3600)))

    client = AmoCRMClient(
        base_url="https://example.amocrm.ru",
        token_file=str(token_path),
        cache_config=CacheConfig.disabled(),
        disable_logging=True,
    )

    assert client._extract_account_name() == "eng"
