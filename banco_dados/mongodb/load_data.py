#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from bson import ObjectId
from passlib.hash import bcrypt

from api.v1.role.model.role_model import RoleIn, Role
from api.v1.usuario.model.usuario_model import Usuario
from banco_dados.mongodb.configuracao.MongoConection import Operacoes, Sessao
from config import settings


def load_data():

    operacao = Operacoes()
    usuario = Usuario(
        id=ObjectId(),
        nome=settings.root_user,
        email=settings.root_email,
        senha=bcrypt.using(rounds=7).hash(settings.root_pass),
        ativo=True,
        roles=[]
    )

    # cria usuário root
    role_root = Role(id=ObjectId(), sigla=settings.root_role, descricao='acesso com poder de superusuário')

    # cria demais roles
    role_admin = Role(id=ObjectId(), sigla='admin', descricao='acesso com poder de administração')
    role_user = Role(id=ObjectId(), sigla='user', descricao='acesso com poder de usuário')

    if not operacao.find(filter={'email': usuario.email}, collection='usuarios'):
        sessao = Sessao()
        with sessao.start_session(causal_consistency=True) as session:
            role_user = Role(**sessao.insert(session, role_user))
            role_admin.precedencias.append(role_user)
            role_admin = RoleIn(**sessao.insert(session, role_admin))
            role_root.precedencias.append(role_admin)
            role_root = RoleIn(**sessao.insert(session, role_root))
            usuario.roles.append(role_root)
            sessao.insert(session, usuario)
