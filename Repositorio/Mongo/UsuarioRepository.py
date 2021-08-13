from functools import lru_cache

from pydantic import BaseModel

from Excecoes.MongoExceptions import MongoFindException1, MongoFindException2
from Model.Usuario import Usuario
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono


class UsuarioRepository:

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
            resultado_bd: dict = MongoSetupSincrono.db_client['usuario'].find_one({'_id': objeto.id})
        elif objeto.email:
            #TODO transformar em id
            resultado_bd: dict = MongoSetupSincrono.db_client['usuario'].find_one({'email': objeto.email})
        elif objeto.nome:
            resultado_bd: dict = MongoSetupSincrono.db_client['usuario'].find_one({'nome': objeto.nome})
        else:
            raise MongoFindException1("Usuário", objeto.id)
        # Jeito MUUUITO errado de fazer a conexão com o banco
        # resultado_bd = MongoClient('localhost', 27017).quickTest.usuario.find_one({'_id': _id})

        if resultado_bd is None:
            raise MongoFindException2("Usuário", objeto.id)
        return Usuario(**resultado_bd)
