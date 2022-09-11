#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import datetime

from passlib.hash import bcrypt

from api.v1.role.model.role_model import RoleUsuario
from api.v1.usuario.model.usuario_model import Usuario, UsuarioIn, UsuarioRoleIn, UsuarioOut, UsuarioReduzido
from recursos.acoes_initiallizer import AcoesInitiallizer


class UsuarioAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: UsuarioIn
    data: Usuario

    def acao_0(self):
        """ use: [find-1, inactivate-1] """
        self.data: Usuario = Usuario(**self.handler.operacao.find_one(id=self._id, collection='usuarios'))

    def acao_2(self):
        """ use : [create-1] """
        # codifica a senha do usuario
        self.model.senha = bcrypt.using(rounds=7).hash(self.model.senha)
        # converte o model para data
        self.model: Usuario = Usuario(**self.model.dict(exclude_none=True))
        self.model.ativo = True

    def acao_3(self):
        """ use : [inactivate-2] """
        self.data.ativo = False
        self.data: Usuario = Usuario(
            **self.handler.operacao.update(id=self._id, model=self.data)
        )
        self.handler.sucesso = {'resultado': 'usuário inativado.'}

    def acao_4(self):
        """ use : [update-1] """
        # dados são retornados do banco e convertidos para objetos pydanticos
        self.model: Usuario = Usuario(**self.model.dict(exclude_none=True))

    def acao_5(self):
        """ use : [soft_delete-2] """
        # Seleciona o usuário
        self.model: Usuario = Usuario()

    def acao_6(self):
        """ use : [adiciona_role-1] """
        # Inicia a sessao
        with self.handler.sessao.start_session(causal_consistency=True) as session:
            # Seleciona a role
            self.model: UsuarioRoleIn
            role: RoleUsuario = RoleUsuario(
                **self.handler.sessao.find_one(
                    session=session,
                    id=self.model.role.id,
                    collection='roles'
                )
            )

            # campos que serão atualizados, role e alterado
            addition = {"roles": role.dict(by_alias=True)}
            self.model.alterado_em = datetime.datetime.now()
            self.model.alterado_por = UsuarioReduzido(_id=self.handler.usuario.id, nome=self.handler.usuario.nome)

            self.data: UsuarioOut = UsuarioOut(
                **self.handler.sessao.add_to_set(
                    session=session,
                    id=self._id,
                    add=addition,
                    model=self.model,
                    collection='usuarios'
                )
            )
            # converte de ObjectId para id
            self.data.id = str(self.data.id)

            self.handler.sucesso = self.data

    def acao_7(self):
        """ use : [remove_role-1] """
        # Inicia a sessao
        with self.handler.sessao.start_session(causal_consistency=True) as session:
            # Seleciona a role
            self.model: UsuarioRoleIn
            role: RoleUsuario = RoleUsuario(
                **self.handler.sessao.find_one(
                    session=session,
                    id=self.model.role.id,
                    collection='roles'
                )
            )

            remove = {"roles": role.dict(by_alias=True)}
            self.model.alterado_em = datetime.datetime.now()
            self.model.alterado_por = UsuarioReduzido(_id=self.handler.usuario.id, nome=self.handler.usuario.nome)

            self.data: UsuarioOut = UsuarioOut(
                **self.handler.sessao.pull_from_set(
                    session=session,
                    id=self._id,
                    model=self.model,
                    remove=remove,
                    collection='usuarios'
                )
            )
            # converte de ObjectId para id
            self.data.id = str(self.data.id)

            self.handler.sucesso = self.data
