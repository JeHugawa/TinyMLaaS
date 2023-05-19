from enum import Enum
from pydantic import BaseModel


from fastapi import FastAPI


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class ModelName(str, Enum):
    tumenet = "tumenet"
    some = "somenet"
    ase = "asenet"


app = FastAPI()

backend_url = "http://127.0.0.1:8000"
@app.get("/")
async def routed():
    return {"Hello": "world"}

@app.post("/item/")
async def create_item(item: Item):
    return Item


@app.get("/models/{model_name}")
async def read_model(model_name: ModelName):
    if model_name is ModelName.tumenet:
        return {"model_name": model_name, "message": "Lets go"}

    if model_name.value == "somenet":
        return {"model_name": model_name, "message": "Some"}

    return {"model_name": model_name, "message": "asettaja"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None, long: bool = True):
    item = {"item_id": item_id}
    if q:
        return {"item_id": item_id, "q": q}
    if long:
        item.update(
            {"item_id": 34567890987654321}
        )
    return item