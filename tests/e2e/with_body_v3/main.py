import json
from pathlib import Path
from typing import Union

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

from ...utils import run_cli

app = FastAPI(title="RoboswagTestAPI")


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.get("/", tags=["root"])
def read_root():
    return {"Hello": "World"}


@app.post("/items/")
async def create_item(item: Item):
    return item


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
