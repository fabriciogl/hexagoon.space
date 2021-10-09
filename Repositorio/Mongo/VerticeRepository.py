from API.V1.Excecoes.MongoExceptions import MongoFindException2
from Model.Vertice import Vertice
from Repositorio.Mongo.Configuracao.MongoSetupAssincrono import MongoSetupAssincrono
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono


class VerticeRepository:

    @staticmethod
    async def aprocura_um(_id: str):
        """
        método assincrono para recuperar do banco dados do tipo especificado
        Args:
            _id: string de identificacao

        Returns:
            model usuario
        """
        resultado_bd: dict = await MongoSetupAssincrono.db_client['vertice'].find_one({'_id': _id})
        return Vertice(**resultado_bd)

    @staticmethod
    def find_one(_id: str):
        """
        método para recuperar do banco dados especificado
        Args:
            i: string de identificacao

        Returns:
            model usuario
        """

        resultado_bd: dict = MongoSetupSincrono \
            .db_client['Vertice'] \
            .find_one({'_id': _id})

        if resultado_bd is None:
            raise MongoFindException2()
        return Vertice(**resultado_bd)

    @staticmethod
    def make_teste(quantidade: int):
        """
        método para recuperar do banco o model especificada
        Args:
            i: string de identificacao

        Returns:
            model usuario
        """

        resultado_bd: dict = MongoSetupSincrono \
            .db_client['Vertice'] \
            .find(limit=quantidade)

        if resultado_bd is None:
            raise MongoFindException2()
        return [Vertice(**questao) for questao in resultado_bd]
