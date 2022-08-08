#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select

from api.v1.recursos.acoes_initiallizer import AcoesInitiallizer
from api.v1.role.model.role_model import RoleIn, Role, RoleOut, RolePrecedencia
from banco_dados.mongodb.configuracao.MongoConection import Sessao


class RoleAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: RoleIn
    data: Role

    def acao_0(self):
        """ use : [find-1, softdelete-1] """
        self.data: Role = Role(**self.handler.operacao.find(id=self._id, collection='roles'))

    def acao_1(self):
        """ use : [find-2] """
        self.data.id = str(self.data.id)
        self.handler.sucesso = self.data


    def acao_2(self):
        """ use : [create-1] """
        # converte o model para data
        self.data = Role(**self.model.dict(exclude_none=True))

    def acao_3(self):
        """ use : [update-1] """
        self.data = Role(
            **self.handler.operacao.update(
                id=self._id,
                model=self.model
            )
        )

    def acao_4(self):
        """ use : [softdelete-2] """
        self.data.deletado_em = False
        self.data.deletado_por = self.handler.usuario
        self.handler.operacao.update(self._id, self.data)

    def acao_5(self):
        """ use : [adiciona_precedencia-1] """
        # declara o modelo específico da ação
        self.model: RolePrecedencia
        # inicia a sessao
        sessao = Sessao()
        with sessao.start_session(causal_consistency=True) as session:
            # realiza a inserção em sessão para manter integridade entre as operações
            role = Role(**sessao.find(session, id=self.model.precedencia, collection='roles'))
            # addToSet adiciona somente valores ao array que não existem
            # mapear a correspondência exata do campo, se for o caso usando dotação
            # Ex. "role.procedencias"
            addition = {"precedencias": role.dict(exclude={'precedencias'})}
            self.data = Role(
                **sessao.add_to_set(
                    session=session,
                    id=self._id,
                    add=addition,
                    collection='roles'
                )
            )
        # converte ObjectId para string
        self.data.id = str(self.data.id)
        # responde a requisição
        self.handler.sucesso = self.data

    def acao_6(self):
        """ use : [remove_precedencia-1] """
        # declara o modelo específico da ação
        self.model: RolePrecedencia
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