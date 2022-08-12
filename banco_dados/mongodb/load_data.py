#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from bson import ObjectId
from passlib.hash import bcrypt

from api.v1.role.model.role_model import Role, RolePrecedenciaIn
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

    if not operacao.find_one(where={'email': usuario.email}, collection='usuarios'):
        sessao = Sessao()
        with sessao.start_session(causal_consistency=True) as session:
            # cria a collection roles com validação de esquema
            sessao.get_db().drop_collection(name_or_collection=Role.Config.title, session=session)
            sessao.get_db().create_collection(
                name=Role.Config.title,
                validator={
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": [ "sigla", "descricao", "precedencias"],
                        "properties": {
                            "sigla": {
                               "bsonType": "string",
                               "description": "texto título da role"
                            },
                            "descricao": {
                               "bsonType": "string",
                               "description": "texto descritivo da role"
                            },
                            "precedencias": {
                               "bsonType": "array",
                               "description": "array de precedencias da role, podendo ser array vazio",
                               "items": {
                                   "bsonType": "object",
                                   "required": ["_id", "sigla"],
                                   "additionalProperties": False,
                                   "properties": {
                                       "_id":{
                                           "bsonType": "objectId",
                                           "description": "O _id da role dada como precedida"
                                       },
                                       "sigla":{
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
            role_user = RolePrecedenciaIn(**sessao.insert(session, role_user))
            role_admin.precedencias.append(role_user)
            role_admin = RolePrecedenciaIn(**sessao.insert(session, role_admin))
            role_root.precedencias.append(role_admin)
            role_root = RolePrecedenciaIn(**sessao.insert(session, role_root))

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
            usuario.roles.append(role_root)
            sessao.insert(session, usuario)
