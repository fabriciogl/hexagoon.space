#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import datetime

from pymongo.errors import OperationFailure

from api.v1.recursos.acoes_initiallizer import AcoesInitiallizer
from api.v1.recursos.basic_exceptions.mongo_exceptions import MongoUpdateException
from api.v1.role.model.role_model import RoleIn, Role, RolePrecedenciaUpdate
from banco_dados.mongodb.configuracao.MongoConection import Sessao


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
        """ use : [softdelete-1] """
        # converte o model de entrada para o modelo do banco
        self.model: Role = Role()

    def acao_5(self):
        """ use : [adiciona_precedencia-1] """
        # declara o modelo específico da ação
        self.model: RolePrecedenciaUpdate
        # inicia a sessao
        sessao = Sessao()
        with sessao.start_session(causal_consistency=True) as session:
            # realiza a inserção em sessão para manter integridade entre as operações
            role = Role(**sessao.find(session, id=self.model.precedencia, collection='roles'))
            # addToSet adiciona somente valores ao array que não existem
            # mapear a correspondência exata do campo, se for o caso usando dotação
            # Ex. "role.procedencias"
            addition = {"precedencias": role.dict(exclude={'precedencias', 'descricao'}, by_alias=True)}
            try:
                self.data = Role(
                    **sessao.add_to_set(
                        session=session,
                        id=self._id,
                        add=addition,
                        collection='roles'
                    )
                )
            except OperationFailure:
                raise MongoUpdateException(self._id)

        # converte ObjectId para string
        self.data.id = str(self.data.id)
        # responde a requisição
        self.handler.sucesso = self.data

    def acao_6(self):
        """ use : [remove_precedencia-1] """
        # declara o modelo específico da ação
        self.model: RolePrecedenciaUpdate
        # inicia a sessao
        sessao = Sessao()
        with sessao.start_session(causal_consistency=True) as session:
            # realiza a inserção em sessão para manter integridade entre as operações
            role = Role(**sessao.find(session, id=self.model.precedencia, collection='roles'))
            # addToSet adiciona somente valores ao array que não existem
            # mapear a correspondência exata do campo, se for o caso usando dotação
            # Ex. "role.procedencias"
            remove = {"precedencias": role.dict(exclude={'precedencias'})}

            self.data = Role(
                **sessao.pull_from_set(
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