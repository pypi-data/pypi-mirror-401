---
name: Publish Package
description: Complete workflow to prepare a Python package for PyPI publication (Metadata, License, CI/CD, Tests).
---

# Publish Package Skill

This skill guides you through preparing a Python package for publication on PyPI.
It includes steps for metadata configuration, license creation, packaging setup, code quality enforcement, and CI/CD automation.

## User Configuration
- **Name**: Roman Medvedev
- **Email**: pypi@romavm.dev
- **GitHub**: romamo
- **License**: MIT

## Instructions

### 1. Update `pyproject.toml` Metadata
Ensure `pyproject.toml` contains the correct metadata.
- **Name**: Package name (kebab-case).
- **Version**: Start with `0.1.0`.
- **Authors**: `[{ name = "Roman Medvedev", email = "pypi@romavm.dev" }]`
- **License**: `license = "MIT"`
- **URLs**:
  ```toml
  [project.urls]
  Homepage = "https://github.com/romamo/<package-name>"
  Repository = "https://github.com/romamo/<package-name>"
  Issues = "https://github.com/romamo/<package-name>/issues"
  ```
- **Classifiers**: Add relevant classifiers.

### 2. Apply Skill (Automated)
Run the automation script to copy standard files (`LICENSE`, `MANIFEST.in`), create `py.typed`, set up `tests/smoke_test.py`, and generate GitHub Actions workflows.

```bash
python .agent/skills/publish_package/scripts/apply_skill.py
```

### 3. Manual Configuration
- **Edit `tests/smoke_test.py`**: Import your actual package.
- **Update `pyproject.toml`**:
    - Add the contents of `.agent/skills/publish_package/resources/pyproject_snippet.toml` to your `pyproject.toml`.
    - Ensure `name`, `version`, `authors`, `description`, `classifiers` are set.


### 4. Code Quality
Ensure `ruff` is configured in `pyproject.toml`:

```toml
[dependency-groups]
dev = ["ruff>=0.9.2", "pytest"]

[tool.ruff]
line-length = 100
target-version = "py310" # Update if min version matches
```

Run checks:
```bash
uv run ruff check --fix .
uv run ruff format .
```

### 5. Final Verification
1. `uv build` -> Check `dist/` folder.
2. `uv run pytest` -> Ensure tests pass.
3. Commit and tag `v0.1.0` to trigger publish.
