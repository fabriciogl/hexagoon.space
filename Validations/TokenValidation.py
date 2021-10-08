#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

import os
from typing import List

import jwt
from fastapi.params import Depends
from fastapi.security import SecurityScopes
from starlette.requests import Request

from API.V1.Endpoints.Handler.ResponseHandler import ResponseHandler
from API.V1.Excecoes.MongoExceptions import MongoFindException2
from API.V1.Excecoes.TokenExceptions import TokenExpiredException, TokenInvalidException, TokenRoleException
from Model.Usuario import Usuario
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository


async def valida_token(request: Request):
    if request.headers.get('Authorization') is None:
        raise TokenInvalidException()
    try:
        payload = jwt.decode(
            jwt=request.headers.get('Authorization').replace('Bearer ', ''),
            key=os.getenv('HASH_1'),
            algorithms=[os.getenv('HASH_2')]
        )
        _id: str = payload.get('sub')
        ip: str = payload.get('on')

    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
        raise TokenExpiredException()

    # Verifica se o IP do request é o mesmo do Token
    if ip != request.client.host:
        raise TokenInvalidException()

    # busca o usuário no banco de dados
    try:
        usuario: Usuario = UsuarioRepository.find_one(_id=_id)
        roles: List[str] = usuario.roles
    except Exception as e:
        raise MongoFindException2()

    if usuario is None:
        raise TokenInvalidException()

    return usuario


async def valida_role(
        security_scopes: SecurityScopes,
        usuario: Usuario = Depends(valida_token)
) -> ResponseHandler:

    for scope in security_scopes.scopes:
        if scope not in usuario.roles:
            raise TokenRoleException()

    handler = ResponseHandler()
    handler.usuario = usuario

    return handler
