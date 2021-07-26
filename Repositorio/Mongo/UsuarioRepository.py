from Model.Questao import Questao
from Model.Usuario import Usuario
from Repositorio.Mongo.Configuracao.MongoSetupAssincrono import MongoSetupAssincrono
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono

class UsuarioRepository:

    @staticmethod
    async def recupera_um(_id: str):
        """
        método para recuperar do banco o objeto especificada
        Args:
            _id: string de identificacao

        Returns:
            objeto questao
        """
        resultado_bd: dict = MongoSetupSincrono.db_client['usuario'].find_one({'_id': _id})
        if resultado_bd is None:
            return
        return Usuario(**resultado_bd)