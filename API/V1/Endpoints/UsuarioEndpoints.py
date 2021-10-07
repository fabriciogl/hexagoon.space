import os
from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends
from starlette.requests import Request

from API.V1.Acoes.UsuarioAcoes import UsuarioAcoes
from API.V1.Endpoints.Handler.ResponseHandler import ResponseHandler
from Model.Token import Token
from Model.Usuario import Usuario
from API.V1.Regras.UsuarioRegras import UsuarioRegras
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository
from Validations.PasswordValidation import check_password
from Validations.PydanticCustomValidations import constr
from Validations.TokenValidation import get_token_header

router = APIRouter(
    prefix="/usuario",
    tags=['Usuários']
)


class UsuarioEndpoints:

    #TODO - O JWT e as roles (vindas do BD) vão ser validados na entrada da requisição,
    # por meio de Depends no APIRouter.

    @staticmethod
    @router.get("/{id}",
                dependencies=[Depends(get_token_header)]
                )
    async def find(id: constr(regex=r'^[a-f\d]{16}U$')):
        handler = ResponseHandler()
        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=id, handler=handler, acao='find')

        return handler.resultado_json

    # O response_model_exclude funciona somente para a resposta do request, mas não para a documentação
    @staticmethod
    @router.post("",
                 response_model=Usuario,
                 response_model_exclude={"senha"},
                 status_code=201)
    async def create(usuario: Usuario):

        handler = ResponseHandler()
        # valida as regras necessárias no model

        # realiza as acoes necessárias no model
        UsuarioAcoes(model=usuario, handler=handler, acao='create')

        return handler.resultado_json

    @staticmethod
    @router.put("/{usuario_id}",
                response_model=Usuario,
                response_model_include={"senha"},
                status_code=202,
                dependencies=[Depends(get_token_header)]
                )
    async def update(usuario: Usuario, usuario_id: constr(regex=r'^[a-f\d]{16}U$')):

        handler = ResponseHandler()

        # regras aplicáveis ao model
        UsuarioRegras(_id=usuario_id, model=usuario, handler=handler, acao='update')

        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=usuario_id, model=usuario, handler=handler, acao='update')

        return handler.resultado_json

    @staticmethod
    @router.post("/login",
                 response_model=Token,
                 status_code=201)
    async def create_token(request: Request, usuario: Usuario = Depends(check_password)):

        ip = request.client.host
        expire = datetime.utcnow() + timedelta(minutes=15)
        data = {"sub": usuario.id, "on": ip, "exp": expire}
        encoded_jwt = jwt.encode(payload=data, key=os.getenv('HASH_1'), algorithm=os.getenv('HASH_2'))

        return {"token": encoded_jwt, "exp": expire}
