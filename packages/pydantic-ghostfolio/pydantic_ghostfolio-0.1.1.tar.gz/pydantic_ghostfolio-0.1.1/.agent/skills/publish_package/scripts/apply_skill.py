import os
import shutil
import sys
from pathlib import Path

import toml

# Paths relative to the script location
SCRIPT_DIR = Path(__file__).parent
RESOURCES_DIR = SCRIPT_DIR.parent / "resources"
PROJECT_ROOT = Path(os.getcwd())


def main():
    print(f"Applying Publish Package Skill to: {PROJECT_ROOT}")

    # 1. Copy LICENSE
    print("-> Creating LICENSE...")
    shutil.copy(RESOURCES_DIR / "LICENSE", PROJECT_ROOT / "LICENSE")

    # 2. Copy MANIFEST.in
    print("-> Creating MANIFEST.in...")
    shutil.copy(RESOURCES_DIR / "MANIFEST.in", PROJECT_ROOT / "MANIFEST.in")

    # 3. Create py.typed
    # Try to find the source directory (simple heuristic: dir with same name as 
    # project name with underscores)
    try:
        pyproject_path = PROJECT_ROOT / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path) as f:
                data = toml.load(f)
                project_name = data.get("project", {}).get("name", "").replace("-", "_")
                if project_name:
                    package_dir = PROJECT_ROOT / project_name
                    if package_dir.exists() and package_dir.is_dir():
                        print(f"-> Creating {package_dir}/py.typed...")
                        (package_dir / "py.typed").touch()
                    else:
                        print(
                            f"Warning: Could not find package directory '{project_name}' "
                            "to create py.typed"
                        )
    except Exception as e:
        print(f"Warning: Failed to detect package name for py.typed: {e}")

    # 4. Create Tests
    print("-> Setting up tests...")
    tests_dir = PROJECT_ROOT / "tests"
    tests_dir.mkdir(exist_ok=True)
    if not (tests_dir / "smoke_test.py").exists():
        shutil.copy(RESOURCES_DIR / "smoke_test.py", tests_dir / "smoke_test.py")
    else:
        print("   Skipping smoke_test.py (already exists)")

    # 5. GitHub Workflows
    print("-> Setting up GitHub Workflows...")
    workflows_dir = PROJECT_ROOT / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    # Publish Workflow
    shutil.copy(RESOURCES_DIR / "publish.yml", workflows_dir / "publish.yml")

    # CI Workflow (Generate)
    print("-> Generating CI Workflow...")
    # Import generate_ci dynamically or run it as a subprocess
    # For simplicity, we'll assume the script is in the same directory
    sys.path.append(str(SCRIPT_DIR))
    try:
        import generate_ci

        generate_ci.generate_ci()
    except ImportError:
        print("Error: Could not import generate_ci script.")

    print("\nSkill Applied Successfully!")
    print("Next Steps:")
    print("1. Edit 'pyproject.toml' with metadata.")
    print(
        "2. Copy config from '.agent/skills/publish_package/resources/"
        "pyproject_snippet.toml' to 'pyproject.toml'."
    )
    print("3. Edit 'tests/smoke_test.py' to import your actual package.")


if __name__ == "__main__":
    main()
