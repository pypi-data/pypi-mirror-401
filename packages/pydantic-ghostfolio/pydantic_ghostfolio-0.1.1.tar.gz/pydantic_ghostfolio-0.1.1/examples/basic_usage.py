import argparse
import json
from pathlib import Path

from pydantic_ghostfolio.models import GhostfolioExport


def main():
    parser = argparse.ArgumentParser(description="Parse Ghostfolio export.")
    parser.add_argument("file_path", nargs="?", help="Path to the export file")
    args = parser.parse_args()

    # Path to your export file
    if args.file_path:
        data_path = Path(args.file_path)
    else:
        # Here we use the test data we created
        data_path = Path(__file__).parent.parent / "tests" / "data" / "export_example.json"

    if not data_path.exists():
        print(f"File not found: {data_path}")
        return

    print(f"Reading export from: {data_path}")
    with open(data_path) as f:
        data = json.load(f)

    # Parse the data into the Pydantic model
    try:
        export = GhostfolioExport(**data)
        print(f"Successfully parsed export version {export.meta.version}")
        print(f"Found {len(export.accounts)} accounts and {len(export.activities)} activities.")

        for activity in export.activities:
            print(
                f"- {activity.type} {activity.quantity} {activity.symbol} @ "
                f"{activity.unitPrice} {activity.currency}"
            )

    except Exception as e:
        print(f"Error parsing export: {e}")


if __name__ == "__main__":
    main()
