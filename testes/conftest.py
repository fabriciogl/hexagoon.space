#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from typing import Generator

import pytest
from bson import ObjectId
from passlib.hash import bcrypt
from starlette.testclient import TestClient

from api.v1.role.model.role_model import Role, SubRoleUpdate
from api.v1.usuario.model.usuario_model import Usuario
from banco_dados.mongodb.configuracao.MongoConection import Operacoes
from banco_dados.mongodb.configuracao.MongoConection import Sessao
from banco_dados.mongodb.configuracao.MongoSetupSincrono import MongoSetupSincrono
from config import settings
from main import app
from testes.endpoints.test_role_endpoints import TestRoleEndpoints
from testes.endpoints.test_usuario_endpoints import TestUsuarioEndpoint


@pytest.fixture(scope="package")
def operacao():
    # inicia a conexão com o banco de dados
    MongoSetupSincrono.connect_client()

    # cria os objetos
    usuario1 = Usuario(
        id=ObjectId(),
        nome=settings.root_user,
        email=settings.root_email,
        senha=bcrypt.using(rounds=7).hash(settings.root_pass),
        ativo=True,
        roles=[]
    )
    usuario2 = Usuario(
        id=ObjectId(),
        nome='Maria da Silva',
        email='maria@hexsaturn.space',
        senha=bcrypt.using(rounds=7).hash('segredodamaria'),
        ativo=False,
        roles=[]
    )

    # cria usuário root
    role_root = Role(id=ObjectId(), sigla=settings.root_role, descricao='acesso com poder de superusuário')

    # cria demais roles
    role_admin = Role(id=ObjectId(), sigla='admin', descricao='acesso com poder de administração')
    role_user = Role(id=ObjectId(), sigla='user', descricao='acesso com poder de usuário')

    # inicia uma sessao
    sessao = Sessao()
    with sessao.start_session(causal_consistency=True) as session:
        # cria a collection roles com validação de esquema
        sessao.get_db().drop_collection(name_or_collection=Role.Config.title, session=session)
        sessao.get_db().create_collection(
            name=Role.Config.title,
            validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["sigla", "descricao", "sub_roles"],
                    "properties": {
                        "sigla": {
                            "bsonType": "string",
                            "description": "texto título da role"
                        },
                        "descricao": {
                            "bsonType": "string",
                            "description": "texto descritivo da role"
                        },
                        "sub_roles": {
                            "bsonType": "array",
                            "description": "array de precedencias da role, podendo ser array vazio",
                            "items": {
                                "bsonType": "object",
                                "required": ["_id", "sigla"],
                                "additionalProperties": False,
                                "properties": {
                                    "_id": {
                                        "bsonType": "objectId",
                                        "description": "O _id da role dada como precedida"
                                    },
                                    "sigla": {
                                        "bsonType": "string",
                                        "description": "título da role precedida"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )
        # cria as collections com validacao de esquema
        role_user = SubRoleUpdate(**sessao.insert(session, role_user))
        role_admin.sub_roles.append(role_user)
        role_admin = SubRoleUpdate(**sessao.insert(session, role_admin))
        role_root.sub_roles.append(role_admin)
        role_root = SubRoleUpdate(**sessao.insert(session, role_root))
        TestRoleEndpoints.id_root = str(role_root.id)

        # cria a collectiona usuarios com validação de esquema
        sessao.get_db().drop_collection(name_or_collection=Usuario.Config.title, session=session)
        sessao.get_db().create_collection(
            name=Usuario.Config.title,
            validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["nome", "email", "senha", "ativo"],
                    "properties": {
                        "nome": {
                            "bsonType": "string",
                            "description": "nome completo do usuário"
                        },
                        "email": {
                            "bsonType": "string",
                            "description": "email do usuário"
                        },
                        "senha": {
                            "bsonType": "string",
                            "description": "senha do usuário"
                        },
                        "ativo": {
                            "bsonType": "bool",
                            "description": "usuário ativo ou inativo"
                        },
                        "roles": {
                            "bsonType": "array",
                            "description": "array de roles, podendo ser array vazio",
                            "items": {
                                "bsonType": "object",
                                "required": ["_id", "sigla"],
                                "additionalProperties": False,
                                "properties": {
                                    "_id": {
                                        "bsonType": "objectId",
                                        "description": "O _id da role dada como precedida"
                                    },
                                    "sigla": {
                                        "bsonType": "string",
                                        "description": "título da role precedida"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )
        usuario1.roles.append(role_root)
        usuario_root = Usuario(**sessao.insert(session, usuario1))
        TestUsuarioEndpoint.id_root = str(usuario_root.id)
        sessao.insert(session, usuario2)

    operacao = Operacoes()

    yield operacao


@pytest.fixture(scope="package")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
