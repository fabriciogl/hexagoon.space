#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from passlib.hash import bcrypt

from api.v1.usuario.model.usuario_model import Usuario, UsuarioIn
from recursos.acoes_initiallizer import AcoesInitiallizer
from recursos.basic_exceptions.mongo_exceptions import MongoFindException


class UsuarioAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: UsuarioIn
    data: Usuario

    def acao_0(self):
        """ use: [find-1, inactivate-1] """
        if data := self.handler.operacao.find_one(id=self._id, collection='usuarios'):
            self.data: Usuario = Usuario(**data)
        else:
            MongoFindException(self._id, 'Usuarios')

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
