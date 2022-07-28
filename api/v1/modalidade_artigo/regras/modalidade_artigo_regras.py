#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from api.v1.modalidade_artigo.excecoes.modalidade_artigo_exceptions import ModalidadeArtigoCreateException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer


class ModalidadeArtigoRegras(RegrasInitiallizer):

    def regra_1(self):
        """ use : [create_1, update_1] """

    def regra_2(self):
        """ use : [softdelete_1] """
        pass




