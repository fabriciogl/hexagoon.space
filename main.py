# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os
# direitos reservados.
import json
import time
from enum import Enum

import uvicorn
from fastapi import FastAPI
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from Excecoes.ValidationExceptions import InvalidIdException
from Repositorio.Mongo.Configuracao.MongoSetupAssincrono import MongoSetupAssincrono
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono
from Entrypoints import QuestaoEntrypoints, UsuarioEntrypoints


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

app.include_router(QuestaoEntrypoints.router)
app.include_router(UsuarioEntrypoints.router)

app.add_event_handler("startup", MongoSetupAssincrono.connect_db)
app.add_event_handler("startup", MongoSetupSincrono.connect_db)
app.add_event_handler("shutdown", MongoSetupAssincrono.close_db)


@app.exception_handler(InvalidIdException)
def _(request: Request,
      exc: InvalidIdException):
    try:
        print(f'IP {request.client.host} - Port {request.client.port} - {request.headers.values()} - {request.path_params}')
    except json.decoder.JSONDecodeError:
        # Request had invalid or no body
        pass

    return JSONResponse({"detail": exc.detail}, status_code=404)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
