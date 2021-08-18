from functools import lru_cache

from pydantic import BaseModel

from Excecoes.MongoExceptions import MongoFindException1, MongoFindException2
from Model.Usuario import Usuario
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono


class UsuarioRepository:

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
            .db_client['usuario'] \
            .find_one({'_id': _id})

        # Jeito MUUUITO errado de fazer a conexão com o banco
        # resultado_bd = MongoClient('localhost', 27017).quickTest.usuario.find_one({'_id': _id})

        if resultado_bd is None:
            raise MongoFindException2()
        return Usuario(**resultado_bd)
