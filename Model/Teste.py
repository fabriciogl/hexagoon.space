#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from typing import List, Optional

from pydantic import Field, BaseModel

from Model.Questao import Questao


# Não se usa dataclass e Base.Model ao mesmo tempo
class Teste(BaseModel):
    nome: str
    usuario_id: str
    lista_questoes: Optional[List[Questao]]
    resultado: Optional[str]
    quantidade_questoes: Optional[int]
    id: str = Field(None, alias='_id')

    class Config:
        title = 'teste'
