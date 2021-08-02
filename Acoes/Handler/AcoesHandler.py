import inspect
import re
from abc import ABC
from re import Match

from Entrypoints.Handler.EntrypointHandler import EntrypointHandler


class AcoesHandler(ABC):
    """ classe que contém o construtor das classes do tipo Acao"""

    def __init__(self, obj: object, handler, acao: str):
        """
        uso : []
        contrutor a ser herdado por toda classe do tipo Acao
        
        Args:
            obj: O objeto que será validado pela classe acao
            acao: string de filtragem da acao desejada
        """

        self.id = None
        self.model = None
        self._resposta = None
        self._excecao = None

        for method in inspect.getmembers(self, predicate=inspect.isfunction):
            #TODO verificar antes se o method pertence ao filho ou ao pai
            uso_casos: Match = re.search(r'uso\s{,4}[:=]{1,2}\s{,4}\[.*]', method[1].__doc__, flags=re.IGNORECASE)
            if not self._excecao and acao in uso_casos.group():
                method[1](obj, handler)
            else:
                break

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
    def excecao(self, value):
        self._excecao = value

    @property
    def resultado(self):
        return self._resposta if self._resposta else self._excecao



