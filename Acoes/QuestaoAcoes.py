import base64

from pydantic.types import constr
from pymongo.results import BulkWriteResult
from starlette import status
from starlette.responses import JSONResponse

from Acoes.Initiallizer.AcoesInitiallizer import AcoesInitiallizer
from Entrypoints.Handler.ResponseHandler import ResponseHandler
from Excecoes.MongoExceptions import MongoCreateException, MongoOperationException, MongoUpsertedException
from Model.Questao import Questao
from Repositorio.Mongo.QuestaoRepository import QuestaoRepository
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository


class QuestaoAcoes(AcoesInitiallizer):
    """ Classe do tipo NAMESPACE para aplicar ações ao objeto Usuario """

    @staticmethod
    def find_1(_id: constr(regex=r'[\w\D]{5,9}Q'), handler: ResponseHandler):
        """ uso : [find] """

        try:
            resultado = QuestaoRepository.find_one(_id=_id)
            handler.resposta = resultado
        except Exception as e:
            handler.excecao = e

    @staticmethod
    def create_1(objeto: Questao, handler: ResponseHandler):
        """ uso : [create] """
        objeto.id = base64.b64encode(objeto.qid.replace('Q', '').encode()).decode()
        handler.operacoes.salvar(objeto)

    @staticmethod
    def create_2(objeto: Questao, handler: ResponseHandler):
        """ uso : [create] """
        # conclui as operacoes no banco
        try:
            # recupera os resultados específicos do objeto
            resultado: BulkWriteResult = handler.operacoes.comitar()[type(objeto).__name__.lower()]

            # banco reconheceu a operação
            if resultado.acknowledged:
                ids_criados: dict = resultado.upserted_ids

                # um objeto novo foi criado
                if objeto.id not in ids_criados.values() and not resultado.matched_count:
                    raise MongoCreateException(objeto)
                elif resultado.matched_count:
                    raise MongoUpsertedException(objeto)
                # resposta de sucesso
                else:
                    handler.resposta = JSONResponse(status_code=status.HTTP_201_CREATED, content=objeto.dict())
            else:
                raise MongoOperationException()
        except Exception as e:
            handler.excecao = e

