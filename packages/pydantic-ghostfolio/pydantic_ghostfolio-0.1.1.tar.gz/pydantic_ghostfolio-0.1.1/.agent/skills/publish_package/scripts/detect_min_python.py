import re
import sys

import toml


def get_min_python():
    try:
        with open("pyproject.toml") as f:
            data = toml.load(f)

        requires = data.get("project", {}).get("requires-python", "")
        if not requires:
            return None

        # Look for >=3.X or >3.X
        match = re.search(r">=?\s*3\.(\d+)", requires)
        if match:
            return int(match.group(1))
        return None
    except FileNotFoundError:
        return None


if __name__ == "__main__":
    min_ver = get_min_python()
    if min_ver:
        print(min_ver)
    else:
        sys.exit(1)
