#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from collections import defaultdict

from pydantic import BaseModel
from pymongo import UpdateOne, DeleteOne
from Repositorio.Mongo.Configuracao.MongoSetupSincrono import MongoSetupSincrono


class MongoBasico:
    # atributo da classe que armazena as operações a serem comitadas
    _operacoes_a_comitar: defaultdict = defaultdict(list)

    def salvar(self: BaseModel) -> None:
        """
          método do OBJETO para salvar a instância em banco.
        Args:
            instância do objeto
        Returns:
            Task.result()
        """
        # identifica o nome da classa do objeto
        # para identificar a coleção para salvar
        #TODO ver como pegar o nome da class com algum método do Pydantic
        collection_name = self.__repr_name__().lower()

        # adiciona a operação à lista a ser comitada
        MongoBasico \
            ._operacoes_a_comitar[collection_name] \
            .append(UpdateOne({'_id': self.id},
                              {'$set': self.dict(by_alias=True)},  # salva no banco com _id ao invés de id
                              upsert=True))

    def deletar(self) -> None:
        """
          método do OBJETO para deletar a instância em banco.
        Args:
            instância do objeto
        Returns:
            pymongo.results.DeleteResult
        """

        # identifica o nome da classa do objeto
        # para identificar a coleção para salvar
        collection_name = self.__repr_name__().lower()

        # recupera o id do objeto e exclui do objeto
        _id = dict(self).get('id')

        # adiciona a operação à lista a ser comitada
        MongoBasico \
            ._operacoes_a_comitar[collection_name] \
            .append(DeleteOne({'_id': _id}))

    @staticmethod
    def comitar(self=None):
        """ Metodo EXCLUSIVO da classe, não chamar diretamento do objeto. """
        if self:
            return
        resultado = []
        for collection, operacoes in MongoBasico._operacoes_a_comitar.items():
            resultado.append(MongoSetupSincrono.db_client[collection].bulk_write(operacoes))

        MongoBasico._operacoes_a_comitar = defaultdict(list)

        return resultado
