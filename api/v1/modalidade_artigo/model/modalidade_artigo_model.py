#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import datetime
from typing import Optional, Union, Any

from pydantic import BaseModel, Field

from api.v1.usuario.model.usuario_model import UsuarioReduzido


class ModalidadeArtigo(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
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
        title = 'modalidade_artigos'
        arbitrary_types_allowed = True


class ModalidadeArtigoFind(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: str
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioReduzido]

    class Config:
        orm_mode = True


class ModalidadeArtigoNome(BaseModel):
    nome: str


class ModalidadeArtigoInCreate(BaseModel):
    nome: str

    class Config:
        orm_mode = True
        title = "modalidade_artigos"


class ModalidadeArtigoOutCreate(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: str
    criado_em: Optional[datetime.datetime]
    criado_por: Optional[UsuarioReduzido]

    class Config:
        orm_mode = True


class ModalidadeArtigoInUpdate(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: str

    class Config:
        title = 'modalidade_artigos'
        arbitrary_types_allowed = True


class ModalidadeArtigoOutUpdate(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: str
    alterado_em: Optional[datetime.datetime]
    alterado_por: Optional[UsuarioReduzido]

    class Config:
        title = "modalidade_artigos"


class ModalidadeArtigoOutDelete(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    nome: str
    deletado_em: Optional[datetime.datetime]
    deletado_por: Optional[UsuarioReduzido]

    class Config:
        title = "modalidade_artigos"


class ModalidadeArtigoReduzido(BaseModel):
    id: Union[str, Any] = Field(alias='_id')
    nome: str

    class Config:
        title = 'modalidade_artigos'
        arbitrary_types_allowed = True