import base64

from pymongo.errors import BulkWriteError
from pymongo.results import BulkWriteResult
from starlette import status
from starlette.responses import JSONResponse

from API.V1.Acoes.Initiallizer.AcoesInitiallizer import AcoesInitiallizer
from API.V1.Excecoes.MongoExceptions import MongoCreateException, MongoUpdateException
from Repositorio.Mongo.QuestaoRepository import QuestaoRepository


class QuestaoAcoes(AcoesInitiallizer):
    """ Classe do tipo NAMESPACE para aplicar ações ao self.model Questao """

    def action_1(self):
        """ use : [find_1] """

        try:
            resultado = QuestaoRepository.find_one(_id=self._id)
            self.handler.resposta_json = resultado
        except Exception as e:
            self.handler.excecao = e

    def action_2(self):
        """ use : [create_1] """
        self.model.id = base64.b64encode(self.model.qid.replace('Q', '').encode()).decode()
        self.handler.operacoes.create(self.model)

    
    def action_3(self):
        """ use : [update_1] """
        self.handler.operacoes.update(_id=self._id, model=self.model)

    
    def action_4(self):
        """ use : [create_2] """
        # conclui as operacoes no banco
        try:
            resultado:BulkWriteResult = self.handler.operacoes.comitar()[self.model.Config.title]
            # banco reconheceu a operação
            if resultado.inserted_count == 1:
                self.handler.resposta_json = JSONResponse(status_code=status.HTTP_201_CREATED,
                                                          content=self.model)
            else:
                #TODO verificar que tipo de excecao cabe aqui
                print(resultado)
        except BulkWriteError as b:
            self.handler.excecao = MongoCreateException(model=self.model,
                                                          msg=b.details['writeErrors'][0]['errmsg'])
        except Exception as e:
            self.handler.excecao = MongoCreateException(model=self.model)

    
    def action_5(self):
        """ use : [update_2] """
        # conclui as operacoes no banco
        try:
            # recupera os resultados específicos do self.model
            resultado: BulkWriteResult = self.handler.operacoes.comitar()[self.model.Config.title]

            # banco reconheceu a operação
            if resultado.modified_count == 1:
                # um self.model foi alterado
                self.handler.resposta_json = JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=self.model.dict())
            # resposta de erro
            else:
                self.handler.excecao = MongoUpdateException(self._id)
        except Exception as e:
            self.handler.excecao = e
