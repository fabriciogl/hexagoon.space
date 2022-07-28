#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr
from pydantic.types import Json

from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigoIn
from api.v1.usuario.model.usuario_model import UsuarioOutReduzido


class ArtigoIn(BaseModel):
    titulo: Optional[str]
    corpo: Optional[Json]
    modalidade_artigo_id: Optional[int]

    class Config:
        title = 'artigos'
        orm_mode = True

class ArtigoOut(BaseModel):
    class Usuario(BaseModel):
        id: int
        nome: str
        email: EmailStr
    id: Optional[int]
    titulo: Optional[str]
    corpo: Optional[Union[dict, str]]
    criado_em: Optional[datetime]
    criado_por: Optional[UsuarioOutReduzido]

    class Config:
        orm_mode = True