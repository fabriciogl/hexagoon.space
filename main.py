# Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os
# direitos reservados.

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from API.V1.Endpoints import QuestaoEndpoints, TesteEndpoints, UsuarioEndpoints
from API.V1.Excecoes.ExceptionHandlers import invalid_id, not_found
from API.V1.Excecoes.GenericValidationExceptions import InvalidIdException
from API.V1.Excecoes.MongoExceptions import MongoFindException2
from Repositorio.Mongo.Configuracao.MongoSetupAssincrono import MongoSetupAssincrono
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono

app = FastAPI()

app.mount("/Estaticos", StaticFiles(directory="Estaticos"), name="Estaticos")

app.include_router(QuestaoEndpoints.router)
app.include_router(UsuarioEndpoints.router)
app.include_router(TesteEndpoints.router)

app.add_event_handler("startup", MongoSetupAssincrono.connect_db)
app.add_event_handler("startup", MongoSetupSincrono.connect_db)
app.add_event_handler("shutdown", MongoSetupAssincrono.close_db)


app.add_exception_handler(InvalidIdException, invalid_id)
app.add_exception_handler(MongoFindException2, not_found)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
