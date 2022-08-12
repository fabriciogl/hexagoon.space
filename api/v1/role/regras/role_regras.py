#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from api.v1.recursos.basic_exceptions.mongo_exceptions import MongoFindException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer
from api.v1.role.model.role_model import Role


class RoleRegras(RegrasInitiallizer):

    def regra_1(self):
        """
        use : [find-1, inactivate-1, update-1, softdelete-1, adiciona_precedencia-1, remove_precedencia-1]

        verifica se o id existe e se está ativo
        """
        try:
            self.data: Role = Role(
                **self.handler.operacao.find_one(id=self._id, collection='roles')
            )
        except TypeError:
            raise MongoFindException(self._id, 'Role')
