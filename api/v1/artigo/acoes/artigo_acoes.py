#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from api.v1.artigo.model.artigo_model import ArtigoInUpdate, Artigo, ArtigoInCreate
from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigo, ModalidadeArtigoIn
from recursos.acoes_initiallizer import AcoesInitiallizer


class ArtigoAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: ArtigoInUpdate
    data: Artigo

    def acao_1(self):
        """ use : [find-1, update-1, soft_delete-1] """
        self.data: Artigo = Artigo(
            **self.handler.operacao.find_one(id=self._id, collection=Artigo.Config.title)
        )

    def acao_2(self):
        """ use : [create-1] """
        self.model: ArtigoInCreate
        modalidade_artigo = self.handler.operacao.find_one(
            id=self.model.modalidade_artigo_id,
            collection=ModalidadeArtigo.Config.title
        )
        self.model: Artigo = Artigo(**self.model.dict())
        self.model.modalidade_artigo = modalidade_artigo
        self.model.titulo = self.model.corpo['blocks'][0]['data']['text']
        self.model.corpo = json.dumps(self.model.corpo)


    def acao_3(self):
        """ use : [update-2] """
        # alterações
        self.model: ArtigoInUpdate
        # modelo pre banco do artigo alterado
        pre_data_artigo = Artigo(**self.model.dict())

        # verifica se a alteração envolve o campo modalidade de artigo
        if self.model.modalidade_artigo_id:
            modalidade_artigo = ModalidadeArtigoIn(
                **self.handler.operacao.find_one(
                ModalidadeArtigo.Config.title,
                id=self.model.modalidade_artigo_id
                )
            )
            pre_data_artigo.modalidade_artigo = modalidade_artigo

        # verifica se a alteração altera o corpo do artigo
        if self.model.corpo:
            self.model.titulo = self.model.corpo['blocks'][0]['data']['text']
            pre_data_artigo.corpo = json.dumps(self.model.corpo)

        self.model: Artigo = pre_data_artigo


    def acao_4(self):
        """ use : [soft_delete-2] """
        self.model: Artigo = Artigo()
