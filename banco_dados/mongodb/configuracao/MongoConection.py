#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from typing import Dict

from bson import ObjectId
from pydantic import BaseModel
from pymongo import InsertOne, MongoClient, ReturnDocument

from banco_dados.mongodb.configuracao.MongoSetupSincrono import MongoSetupSincrono


class Operacoes:
    # atributo da classe que armazena as operações a serem comitadas
    def __init__(self):
        self._db: MongoClient = MongoSetupSincrono.get_db_client()

    def find_all(
            self,
            collection: str,
            filter: dict = None
    ) -> list:
        """
          Metodo do handler para bucar todos os documentos da coleção
        """

        return list(self._db[collection].find(filter=filter))

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
        if not where:
            where = {}
        if id:
            where['_id'] = ObjectId(id)
        if not soft_deleteds:
            where['deletado_em'] = None

        return self._db[collection].find_one(
            filter=where
        )

    def find_lef_join(
            self,
            collection: str,
            where: dict = None,
            id: str = None
    ) -> Dict:
        """
          Metodo do handler para bucar documento no banco realizando $lookup
        """

        if id:
            match = {"$match": {"_id": ObjectId(id)}}
        elif where:
            match = {"$match": where}

        left_join = [
            match,
            {"$lookup":
                 {"from": "roles",
                  "localField": "roles._id",
                  "foreignField": "_id",
                  "as": "rolePrecedencias"
                  }
             }
        ]

        # adiciona a operação à lista a ser comitada
        return self._db[collection].aggregate(left_join).next()

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
            filter={'z': 'z'},
            replacement=model.dict(by_alias=True, exclude_none=True),  # salva no banco com _id ao invés de id
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

    def update(self, id: str, model: BaseModel) -> Dict:
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

    # def comitar(self):
    #     """ Metodo EXCLUSIVO da classe, não chamar diretamento do model. """
    #
    #     resultado = {}
    #     for collection, operacoes in self._operacoes_a_comitar.items():
    #         resultado[collection] = \
    #             MongoSetupSincrono \
    #                 .db_client[collection] \
    #                 .bulk_write(operacoes)
    #
    #     return resultado


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

    def find(
            self,
            session,
            filter: dict = None,
            id: str = None,
            collection: str = None
    ) -> Dict:
        """
          Metodo do handler para bucar documento no banco
        """

        # adiciona a operação à lista a ser comitada
        if id:
            return self._db[collection].find_one(where={'_id': ObjectId(id)}, session=session)
        return self._db[collection].find_one(
            where=filter,
            session=session
        )

    def insert(self, session, model: BaseModel, id: str = None) -> Dict:
        """
          Metodo do handler para inserir o documento no banco
        """
        # identifica o nome da classe do model
        # para identificar a coleção para salvar
        collection = model.Config.title

        # adiciona a operação à lista a ser comitada
        return self._db[collection] \
            .find_one_and_replace(
            filter=id if id else {'id': ''},
            replacement=model.dict(by_alias=True, exclude_none=True),  # salva no banco com _id ao invés de id
            upsert=True,
            return_document=ReturnDocument.AFTER,
            session=session
        )

    def update(self, session, id: str, model: BaseModel) -> Dict:
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
            add: dict,
            collection: str
    ) -> dict:
        """
          Metodo do handler para persistir a instância em memória.
        """

        # adiciona a operação à lista a ser comitada
        return self._db[collection] \
            .find_one_and_update(
            filter={'_id': ObjectId(id)},
            update={'$addToSet': add},
            return_document=ReturnDocument.AFTER,
            session=session
        )

    def pull_from_set(
            self,
            session,
            id: str,
            remove: dict,
            collection: str
    ) -> dict:
        """
          Metodo do handler para persistir a instância em memória.
        """

        # adiciona a operação à lista a ser comitada
        return self._db[collection] \
            .find_one_and_update(
            filter={'_id': ObjectId(id)},
            update={'$pull': remove},
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
