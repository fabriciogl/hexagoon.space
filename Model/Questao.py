# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from datetime import datetime
from pydantic import BaseModel, Field
from Repositorio.Mongo.Configuracao.MongoBasico import MongoBasico


class Questao(BaseModel, MongoBasico):
    banca: str
    data: datetime
    conteudo_texto: str
    conteudo_imagem: str
    resposta: str
    id: str = Field(..., alias='_id')  #alias, pois o Pydantic esconde campos privados

