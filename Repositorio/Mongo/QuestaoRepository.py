from functools import lru_cache

from pydantic import BaseModel

from Excecoes.MongoExceptions import MongoFindException1, MongoFindException2
from Model.Questao import Questao
from Repositorio.Mongo.Configuracao.MongoSetupAssincrono import MongoSetupAssincrono
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono

class QuestaoRepository:

    @staticmethod
    async def aprocura_um(_id: str):
        """
        método para recuperar do banco objeto do tipo questao
        Args:
            _id: string de identificacao

        Returns:
            objeto questao
        """
        resultado_bd: dict = await MongoSetupAssincrono.db_client['questao'].find_one({'_id': _id})
        return Questao(**resultado_bd)

    @staticmethod
    def find_one(objeto: BaseModel):
        """
        método para recuperar do banco o objeto especificada
        Args:
            i: string de identificacao

        Returns:
            objeto questao
        """
        #TODO analisar a possibilidade de injection
        if objeto.id:
            resultado_bd: dict = MongoSetupSincrono\
                .db_client[type(objeto).__name__.lower()]\
                .find_one({'_id': objeto.id})
        elif objeto.qid:
            #TODO transformar em id
            resultado_bd: dict = MongoSetupSincrono \
                .db_client[type(objeto).__name__.lower()] \
                .find_one({'qid': objeto.qid})
        else:
            raise MongoFindException1("Questao", objeto.id)
        # Jeito MUUUITO errado de fazer a conexão com o banco
        # resultado_bd = MongoClient('localhost', 27017).quickTest.usuario.find_one({'_id': _id})

        if resultado_bd is None:
            raise MongoFindException2("Questao", objeto.id)
        return Questao(**resultado_bd)