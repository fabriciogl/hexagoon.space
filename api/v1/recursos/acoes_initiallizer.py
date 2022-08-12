#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

import inspect
import re
from abc import ABC
import datetime
from operator import itemgetter
from typing import Callable, Union, re as t_re, Optional

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, DataError

from api.v1.recursos.basic_exceptions.mongo_exceptions import MongoCreateException
from api.v1.recursos.response_handler import ResponseHandler


class AcoesInitiallizer(ABC):
    """ classe que contém o construtor das classes do tipo Acao"""

    def __init__(
            self,
            handler: ResponseHandler,
            acao: str,
            _id: Optional[Union[int, str]] = None,
            model: BaseModel = None
    ):
        self._id = _id
        self.model = model
        self.data = None
        self.handler = handler

        # informa a acao que esta sendo executada para posterior utilizacao do listener do SQLAlchemy
        handler.acao = acao

        # verifica se a lista de acoes do objeto foi inicializada
        # metodo da classe instaciada
        self.create_list_action()

        # Calable usa um conchetes com a primeira posição sendo os parametros, e a segunda o retorno
        method: Callable[[Union[str, BaseModel], ResponseHandler], None]

        # run the methods found in the action class
        # como estou chamando as actions em funcao da classe ligada ao primeiro objeto,
        # o self implicito dentro dos metodos sera sempre do primeiro objeto.

        for order, function in self.__class__.actions[acao]:
            if self.handler.sucesso:
                break
            else:
                function(self)

    @classmethod
    def create_list_action(cls):
        """metodo que cria a lista de acoes de cada classe instaciada
           a ser executado pelos endpoints"""
        if not hasattr(cls, 'actions'):
            # cria um atributo na classe instaciada, chamado 'action'
            setattr(cls, 'actions', {})
            # caso não tenha, aloca as acoes e metodos de forma ordenada
            for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
                doc_string = method.__doc__ if method.__doc__ else '' # evita erro de metodo/funcao sem docstring
                use_cases: t_re.Match = re.search(r'(?P<use>use\s{,4}[:=]{1,2}\s{,4}\[.*])', doc_string, flags=re.IGNORECASE)
                if use_cases and use_cases.group('use'):
                    # identifica todas as acoes declaradas na funcao
                    list_uses = re.findall(r'\w*-\d', use_cases.group('use'))
                    for use_order in list_uses:
                        use, order = use_order.split('-')
                        # Adicionei ao dicionario actions uma chave com o nome do metodo e valor
                        # após, uma chave com a ordem e o metodo como valor
                        cls.actions \
                            .setdefault(use, []) \
                            .append((int(order), method))

            # ordena a lista de metodos de cada action
            for action in cls.actions:
                cls.actions[action].sort(key=itemgetter(0))



    def encerra_find(self):
        """ use : [find-999] """
        self.data.id = str(self.data.id)
        self.handler.sucesso = self.data
    def encerra_create(self):
        """ use : [create-999] """
        self.model.criado_em = datetime.datetime.now()
        self.model.criado_por = self.handler.usuario.id
        # insere no banco
        self.data = self.handler.operacao.insert(self.model)
        # converte ObjectId para string
        self.data['_id'] = str(self.data['_id'])
        # responde o usuario
        self.handler.sucesso = self.data

    def encerra_update(self):
        """ use : [update-999] """
        self.model.alterado_em = datetime.datetime.now()
        self.model.alterado_por = self.handler.usuario.id

        self.data = self.handler.operacao.update(
            id=self._id,
            model=self.model
        )
        # converte ObjectId para string
        self.data['_id'] = str(self.data['_id'])
        # responde o usuario
        self.handler.sucesso = self.data

    def encerra_softdelete(self):
        """ use : [softdelete-999] """
        self.model.deletado_em = datetime.datetime.now()
        self.model.deletado_por = self.handler.usuario.id
        self.handler.operacao.update(self._id, self.model)
        self.handler.sucesso = {'resultado': 'Conteúdo deletado.'}



