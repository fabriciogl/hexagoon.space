#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

import os

import jwt
from starlette.requests import Request

from API.V1.Excecoes.MongoExceptions import MongoFindException2
from API.V1.Excecoes.TokenExceptions import TokenExpiredException, TokenInvalidException
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository

#TODO construir uma funcao a ser iniciada com o app que varerá as classes endpoints
# e criará uma lista de classes/metodos e autorizacoes. As autorizacoes serão declaradas nos
# doc de cada endpoint.
async def check_roles_authorized(request: Request):
    if request.headers.get('Authorization') is None:
        raise TokenInvalidException()
    try:
        payload = jwt.decode(
            jwt=request.headers.get('Authorization').replace('Bearer ', ''),
            key=os.getenv('HASH_1'),
            algorithms=[os.getenv('HASH_2')]
        )
        _id: str = payload.get('sub')
        ip: str = payload.get('ip')

    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()

    # Verifica se o IP do request é o mesmo do Token
    if ip is not request.client.host:
        raise TokenInvalidException()

    # busca o usuário no banco de dados
    try:
        user = UsuarioRepository.find_one(_id=_id)
    except Exception as e:
        raise MongoFindException2()

    if user is None:
        raise TokenInvalidException()

    #TODO checar se as roles do usuario permitem acessar o endpoint

