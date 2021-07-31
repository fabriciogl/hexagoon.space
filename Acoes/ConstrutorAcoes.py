import inspect
import re
from abc import ABC
from re import Match


class ConstrutorRegras(ABC):
    """ classe que contém o construtor das classes do tipo Acao"""

    def __init__(self, obj: object, acao: str):
        """
        contrutor a ser herdado por toda classe do tipo Acao
        
        Args:
            obj: O objeto que será validado pela classe acao
            acao: string de filtragem da acao desejada
        """

        for method in inspect.getmembers(self, predicate=inspect.isfunction):
            uso_casos: Match = re.search(r'uso\s{,4}[:=]{1,2}\s{,4}\[.*]', method[1].__doc__, flags=re.IGNORECASE)
            if acao in uso_casos.group():
                method[1](obj)
