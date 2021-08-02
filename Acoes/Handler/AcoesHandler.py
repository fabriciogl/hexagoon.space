import inspect
import re
from abc import ABC
from re import Match
from typing import Callable, Union

from pydantic import BaseModel

from Entrypoints.Handler.ResponseHandler import ResponseHandler


class AcoesHandler(ABC):
    """ classe que contém o construtor das classes do tipo Acao"""

    def __init__(self, obj: Union[str, BaseModel], handler: ResponseHandler, acao: str):
        """
        uso : []
        contrutor a ser herdado por toda classe do tipo Acao
        
        Args:
            obj: O objeto que será validado pela classe acao
            acao: string de filtragem da acao desejada
        """

        self.id = None
        self.model = None

        metodo: Callable[[Union[str, BaseModel], ResponseHandler], None]
        for name, metodo in inspect.getmembers(self, predicate=inspect.isfunction):
            #TODO verificar antes se o method pertence ao filho ou ao pai
            uso_casos: Match = re.search(r'uso\s{,4}[:=]{1,2}\s{,4}\[.*]', metodo.__doc__, flags=re.IGNORECASE)
            if (not handler.resultado)\
                and (metodo.__qualname__.startswith(type(self).__name__))\
                and (acao in uso_casos.group()):
                metodo(obj, handler)
            else:
                break



