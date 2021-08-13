# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from typing import Optional

from Repositorio.Mongo.Configuracao.MongoBasico import MongoBasico


class ResponseHandler:

    def __init__(self):
        self._resposta: Optional[dict] = None
        self._excecao: Optional[Exception] = None
        self._operacoes: MongoBasico = MongoBasico()

    @property
    def resposta(self):
        return self._resposta

    @resposta.setter
    def resposta(self, value):
        self._resposta = value

    @property
    def excecao(self):
        return self._excecao

    @excecao.setter
    def excecao(self, excecao: Exception):
        self._excecao = excecao

    @property
    def operacoes(self):
        return self._operacoes

    @operacoes.setter
    def operacoes(self, operacoes: MongoBasico):
        self._operacoes = operacoes

    @property
    def resultado(self):
        if self._excecao:
            raise self._excecao
        elif self._resposta:
            return self._resposta
