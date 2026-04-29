# C# equivalent: namespace Bookstore.Database { }
from bookstore.database.connection import get_database, close_connection

__all__ = ["get_database", "close_connection"]
