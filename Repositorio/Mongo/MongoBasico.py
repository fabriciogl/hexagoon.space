#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from asyncio import Task
from typing import Union, Any, Dict
import motor.motor_asyncio
import asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.quickTest


class MongoBasico:

    def salvar(self) -> Task.result:
        """
          método do OBJETO para salvar a instância em banco.
        Args:
            instância do objeto
        Returns:
            Task.result()
        """
        # identifica o nome da classa do objeto
        # para identificar a coleção para salvar
        object_name = self.__repr_name__().lower()

        # recupera o id do objeto e exclui do objeto
        id = dict(self).get('id')
        self.__dict__.pop('id')

        # salva em banco
        return db[object_name].update_one({'_id': id},
                                          {'$set': self.__dict__},
                                          upsert=True)

        # Funciona com loop.run_until_complete()
        # return await db['dev'].update_one({'id': self.__dict__['id']},
        #                                {'$set': self.__dict__},
        #                                upsert=True)

    def deletar(self) -> Task.result:
        """
          método do OBJETO para deletar a instância em banco.
        Args:
            instância do objeto
        Returns:
            Task.result()
        """

        # identifica o nome da classa do objeto
        # para identificar a coleção para salvar
        object_name = self.__repr_name__().lower()

        # recupera o id do objeto e exclui do objeto
        id = dict(self).get('id')

        # salva em banco
        return db[object_name].delete_one({'_id': id})
