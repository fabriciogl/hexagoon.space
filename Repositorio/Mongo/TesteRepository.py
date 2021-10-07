from API.V1.Excecoes.MongoExceptions import MongoFindException2
from Model.Questao import Questao
from Model.Teste import Teste
from Repositorio.Mongo.Configuracao.MongoSetupAssincrono import MongoSetupAssincrono
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono


class TesteRepository:

    @staticmethod
    async def aprocura_um(_id: str):
        """
        método para recuperar do banco model do tipo usuario
        Args:
            _id: string de identificacao

        Returns:
            model usuario
        """
        resultado_bd: dict = await MongoSetupAssincrono.db_client['usuario'].find_one({'_id': _id})
        return Questao(**resultado_bd)

    @staticmethod
    def find_one(_id: str):
        """
        método para recuperar do banco o model especificada
        Args:
            i: string de identificacao

        Returns:
            model usuario
        """

        resultado_bd: dict = MongoSetupSincrono \
            .db_client['teste'] \
            .find_one({'_id': _id})

        if resultado_bd is None:
            raise MongoFindException2()
        return Teste(**resultado_bd)
