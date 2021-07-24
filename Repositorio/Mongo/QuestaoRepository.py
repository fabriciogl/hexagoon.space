from Repositorio.Mongo.MongoSetup import MongoSetup


class QuestaoRepository:

    @staticmethod
    async def procura_um(_id: str):
        """
        método para recuperar do banco objeto do tipo questao
        Args:
            _id: string de identificacao

        Returns:
            objeto questao
        """

        return await MongoSetup.db_client['questao'].find_one({'_id': _id})
