#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from recursos.basic_exceptions.sql_exceptions import SQLFindException
from recursos.regras_initiallizer import RegrasInitiallizer
from banco_dados.sql_alchemy.configuracao.oracle.data_oracle import Role


class RoleRegras(RegrasInitiallizer):

    def regra_1(self):
        """
        use : [find-1, inactivate-1, update-1, soft_delete-1]

        verifica se o id existe e se está ativo
        """
        select_query = select(Role).where(Role.id == self._id)
        try:
            self.data: Role = self.handler.sessao.execute(select_query).scalar_one()
        except NoResultFound:
            raise SQLFindException(self._id, 'Role')