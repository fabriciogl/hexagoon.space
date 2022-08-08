#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from passlib.hash import bcrypt

from api.v1.recursos.acoes_initiallizer import AcoesInitiallizer
from api.v1.usuario.model.usuario_model import Usuario, UsuarioIn


class UsuarioAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: UsuarioIn
    data: Usuario

    def acao_0(self):
        """ use: [find-1] """
        self.data: Usuario = self.handler.operacao.find(id=self._id, collection='usuarios')

    def acao_2(self):
        """ use : [create-1] """
        # codifica a senha do usuario
        self.model.senha = bcrypt.using(rounds=7).hash(self.model.senha)
        # converte o model para data
        self.data = Usuario(**self.model.dict(exclude_none=True))
        self.data.ativo = True

    def acao_3(self):
        """ use : [inactivate-2] """
        self.data.ativo = False
        self.handler.sucesso = {'resultado': 'usuário inativado.'}

    def acao_4(self):
        """ use : [update-2] """
        # dados são retornados do banco e convertidos para objetos pydanticos
        self.data = Usuario(
            **self.handler.operacao.update(
                id=self._id,
                model=self.model
            )
        )

    def acao_5(self):
        """ use : [softdelete-1] """
        # Seleciona o usuário
        self.data.deletado_em = False
        self.data.deletado_por = self.handler.usuario
        self.handler.operacao.update(self._id, self.data)
