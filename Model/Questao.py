# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from datetime import datetime

from pydantic.dataclasses import dataclass

from Repositorio.Mongo.MongoBasico import MongoBasico


@dataclass
class Questao(MongoBasico):

    id: str
    banca: str
    data: datetime
    conteudo_texto: str
    conteudo_imagem: str
    resposta: str