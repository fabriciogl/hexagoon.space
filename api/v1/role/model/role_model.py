#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import datetime
from typing import Optional, Union, Any

from bson import ObjectId
from pydantic import BaseModel, Field


class RoleOut(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    sigla: Optional[str]
    descricao: Optional[str]

    class SubRoles(BaseModel):
        sigla: Optional[str]

    sub_roles: Optional[list[SubRoles]] = []

    class Config:
        title = 'roles'
        arbitrary_types_allowed = True


class RoleIn(BaseModel):
    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    sigla: Optional[str]
    descricao: Optional[str]

    class Config:
        title = 'roles'
        arbitrary_types_allowed = True


class RoleUsuarioTokenOut(BaseModel):
    sigla: Optional[str]


class SubRoleUpdate(BaseModel):
    """ Role gerada para ser inserida como sub_role em outra Role """
    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    sigla: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class Role(BaseModel):
    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    sigla: Optional[str]
    descricao: Optional[str]

    class SubRoles(BaseModel):
        id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
        sigla: Optional[str]

        class Config:
            arbitrary_types_allowed = True

    sub_roles: Optional[list[SubRoles]] = []

    # accountability
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[ObjectId]
    alterado_em: Optional[datetime.datetime]
    alterado_por: Optional[ObjectId]
    # soft_delete
    deletado_em: Optional[datetime.datetime]
    deletado_por: Optional[ObjectId]

    class Config:
        title = 'roles'
        arbitrary_types_allowed = True


class SubRoleIn(BaseModel):
    sub_role: str

    class Config:
        title = 'roles'
