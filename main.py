# Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os
# direitos reservados.

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from passlib.hash import bcrypt
from starlette.staticfiles import StaticFiles

from api.v1.usuario.endpoint import usuario_endpoints
from api.v1.autenticacao.endpoint import autenticacao_endpoints
from api.v1.role.endpoint import role_endpoints
# from api.V1.Excecoes.ExceptionHandlers import invalid_id, not_found
# from api.V1.Excecoes.GenericValidationExceptions import InvalidIdException
# from api.V1.Excecoes.MongoExceptions import MongoFindException2
from api.v1.recursos.response_handler import ResponseHandler
from api.v1.usuario.model.usuario_model import Usuario
from banco_dados.mongodb.configuracao.MongoConection import Operacoes
from banco_dados.mongodb.configuracao.MongoSetupSincrono import MongoSetupSincrono
from banco_dados.mongodb.load_data import load_data

app = FastAPI()

app.mount("/estaticos", StaticFiles(directory="estaticos"), name="estaticos")

# app.include_router(VerticeEndpoints.router)
app.include_router(usuario_endpoints.router)
app.include_router(autenticacao_endpoints.router)
app.include_router(role_endpoints.router)
# app.include_router(TesteEndpoints.router)

# app.add_event_handler("startup", MongoSetupAssincrono.connect_db)
app.add_event_handler("startup", MongoSetupSincrono.connect_client)
app.add_event_handler("startup", load_data)


# app.add_event_handler("shutdown", MongoSetupAssincrono.close_db)


# app.add_exception_handler(InvalidIdException, invalid_id)
# app.add_exception_handler(MongoFindException2, not_found)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Hexagoon (based on FastApi)",
        version="0.0.1",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
async def root():
    handler = ResponseHandler(Operacoes())
    senha = bcrypt.using(rounds=7).hash('cookies')
    documento = handler.operacao.insert(
        Usuario(
            nome="Fabricio",
            email="fabricio@hexagoon.space",
            senha=senha,
            ativo=True,
            roles=[
                {'_id': 'root'},
                {'_id': 'admin'}
            ]
        )
    )
    documento['_id'] = 'X1'
    return documento


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
