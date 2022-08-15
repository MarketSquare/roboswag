from ...utils import TEST_DATA_DIR, run_cli


def test_openapi_v2_missing_optionals():
    spec = TEST_DATA_DIR / "missing_optionals_v2" / "spec.json"
    run_cli(f"generate -s {spec}".split())
