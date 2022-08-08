#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy.exc import NoResultFound

from api.v1.recursos.basic_exceptions.sql_exceptions import SQLFindException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer
from api.v1.usuario.excecoes.usuario_excecoes import UsuarioCreateException, UsuarioUpdateException
from api.v1.usuario.model.usuario_model import Usuario


class UsuarioRegras(RegrasInitiallizer):
    model: Usuario
    data: Usuario

    def regra_1(self):
        """
        use : [create-1]
        """
        # Necessário passar por string para pegar casos deletados.
        resultado = self.handler.operacao \
            .find(filter={'email': self.model.email}, collection='usuarios')

        if resultado:
            raise UsuarioCreateException('Email informado possui cadastro. Utilize opção de recuperação de senha.')

    def regra_2(self):
        """
        use : [find-1, inactivate-1, update-1]

        verifica se o id existe e se está ativo
        """
        self.data: Usuario = Usuario(
            **self.handler.operacao.find(id=self._id, collection='usuarios')
        )
        if not self.data:
            raise SQLFindException(self._id, 'Usuário')

    def regra_3(self):
        """
        use : [update-2]

        verifica se trata de tentativa de alterar email do cadastro
        """

        if self.model.email:
            if self.data.email != self.model.email:
                raise UsuarioUpdateException('Não é possível alterar o email de cadastro.')

    def regra_4(self):
        """
        use : [softdelete-1]

        verifica se o id existe.
        """
        try:
            self.data: Usuario = Usuario(
                **self.handler.operacao.find(model=self.model, id=self._id)
            )
        except NoResultFound:
            raise SQLFindException(self._id, 'Usuário')
