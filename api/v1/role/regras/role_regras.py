#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from api.v1.recursos.basic_exceptions.sql_exceptions import SQLFindException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer
from api.v1.role.model.role_model import Role


class RoleRegras(RegrasInitiallizer):

    def regra_1(self):
        """
        use : [find-1, inactivate-1, update-1, softdelete-1, adiciona_precedencia-1, remove_precedencia-1]

        verifica se o id existe e se está ativo
        """
        self.data: Role = Role(
            **self.handler.operacao.find(id=self._id, collection='roles')
        )
        if not self.data:
            raise SQLFindException(self._id, 'Role')
