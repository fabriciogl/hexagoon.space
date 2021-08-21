import base64

import libscrc
from fastapi.responses import JSONResponse
from pymongo.errors import BulkWriteError
from pymongo.results import BulkWriteResult
from starlette import status

from Acoes.Initiallizer.AcoesInitiallizer import AcoesInitiallizer
from Excecoes.MongoExceptions import MongoCreateException, MongoOperationException, MongoUpsertedException, \
    MongoUpdateException
from Excecoes.UsuarioExceptions import UsuarioCreateException
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository


class UsuarioAcoes(AcoesInitiallizer):
    """ Classe do tipo NAMESPACE para aplicar ações ao model Usuario """

    def _1_find(self):
        """ uso : [find] """

        try:
            resultado = UsuarioRepository.find_one(_id=self._id)
            self.handler.resposta_json = resultado.dict(exclude={'senha'})
        except Exception as e:
            self.handler.excecao = e

    def _1_create(self):
        """ uso : [create] """
        self.model.id = hex(libscrc.xz64(self.model.email.encode()) % 2**64)[2:]+'U'
        self.handler.operacoes.create(self.model)

    def _2_create(self):
        """ uso : [create] """
        # conclui as operacoes no banco
        try:
            resultado:BulkWriteResult = self.handler.operacoes.comitar()[self.model.Config.title]
            # banco reconheceu a operação
            if resultado.inserted_count == 1:
                self.handler.resposta_json = JSONResponse(status_code=status.HTTP_201_CREATED,
                                                          content=self.model.dict(exclude={'senha'}))
            else:
                #TODO verificar que tipo de excecao cabe aqui
                print(resultado)
        except BulkWriteError as b:
            self.handler.excecao = UsuarioCreateException(model=self.model,
                                                          msg=b.details['writeErrors'][0]['errmsg'])
        except Exception as e:
            self.handler.excecao = MongoCreateException(model=self.model)

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
                self.handler.resposta_json = JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=self.model.dict())
            # resposta de erro
            else:
                self.handler.excecao = MongoUpdateException(self._id)
        except Exception as e:
            self.handler.excecao = e