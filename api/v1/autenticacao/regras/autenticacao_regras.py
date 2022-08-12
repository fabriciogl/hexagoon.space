#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy.exc import NoResultFound

from api.v1.recursos.basic_exceptions.mongo_exceptions import MongoFindException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer
from api.v1.usuario.model.usuario_model import UsuarioIn, Usuario


class AutenticacaoRegras(RegrasInitiallizer):

    model: UsuarioIn
    data: Usuario


    def regra_1(self):
        """
        use : [recuperar-1]
        """
        self.data: Usuario = self.handler.operacao.find_one(
            collection="usuarios",
            where=self.model.dict(exclude_none=True, exclude={'senha'})
        )

        if not self.data:
            raise MongoFindException(self.model.email, 'usuário')

    def regra_2(self):
        """
        use : [login-1]
        """