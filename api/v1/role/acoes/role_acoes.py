#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select

from recursos.acoes_initiallizer import AcoesInitiallizer
from api.v1.role.model.role_model import RoleIn
from banco_dados.sql_alchemy.configuracao.oracle.data_oracle import Role as RoleData


class RoleAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: RoleIn
    data: RoleData

    def acao_0(self):
        """ use : [find-1, inactivate-1, update-1, soft_delete-1] """
        select_query = select(RoleData).filter_by(id=self._id)
        self.data: RoleData = self.handler.sessao.execute(select_query).scalar_one()

    def acao_1(self):
        """ use : [find-2] """
        self.handler.sucesso = self.data


    def acao_2(self):
        """ use : [create-1] """
        # cria o id do usuario
        self.data = RoleData(**self.model.dict())
        self.handler.sessao.add(self.data)
        # O refresh resolve o caso de objetos sofrendo lazy load após uma sessão ser encerrada.
        # outra solução é usar o parametro expire_on_commit para falso
        # self.handler.operacoes.refresh(self.data)

        self.handler.sessao.flush()
        self.handler.sucesso = self.data

    def acao_3(self):
        """ use : [update-2] """
        self.data.update(self.model)


    def acao_4(self):
        """ use : [soft_delete-2] """
        self.data.soft_delete()

