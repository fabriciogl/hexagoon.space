#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select

from api.v1.as_usuario_role.model.as_usuario_role_model import AsUsuarioRoleIn
from recursos.acoes_initiallizer import AcoesInitiallizer
from banco_dados.sql_alchemy.configuracao.oracle.data_oracle import Usuario as UsuarioData, Role as RoleData, \
    AsUsuarioRole


class AsUsuarioRoleAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: AsUsuarioRoleIn
    data: AsUsuarioRole

    def acao_0(self):
        """ use : [find-0, update-0, soft_delete-0] """
        select_query = select(AsUsuarioRole).filter_by(id=self._id)
        self.data: AsUsuarioRole = self.handler.sessao.execute(select_query).scalar_one()

    def acao_1(self):
        """ use : [find-1] """
        self.handler.sucesso = self.data

    def acao_2(self):
        """ use : [create-1] """
        # Seleciona o usuário
        select_usuario = select(UsuarioData).filter_by(id=self.model.usuario_id)
        usuario: UsuarioData = self.handler.sessao.execute(select_usuario).scalar_one()

        # Seleciona a role
        select_role = select(RoleData).filter_by(id=self.model.role_id)
        role: RoleData = self.handler.sessao.execute(select_role).scalar_one()

        #Cria o objeto Associacao
        self.data = AsUsuarioRole(usuario=usuario, role=role)
        self.handler.sessao.add(self.data)


    def acao_3(self):
        """ use : [soft_delete-1] """
        self.data.soft_delete()

    def acao_4(self):
        """ use : [update-1] """
        self.data.update(self.model)




