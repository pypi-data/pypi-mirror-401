import os
import re

import toml


def get_min_python():
    try:
        with open("pyproject.toml") as f:
            data = toml.load(f)
        requires = data.get("project", {}).get("requires-python", "")
        if not requires:
            return 10  # Default to 3.10
        match = re.search(r">=?\s*3\.(\d+)", requires)
        if match:
            return int(match.group(1))
        return 10
    except Exception:
        return 10


def generate_ci():
    min_ver = get_min_python()
    max_ver = 15  # Update this as new versions come out

    versions = [f"3.{v}" for v in range(min_ver, max_ver + 1)]
    version_list = "\n          - ".join([f'"{v}"' for v in versions])

    content = f"""name: "CI"

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version:
          - {version_list}
      fail-fast: false
    steps:
      - name: Checkout
        uses: actions/checkout@v5

      - name: Install uv
        uses: astral-sh/setup-uv@v7

      - name: Set up Python ${{{{ matrix.python-version }}}}
        run: uv python install ${{{{ matrix.python-version }}}}
        continue-on-error: true

      - name: Install dependencies
        run: uv sync --all-extras --dev

      - name: Run tests
        run: uv run pytest
"""

    os.makedirs(".github/workflows", exist_ok=True)
    with open(".github/workflows/ci.yml", "w") as f:
        f.write(content)
    print(f"Generated .github/workflows/ci.yml for Python 3.{min_ver} to 3.{max_ver}")


if __name__ == "__main__":
    generate_ci()
