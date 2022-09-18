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
            if settings.current_env in ['production']:
                MongoSetupSincrono.client = MongoClient(settings.db_address,
                                                        tls=True,
                                                        tlsCertificateKeyFile='banco_dados/mongodb/configuracao/X509-cert.pem',
                                                        server_api=ServerApi('1'))

    @staticmethod
    async def close_db():
        """Close database connection."""
        await MongoSetupSincrono.client.close()
