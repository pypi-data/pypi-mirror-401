import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest

from amochka import AmoCRMClient, CacheConfig, APIError


def make_client():
    token_data = {"access_token": "token", "expires_at": str(time.time() + 3600)}
    return AmoCRMClient(
        base_url="https://example.amocrm.ru",
        token_file=json.dumps(token_data),
        cache_config=CacheConfig.disabled(),
        disable_logging=True,
    )


def test_get_entity_notes_handles_none_response(monkeypatch):
    client = make_client()
    monkeypatch.setattr(client, "_make_request", lambda *args, **kwargs: None)
    assert client.get_entity_notes("lead", 1, get_all=True) == []


def test_get_entity_events_handles_none_response(monkeypatch):
    client = make_client()
    monkeypatch.setattr(client, "_make_request", lambda *args, **kwargs: None)
    assert client.get_entity_events("lead", 1, get_all=True) == []


def test_get_entity_notes_note_type_list_serialized(monkeypatch):
    client = make_client()
    captured = {}

    def fake_request(method, endpoint, params=None, **kwargs):
        captured["params"] = params
        return {"_embedded": {"notes": []}, "_page_count": 1}

    monkeypatch.setattr(client, "_make_request", fake_request)
    notes = client.get_entity_notes("lead", 1, note_type=["common", "call_in"])
    assert notes == []
    assert captured["params"]["filter[note_type]"] == "common,call_in"


def test_get_entity_notes_note_type_string_kept(monkeypatch):
    client = make_client()
    captured = {}

    def fake_request(method, endpoint, params=None, **kwargs):
        captured["params"] = params
        return {"_embedded": {"notes": []}, "_page_count": 1}

    monkeypatch.setattr(client, "_make_request", fake_request)
    client.get_entity_notes("lead", 1, note_type="common")
    assert captured["params"]["filter[note_type]"] == "common"


def test_iter_notes_note_type_list_serialized(monkeypatch):
    client = make_client()
    captured = {}

    def fake_request(method, endpoint, params=None, **kwargs):
        captured["params"] = params
        return {"_embedded": {"notes": []}, "_page_count": 1}

    monkeypatch.setattr(client, "_make_request", fake_request)
    list(client.iter_notes(note_type=["common", "call_in"], max_pages=1))
    assert captured["params"]["filter[note_type]"] == "common,call_in"


def test_get_entity_note_invalid_response_raises(monkeypatch):
    client = make_client()
    monkeypatch.setattr(client, "_make_request", lambda *args, **kwargs: None)
    with pytest.raises(APIError):
        client.get_entity_note("lead", 1, 2)


def test_get_event_invalid_response_raises(monkeypatch):
    client = make_client()
    monkeypatch.setattr(client, "_make_request", lambda *args, **kwargs: None)
    with pytest.raises(APIError):
        client.get_event(123)
