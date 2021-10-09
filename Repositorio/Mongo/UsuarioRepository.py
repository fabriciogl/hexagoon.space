from typing import Any, Tuple

from API.V1.Excecoes.MongoExceptions import MongoFindException2
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
            .db_client['Usuario'] \
            .find_one({'_id': _id})

        # Jeito MUUUITO errado de fazer a conexão com o banco
        # resultado_bd = MongoClient('localhost', 27017).quickTest.usuario.find_one({'_id': _id})

        if resultado_bd is None:
            raise MongoFindException2()
        return Usuario(**resultado_bd)

    @staticmethod
    def find_one_by(campo_valor: Tuple[str, str]):
        """
        método para recuperar do banco o model especificada
        Args:
            campo_valor: tupla do nome do campo e valor

        Returns:
            model usuario
        """
        campo, valor = campo_valor
        resultado_bd: dict = MongoSetupSincrono \
            .db_client['Usuario'] \
            .find_one({campo: valor})

        # Jeito MUUUITO errado de fazer a conexão com o banco
        # resultado_bd = MongoClient('localhost', 27017).quickTest.usuario.find_one({'_id': _id})

        if resultado_bd is None:
            raise MongoFindException2()
        return Usuario(**resultado_bd)
