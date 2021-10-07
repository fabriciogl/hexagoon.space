# Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from typing import Optional

from pydantic import BaseModel, Field


class Questao(BaseModel):
    banca: Optional[str]
    ano: Optional[str]
    conteudo: Optional[str]
    conteudo_imagem: Optional[str]
    resposta: Optional[str]
    qid: Optional[str]
    revisada: Optional[bool]
    id: str = Field(None, alias='_id')  #alias, pois o Pydantic esconde campos privados

    class Config:
        title = 'questao'

