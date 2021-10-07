#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from passlib.hash import bcrypt

from API.V1.Excecoes.LoginExceptions import LoginException
from API.V1.Excecoes.MongoExceptions import MongoFindException2
from API.V1.Excecoes.TokenExceptions import TokenInvalidException
from Model.Usuario import Usuario
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository


async def check_password(usuario_externo: Usuario) -> Usuario:

    # busca o usuário no banco de dados
    try:
        usuario_interno: Usuario = UsuarioRepository.find_one_by(('email', usuario_externo.email))
    except Exception as e:
        raise MongoFindException2()

    if usuario_interno is None:
        raise TokenInvalidException()

    if bcrypt.verify(usuario_externo.senha, usuario_interno.senha) is False:
        raise LoginException()

    return usuario_interno
