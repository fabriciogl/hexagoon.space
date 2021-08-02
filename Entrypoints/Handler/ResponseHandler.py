# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from typing import Optional

from pydantic import BaseModel, Field


class ResponseHandler():
    _resposta: Optional[dict] = None
    _excecao: Optional[dict] = None

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
    def excecao(self, excecao: Optional[Exception]):
        self._excecao = {excecao.__class__.__name__: excecao.__str__()}

    @property
    def resultado(self):
        return self._excecao if self._excecao else self._resposta
