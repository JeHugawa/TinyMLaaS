from enum import Enum
from pydantic import BaseModel


from fastapi import FastAPI


class Model(BaseModel):
    name: str
    description: str


class ModelName(str, Enum):
    facerecognition = "Face Recognition"
    carrecognition = "Car Recognition"


models = {0: {"name": None, "description": None}}

app = FastAPI()

backend_url = "http://127.0.0.1:8000"


@app.post("/item/")
async def create_item(model: Model):
    models[1] = {"name": model.name, "description": model.description}
    return {"message": "Model added"}


@app.get("/models/")
async def read_model(model_name: ModelName | None = None,
                     model_id: int = 0):
    if model_name is ModelName.facerecognition:
        return {"model_name": model_name,
                "message": "Model for recognizing faces"}

    if model_name is ModelName.carrecognition:
        return {"model_name": model_name,
                "message": "Model for detecting cars"}

    return {"model": models[model_id]["name"],
            "description": models[model_id]["description"]}