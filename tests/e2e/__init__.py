import json
import subprocess
from pathlib import Path

import uvicorn
from fastapi.openapi.utils import get_openapi

from ..utils import run_cli
from .api_server import Server


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
        json.dump(spec, fp, indent=4)


def get_api_server(app):
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="error")
    return Server(config=config)


def run_robot(source, output_dir):
    cmd = f"robot --outputdir {output_dir} {source}".split()
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise AssertionError("Robot tests failed.")


def run_e2e(app, test_name: str):
    results_dir = prepare_test_result_dir(test_name)
    spec_path = results_dir / "openapi.json"
    generate_openapi(app, spec_path)
    run_cli(f"generate -s {spec_path} -o {results_dir}".split())

    robot_test = Path(__file__).parent / test_name / "test.robot"
    if not robot_test.is_file():
        return
    server = get_api_server(app)
    with server.run_in_thread():
        run_robot(robot_test, results_dir)
