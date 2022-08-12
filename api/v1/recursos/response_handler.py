# Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from typing import Optional, Any

from starlette.requests import Request

from api.v1.usuario.model.usuario_model import Usuario, UsuarioIn
from banco_dados.mongodb.configuracao.MongoConection import Operacoes


class ResponseHandler:

    def __init__(self, operacao: Operacoes = None):
        self._operacao: Optional[Operacoes] = operacao
        self._request: Optional[Request] = None
        self._usuario: Optional[Usuario] = None
        self._sucesso: Optional[Any] = None
        self._acao: Optional[str] = None

    @property
    def sucesso(self):
        return self._sucesso

    @sucesso.setter
    def sucesso(self, value):
        self._sucesso = value

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, usuario: UsuarioIn):
        self._usuario = usuario

    @property
    def operacao(self):
        return self._operacao

    @operacao.setter
    def operacao(self, sessao: Operacoes):
        self._operacao = sessao

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request: Request):
        self._request = request

    @property
    def acao(self):
        return self._acao

    @acao.setter
    def acao(self, acao: str):
        self._acao = acao
