# Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os
# direitos reservados.

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from banco_dados.sql_alchemy.configuracao.oracle.data_oracle import criar_tabelas
from config import settings
from recursos.basic_exceptions.generic_validation_exceptions import InvalidIdException
from recursos.basic_exceptions.handler_exception import invalid_id
from recursos.routers_build import routers_build

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=False,  # se vai aceitar cookies como credenciais
    allow_methods=["*"],  # métodos que o request pode apresentar para o backend
    allow_headers=["*"],  # atributos do headers que o request pode apresentar para o backend
    expose_headers=["Authorization"]  # atributos do headers que o browser pode acessar do response
)

app.mount("/estaticos", StaticFiles(directory="estaticos"), name="estaticos")

# metodo para importar todas as rotas declaradas na pasta api
routers_build('v1', app)

if settings.current_env in ['production', 'development']:
    app.add_event_handler("startup", criar_tabelas)
# app.add_event_handler("startup", iniciar_gcp_logger)

app.add_exception_handler(InvalidIdException, invalid_id)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Hexagoon (based on FastApi)",
        version="0.0.1",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
