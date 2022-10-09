#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados
import datetime
from typing import Optional, Union, Any

from pydantic import BaseModel, Field
from pydantic.types import Json

from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigoInUpdate, ModalidadeArtigoNome
from api.v1.usuario.model.usuario_model import UsuarioReduzido, UsuarioBlameOut


class Artigo(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    modalidade_artigo: Optional[ModalidadeArtigoInUpdate]

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


class ArtigoFind(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    modalidade_artigo: Optional[ModalidadeArtigoNome]

    # accountability
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioBlameOut]
    alterado_em: Optional[datetime.datetime]
    alterado_por: Optional[UsuarioBlameOut]
    # soft_delete
    deletado_em: Optional[datetime.datetime]
    deletado_por: Optional[UsuarioBlameOut]

    class Config:
        title = "artigos"
        arbitrary_types_allowed = True


class ArtigoInCreate(BaseModel):
    corpo: Json
    modalidade_artigo_id: str

    class Config:
        title = 'artigos'


class ArtigoOutCreate(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    modalidade_artigo: Optional[ModalidadeArtigoNome]
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioReduzido]


class ArtigoInUpdate(BaseModel):
    corpo: Optional[Json]
    modalidade_artigo_id: Optional[str]

    class Config:
        title = 'artigos'
        arbitrary_types_allowed: True


class ArtigoOutUpdate(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    modalidade_artigo: Optional[ModalidadeArtigoNome]
    alterado_em: Optional[datetime.datetime]
    alterado_por: Optional[UsuarioReduzido]


class ArtigoOutDelete(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    deletado_em: Optional[datetime.datetime]
    deletado_por: Optional[UsuarioReduzido]
