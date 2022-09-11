#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from typing import Dict

from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient, ReturnDocument

def where_setup(
        id = None,
        where=None,
        soft_deleteds=None
):
    """ Função para setar o campo where antes do find ou update"""
    if not where:
        where = {}
    if id:
        where['_id'] = ObjectId(id)
    if not soft_deleteds:
        where['deletado_em'] = None

    return where



from banco_dados.mongodb.configuracao.MongoSetupSincrono import MongoSetupSincrono

class Operacoes:
    # atributo da classe que armazena as operações a serem comitadas
    def __init__(self):
        self._db: MongoClient = MongoSetupSincrono.get_db_client()

    def find_all(
            self,
            collection: str,
            where: dict = None,
            soft_deleteds: bool = False,
            cursor: bool = False
    ) -> list:
        """
          Metodo do handler para bucar todos os documentos da coleção
        """

        # mongo considera null campos com valor null ou que não existem
        if not where:
            where = {}
        if not soft_deleteds:
            where['deletado_em'] = None

        if cursor:
            return self._db[collection].find(filter=where)
        # retorna list para consumir o cursor
        return list(self._db[collection].find(filter=where))

    def find_one(
            self,
            collection: str,
            where: dict = None,
            id: str = None,
            soft_deleteds: bool = False
    ) -> Dict:
        """
          Metodo do handler para bucar documento no banco
        """
        where = where_setup(
            id=id,
            where=where,
            soft_deleteds=soft_deleteds
        )

        return self._db[collection].find_one(
            filter=where
        )

    def find_with_join(
            self,
            collection: str,
            join: list = None
    ) -> Dict:
        """
          Metodo do handler para bucar documento no banco realizando $lookup
        """
        # adiciona a operação à lista a ser comitada
        return self._db[collection].aggregate(join).next()

    def insert(self, model: BaseModel) -> Dict:
        """
          Metodo do handler para inserir o documento no banco
        """
        # identifica o nome da classe do model
        # para identificar a coleção para salvar
        collection = model.Config.title

        # utiliza find and replace para poder retornar o objeto inserido
        return self._db[collection] \
            .find_one_and_replace(
            filter={'_id': model.id},  # necessário passar um filter para find_one_and_replace
            replacement=model.dict(by_alias=True, exclude_none=True),  # salva no banco com _id ao invés de id
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

    def update(
            self,
            model: BaseModel,
            where: dict = None,
            id: str = None
    ) -> Dict:
        """
          Metodo do handler para atualizar o documento no banco
        """

        where = where_setup(where=where, id=id)

        # identifica o nome da classe do model
        # para identificar a coleção para salvar
        collection = model.Config.title

        # adiciona a operação à lista a ser comitada
        return self._db[collection] \
            .find_one_and_update(
            filter=where,
            update={'$set': model.dict(by_alias=True, exclude_none=True)},  # salva no banco com _id ao invés de id
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

    def deletar(self, _id: str, model: BaseModel) -> None:
        """
          Metodo do handler para deletar o documento no banco
        """

        # identifica o nome da classa do model
        # para identificar a coleção para salvar
        collection = model.Config.title

        # adiciona a operação à lista a ser comitada
        return self._db[collection] \
            .delete_one(filter={'_id': _id})


class Sessao:
    # atributo da classe que armazena as operações a serem comitadas
    def __init__(self):
        self._operacoes_a_comitar: dict = {}
        self._client = MongoSetupSincrono.client
        self._db: MongoClient = MongoSetupSincrono.get_db_client()

    def start_session(self, *args, **kwargs):
        return self._client.start_session(*args, **kwargs)

    def get_db(self):
        return self._db

    def find_one(
            self,
            session,
            collection: str,
            where: dict = None,
            id: str = None,
            soft_deleteds: bool = False
    ) -> Dict:
        """
          Metodo do handler para bucar documento no banco
        """
        if not where:
            where = {}
        if id:
            where['_id'] = ObjectId(id)
        if not soft_deleteds:
            where['deletado_em'] = None

        return self._db[collection].find_one(
            filter=where,
            session=session
        )

    def find_with_join(
            self,
            session,
            collection: str,
            join: list = None
    ) -> Dict:
        """
          Metodo do handler para bucar documento no banco realizando $lookup
        """
        # adiciona a operação à lista a ser comitada
        return self._db[collection].aggregate(join, session=session).next()

    def insert(self, session, model: BaseModel) -> Dict:
        """
          Metodo do handler para inserir o documento no banco
        """
        # identifica o nome da classe do model
        # para identificar a coleção para salvar
        collection = model.Config.title

        # adiciona a operação à lista a ser comitada
        return self._db[collection] \
            .find_one_and_replace(
            filter={'id': ''},
            replacement=model.dict(by_alias=True, exclude_none=True),  # salva no banco com _id ao invés de id
            upsert=True,
            return_document=ReturnDocument.AFTER,
            session=session
        )

    def update(
            self,
            session,
            id: str,
            model: BaseModel
    ) -> Dict:
        """
          Metodo do handler para atualizar o documento no banco
        """
        # identifica o nome da classe do model
        # para identificar a coleção para salvar
        collection = model.Config.title

        # adiciona a operação à lista a ser comitada
        return self._db[collection] \
            .find_one_and_update(
            filter={'_id': ObjectId(id)},
            update={'$set': model.dict(exclude_none=True)},  # salva no banco com _id ao invés de id
            upsert=True,
            return_document=ReturnDocument.AFTER,
            session=session
        )

    def add_to_set(
            self,
            session,
            id: str,
            model: BaseModel,
            add: dict,
            collection: str
    ) -> dict:
        """
          Método para adicionar valores ao array
        """
        return self._db[collection] \
            .find_one_and_update(
            filter={'_id': ObjectId(id)},
            update={'$addToSet': add, '$set': model.dict(exclude_none=True)},
            return_document=ReturnDocument.AFTER,
            session=session
        )

    def pull_from_set(
            self,
            session,
            id: str,
            model: BaseModel,
            remove: dict,
            collection: str
    ) -> dict:
        """
           Método para remover valores ao array
        """

        # adiciona a operação à lista a ser comitada
        return self._db[collection] \
            .find_one_and_update(
            filter={'_id': ObjectId(id)},
            update={'$pull': remove, '$set': model.dict(exclude_none=True)},
            return_document=ReturnDocument.AFTER,
            session=session
        )

    def deletar(self, _id: str, model: BaseModel) -> None:
        """
          Metodo do handler para deletar o documento no banco
        """

        # identifica o nome da classa do model
        # para identificar a coleção para salvar
        collection = model.Config.title

        # adiciona a operação à lista a ser comitada
        return self._db[collection] \
            .delete_one(filter={'_id': _id})
