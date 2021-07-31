import inspect
import re
from abc import ABC


class ConstrutorRegras(ABC):
    """ classe que contém o construtor das classes do tipo Regra"""

    def __init__(self, obj: object, acao: str):
        """
        contrutor a ser herdado por toda classe do tipo Regra
        
        Args:
            obj: O objeto que será validado pela classe regra 
            regra: string de filtragem da regra desejada
        """

        for method in inspect.getmembers(self, predicate=inspect.isfunction):
            if acao in re.search(r'uso\s{,4}[:=]{1,2}\s{,4}\[.*]', method[1].__doc__, flags=re.IGNORECASE):
                method[1](obj)
