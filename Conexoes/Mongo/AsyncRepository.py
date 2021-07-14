#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from typing import Union, Any, Dict
import motor.motor_asyncio
import asyncio

class MongoRepository:

    client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    db = client.quickTest

    def find_one(self=None, parametro: Dict[Any] = None):

        if self:
            return self

        return await self.db['dev'].find_one({**parametro})

