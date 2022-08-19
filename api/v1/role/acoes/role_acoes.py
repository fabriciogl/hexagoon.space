#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from pymongo.errors import OperationFailure

from recursos.acoes_initiallizer import AcoesInitiallizer
from recursos.basic_exceptions.mongo_exceptions import MongoUpdateException
from api.v1.role.model.role_model import Role, SubRoleIn, SubRoleUpdate


class RoleAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: Role
    data: Role

    def acao_0(self):
        """ use : [find-1] """
        self.data: Role = Role(**self.handler.operacao.find_one(id=self._id, collection='roles'))

    def acao_1(self):
        """ use : [find-2] """
        self.data.id = str(self.data.id)
        self.handler.sucesso = self.data


    def acao_2(self):
        """ use : [create-1, update-1] """
        # converte o model de entrada para o modelo do banco
        self.model: Role = Role(**self.model.dict(exclude_none=True))

    def acao_3(self):
        """ use : [soft_delete-1] """
        # converte o model de entrada para o modelo do banco
        self.model: Role = Role()

    def acao_5(self):
        """ use : [adiciona_sub_role-1] """
        # declara o modelo específico da ação
        self.model: SubRoleIn
        with self.handler.sessao.start_session(causal_consistency=True) as session:
            # realiza a inserção em sessão para manter integridade entre as operações
            role = SubRoleUpdate(**self.handler.sessao.find_one(session=session, id=self.model.sub_role, collection='roles'))
            # addToSet adiciona somente valores ao array que não existem
            # mapear a correspondência exata do campo, se for o caso usando dotação
            # Ex. "role.procedencias"
            addition = {"sub_roles": role.dict(exclude={'sub_roles', 'descricao'}, by_alias=True)}
            try:
                self.data = Role(
                    **self.handler.sessao.add_to_set(
                        session=session,
                        id=self._id,
                        add=addition,
                        collection='roles'
                    )
                )
            except OperationFailure as e:
                raise MongoUpdateException(self._id)

        # converte ObjectId para string
        self.data.id = str(self.data.id)
        # responde a requisição
        self.handler.sucesso = self.data

    def acao_6(self):
        """ use : [remove_sub_role-1] """
        # declara o modelo específico da ação
        self.model: SubRoleIn
        with self.handler.sessao.start_session(causal_consistency=True) as session:
            # realiza a inserção em sessão para manter integridade entre as operações
            role = SubRoleUpdate(**self.handler.sessao.find_one(session=session, id=self.model.sub_role, collection='roles'))
            # addToSet adiciona somente valores ao array que não existem
            # mapear a correspondência exata do campo, se for o caso usando dotação
            # Ex. "role.sub_roles"
            remove = {"sub_roles": role.dict(exclude={'sub_roles'}, by_alias=True)}

            self.data = Role(
                **self.handler.sessao.pull_from_set(
                    session=session,
                    id=self._id,
                    remove=remove,
                    collection='roles'
                )
            )
        # converte ObjectId para string
        self.data.id = str(self.data.id)
        # responde a requisição
        self.handler.sucesso = self.data