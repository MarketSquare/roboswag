from pathlib import Path
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from .. import run_e2e

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


def test_e2e():
    test_name = Path(__file__).parent.name
    run_e2e(app, test_name)
