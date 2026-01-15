import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from amochka.etl import export_contacts_to_ndjson, write_ndjson


def test_write_ndjson_transform_and_on_record(tmp_path):
    records = [{"id": 1, "updated_at": 123}]
    seen = []

    def transform(record):
        return {"id": record["id"], "flag": True}

    def on_record(record):
        seen.append(record["id"])

    output_path = tmp_path / "out.ndjson"
    count = write_ndjson(
        records,
        output_path,
        entity="lead",
        account_id=42,
        transform=transform,
        on_record=on_record,
    )
    assert count == 1
    payload = json.loads(output_path.read_text().strip())
    assert payload["entity"] == "lead"
    assert payload["account_id"] == 42
    assert payload["payload"]["flag"] is True
    assert seen == [1]


def test_export_contacts_handles_empty_response(tmp_path):
    class DummyClient:
        def _make_request(self, *args, **kwargs):
            return None

        def get_contact_by_id(self, *_args, **_kwargs):
            raise Exception("not found")

        def iter_contacts(self, *args, **kwargs):
            return iter(())

    client = DummyClient()
    output_path = tmp_path / "contacts.ndjson"
    count = export_contacts_to_ndjson(
        client,
        output_path,
        account_id=1,
        contact_ids=[123],
    )
    assert count == 0
    assert output_path.read_text() == ""
