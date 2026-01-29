import json
from pathlib import Path
from uuid import UUID

from pydantic_ghostfolio.models import ActivityType, DataSource, GhostfolioExport


def test_parse_export_example():
    """Test parsing the anonymized export example."""
    data_path = Path(__file__).parent / "data" / "export_example.json"
    with open(data_path) as f:
        data = json.load(f)

    export = GhostfolioExport(**data)

    assert export.meta.version == "2.0.0"
    assert len(export.accounts) == 1
    assert export.accounts[0].id == UUID("e0c4667d-9659-498c-9a4f-563d76326694")
    assert export.accounts[0].balance == 1000

    assert len(export.activities) == 1
    activity = export.activities[0]
    assert activity.type == ActivityType.BUY
    assert activity.symbol == "TEST"
    assert activity.quantity == 10
    assert activity.unitPrice == 50
    assert activity.dataSource == DataSource.MANUAL

    # Check string enum parsing
    assert activity.type == "BUY"


def test_round_trip():
    """Test that the model can be dumped back to JSON."""
    data_path = Path(__file__).parent / "data" / "export_example.json"
    with open(data_path) as f:
        data = json.load(f)

    export = GhostfolioExport(**data)
    dumped = export.model_dump(mode="json")

    # Simple check of structure
    assert dumped["meta"]["version"] == data["meta"]["version"]
    assert dumped["activities"][0]["symbol"] == data["activities"][0]["symbol"]
