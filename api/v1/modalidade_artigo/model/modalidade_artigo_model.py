#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import datetime
from typing import Optional, Union, Any

from bson import ObjectId
from pydantic import BaseModel, Field

from api.v1.usuario.model.usuario_model import UsuarioReduzido


class ModalidadeArtigo(BaseModel):
    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    nome: Optional[str]

    # accountability
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioReduzido]
    alterado_em: Optional[datetime.datetime]
    alterado_por: Optional[UsuarioReduzido]
    # soft_delete
    deletado_em: Optional[datetime.datetime]
    deletado_por: Optional[UsuarioReduzido]

    class Config:
        title = 'modalidadeArtigos'
        arbitrary_types_allowed = True


class ModalidadeArtigoIn(BaseModel):
    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    nome: str

    class Config:
        title = 'modalidadeArtigos'
        orm_mode = True
        arbitrary_types_allowed = True


class ModalidadeArtigoInCreate(BaseModel):
    nome: str
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioReduzido]

    class Config:
        orm_mode = True
        title = "modalidadeArtigos"


class ModalidadeArtigoOut(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: str
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioReduzido]

    class Config:
        orm_mode = True


class ModalidadeArtigoReduzido(BaseModel):
    nome: str


class ModalidadeArtigoOutCreate(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: str
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioReduzido]

    class Config:
        orm_mode = True


class ModalidadeArtigoUpdate(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: str
    alterado_em: Optional[datetime.datetime]
    alterado_por: Optional[UsuarioReduzido]

    class Config:
        orm_mode = True
        title = "modalidadeArtigos"


class ModalidadeArtigoOutDelete(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: str
    deletado_em: Optional[datetime.datetime]
    deletado_por: Optional[UsuarioReduzido]

    class Config:
        orm_mode = True
        title = "modalidadeArtigos"
