#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy.exc import NoResultFound

from api.v1.recursos.basic_exceptions.sql_exceptions import SQLFindException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer
from api.v1.usuario.model.usuario_model import UsuarioIn, Usuario


class AutenticacaoRegras(RegrasInitiallizer):

    model: UsuarioIn
    data: Usuario


    def regra_1(self):
        """
        use : [recuperar_1]
        """

        try:
            self.data: Usuario = self.handler.operacao.find_one(
                filter=self.model.dict(exclude_none=True)
            )

        except NoResultFound:
            raise SQLFindException(self.model.email, 'usuário')

    def regra_2(self):
        """
        use : [login_1]
        """