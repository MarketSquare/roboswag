import pytest

from ...utils import TEST_DATA_DIR, run_cli


def test_openapi_v2_missing_optionals():
    spec = TEST_DATA_DIR / "missing_optionals_v2" / "spec.json"
    run_cli(f"generate -s {spec}".split())


def test_openapi_v2_missing_one_tag():
    spec = TEST_DATA_DIR / "missing_one_tag_v2" / "spec.json"
    run_cli(f"generate -s {spec}".split())


def test_yaml_v3():
    spec = TEST_DATA_DIR / "yaml_v3" / "spec.yaml"
    run_cli(f"generate -s {spec}".split())


@pytest.mark.parametrize("dir_exists", [False, True])
@pytest.mark.parametrize(
    "output_option, output_directory", [("-o", "output_directory"), ("--output-dir", "nested/subdirs/output_dir")]
)
def test_generate_to_output_dir(tmp_path, dir_exists, output_directory, output_option):
    spec = TEST_DATA_DIR / "yaml_v3" / "spec.yaml"
    output_dir = tmp_path / output_directory
    if dir_exists:
        output_dir.mkdir(parents=True)
    run_cli(f"generate -s {spec} {output_option} {output_dir}".split())


def test_generate_to_output_dir_is_file(tmp_path):
    spec = TEST_DATA_DIR / "yaml_v3" / "spec.yaml"
    output_dir = tmp_path / "file.ext"
    with open(output_dir, "w"):
        pass
    run_cli(f"generate -s {spec} -o {output_dir}".split(), exit_code=2)
