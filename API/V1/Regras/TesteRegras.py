from API.V1.Excecoes.TesteExceptions import TesteCreateException
from Model.Teste import Teste
from API.V1.Regras.Initiallizer.RegrasInitiallizer import RegrasInitiallizer


class TesteRegras(RegrasInitiallizer):
    """ Regras para sempre aplicadas ao model teste """

    def create_1(self):
        """
        uso : [create]

        Args:
            handler:
            model: model a ser validado

        Returns:
        """
        teste: Teste = self.model
        if not teste.quantidade_questoes:
            self.handler.excecao = TesteCreateException(self.model)