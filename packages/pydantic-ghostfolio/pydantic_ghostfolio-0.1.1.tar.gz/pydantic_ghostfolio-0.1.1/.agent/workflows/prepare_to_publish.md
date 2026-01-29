---
description: Prepare a Python package for PyPI publication using uv and GitHub Actions.
---

1. **Update `pyproject.toml` Metadata**
   - Ensure `name`, `version` (start with 0.1.0), `description` are set.
   - Set `authors` correctly (e.g., `{ name = "Your Name", email = "email@example.com" }`).
   - Set `license = "MIT"` (or your preferred license).
   - Update `classifiers` to include:
     - Development Status
     - Intended Audience
     - License
     - Programming Language :: Python :: 3.10 - 3.14
   - Add `[project.urls]` (Homepage, Repository, Issues).
   - Ensure `dependencies` are correct.

2. **Create `LICENSE` File**
   - Create a `LICENSE` file in the root directory (e.g., MIT License text).

3. **Packaging Configuration**
   - Create `MANIFEST.in` with content:
     ```
     global-exclude *.py[cod]
     global-include *.typed
     ```
   - Create an empty `py.typed` file in the package source directory (e.g., `src/your_package/py.typed` or `your_package/py.typed`) to mark it as PEP 561 compatible.

4. **Refine Exports**
   - Update `__init__.py` to explicit export the public API using `from .module import Class` and defining `__all__`.

5. **Code Quality (Ruff)**
   - Add `ruff` to `dev` dependencies in `pyproject.toml`.
   - Add `[tool.ruff]` configuration (e.g., `line-length = 100`, `target-version = "py310"`).
   - Run `uv run ruff check --fix .`
   - Run `uv run ruff format .`

6. **Create Smoke Test**
   - Create `tests/smoke_test.py` to verify the package can be imported and key components are available.
     ```python
     from your_package import YourMainClass
     def test_smoke():
         assert YourMainClass
     if __name__ == "__main__":
         test_smoke()
     ```

7. **Setup GitHub Actions**
   - **CI Workflow**: Create `.github/workflows/ci.yml` that runs tests on push/PR for Python versions 3.10 through 3.15 (allow failure/continue-on-error for experimental versions like 3.14/3.15).
   - **Publish Workflow**: Create `.github/workflows/publish.yml` that runs on tags (`v*`).
     - Use `id-token: write` for Trusted Publishing.
     - Steps: Checkout, Install uv, Install Python 3.14 (or latest), Build, Smoke Test (wheel & sdist), Publish (`uv publish`).

8. **Final Verification**
   - Run `uv build` to ensure artifacts are created successfully.
   - Run `uv run pytest` to ensure all tests pass.
   - Check `README.md` for correct installation instructions (`pip install your-package`) and usage examples.
