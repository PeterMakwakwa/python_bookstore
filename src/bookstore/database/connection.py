# bookstore/database/connection.py
#
# C# equivalent: a MongoClient singleton you'd register in DI as IMongoClient.
# Python doesn't have DI containers built-in, so we use a module-level singleton
# instead — Python modules are cached after first import (effectively a singleton).

import os
from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv

# load_dotenv() reads your .env file and injects variables into os.environ
# C# equivalent: builder.Configuration.AddJsonFile("appsettings.json")
load_dotenv()

# -----------------------------------------------------------------------
# Module-level singleton — created once, reused across all imports
# -----------------------------------------------------------------------
_client: MongoClient | None = None   # The pipe: handles connection pooling automatically
_db: Database | None = None


def get_database() -> Database:
    """
    Returns the shared database instance.

    C# equivalent:
        private readonly IMongoDatabase _db;
        public MyService(IMongoClient client) {
            _db = client.GetDatabase("bookstore_db");
        }
    """
    global _client, _db

    if _db is None:
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB_NAME", "bookstore_db")

        # MongoClient manages a connection pool — same as the C# driver
        _client = MongoClient(uri)
        _db = _client[db_name]   # dict-style access is idiomatic in PyMongo

        # Quick connectivity check — raises ServerSelectionTimeoutError if Mongo is down
        _client.admin.command("ping")
        print(f"✅ Connected to MongoDB: {db_name}")

    return _db


def close_connection() -> None:
    """Call this on application shutdown. C# equivalent: client.Dispose()"""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        print("🔌 MongoDB connection closed.")
