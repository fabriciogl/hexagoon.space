#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from api.v1.artigo.excecoes.artigo_exceptions import ArtigoCreateException
from api.v1.artigo.model.artigo_model import Artigo, ArtigoInCreate
from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigo
from recursos.basic_exceptions.mongo_exceptions import MongoFindException
from recursos.regras_initiallizer import RegrasInitiallizer


class ArtigoRegras(RegrasInitiallizer):
    model: ArtigoInCreate
    def regra_1(self):
        """ use : [find-1, update-1, soft_delete-1] """
        if data := self.handler.operacao.find_one(id=self._id, collection='artigos'):
            self.data: Artigo = Artigo(**data)
        else:
            raise MongoFindException(self._id, 'Artigo')

    def regra_2(self):
        """ use : [create-1] """
        if self.handler.operacao.find_one(id=self.model.modalidade_artigo_id, collection='modalidadeArtigos'):
            pass
        else:
            raise MongoFindException(self._id, 'ModalidadeArtigo')


