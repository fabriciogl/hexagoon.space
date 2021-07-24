# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os
# direitos reservados.
from enum import Enum
from functools import lru_cache

import uvicorn
from fastapi import FastAPI
from Repositorio.Mongo.MongoSetup import MongoSetup

from Repositorio.Mongo.QuestaoRepository import QuestaoRepository


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()
app.add_event_handler("startup", MongoSetup.connect_db)
app.add_event_handler("shutdown", MongoSetup.close_db)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/questao/{questao_id}")
async def read_item(questao_id: str):
    resultado = await QuestaoRepository.procura_um(_id=questao_id)
    return {"item_id": resultado}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
