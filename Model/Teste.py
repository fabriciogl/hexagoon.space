#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from typing import List

from pydantic import Field, BaseModel

from Model.Questao import Questao
from Model.Usuario import Usuario
from Repositorio.Mongo.Configuracao.MongoBasico import MongoBasico


# Não se usa dataclass e Base.Model ao mesmo tempo
class Teste(BaseModel, MongoBasico):
    nome: str
    usuario: Usuario
    listaQuestoes: List[Questao]
    resultado: str
    id: str = Field(..., alias='_id')
