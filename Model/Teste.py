#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from typing import List

from pydantic.dataclasses import dataclass

from Repositorio.Mongo.MongoBasico import MongoBasico
from Model.Questao import Questao
from Model.Usuario import Usuario


@dataclass # Não se usa dataclass e Base.Model ao mesmo tempo
class Teste(MongoBasico):
    id: str
    nome: str
    usuario: Usuario
    listaQuestoes: List[Questao]
    resultado: str


t = Teste(id='fa123', nome='IRB', usuario=Usuario(id='fa3123', nome='Joana', email='g@m.co', senha='3ofasdf'),
          listaQuestoes=[Questao(), Questao()], resultado='3/5')

c = t