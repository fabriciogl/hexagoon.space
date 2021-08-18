import libscrc

from Excecoes.UsuarioExceptions import UsuarioUpdateException
from Regras.Initiallizer.RegrasInitiallizer import RegrasInitiallizer


class UsuarioRegras(RegrasInitiallizer):
    """ Regras para sempre aplicadas ao model usuario """

    def update_1(self):
        """
        uso : [update]

        Args:
            handler:
            model: model a ser validado

        Returns:
        """
        if self._id != hex(libscrc.xz64(self.model.email.encode()) % 2**64)[2:]+'U':
            self.handler.excecao = UsuarioUpdateException(self.model)