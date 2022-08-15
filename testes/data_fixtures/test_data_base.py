#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from api.v1.usuario.model.usuario_model import Usuario


def test_usuario(operacao):
    # insercao de usuário
    assert len(operacao.find_all(collection="usuarios")) == 2

    # valida quantidade de usuarios ativos
    usuarios_ativos = operacao.find_all(collection="usuarios", where={"ativo": True})
    assert len(usuarios_ativos) == 1
    usuario = Usuario(**operacao.find_one(collection="usuarios", where={"ativo": True}))
    # valida quantidade de roles do usuario ativo
    assert len(usuario.roles) == 1


def test_role(operacao):
    assert len(operacao.find_all(collection="roles")) == 3
    # fazer teste de precedencias com lef_join no root
