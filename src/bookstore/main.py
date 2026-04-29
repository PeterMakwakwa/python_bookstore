# bookstore/main.py — application entry point
#
# C# equivalent: Program.cs / your static void Main() or top-level statements.

import sys

from bookstore.database import get_database, close_connection
from bookstore.models import Book
from bookstore.repositories import BookRepository


# Windows console defaults to cp1252 on Python <3.15 — emoji prints would crash.
# Force UTF-8 on stdout/stderr so output works without `-X utf8` or PYTHONUTF8=1.
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def seed_books(repo: BookRepository) -> list[Book]:
    """Insert some sample data to work with."""
    print("\n📚 --- SEEDING BOOKS ---")

    books_data = [
        Book(title="Clean Code",          author="Robert C. Martin", genre="Programming", price=35.99),
        Book(title="The Pragmatic Programmer", author="Hunt & Thomas", genre="Programming", price=42.00),
        Book(title="Design Patterns",     author="Gang of Four",      genre="Programming", price=55.00),
        Book(title="Dune",                author="Frank Herbert",     genre="Sci-Fi",      price=14.99),
        Book(title="Foundation",          author="Isaac Asimov",      genre="Sci-Fi",      price=12.50),
    ]

    # List comprehension to insert all books and collect results
    # C# equivalent: books.Select(b => repo.Create(b)).ToList()
    created = [repo.create(b) for b in books_data]

    for book in created:
        print(f"   ➕ {book}")

    return created


def demo_read(repo: BookRepository) -> None:
    """Demonstrate various read patterns."""
    print("\n📖 --- READ OPERATIONS ---")

    # --- Get all ---
    all_books = repo.get_all()
    print(f"\n All books ({len(all_books)} total):")
    for b in all_books:
        print(f"   {b}")

    # --- Get by ID ---
    first_id = all_books[0].id
    found = repo.get_by_id(first_id)
    print(f"\n Get by ID '{first_id}':\n   {found}")

    # --- Search with filters ---
    # Python keyword arguments make calls self-documenting — no positional guessing
    programming_books = repo.search(genre="Programming", max_price=45.00)
    print(f"\n Programming books under $45 ({len(programming_books)} found):")
    for b in programming_books:
        print(f"   {b}")


def demo_update(repo: BookRepository, book: Book) -> None:
    """Demonstrate partial updates ($set)."""
    print("\n✏️  --- UPDATE OPERATION ---")

    print(f" Before: {book}")

    # Pass only the fields you want to change — like a PATCH request
    # C# equivalent: new UpdateDefinition using Builders<Book>.Update.Set(...)
    updated = repo.update(book.id, {
        "price": 29.99,
        "in_stock": False,
    })

    print(f" After:  {updated}")


def demo_delete(repo: BookRepository, book: Book) -> None:
    """Demonstrate delete."""
    print("\n🗑️  --- DELETE OPERATION ---")

    success = repo.delete(book.id)
    print(f" Deleted: {success}")

    # Verify it's gone
    gone = repo.get_by_id(book.id)
    print(f" Verify (should be None): {gone}")


def main() -> None:
    """Application entry point — callable from __main__.py or programmatically."""
    db = None
    try:
        # --- Setup ---
        db = get_database()
        repo = BookRepository(db)
        repo.create_indexes()

        # --- Wipe previous run's data for a clean demo ---
        db["books"].drop()
        print("🧹 Cleared existing books collection.")

        # --- Run demos ---
        created_books = seed_books(repo)
        demo_read(repo)
        demo_update(repo, created_books[0])   # Update 'Clean Code'
        demo_delete(repo, created_books[-1])  # Delete 'Foundation'

        print("\n✅ All CRUD operations completed successfully!")

    except Exception as e:
        # Python exceptions work the same as C# — you can catch specific types:
        # except ConnectionError as e: ...
        # except ValueError as e: ...
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        raise   # Re-raise — equivalent to C# 'throw;' (preserves stack trace)

    finally:
        # finally runs regardless of success or exception — same as C#
        close_connection()
