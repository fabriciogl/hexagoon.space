from motor.motor_asyncio import AsyncIOMotorClient


class MongoSetupAssincrono:
    db_client: AsyncIOMotorClient = None

    @staticmethod
    def get_db_client() -> AsyncIOMotorClient:
        """Return database client instance."""
        return MongoSetupAssincrono.db_client

    @staticmethod
    async def connect_db():
        """Create database connection."""
        MongoSetupAssincrono.db_client = AsyncIOMotorClient('localhost', 27017).quickTest

    @staticmethod
    async def close_db():
        """Close database connection."""
        await MongoSetupAssincrono.db_client.close()
