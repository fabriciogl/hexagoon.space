from Model.Questao import Questao
from Regras.Handler.RegrasHandler import RegrasHandler


class QuestaoRegra(RegrasHandler):
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