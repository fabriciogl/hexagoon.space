import libscrc
from fastapi.responses import JSONResponse
from pymongo.errors import BulkWriteError
from pymongo.results import BulkWriteResult
from starlette import status
from passlib.hash import bcrypt

from API.V1.Acoes.Initiallizer.AcoesInitiallizer import AcoesInitiallizer
from API.V1.Excecoes.MongoExceptions import MongoCreateException, MongoUpdateException
from API.V1.Excecoes.UsuarioExceptions import UsuarioCreateException
from Model.Usuario import Usuario
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository


class UsuarioAcoes(AcoesInitiallizer):
    """ Classe do tipo NAMESPACE para aplicar ações ao model Usuario """
    # declara o tipo do model
    model: Usuario

    def acao_1(self):
        """ use : [find_1] """

        try:
            resultado = UsuarioRepository.find_one(_id=self._id)
            self.handler.resposta_json = resultado.dict(exclude={'senha'})
        except Exception as e:
            self.handler.excecao = e

    def acao_2(self):
        """ use : [create_1] """
        # cria o id do usuario
        self.model.id = hex(libscrc.xz64(self.model.email.encode()) % 2**64)[2:]+'U'
        # codifica a senha do usuario
        self.model.senha = bcrypt.using(rounds=7).hash(self.model.senha)
        # persiste o usuario
        self.handler.operacoes.create(self.model)

    def acao_3(self):
        """ use : [create_2] """
        # conclui as operacoes no banco
        try:
            resultado:BulkWriteResult = self.handler.operacoes.comitar()[self.model.Config.title]
            # banco reconheceu a operação
            if resultado.inserted_count == 1:
                self.handler.resposta_json = self.model
            else:
                #TODO verificar que tipo de excecao cabe aqui
                print(resultado)
        except BulkWriteError as b:
            self.handler.excecao = UsuarioCreateException(model=self.model,
                                                          msg=b.details['writeErrors'][0]['errmsg'])
        except Exception as e:
            self.handler.excecao = MongoCreateException(model=self.model)

    def acao_4(self):
        """ use : [update_1] """
        self.handler.operacoes.update(_id=self._id, model=self.model)

    def acao_5(self):
        """ use : [update_2] """
        # conclui as operacoes no banco
        try:
            # recupera os resultados específicos do self.model
            #TODO verificar se compensa alterar o update para findAndModify para usar o valor que foi salvo no banco.
            resultado: BulkWriteResult = self.handler.operacoes.comitar()[self.model.Config.title]

            # banco reconheceu a operação
            if resultado.modified_count == 1:
                # um self.model foi alterado
                self.handler.resposta_json = self.model
            # resposta de erro
            else:
                self.handler.excecao = MongoUpdateException(self._id)
        except Exception as e:
            self.handler.excecao = e