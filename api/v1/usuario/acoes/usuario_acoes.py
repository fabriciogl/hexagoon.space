#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from passlib.hash import bcrypt
from sqlalchemy import select

from recursos.acoes_initiallizer import AcoesInitiallizer
from api.v1.usuario.model.usuario_model import UsuarioIn
from banco_dados.sql_alchemy.configuracao.oracle.data_oracle import Usuario
from templates.Jinja2 import create_templates

templates = create_templates()

class UsuarioAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: UsuarioIn
    data: Usuario

    def acao_0(self):
        """ use: [find-1, update-1, inactivate-1] """
        select_query = select(Usuario).where((Usuario.id == self._id) & (Usuario.ativo == True))
        self.data: Usuario = self.handler.sessao.execute(select_query).scalar_one()


    def acao_1(self):
        """ use : [find-2] """
        self.handler.sucesso = self.data

    def acao_2(self):
        """ use : [create-1] """
        # codifica a senha do usuario
        self.model.senha = bcrypt.using(rounds=7).hash(self.model.senha)
        # persiste o usuario
        self.data = Usuario(**self.model.dict(exclude_none=True))
        self.handler.sessao.add(self.data)

    def acao_3(self):
        """ use : [inactivate-2] """
        self.data.ativo = False
        self.handler.sucesso = {'resultado': 'usuário inativado.'}

    def acao_4(self):
        """ use : [update-2] """
        # Não é necessário adicionar na sessão, pois ao fazer a query o objeto já foi adicionado
        # e está em estado de observação.
        self.data.update(self.model)

    def acao_5(self):
        """ use : [soft_delete-1] """
        # Seleciona o usuário
        select_usuario = select(Usuario).where((Usuario.id == self._id))
        self.data = self.handler.sessao.execute(select_usuario).scalar_one()
        # Não é necessário adicionar na sessão, pois ao fazer a query o objeto já foi adicionado
        # e está em estado de observação.
        self.data.soft_delete()
