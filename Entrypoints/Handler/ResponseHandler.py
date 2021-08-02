# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

from Excecoes.MongoExceptions import MongoFindException


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
        self._excecao = excecao

    @property
    def resultado(self):
        if self._excecao:
            raise self._excecao
        elif self._resposta:
            return self._resposta
