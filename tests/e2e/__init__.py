import json
from pathlib import Path

from fastapi.openapi.utils import get_openapi

from ..utils import run_cli


def remove_path(path: Path):
    if path.is_file():
        path.unlink()
        return
    if not path.is_dir():
        return
    for p in path.iterdir():
        remove_path(p)
    path.rmdir()


def prepare_test_result_dir(test_name: str):
    spec_path = Path(__file__).parent / "results" / test_name
    remove_path(spec_path)
    spec_path.mkdir(parents=True)
    return spec_path


def generate_openapi(app, spec_path: Path):
    spec = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )
    with open(spec_path, "w") as fp:
        json.dump(spec, fp)


def run_e2e(app, test_name: str):
    results_dir = prepare_test_result_dir(test_name)
    spec_path = results_dir / "openapi.json"
    generate_openapi(app, spec_path)
    run_cli(f"generate -s {spec_path} -o {results_dir}".split())
