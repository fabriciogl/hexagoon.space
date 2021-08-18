#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from starlette.requests import Request
from starlette.responses import JSONResponse

from Excecoes.GenericValidationExceptions import InvalidIdException
from Excecoes.MongoExceptions import MongoFindException2


def invalid_id(request: Request,
      exc: InvalidIdException):
    try:
        print(
            f'IP {request.client.host} - Port {request.client.port} - {request.headers.values()} - {request.path_params}')
    except json.decoder.JSONDecodeError:
        # Request had invalid or no body
        pass

    return JSONResponse({"detail": exc.detail}, status_code=404)


def not_found(request: Request,
              exc: MongoFindException2):
    try:
        print(
            f'IP {request.client.host} - Port {request.client.port} - {request.headers.values()} - {request.path_params}')
    except json.decoder.JSONDecodeError:
        # Request had invalid or no body
        pass

    return JSONResponse({"detail": exc.detail}, status_code=404)
