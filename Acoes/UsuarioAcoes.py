import base64
import datetime
import random
from functools import lru_cache

from Acoes.ConstrutorAcoes import ConstrutorRegras
from Model.Questao import Questao
from Model.Usuario import Usuario


class UsuarioAcoes(ConstrutorRegras):
    """ Classe do tipo NAMESPACE para aplicar ações ao objeto Usuario """

    @staticmethod
    def acao_1(objeto: Usuario):
        """ uso : [create] """
        objeto.id = base64.b64encode(objeto.email.encode()).decode()
        objeto.salvar()

        # for i in range(1000):
        #     usuario = Usuario(_id=str(random.randrange(0, 1000)),
        #                       nome=f'Fabricio {i}',
        #                       email=f'fa_gatto{i}@gmail.com',
        #                       senha="fdasdfasdf")
        #     usuario.salvar()
