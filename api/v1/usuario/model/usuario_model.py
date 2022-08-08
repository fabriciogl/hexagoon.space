#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from typing import Optional, List, Union

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from api.v1.role.model.role_model import RoleIn, RoleOut


class UsuarioIn(BaseModel):
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]

    class Config:
        title = 'usuarios'

class Usuario(BaseModel):

    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    ativo: Optional[bool]
    roles: Optional[list[RoleIn]]

    class Config:
        title = 'usuarios'
        arbitrary_types_allowed = True

class UsuarioTokenIn(BaseModel):
    email: Optional[EmailStr]
    senha: Optional[str]

    class Config:
        title = 'usuarios'


class UsuarioOut(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    nome: Optional[str]
    email: Optional[EmailStr]
    ativo: Optional[str]
    roles: Optional[List[RoleOut]]
    class Config:
        title = 'usuarios'
        arbitrary_types_allowed = True


class UsuarioOutReduzido(BaseModel):
    id: int
    nome: str
    email: EmailStr

