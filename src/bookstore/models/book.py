# bookstore/models/book.py
#
# C# equivalent: a record or class that maps to a MongoDB document.
# In C# you'd use [BsonElement] attributes and BsonDocument serialization.
# In Python we use @dataclass (or Pydantic for validation — think FluentValidation).

from dataclasses import dataclass, field
from datetime import datetime, timezone
from bson import ObjectId      # ObjectId lives in the 'bson' package (installed with pymongo)
from typing import Optional


# -----------------------------------------------------------------------
# @dataclass is like a C# record — auto-generates __init__, __repr__, __eq__
# -----------------------------------------------------------------------
@dataclass
class Book:
    title: str
    author: str
    genre: str
    price: float
    in_stock: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # _id is Optional because MongoDB assigns it on insert — we don't set it ourselves
    # C# equivalent: public ObjectId Id { get; set; }
    id: Optional[str] = field(default=None)

    # ------------------------------------------------------------------
    # to_dict() — serialize to a plain dict for PyMongo
    # C# equivalent: the BSON driver serializes your class automatically.
    # PyMongo works with plain dicts, so we convert manually (or use Pydantic).
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        doc = {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "price": self.price,
            "in_stock": self.in_stock,
            "created_at": self.created_at,
        }
        # Only include _id if it already exists (i.e. this is an existing document)
        if self.id:
            doc["_id"] = ObjectId(self.id)
        return doc

    # ------------------------------------------------------------------
    # @classmethod is a static factory method — like a C# static constructor
    # from_dict() converts a raw MongoDB document (dict) back into a Book
    # ------------------------------------------------------------------
    @classmethod
    def from_dict(cls, doc: dict) -> "Book":
        return cls(
            id=str(doc["_id"]),           # ObjectId → string (JSON-friendly)
            title=doc["title"],
            author=doc["author"],
            genre=doc["genre"],
            price=doc["price"],
            in_stock=doc.get("in_stock", True),     # .get() = safe access with default
            created_at=doc.get("created_at"),
        )

    def __repr__(self) -> str:
        # __repr__ is like C# ToString()
        return (
            f"Book(id={self.id}, title='{self.title}', "
            f"author='{self.author}', price=${self.price:.2f})"
        )
