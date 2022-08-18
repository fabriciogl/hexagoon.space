#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from api.v1.artigo.model.artigo_model import ArtigoIn
from recursos.acoes_initiallizer import AcoesInitiallizer
from recursos.basic_exceptions.sql_exceptions import SQLFindException
from banco_dados.sql_alchemy.configuracao.oracle.data_oracle import Artigo


class ArtigoAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: ArtigoIn
    data: Artigo

    def acao_1(self):
        """ use : [find-1, update-1, soft_delete-1] """
        select_query = select(Artigo).filter_by(id=self._id)
        try:
            self.data = self.handler.sessao.execute(select_query).scalar_one()

        except NoResultFound:
            raise SQLFindException(self._id, 'Artigo')

        self.handler.sucesso = self.data

    def acao_2(self):
        """ use : [create-1] """
        self.data = Artigo(**self.model.dict())
        self.data.titulo = self.model.corpo['blocks'][0]['data']['text']
        self.data.corpo = json.dumps(self.data.corpo)
        self.handler.sessao.add(self.data)


    def acao_3(self):
        """ use : [update-2] """
        # alterações
        self.model.titulo = self.model.corpo['blocks'][0]['data']['text']
        self.model.corpo = json.dumps(self.model.corpo)
        self.data.update(self.model)


    def acao_4(self):
        """ use : [soft_delete-2] """
        self.data.soft_delete()

