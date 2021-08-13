# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from Repositorio.Mongo.Configuracao.MongoBasico import MongoBasico


class Questao(BaseModel):
    banca: Optional[str]
    data: Optional[datetime] = Field(None, alias='ano')
    conteudo_texto: Optional[str] = Field(None, alias='conteudo')
    conteudo_imagem: Optional[str]
    resposta: Optional[str] = Field(None, alias='respostas')
    qid: Optional[str]
    id: str = Field(None, alias='_id')  #alias, pois o Pydantic esconde campos privados

