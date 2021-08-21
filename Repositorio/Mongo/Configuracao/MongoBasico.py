#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import copy
from collections import defaultdict

from pydantic import BaseModel
from pymongo import UpdateOne, DeleteOne, InsertOne
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono


class MongoBasico:
    # atributo da classe que armazena as operações a serem comitadas
    def __init__(self):
        self._operacoes_a_comitar: dict = {}

    def create(self, model: BaseModel) -> None:
        """
          método do OBJETO para salvar a instância em banco.
        Args:
            instância do model
        Returns:
            Task.result()
        """
        # identifica o nome da classe do model
        # para identificar a coleção para salvar
        collection_name = model.Config.title

        # adiciona a operação à lista a ser comitada
        self._operacoes_a_comitar \
            .setdefault(collection_name, []) \
            .append(InsertOne(model.dict(by_alias=True))) # salva no banco com _id ao invés de id

    def update(self, _id: str, model: BaseModel) -> None:
        """
          método do OBJETO para salvar a instância em banco.
        Args:
            instância do model
        Returns:
            Task.result()
        """
        # identifica o nome da classe do model
        # para identificar a coleção para salvar
        collection_name = model.Config.title

        # adiciona a operação à lista a ser comitada
        self._operacoes_a_comitar \
            .setdefault(collection_name, []) \
            .append(UpdateOne({'_id': _id},
                              {'$set': model.dict(exclude_none=True)}))

    def deletar(self, _id: str, model: BaseModel) -> None:
        """
          método do OBJETO para deletar a instância em banco.
        Args:
            instância do model
        Returns:
            pymongo.results.DeleteResult
        """

        # identifica o nome da classa do model
        # para identificar a coleção para salvar
        collection_name = model.Config.title

        # adiciona a operação à lista a ser comitada
        self._operacoes_a_comitar \
            .setdefault(collection_name, []) \
            .append(DeleteOne({'_id': _id}))

    def comitar(self):
        """ Metodo EXCLUSIVO da classe, não chamar diretamento do model. """

        resultado = {}
        for collection, operacoes in self._operacoes_a_comitar.items():
            resultado[collection] = \
                MongoSetupSincrono \
                .db_client[collection] \
                .bulk_write(operacoes)

        return resultado
