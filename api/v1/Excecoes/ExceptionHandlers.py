#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from starlette.requests import Request
from starlette.responses import JSONResponse

from api.V1.Excecoes.GenericValidationExceptions import InvalidIdException
from api.V1.Excecoes.MongoExceptions import MongoFindException2


def invalid_id(request: Request, exc: InvalidIdException):
    try:
        print(
            f'IP {request.client.host} - Port {request.client.port} - {request.headers.values()} - {request.path_params}')
    except json.decoder.JSONDecodeError as e:
        # Request had invalid or no body
        print(e)

    return JSONResponse({"detail": exc.detail}, status_code=404)


def not_found(request: Request,
              exc: MongoFindException2):
    try:
        print(
            f'IP {request.client.host} - Port {request.client.port} - {request.headers.values()} - {request.path_params}')
    except json.decoder.JSONDecodeError as e:
    # Request had invalid or no body
        print(e)

    return JSONResponse({"detail": exc.detail}, status_code=404)
