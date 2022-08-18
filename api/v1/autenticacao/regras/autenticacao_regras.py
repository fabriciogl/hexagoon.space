#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from recursos.basic_exceptions.sql_exceptions import SQLFindException
from recursos.regras_initiallizer import RegrasInitiallizer
from api.v1.usuario.model.usuario_model import UsuarioIn
from banco_dados.sql_alchemy.configuracao.oracle.data_oracle import Usuario


class AutenticacaoRegras(RegrasInitiallizer):

    model: UsuarioIn
    data: Usuario


    def regra_1(self):
        """
        use : [recuperar-1]
        """
        select_query = select(Usuario).where(Usuario.email == self.model.email)

        try:
            self.handler.sessao.execute(select_query).scalar_one()

        except NoResultFound:
            raise SQLFindException(self.model.email, 'usuário')

    def regra_2(self):
        """
        use : [login-1]
        """