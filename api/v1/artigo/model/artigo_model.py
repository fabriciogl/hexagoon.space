#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from datetime import datetime
from typing import Optional, Union, Any

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from pydantic.types import Json

from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigoIn
from api.v1.usuario.model.usuario_model import UsuarioOutReduzido

class Artigo(BaseModel):

    id: Optional[Union[str, ObjectId]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    criado_em: Optional[datetime]
    criado_por: Optional[UsuarioOutReduzido]

    class Config:
        title = "artigos"
        arbitrary_types_allowed = True

class ArtigoIn(BaseModel):
    titulo: Optional[str]
    corpo: Optional[Json]
    modalidade_artigo_id: Optional[int]

    class Config:
        title = 'artigos'

class ArtigoOut(BaseModel):
    id: Optional[Union[str, Any]] = Field(None, alias='_id')
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    criado_em: Optional[datetime]
    criado_por: Optional[UsuarioOutReduzido]