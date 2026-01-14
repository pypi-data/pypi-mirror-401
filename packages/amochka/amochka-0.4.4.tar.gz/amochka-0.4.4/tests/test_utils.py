import json
import os
import sys
import time
from datetime import datetime

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from amochka import AmoCRMClient, CacheConfig


class PaginationClient(AmoCRMClient):
    def __init__(self, responses):
        token_data = {"access_token": "token", "expires_at": str(time.time() + 3600)}
        super().__init__(
            base_url="https://example.amocrm.ru",
            token_file=json.dumps(token_data),
            cache_config=CacheConfig.disabled(),
            disable_logging=True,
        )
        self._responses = list(responses)
        self.calls = 0

    def _make_request(self, method, endpoint, params=None, data=None, timeout=10):
        self.calls += 1
        return self._responses.pop(0)


def make_client():
    token_data = {"access_token": "token", "expires_at": str(time.time() + 3600)}
    return AmoCRMClient(
        base_url="https://example.amocrm.ru",
        token_file=json.dumps(token_data),
        cache_config=CacheConfig.disabled(),
        disable_logging=True,
    )


def test_to_timestamp():
    client = make_client()
    dt = datetime(2020, 1, 1, 0, 0, 0)
    assert client._to_timestamp(dt) == int(dt.timestamp())
    assert client._to_timestamp(1700000000) == 1700000000
    assert client._to_timestamp(1700000000.5) == 1700000000
    iso = "2020-01-01T00:00:00"
    assert client._to_timestamp(iso) == int(datetime.fromisoformat(iso).timestamp())
    iso_z = "2020-01-01T00:00:00Z"
    assert client._to_timestamp(iso_z) == int(datetime.fromisoformat("2020-01-01T00:00:00+00:00").timestamp())
    with pytest.raises(ValueError):
        client._to_timestamp("bad-date")
    with pytest.raises(TypeError):
        client._to_timestamp(object())


def test_format_filter_values():
    client = make_client()
    assert client._format_filter_values(None) is None
    assert client._format_filter_values(123) == "123"
    assert client._format_filter_values(["1", 2]) == ["1", "2"]


def test_extract_collection():
    client = make_client()
    response = {"_embedded": {"items": [{"id": 1}]}}
    assert client._extract_collection(response, ("_embedded", "items")) == [{"id": 1}]
    assert client._extract_collection(response, ("_embedded", "missing")) == []
    assert client._extract_collection({"_embedded": {"items": {"id": 1}}}, ("_embedded", "items")) == []


def test_iterate_paginated_links_next():
    responses = [
        {"_embedded": {"items": [{"id": 1}]}, "_links": {"next": {"href": "next"}}},
        {"_embedded": {"items": [{"id": 2}]}, "_links": {}},
    ]
    client = PaginationClient(responses)
    items = list(client._iterate_paginated("/api/v4/items", data_path=("_embedded", "items")))
    assert [item["id"] for item in items] == [1, 2]
    assert client.calls == 2


def test_iterate_paginated_max_pages():
    responses = [
        {"_embedded": {"items": [{"id": 1}]}, "_page_count": 3},
        {"_embedded": {"items": [{"id": 2}]}, "_page_count": 3},
    ]
    client = PaginationClient(responses)
    items = list(client._iterate_paginated("/api/v4/items", data_path=("_embedded", "items"), max_pages=1))
    assert [item["id"] for item in items] == [1]
    assert client.calls == 1
