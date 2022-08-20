import json
from pathlib import Path
from typing import Union

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from ...utils import run_cli

app = FastAPI(title="RoboswagTestAPI")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def generate_openapi(spec_path: Path):
    with open(spec_path, "w") as fp:
        json.dump(
            get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
                tags=app.openapi_tags,
            ),
            fp,
        )


def test_gen_spec_and_library():
    spec_path = Path(__file__).parent / "tmp_openapi.json"
    generate_openapi(spec_path)
    run_cli(f"generate -s {spec_path}".split())
