from pathlib import Path
from typing import Union

from fastapi import FastAPI

from .. import run_e2e

app = FastAPI(title="RoboswagTestAPI")


@app.get("/", tags=["root"], operation_id="root")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}", tags=["items"], operation_id="read_item")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def test_e2e():
    test_name = Path(__file__).parent.name
    run_e2e(app, test_name)
