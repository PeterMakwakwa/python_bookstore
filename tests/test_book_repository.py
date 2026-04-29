# Integration tests for BookRepository — these hit a real MongoDB.
#
# Requires `docker compose up -d` to be running (or any reachable Mongo).
# Each test gets a fresh `repo` fixture from conftest.py, backed by a
# disposable `bookstore_test_db` database that's dropped after the test.
#
# C# equivalent: integration tests using a TestContainer or ephemeral DB.

from bson import ObjectId

from bookstore.models import Book


# -------------------- CREATE --------------------

def test_create_assigns_id(repo):
    """create() should return a Book with a populated id (assigned by Mongo)."""
    book = repo.create(Book(title="T", author="A", genre="G", price=1.0))

    assert book.id is not None
    # ObjectId() will raise InvalidId if the string isn't a valid ObjectId
    ObjectId(book.id)


# -------------------- READ --------------------

def test_get_by_id_returns_inserted_book(repo):
    inserted = repo.create(Book(title="Clean Code", author="Bob", genre="Prog", price=35.99))

    found = repo.get_by_id(inserted.id)

    assert found is not None
    assert found.title == "Clean Code"
    assert found.id == inserted.id


def test_get_by_id_returns_none_when_not_found(repo):
    """A valid-shaped id that doesn't exist in the DB should return None, not raise."""
    assert repo.get_by_id(str(ObjectId())) is None


def test_get_all_returns_every_book(repo):
    repo.create(Book(title="A", author="X", genre="G", price=1.0))
    repo.create(Book(title="B", author="Y", genre="G", price=2.0))

    all_books = repo.get_all()

    assert len(all_books) == 2


# -------------------- SEARCH --------------------

def test_search_filters_by_genre(repo):
    repo.create(Book(title="Dune",       author="Herbert", genre="Sci-Fi",      price=14.99))
    repo.create(Book(title="Clean Code", author="Martin",  genre="Programming", price=35.99))

    sci_fi = repo.search(genre="Sci-Fi")

    assert len(sci_fi) == 1
    assert sci_fi[0].title == "Dune"


def test_search_filters_by_max_price(repo):
    repo.create(Book(title="Cheap",  author="X", genre="G", price=5.0))
    repo.create(Book(title="Pricey", author="Y", genre="G", price=50.0))

    affordable = repo.search(max_price=10.0)

    assert len(affordable) == 1
    assert affordable[0].title == "Cheap"


def test_search_sorts_by_title_ascending(repo):
    repo.create(Book(title="Zebra",   author="X", genre="G", price=1.0))
    repo.create(Book(title="Apple",   author="Y", genre="G", price=1.0))
    repo.create(Book(title="Mango",   author="Z", genre="G", price=1.0))

    results = repo.search()

    assert [b.title for b in results] == ["Apple", "Mango", "Zebra"]


# -------------------- UPDATE --------------------

def test_update_modifies_only_given_fields(repo):
    book = repo.create(Book(title="T", author="A", genre="G", price=1.0))

    updated = repo.update(book.id, {"price": 99.0})

    assert updated.price == 99.0
    assert updated.title == "T"        # untouched
    assert updated.author == "A"       # untouched


def test_update_returns_none_when_book_missing(repo):
    assert repo.update(str(ObjectId()), {"price": 1.0}) is None


# -------------------- DELETE --------------------

def test_delete_removes_book(repo):
    book = repo.create(Book(title="T", author="A", genre="G", price=1.0))

    assert repo.delete(book.id) is True
    assert repo.get_by_id(book.id) is None


def test_delete_returns_false_when_book_missing(repo):
    assert repo.delete(str(ObjectId())) is False
