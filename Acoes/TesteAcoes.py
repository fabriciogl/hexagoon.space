import base64
from datetime import datetime

from pymongo.errors import BulkWriteError
from pymongo.results import BulkWriteResult
from starlette import status
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from Acoes.Initiallizer.AcoesInitiallizer import AcoesInitiallizer
from Excecoes.MongoExceptions import MongoCreateException, MongoUpdateException
from Model.Teste import Teste
from Repositorio.Mongo.TesteRepository import TesteRepository
from Repositorio.Mongo.QuestaoRepository import QuestaoRepository

templates = Jinja2Templates(directory="Templates")

class TesteAcoes(AcoesInitiallizer):
    """ Classe do tipo NAMESPACE para aplicar ações ao self.model Teste """

    def _1_find(self):
        """ uso : [find] """

        try:
            resultado = TesteRepository.find_one(_id=self._id)
            self.handler.resposta_html = templates.TemplateResponse("testeCorreto.html",
                                                                    {"request": self.handler.request,
                                                                     "teste": resultado.dict()})
        except Exception as e:
            self.handler.excecao = e

    def _1_create(self):
        """ uso : [create.1] """
        self.model: Teste
        self.model.id = base64.b64encode(datetime.now().strftime('%Y%m%d%H%M%S').encode()).decode()

        lista_questoes = QuestaoRepository.make_teste(self.model.quantidade_questoes)
        self.model.lista_questoes = lista_questoes
        self.handler.operacoes.create(self.model)
    
    def _2_create(self):
        """ uso : [create.2] """
        # conclui as operacoes no banco
        try:
            resultado:BulkWriteResult = self.handler.operacoes.comitar()[self.model.Config.title]
            # banco reconheceu a operação
            if resultado.inserted_count == 1:
                self.handler.resposta_html = templates.TemplateResponse("testeCorreto.html",
                                                                        {"request": self.handler.request,
                                                                         "teste": self.model.dict()})
            else:
                #TODO verificar que tipo de excecao cabe aqui
                print(resultado)
        except BulkWriteError as b:
            self.handler.excecao = MongoCreateException(model=self.model,
                                                          msg=b.details['writeErrors'][0]['errmsg'])
        except Exception as e:
            self.handler.excecao = MongoCreateException(model=self.model, msg=e.args[0])

    def _1_update(self):
        """ uso : [update] """
        self.handler.operacoes.update(_id=self._id, model=self.model)
    
    def _2_update(self):
        """ uso : [update] """
        # conclui as operacoes no banco
        try:
            # recupera os resultados específicos do self.model
            resultado: BulkWriteResult = self.handler.operacoes.comitar()[self.model.Config.title]

            # banco reconheceu a operação
            if resultado.modified_count == 1:
                # um self.model foi alterado
                self.handler.resposta_json = JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                                                          content=self.model.dict(exclude_none=True))
            # resposta de erro
            else:
                self.handler.excecao = MongoUpdateException(self._id)
        except Exception as e:
            self.handler.excecao = e
