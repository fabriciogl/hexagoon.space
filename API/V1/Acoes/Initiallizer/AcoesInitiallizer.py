import inspect
import re
from abc import ABC
from operator import itemgetter
from typing import Callable, Union, re as t_re

from pydantic import BaseModel

from API.V1.Endpoints.Handler.ResponseHandler import ResponseHandler


class AcoesInitiallizer(ABC):
    """ classe que contém o construtor das classes do tipo Acao"""

    def __init__(self, handler: ResponseHandler, acao: str, _id: str = None, model: BaseModel = None):
        """
        uso : []
        contrutor a ser herdado por toda classe do tipo Acao
        
        Args:
            _id (str): id do model
            model: O model que será validado pela classe acao
            acao: string da acao desejada
        """
        self._id = _id
        self.model = model
        self.handler = handler

        # verifica se a lista de acoes do objeto foi inicializada
        # metodo da classe instaciada
        self.create_list_action()

        # Calable usa um conchetes com a primeira posição sendo os parametros, e a segunda o retorno
        method: Callable[[Union[str, BaseModel], ResponseHandler], None]

        # run the methods found in the action class
        # como estou chamando as actions em funcao da classe ligada ao primeiro objeto,
        # o self implicito dentro dos metodos sera sempre do primeiro objeto.
        for order, function in self.__class__.actions[acao]:
            if self.handler.resultado_json:
                break
            else:
                function(self)

    @classmethod
    def create_list_action(cls):
        """metodo que cria a lista de acoes de cada classe instaciada de acoes
           e salva em um dicionario criado na classe instaciada"""
        if not hasattr(cls, 'actions'):
            # cria um atributo na classe instaciada, chamado 'action'
            setattr(cls, 'actions', {})
            # caso não tenha, aloca as acoes e metodos de forma ordenada
            for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
                doc_string = method.__doc__ if method.__doc__ else '' # evita erro de metodo/funcao sem docstring
                use_cases: t_re.Match = re.search(r'(?P<use>use\s{,4}[:=]{1,2}\s{,4}\[.*])', doc_string, flags=re.IGNORECASE)
                if use_cases and use_cases.group('use'):
                    # identifica todas as acoes declaradas na funcao
                    list_uses = re.findall(r'\w*\d', use_cases.group('use'))
                    for use_order in list_uses:
                        use, order = use_order.split('_')
                        # Adicionei ao dicionario actions uma chave com o nome do metodo e valor
                        # após, uma chave com a ordem e o metodo como valor
                        cls.actions \
                            .setdefault(use, []) \
                            .append((int(order), method))

            # ordena a lista de metodos de cada action
            for action in cls.actions:
                cls.actions[action].sort(key=itemgetter(0))



