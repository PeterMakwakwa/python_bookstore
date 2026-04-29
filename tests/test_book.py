# Unit tests for the Book dataclass — no DB needed, pure logic.
#
# C# equivalent: tests on a plain DTO using xUnit/NUnit/MSTest.
# pytest convention: test functions just need to start with `test_`.

from bson import ObjectId

from bookstore.models import Book


def test_to_dict_omits_id_for_new_book():
    """A brand-new Book (no id yet) should NOT include _id in its dict."""
    book = Book(title="Clean Code", author="Bob", genre="Programming", price=35.99)

    doc = book.to_dict()

    # `assert` is pytest's whole assertion API — no Assert.Equal/Assert.True boilerplate
    assert "_id" not in doc
    assert doc["title"] == "Clean Code"
    assert doc["price"] == 35.99
    assert doc["in_stock"] is True   # default value


def test_to_dict_includes_id_when_set():
    """An existing Book (with an id) should include _id as an ObjectId in its dict."""
    oid = ObjectId()
    book = Book(title="X", author="Y", genre="Z", price=1.0, id=str(oid))

    doc = book.to_dict()

    assert doc["_id"] == oid


def test_from_dict_round_trip():
    """from_dict should reconstruct a Book from a Mongo document."""
    oid = ObjectId()
    doc = {
        "_id": oid,
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": "Sci-Fi",
        "price": 14.99,
        "in_stock": False,
        "created_at": None,
    }

    book = Book.from_dict(doc)

    assert book.id == str(oid)
    assert book.title == "Dune"
    assert book.in_stock is False


def test_from_dict_defaults_in_stock_when_missing():
    """If the Mongo doc has no in_stock field, it should default to True."""
    doc = {
        "_id": ObjectId(),
        "title": "X",
        "author": "Y",
        "genre": "Z",
        "price": 1.0,
        # no in_stock, no created_at
    }

    book = Book.from_dict(doc)

    assert book.in_stock is True
