from Model.Questao import Questao
from Regras.ConstrutorRegras import ConstrutorRegras


class QuestaoRegra(ConstrutorRegras):
    """ Regras para sempre aplicadas ao objeto questao """

    def regra_1(self, objeto: Questao):
        """
        uso : [create]

        Args:
            objeto: objeto a ser validado

        Returns:
        """

        objeto.atributo1 = 4