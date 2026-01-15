import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import amochka.client as client_module
from amochka import AmoCRMClient, CacheConfig


def make_client(cache_config):
    token_data = {"access_token": "token", "expires_at": str(time.time() + 3600)}
    return AmoCRMClient(
        base_url="https://example.amocrm.ru",
        token_file=json.dumps(token_data),
        cache_config=cache_config,
        disable_logging=True,
    )


def make_file_client(tmp_path, lifetime_hours=1):
    token_path = tmp_path / "token.json"
    token_path.write_text(json.dumps({"access_token": "token", "expires_at": str(time.time() + 3600)}))
    cache_dir = tmp_path / "cache"
    cache_config = CacheConfig.file_cache(base_dir=str(cache_dir), lifetime_hours=lifetime_hours)
    return AmoCRMClient(
        base_url="https://example.amocrm.ru",
        token_file=str(token_path),
        cache_config=cache_config,
        disable_logging=True,
    )


def test_memory_cache_ttl(monkeypatch):
    client = make_client(CacheConfig.memory_only())
    client._memory_cache_ttl = 10

    now = {"value": 100.0}

    def fake_time():
        return now["value"]

    monkeypatch.setattr(client_module.time, "time", fake_time)

    calls = {"count": 0}

    def fetch():
        calls["count"] += 1
        return [calls["count"]]

    assert client._get_cached_resource("users", fetch) == [1]
    now["value"] = 105.0
    assert client._get_cached_resource("users", fetch) == [1]
    assert calls["count"] == 1
    now["value"] = 120.0
    assert client._get_cached_resource("users", fetch) == [2]
    assert calls["count"] == 2


def test_file_cache_save_and_load(tmp_path):
    client = make_file_client(tmp_path, lifetime_hours=1)
    payload = [{"id": 1}]
    client._save_cache("users", payload)
    loaded = client._load_cache("users")
    assert loaded == payload


def test_file_cache_expired_returns_none(tmp_path):
    client = make_file_client(tmp_path, lifetime_hours=1)
    payload = [{"id": 1}]
    client._save_cache("users", payload)
    cache_path = client._get_cache_file_path("users")
    with open(cache_path, "r", encoding="utf-8") as handle:
        cache_data = json.loads(handle.read())
    cache_data["last_updated"] = time.time() - 7200
    with open(cache_path, "w", encoding="utf-8") as handle:
        json.dump(cache_data, handle)
    assert client._load_cache("users") is None


def test_get_lifetime_default_and_none():
    config = CacheConfig(lifetime_hours={"users": 5})
    assert config.get_lifetime("users") == 5
    assert config.get_lifetime("unknown") == 24
    config = CacheConfig(lifetime_hours=None)
    assert config.get_lifetime("users") is None
