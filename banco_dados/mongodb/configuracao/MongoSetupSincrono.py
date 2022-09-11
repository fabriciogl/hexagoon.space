from pymongo import MongoClient
from pymongo.server_api import ServerApi

from config import settings


class MongoSetupSincrono:
    client: MongoClient = None

    @staticmethod
    def get_db_client() -> MongoClient:
        """Return database client instance."""
        return MongoSetupSincrono.client[settings.db_name]

    @staticmethod
    def connect_client():
        """Create database connection."""
        if not MongoSetupSincrono.client:
            if settings.current_env in ['testing', 'development']:
                MongoSetupSincrono.client = MongoClient('localhost', 27017)
            if settings.current_env in ['development']:
                uri = "mongodb+srv://hexagoon.j6rb8f9.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
                MongoSetupSincrono.client = MongoClient(uri,
                                                        tls=True,
                                                        tlsCertificateKeyFile='banco_dados/mongodb/configuracao/X509-cert.pem',
                                                        server_api=ServerApi('1'))

    @staticmethod
    async def close_db():
        """Close database connection."""
        await MongoSetupSincrono.client.close()
