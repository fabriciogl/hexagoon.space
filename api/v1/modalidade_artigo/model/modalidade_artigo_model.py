#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from api.v1.usuario.model.usuario_model import UsuarioOutReduzido


class ModalidadeArtigoIn(BaseModel):
    modalidade: str

    class Config:
        title = 'modalidadeArtigos'
        orm_mode = True

class ModalidadeArtigoOut(BaseModel):
    id: Optional[int]
    modalidade: str
    criado_em: Optional[datetime]
    criado_por: Optional[UsuarioOutReduzido]

    class Config:
        orm_mode = True