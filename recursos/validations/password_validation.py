#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi.params import Depends
from passlib.hash import bcrypt
from starlette.requests import Request

from recursos.basic_exceptions.login_exceptions import LoginException
from recursos.response_handler import ResponseHandler
from api.v1.usuario.model.usuario_model import UsuarioTokenIn, Usuario, UsuarioOut
from banco_dados.mongodb.configuracao import MongoConection
from banco_dados.mongodb.configuracao.MongoConection import Operacoes


async def check_password(
        request: Request,
        usuario_model: UsuarioTokenIn,
        operacao: Operacoes = Depends(MongoConection.Operacoes)
) -> ResponseHandler:

    if data := operacao.find_one(where={'email':usuario_model.email}, collection='usuarios'):
        usuario_validation: Usuario = Usuario(**data)
        usuario_handler: UsuarioOut = UsuarioOut(**data)
    else:
        raise LoginException(ordem=1, usuario=usuario_model, request=request)

    if not usuario_validation.ativo:
        raise LoginException(ordem=2, usuario=usuario_model, request=request)

    if bcrypt.verify(usuario_model.senha, usuario_validation.senha) is False:
        raise LoginException(ordem=3, usuario=usuario_model, request=request)

    # cria o handler da requisicao
    handler = ResponseHandler(operacao=operacao)
    handler.usuario = usuario_handler
    handler.request = request

    return handler
