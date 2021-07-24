from pymongo import MongoClient

class MongoSetupSincrono:
    db_client: MongoClient = None

    @staticmethod
    def get_db_client() -> MongoClient:
        """Return database client instance."""
        return MongoSetupSincrono.db_client

    @staticmethod
    async def connect_db():
        """Create database connection."""
        MongoSetupSincrono.db_client = MongoClient('localhost', 27017).quickTest

    @staticmethod
    async def close_db():
        """Close database connection."""
        await MongoSetupSincrono.db_client.close()
