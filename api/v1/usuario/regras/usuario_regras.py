#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from recursos.basic_exceptions.mongo_exceptions import MongoFindException
from recursos.regras_initiallizer import RegrasInitiallizer
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
            .find_one(where={'email': self.model.email}, collection='usuarios', soft_deleteds=True)

        if resultado:
            raise UsuarioCreateException('Email informado possui cadastro. Utilize opção de recuperação de senha.')

    def regra_2(self):
        """
        use : [find-1, inactivate-1, update-1]

        verifica se o id existe e se está ativo
        """
        if data := self.handler.operacao.find_one(id=self._id, collection='usuarios'):
            self.data: Usuario = Usuario(**data)
        else:
            raise MongoFindException(self._id, 'Usuário')

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
        use : [soft_delete-1]

        verifica se o id existe.
        """
        if data := self.handler.operacao.find_one(id=self._id, collection='usuarios'):
            self.data: Usuario = Usuario(**data)
        else:
            raise MongoFindException(self._id, 'Usuário')

    def regra_5(self):
        """
        use : [adiciona_role-1]

        verifica se o id existe.
        """

    def regra_6(self):
        """
        use : [remove_role-1]

        verifica se o id existe.
        """