#  Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

import pymongo #type: ignore
import os

#TODO migrar para MOTOR para usar asyncio com mongoDB

if not os.environ.get("MONGO_URL"):
    os.environ["MONGO_URL"] = 'localhost'

def conexaoBancoMongo(db: str, collection: str) -> pymongo:
    return pymongo.MongoClient(os.environ["MONGO_URL"], 27017)[db][collection]
