#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigo
from recursos.basic_exceptions.mongo_exceptions import MongoFindException
from recursos.regras_initiallizer import RegrasInitiallizer


class ModalidadeArtigoRegras(RegrasInitiallizer):

    def regra_1(self):
        """ use : [find-1, create-1, update-1, soft_delete-1] """
        if data := self.handler.operacao.find_one(id=self._id, collection='modalidadeArtigos'):
            self.data: ModalidadeArtigo = ModalidadeArtigo(**data)
        else:
            raise MongoFindException(self._id, 'ModalidadeArtigo')





