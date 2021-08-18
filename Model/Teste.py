#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from typing import List, Optional

from pydantic import Field, BaseModel

from Model.Questao import Questao
from Model.Usuario import Usuario


# Não se usa dataclass e Base.Model ao mesmo tempo
class Teste(BaseModel):
    nome: str
    usuario_id: str
    lista_questoes_id: List[str]
    resultado: Optional[str]
    id: str = Field(None, alias='_id')

    class Config:
        title = 'teste'
