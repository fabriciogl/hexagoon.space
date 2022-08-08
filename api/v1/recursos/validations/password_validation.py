#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi.params import Depends
from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette.requests import Request

from api.v1.recursos.basic_exceptions.login_exceptions import LoginException
from api.v1.recursos.response_handler import ResponseHandler
from api.v1.usuario.model.usuario_model import UsuarioTokenIn, Usuario
from banco_dados.mongodb.configuracao import MongoConection
from banco_dados.mongodb.configuracao.MongoConection import Operacoes


async def check_password(
        request: Request,
        usuario_model: UsuarioTokenIn,
        operacao: Operacoes = Depends(MongoConection.Operacoes)
) -> ResponseHandler:

    if data := operacao.find(filter={'email':usuario_model.email}, collection='usuarios'):
        usuario_data: Usuario = Usuario(**data)
    else:
        raise LoginException(ordem=1, usuario=usuario_model, request=request)

    if not usuario_data.ativo:
        raise LoginException(ordem=2, usuario=usuario_model, request=request)

    if bcrypt.verify(usuario_model.senha, usuario_data.senha) is False:
        raise LoginException(ordem=3, usuario=usuario_model, request=request)

    # cria o handler da requisicao
    handler = ResponseHandler()
    handler.usuario = usuario_data
    handler.operacao = operacao
    handler.request = request

    return handler
