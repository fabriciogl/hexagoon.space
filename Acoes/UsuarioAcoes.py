import base64

from pymongo.results import BulkWriteResult
from starlette import status

from Acoes.Initiallizer.AcoesInitiallizer import AcoesInitiallizer
from Entrypoints.Handler.ResponseHandler import ResponseHandler
from Excecoes.MongoExceptions import MongoCreateException, MongoOperationException, MongoUpsertedException
from Model.Usuario import Usuario
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository
from fastapi.responses import JSONResponse


class UsuarioAcoes(AcoesInitiallizer):
    """ Classe do tipo NAMESPACE para aplicar ações ao objeto Usuario """

    @staticmethod
    def find_1(_id: str, handler: ResponseHandler):
        """ uso : [find] """

        try:
            resultado = UsuarioRepository.find_one(_id=_id)
            handler.resposta = resultado.dict(exclude={'senha'})
        except Exception as e:
            handler.excecao = e

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
                    raise MongoCreateException(objeto)
                elif resultado.matched_count:
                    raise MongoUpsertedException(objeto)
                # resposta de sucesso
                else:
                    handler.resposta = JSONResponse(status_code=status.HTTP_201_CREATED,
                                                    content=objeto.dict(exclude={'senha'}))
            else:
                raise MongoOperationException()
        except Exception as e:
            handler.excecao = e

