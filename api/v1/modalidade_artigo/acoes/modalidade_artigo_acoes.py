#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from api.v1.artigo.model.artigo_model import ArtigoIn
from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigo
from recursos.acoes_initiallizer import AcoesInitiallizer


class ModalidadeArtigoAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: ArtigoIn
    data: ModalidadeArtigo

    def acao_1(self):
        """ use : [find-1] """
        # select_query = select(ModalidadeArtigo).filter_by(id=self._id)
        # try:
        #     self.data = self.handler.sessao.execute(select_query).scalar_one()
        #
        # except NoResultFound:
        #     raise SQLFindException(self._id, 'ModalidadeArtigo')

        self.handler.sucesso = self.data

    def acao_2(self):
        """ use : [create-1] """
        self.data = ModalidadeArtigo(**self.model.dict())
        self.handler.sessao.add(self.data)


    def acao_3(self):
        """ use : [update-1] """
        # select_query = select(ModalidadeArtigo).filter_by(id=self._id)
        # try:
        #     self.data = self.handler.sessao.execute(select_query).scalar_one()
        #
        # except NoResultFound:
        #     raise SQLFindException(self._id, 'ModalidadeArtigo')
        #
        # # alterações
        # self.data.update(self.model)


    def acao_4(self):
        """ use : [soft_delete-1] """
        # select_query = select(ModalidadeArtigo).filter_by(id=self._id)
        #
        # try:
        #     if data := self.handler.sessao.execute(select_query).scalar_one():
        #         self.data = data
        #
        # except NoResultFound:
        #     raise SQLFindException(self._id, 'Role')
        #
        # self.data.soft_delete()

