import base64

from pymongo.results import BulkWriteResult

from Acoes.Handler.AcoesHandler import AcoesHandler
from Entrypoints.Handler.ResponseHandler import ResponseHandler
from Excecoes.MongoExceptions import MongoCreateException, MongoOperationException, MongoUpsertedException
from Model.Usuario import Usuario
from Repositorio.Mongo.Configuracao.MongoBasico import MongoBasico
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository


class UsuarioAcoes(AcoesHandler):
    """ Classe do tipo NAMESPACE para aplicar ações ao objeto Usuario """

    @staticmethod
    def find_1(usuario_id: str, handler: ResponseHandler):
        """ uso : [find] """

        try:
            resultado = UsuarioRepository.recupera_um(i=usuario_id)
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
    def create_1(objeto: Usuario, handler: ResponseHandler):
        """ uso : [create] """
        objeto.id = base64.b64encode(objeto.email.encode()).decode()
        handler.operacoes.salvar(objeto)

        # for i in range(1000):
        #     usuario = Usuario(_id=str(random.randrange(0, 1000)),
        #                       nome=f'Fabricio {i}',
        #                       email=f'fa_gatto{i}@gmail.com',
        #                       senha="fdasdfasdf")
        #     usuario.salvar()

    @staticmethod
    def create_2(objeto: Usuario, handler: ResponseHandler):
        """ uso : [create] """
        # conclui as operacoes no banco
        try:
            resultado:BulkWriteResult = handler.operacoes.comitar()[type(objeto).__name__.lower()]

            # banco reconheceu a operação
            if resultado.acknowledged:
                ids_criados:dict = resultado.upserted_ids

                # um objeto novo foi criado
                if objeto.id not in ids_criados.values() and not resultado.matched_count:
                    raise MongoCreateException('Usuário', objeto.id)
                elif resultado.matched_count:
                    raise MongoUpsertedException('Usuário', objeto.id)
                # resposta de sucesso
                else:
                    handler.resposta = {'created': objeto.dict()}
            else:
                raise MongoOperationException()
        except Exception as e:
            handler.excecao = e

