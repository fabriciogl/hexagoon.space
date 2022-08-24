#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigo, ModalidadeArtigoIn, \
    ModalidadeArtigoUpdate
from recursos.acoes_initiallizer import AcoesInitiallizer


class ModalidadeArtigoAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: ModalidadeArtigoIn
    data: ModalidadeArtigo

    def acao_1(self):
        """ use : [find-1] """

        self.data: ModalidadeArtigo = ModalidadeArtigo(
            **self.handler.operacao.find_one(
                id=self._id,
                collection='modalidadeArtigos'
            ))

    def acao_2(self):
        """ use : [create-1] """
        self.model: ModalidadeArtigo = ModalidadeArtigo(**self.model.dict())

    def acao_3(self):
        """ use : [update-1] """
        self.model: ModalidadeArtigoUpdate = ModalidadeArtigoUpdate(**self.model.dict())

    def acao_4(self):
        """ use : [soft_delete-1] """
        self.model: ModalidadeArtigo = ModalidadeArtigo()
