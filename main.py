# Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os
# direitos reservados.

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.staticfiles import StaticFiles

# from api.V1.Excecoes.ExceptionHandlers import invalid_id, not_found
# from api.V1.Excecoes.GenericValidationExceptions import InvalidIdException
# from api.V1.Excecoes.MongoExceptions import MongoFindException2
from banco_dados.mongodb.configuracao.MongoSetupSincrono import MongoSetupSincrono
from banco_dados.mongodb.load_data import load_data
from recursos.routers_build import routers_build

app = FastAPI()

app.mount("/estaticos", StaticFiles(directory="estaticos"), name="estaticos")

routers_build('v1', app)

app.add_event_handler("startup", MongoSetupSincrono.connect_client)
app.add_event_handler("startup", load_data)


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
    return {'return': 'Hello World'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
