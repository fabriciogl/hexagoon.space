#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from api.v1.artigo.model.artigo_model import ArtigoIn, Artigo, ArtigoInCreate
from recursos.acoes_initiallizer import AcoesInitiallizer


class ArtigoAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: ArtigoIn
    data: Artigo

    def acao_1(self):
        """ use : [find-1, update-1, soft_delete-1] """
        self.data: Artigo = Artigo(
            **self.handler.operacao.find_one(id=self._id, collection='artigos')
        )

    def acao_2(self):
        """ use : [create-1] """
        self.model: ArtigoInCreate
        modalidade_artigo = self.handler.operacao.find_one(
            id=self.model.modalidade_artigo_id,
            collection='modalidadeArtigos'
        )
        self.model: Artigo = Artigo(**self.model.dict())
        self.model.modalidade_artigo = modalidade_artigo
        # self.data.titulo = self.model.corpo['blocks'][0]['data']['text']
        self.model.corpo = json.dumps(self.model.corpo)


    def acao_3(self):
        """ use : [update-2] """
        # alterações
        # self.model.titulo = self.model.corpo['blocks'][0]['data']['text']
        self.model.corpo = json.dumps(self.model.corpo)
        self.model: Artigo = Artigo(**self.model.dict())


    def acao_4(self):
        """ use : [soft_delete-2] """
        self.model: Artigo = Artigo()
