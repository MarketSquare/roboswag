import contextlib
import os
from pathlib import Path
from typing import List

from click.testing import CliRunner

from roboswag.cli import cli

TEST_DATA_DIR = Path(__file__).parent / "test_data"


def run_cli(args: List[str] = None, exit_code: int = 0, temp_work_dir: bool = True):
    runner = CliRunner()
    arguments = args if args is not None else []
    if temp_work_dir:
        with runner.isolated_filesystem():
            result = runner.invoke(cli, arguments)
    else:
        result = runner.invoke(cli, arguments)
    if result.exit_code != exit_code:
        print(result.output)
        raise AssertionError(f"robotidy exit code: {result.exit_code} does not match expected: {exit_code}")
    return result


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit"""
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
