from pymongo import MongoClient

from config import settings


class MongoSetupSincrono:
    client: MongoClient = None

    @staticmethod
    def get_db_client() -> MongoClient:
        """Return database client instance."""
        return MongoSetupSincrono.client[settings.db_name]

    @staticmethod
    async def connect_client():
        """Create database connection."""
        if not MongoSetupSincrono.client:
            MongoSetupSincrono.client = MongoClient('localhost', 27017)

    @staticmethod
    async def close_db():
        """Close database connection."""
        await MongoSetupSincrono.client.close()
