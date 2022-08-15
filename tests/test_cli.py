import pytest

from .utils import TEST_DATA_DIR, run_cli


class TestGenerate:
    def test_generate(self):
        """Asserts that roboswag does not fail when generating from spec file."""
        spec = TEST_DATA_DIR / "petstore_v2" / "petstore.json"
        run_cli(f"generate -s {spec}".split())


@pytest.mark.parametrize("help_cmd", ["-h", "--help"])
@pytest.mark.parametrize("command", [None, "generate"])
def test_help(command, help_cmd):
    if command:
        args = [command, help_cmd]
    else:
        args = [help_cmd]
    result = run_cli(args)
    assert "Usage: " in result.output


def test_version():
    result = run_cli(["--version"])
    assert "roboswag, version" in result.output
