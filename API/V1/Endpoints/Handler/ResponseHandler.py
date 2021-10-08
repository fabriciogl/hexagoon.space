# Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from typing import Optional

from starlette.requests import Request

from Model.Usuario import Usuario
from Repositorio.Mongo.Configuracao.MongoBasico import MongoBasico


class ResponseHandler:

    def __init__(self, request: Request = None):
        self._usuario: Optional[Usuario] = None
        self._resposta_json: Optional[dict] = None
        self._resposta_html: Optional[str] = None
        self._excecao: Optional[Exception] = None
        self._operacoes: MongoBasico = MongoBasico()
        self.request = request

    @property
    def resposta_json(self):
        return self._resposta_json

    @resposta_json.setter
    def resposta_json(self, value):
        self._resposta_json = value

    @property
    def resposta_html(self):
        return self._resposta_html

    @resposta_html.setter
    def resposta_html(self, value):
        self._resposta_html = value

    @property
    def excecao(self):
        return self._excecao

    @excecao.setter
    def excecao(self, excecao: Exception):
        self._excecao = excecao

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, usuario: Usuario):
        self._usuario = usuario

    @property
    def operacoes(self):
        return self._operacoes

    @operacoes.setter
    def operacoes(self, operacoes: MongoBasico):
        self._operacoes = operacoes

    #TODO verificar uma forma de tornar o resultado uma classe abstrata,
    # que desconhe o tipo de resposta
    @property
    def resultado_json(self):
        if self._excecao:
            raise self._excecao
        elif self._resposta_json:
            return self._resposta_json

    @property
    def resultado_html(self):
        if self._excecao:
            raise self._excecao
        elif self._resposta_html:
            return self._resposta_html
