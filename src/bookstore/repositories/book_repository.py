# bookstore/repositories/book_repository.py
#
# C# equivalent: a Repository class injected with IMongoCollection<Book>.
# In Python, a class is just a class — no interfaces needed (duck typing).
# If you want an interface/contract, use Python's `abc` module (Abstract Base Class).

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Optional

from bookstore.models.book import Book


class BookRepository:
    """
    Handles all MongoDB operations for the Book collection.

    C# equivalent:
        public class BookRepository : IBookRepository {
            private readonly IMongoCollection<Book> _collection;
            public BookRepository(IMongoDatabase db) {
                _collection = db.GetCollection<Book>("books");
            }
        }
    """

    def __init__(self, db: Database):
        # Type hints (Database, Collection) are optional but great for IDE support
        # C# equivalent: IMongoCollection<Book> — the type hint IS the contract here
        self._collection: Collection = db["books"]

    # ==================================================================
    # CREATE
    # ==================================================================
    def create(self, book: Book) -> Book:
        """
        Inserts a new book document.

        C# equivalent:
            await _collection.InsertOneAsync(book);
        PyMongo is synchronous by default — for async use 'motor' (the async driver).
        """
        doc = book.to_dict()
        result = self._collection.insert_one(doc)

        # insert_one mutates 'doc' in place, adding '_id' — grab it back
        book.id = str(result.inserted_id)
        print(f"✅ Created book with id: {book.id}")
        return book

    # ==================================================================
    # READ — get by ID
    # ==================================================================
    def get_by_id(self, book_id: str) -> Optional[Book]:
        """
        Finds a single document by its _id.

        C# equivalent:
            var filter = Builders<Book>.Filter.Eq(b => b.Id, ObjectId.Parse(id));
            return await _collection.Find(filter).FirstOrDefaultAsync();
        """
        # ObjectId() parses the string — raises InvalidId if malformed
        doc = self._collection.find_one({"_id": ObjectId(book_id)})

        # Pythonic None check — no null-conditional operator (?.) needed
        # The 'if doc' check works because an empty dict is falsy in Python
        return Book.from_dict(doc) if doc else None

    # ==================================================================
    # READ — get all (with optional filtering)
    # ==================================================================
    def get_all(self, filter: Optional[dict] = None) -> list[Book]:
        """
        Returns all books, with an optional filter dict.

        C# equivalent:
            var filter = Builders<Book>.Filter.Empty;
            var books = await _collection.Find(filter).ToListAsync();

        Python tip: passing None as default and using 'or {}' avoids the
        mutable default argument trap (a common Python gotcha — never use
        def get_all(self, filter={}) as the dict is shared across calls!).
        """
        cursor = self._collection.find(filter or {})

        # List comprehension — C# equivalent: cursor.Select(Book.from_dict).ToList()
        return [Book.from_dict(doc) for doc in cursor]

    # ==================================================================
    # READ — find with query + sort + pagination
    # ==================================================================
    def search(
        self,
        genre: Optional[str] = None,
        max_price: Optional[float] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Book]:
        """
        Flexible search with optional filters, sorting, and pagination.

        C# equivalent:
            var filter = Builders<Book>.Filter.And(
                genre != null ? Builders<Book>.Filter.Eq(b => b.Genre, genre) : FilterDefinition<Book>.Empty,
                maxPrice.HasValue ? Builders<Book>.Filter.Lte(b => b.Price, maxPrice.Value) : ...
            );
            return await _collection.Find(filter)
                .SortBy(b => b.Title)
                .Skip(skip).Limit(limit)
                .ToListAsync();
        """
        query: dict = {}

        if genre:
            query["genre"] = genre                    # Exact match

        if max_price is not None:
            query["price"] = {"$lte": max_price}      # $lte = less than or equal

        cursor = (
            self._collection
            .find(query)
            .sort("title", 1)     # 1 = ascending,  -1 = descending
            .skip(skip)
            .limit(limit)
        )

        return [Book.from_dict(doc) for doc in cursor]

    # ==================================================================
    # UPDATE — replace specific fields
    # ==================================================================
    def update(self, book_id: str, updates: dict) -> Optional[Book]:
        """
        Updates specific fields using $set — like a PATCH endpoint.

        C# equivalent:
            var update = Builders<Book>.Update.Set(b => b.Price, newPrice);
            await _collection.UpdateOneAsync(filter, update);
        """
        result = self._collection.find_one_and_update(
            {"_id": ObjectId(book_id)},
            {"$set": updates},               # Only the provided fields are changed
            return_document=True,            # Return the UPDATED document
        )

        if result is None:
            print(f"⚠️  No book found with id: {book_id}")
            return None

        print(f"✅ Updated book: {book_id}")
        return Book.from_dict(result)

    # ==================================================================
    # DELETE
    # ==================================================================
    def delete(self, book_id: str) -> bool:
        """
        Deletes a document by ID. Returns True if deleted, False if not found.

        C# equivalent:
            var result = await _collection.DeleteOneAsync(filter);
            return result.DeletedCount > 0;
        """
        result = self._collection.delete_one({"_id": ObjectId(book_id)})

        deleted = result.deleted_count > 0
        if deleted:
            print(f"🗑️  Deleted book: {book_id}")
        else:
            print(f"⚠️  No book found with id: {book_id}")

        return deleted

    # ==================================================================
    # UTILITY — create an index
    # ==================================================================
    def create_indexes(self) -> None:
        """
        C# equivalent:
            var indexKeys = Builders<Book>.IndexKeys.Ascending(b => b.Author);
            await _collection.Indexes.CreateOneAsync(new CreateIndexModel<Book>(indexKeys));
        """
        self._collection.create_index("author")
        self._collection.create_index([("title", 1), ("genre", 1)])  # Compound index
        print("✅ Indexes created.")
