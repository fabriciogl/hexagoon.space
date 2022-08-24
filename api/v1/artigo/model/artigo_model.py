#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados
import datetime
from typing import Optional, Union, Any

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from pydantic.types import Json

from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigoIn
from api.v1.usuario.model.usuario_model import UsuarioReduzido, UsuarioOut


class Artigo(BaseModel):
    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    modalidade_artigo: Optional[ModalidadeArtigoIn]

    # accountability
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioReduzido]
    alterado_em: Optional[datetime.datetime]
    alterado_por: Optional[UsuarioReduzido]
    # soft_delete
    deletado_em: Optional[datetime.datetime]
    deletado_por: Optional[UsuarioReduzido]

    class Config:
        title = "artigos"
        arbitrary_types_allowed = True


class ArtigoIn(BaseModel):
    titulo: Optional[str]
    corpo: Optional[Json]
    modalidade_artigo_id: Optional[str]

    class Config:
        title = 'artigos'


class ArtigoInCreate(BaseModel):
    titulo: str
    corpo: Json
    modalidade_artigo_id: str

    class Config:
        title = 'artigos'


class ArtigoFind(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]

    # accountability
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioOut]
    alterado_em: Optional[datetime.datetime]
    alterado_por: Optional[UsuarioOut]
    # soft_delete
    deletado_em: Optional[datetime.datetime]
    deletado_por: Optional[UsuarioOut]

    class Config:
        title = "artigos"
        arbitrary_types_allowed = True


class ArtigoOutCreate(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioReduzido]


class ArtigoOutUpdate(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    alterado_em: Optional[datetime.datetime]
    alterado_por: Optional[UsuarioReduzido]


class ArtigoOutDelete(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    deletado_em: Optional[datetime.datetime]
    deletado_por: Optional[UsuarioReduzido]
