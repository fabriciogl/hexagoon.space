#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from typing import Optional, Union, Any

from bson import ObjectId
from pydantic import BaseModel, Field


class RoleOut(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    sigla: Optional[str]
    descricao: Optional[str]

    class RolePrecendida(BaseModel):
        sigla: Optional[str]

    precedencias: Optional[list[RolePrecendida]] = []

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


class Role(BaseModel):
    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    sigla: Optional[str]
    descricao: Optional[str]

    class RolePrecendida(BaseModel):
        id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
        sigla: Optional[str]

        class Config:
            arbitrary_types_allowed = True

    precedencias: Optional[list[RolePrecendida]] = []

    class Config:
        title = 'roles'
        arbitrary_types_allowed = True

class RolePrecedencia(BaseModel):
    precedencia: str

    class Config:
        title = 'roles'
        arbitrary_types_allowed = True