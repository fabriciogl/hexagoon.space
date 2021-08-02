import base64

from Acoes.Handler.AcoesHandler import AcoesHandler
from Entrypoints.Handler.EntrypointHandler import EntrypointHandler
from Model.Usuario import Usuario
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository


class UsuarioAcoes(AcoesHandler):
    """ Classe do tipo NAMESPACE para aplicar ações ao objeto Usuario """

    @staticmethod
    def acao_1(usuario_id: str, handler):
        """ uso : [find] """

        try:
            resultado = UsuarioRepository.recupera_um(_id=usuario_id)
            handler.resposta = resultado
        except Exception as e:
            handler.excecao = e

        # for i in range(1000):
        #     usuario = Usuario(_id=str(random.randrange(0, 1000)),
        #                       nome=f'Fabricio {i}',
        #                       email=f'fa_gatto{i}@gmail.com',
        #                       senha="fdasdfasdf")
        #     usuario.salvar()

    @staticmethod
    def acao_2(objeto: Usuario, handler):
        """ uso : [create] """
        objeto.id = base64.b64encode(objeto.email.encode()).decode()
        objeto.salvar()

        # for i in range(1000):
        #     usuario = Usuario(_id=str(random.randrange(0, 1000)),
        #                       nome=f'Fabricio {i}',
        #                       email=f'fa_gatto{i}@gmail.com',
        #                       senha="fdasdfasdf")
        #     usuario.salvar()