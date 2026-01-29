from pydantic_ghostfolio import GhostfolioExport, __all__


def test_smoke():
    print("Smoke test starting...")
    print(f"Exported members: {__all__}")
    assert GhostfolioExport
    print("Smoke test passed: GhostfolioExport imported successfully.")


if __name__ == "__main__":
    test_smoke()
