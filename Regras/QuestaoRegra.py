from Model.Questao import Questao
from Regras.ConstrutorRegras import ConstrutorRegras


class QuestaoRegra(ConstrutorRegras):
    """ Regras para sempre aplicadas ao objeto questao """

    @staticmethod
    def regra_1(objeto: Questao):
        """
        uso : [create]

        Args:
            objeto: objeto a ser validado

        Returns:
        """

        objeto.atributo1 = 4