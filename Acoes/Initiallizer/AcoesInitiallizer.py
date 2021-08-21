import inspect
import re
from abc import ABC
from typing import Callable, Union, Protocol

from pydantic import BaseModel

from Entrypoints.Handler.ResponseHandler import ResponseHandler


class AcoesInitiallizer(ABC):
    """ classe que contém o construtor das classes do tipo Acao"""

    def __init__(self, handler: ResponseHandler, acao: str, _id: str = None, model: Union[str, BaseModel] = None):
        """
        uso : []
        contrutor a ser herdado por toda classe do tipo Acao
        
        Args:
            _id (str): id do model
            model: O model que será validado pela classe acao
            acao: string de filtragem da acao desejada
        """
        self._id = _id
        self.model = model
        self.handler = handler

        method: Callable[[Union[str, BaseModel], ResponseHandler], None]
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            use_cases: re.Match = re.search(r'uso\s{,4}[:=]{1,2}\s{,4}\[.*]', method.__doc__, flags=re.IGNORECASE)
            if handler.resultado_json:
                break
            elif use_cases and acao in use_cases.group():
                method()
            else:
                continue



