#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from collections import defaultdict

from pydantic import BaseModel
from pymongo import UpdateOne, DeleteOne
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono


class MongoBasico:
    # atributo da classe que armazena as operações a serem comitadas
    def __init__(self):
        self._operacoes_a_comitar: dict = {}

    def salvar(self, objeto: BaseModel) -> None:
        """
          método do OBJETO para salvar a instância em banco.
        Args:
            instância do objeto
        Returns:
            Task.result()
        """
        # identifica o nome da classe do objeto
        # para identificar a coleção para salvar
        # TODO ver como pegar o nome da class com algum método do Pydantic
        collection_name = objeto.__repr_name__().lower()

        # adiciona a operação à lista a ser comitada
        self \
            ._operacoes_a_comitar \
            .setdefault(collection_name, []) \
            .append(UpdateOne({'_id': objeto.id},
                              {'$set': objeto.dict(by_alias=True)},  # salva no banco com _id ao invés de id
                              upsert=True))

    def deletar(self, objeto: BaseModel) -> None:
        """
          método do OBJETO para deletar a instância em banco.
        Args:
            instância do objeto
        Returns:
            pymongo.results.DeleteResult
        """

        # identifica o nome da classa do objeto
        # para identificar a coleção para salvar
        collection_name = objeto.__repr_name__().lower()

        # adiciona a operação à lista a ser comitada
        self \
            ._operacoes_a_comitar \
            .setdefault(collection_name, []) \
            .append(DeleteOne({'_id': objeto.id}))

    def comitar(self):
        """ Metodo EXCLUSIVO da classe, não chamar diretamento do objeto. """

        resultado = {}
        for collection, operacoes in self._operacoes_a_comitar.items():
            resultado[collection] = \
                MongoSetupSincrono \
                .db_client[collection] \
                .bulk_write(operacoes)

        return resultado
