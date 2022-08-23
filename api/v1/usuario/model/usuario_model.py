#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import datetime
from typing import Optional, List, Union, Any

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from api.v1.role.model.role_model import RoleUsuarioOut


class UsuarioIn(BaseModel):
    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    ativo: Optional[bool]

    class Config:
        title = 'usuarios'
        arbitrary_types_allowed = True

# modelo passado para o handler após validação do token
class UsuarioHandlerToken(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: Optional[str]
    roles: Optional[List] = Field(None, alias='sub_roles')

    class Config:
        title = 'usuarios'


class UsuarioOutReduzido(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: str

class Usuario(BaseModel):
    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    ativo: Optional[bool]
    roles: Optional[List[RoleUsuarioOut]]

    # accountability
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioOutReduzido]
    alterado_em: Optional[datetime.datetime]
    alterado_por: Optional[UsuarioOutReduzido]
    # soft_delete
    deletado_em: Optional[datetime.datetime]
    deletado_por: Optional[UsuarioOutReduzido]

    class Config:
        title = 'usuarios'
        arbitrary_types_allowed = True


# modelo utilizado na criação do token, quando é passado email e senha
class UsuarioTokenIn(BaseModel):
    email: Optional[EmailStr]
    senha: Optional[str]

    class Config:
        title = 'usuarios'

# modelo utilizado no handler, após validação da senha
class UsuarioHandlerSenha(BaseModel):
    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    nome: Optional[str]
    roles: Optional[list[RoleUsuarioOut]]
    class Config:
        title = 'usuarios'
        arbitrary_types_allowed = True
class UsuarioTokenOut(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: Optional[str]
    senha: Optional[str]
    roles: Optional[list] = Field(None, alias='sub_roles')

    class Config:
        title = 'usuarios'


class UsuarioOutFind(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: Optional[str]
    roles: Optional[List[RoleUsuarioOut]]

    class Config:
        title = 'usuarios'