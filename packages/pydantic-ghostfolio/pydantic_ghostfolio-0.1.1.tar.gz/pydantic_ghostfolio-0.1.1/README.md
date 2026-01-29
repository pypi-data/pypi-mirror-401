# Pydantic Ghostfolio

Pydantic models for [Ghostfolio](https://github.com/ghostfolio/ghostfolio) export/import format.
This package allows you to parse, validate, and type-check Ghostfolio data in Python.

## Installation

```bash
pip install pydantic-ghostfolio
```

## Usage

See [examples/basic_usage.py](examples/basic_usage.py) for a complete example.

```python
from pydantic_ghostfolio import GhostfolioExport
import json

with open("ghostfolio-export.json", "r") as f:
    data = json.load(f)

export = GhostfolioExport(**data)
print(f"Export version: {export.meta.version}")
```

## References

The models are based on the Ghostfolio source code interfaces:

- **Export Response Schema**: [export-response.interface.ts](https://github.com/ghostfolio/ghostfolio/blob/main/libs/common/src/lib/interfaces/responses/export-response.interface.ts)
- **Activity Interface**: [activities.interface.ts](https://github.com/ghostfolio/ghostfolio/blob/main/libs/common/src/lib/interfaces/activities.interface.ts)
- **Prisma Schema**: [schema.prisma](https://github.com/ghostfolio/ghostfolio/blob/main/prisma/schema.prisma)

## Development

Run tests:
```bash
uv run pytest
```
