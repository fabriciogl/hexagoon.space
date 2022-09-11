#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from recursos.basic_exceptions.token_exceptions import RoleException
from recursos.regras_initiallizer import RegrasInitiallizer
from api.v1.usuario.model.usuario_model import UsuarioIn, Usuario


class HTMLRegras(RegrasInitiallizer):

    model: UsuarioIn
    data: Usuario


    def regra_1(self):
        """
        use : [login-1]
        """
        pass

    def regra_2(self):
        """
        use : [admin-1]
        """

    def regra_3(self):
        """
        use : [redirect-1]
        """
        pass

    def regra_4(self):
        """
        use : [article-1]
        """
        # select_query = select(Artigo).where((Artigo.id == self._id))
        # try:
        #     self.handler.sessao.execute(select_query).scalar_one()
        #
        # except NoResultFound:
        #     raise SQLException('O artigo solicitado não existe.')

    def regra_5(self):
        """
        use : [articleAll-1]
        """
        # # forma de se recuperar somente algumas colunas da tabela
        # select_query = select(Artigo.id, Artigo.titulo)
        #
        # try:
        #     self.handler.operacoes.execute(select_query).scalar_one()
        #
        # except NoResultFound:
        #     raise SQLException('Não há objetos do tipo artigo.')

    def regra_6(self):
        """
        use : [articleGroup-1]
        """
        # # forma de se recuperar somente algumas colunas da tabela
        # select_query = select(Artigo.id, Artigo.titulo)
        #
        # try:
        #     self.handler.operacoes.execute(select_query).scalar_one()
        #
        # except NoResultFound:
        #     raise SQLException('Não há objetos do tipo artigo.')
