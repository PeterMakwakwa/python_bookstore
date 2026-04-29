# 📚 Python + MongoDB Bookstore — C# Dev's Guide

A small CRUD demo wired up with the same patterns a C# developer would expect:
namespaces (Python packages), a repository class, dependency configuration in
a manifest file, and a separate test project.

## Project Structure

```
bookstore/
├── .env                              # Config (like appsettings.json) — gitignored
├── .gitignore                        # Excludes .venv, .env, *.egg-info, __pycache__
├── .vscode/
│   └── settings.json                 # Auto-configures pytest in VS Code
├── docker-compose.yml                # Spins up MongoDB + Mongo Express UI
├── pyproject.toml                    # Manifest (like .csproj) — deps + package metadata
├── README.md
├── src/
│   └── bookstore/                    # → namespace Bookstore
│       ├── __init__.py
│       ├── __main__.py               # Enables `python -m bookstore`
│       ├── main.py                   # Entry point (like Program.cs)
│       ├── models/                   # → namespace Bookstore.Models
│       │   ├── __init__.py
│       │   └── book.py               # @dataclass (like a C# record/POCO)
│       ├── repositories/             # → namespace Bookstore.Repositories
│       │   ├── __init__.py
│       │   └── book_repository.py    # CRUD repository
│       └── database/                 # → namespace Bookstore.Database
│           ├── __init__.py
│           └── connection.py         # MongoClient singleton
└── tests/                            # → like a Bookstore.Tests project
    ├── conftest.py                   # Shared pytest fixtures (like [SetUp]/[TearDown])
    ├── test_book.py                  # Unit tests — no DB required
    └── test_book_repository.py       # Integration tests — needs Mongo running
```

> **Folders + `__init__.py` = packages.** A package is Python's closest analogue
> to a C# namespace. Importing follows the folder path:
> `from bookstore.repositories import BookRepository`.

---

## Step 1 — Install Python (if needed)

```bash
python --version      # You want 3.10+
# Windows: install from https://python.org
# macOS:   brew install python
```

---

## Step 2 — Start MongoDB with Docker

```bash
cd bookstore
docker compose up -d
```

- MongoDB runs on **localhost:27017**
- Mongo Express UI runs on **http://localhost:8081** (visual database browser)

The compose file creates a root user `admin` / `secret`. The `.env` file uses
those credentials — keep it in sync if you change the compose file.

---

## Step 3 — Set Up Python Virtual Environment

```bash
# Create a virtual environment — like a scoped NuGet package cache per project
python -m venv .venv

# Activate it (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate it (macOS/Linux)
source .venv/bin/activate

# Your terminal prompt will change to show (.venv)
```

> **Why venv?** Without it, pip installs packages globally — like putting all NuGet
> packages in the GAC. venv isolates dependencies per project.

---

## Step 4 — Install the Project (editable mode)

```bash
# Installs runtime deps + makes `bookstore` importable from anywhere
pip install -e .

# Or include test/dev tools (pytest)
pip install -e ".[dev]"
```

> **What's `-e`?** Editable install. Equivalent to a project reference in a
> `.sln` rather than a NuGet package — code changes in `src/bookstore/` are
> picked up live without reinstalling.

---

## Step 5 — Run the App

```bash
python -m bookstore       # runs src/bookstore/__main__.py
# OR
bookstore                  # console script declared in pyproject.toml
```

Expected output:
```
✅ Connected to MongoDB: bookstore_db
✅ Indexes created.
🧹 Cleared existing books collection.

📚 --- SEEDING BOOKS ---
   ➕ Book(id=..., title='Clean Code', author='Robert C. Martin', price=$35.99)
   ...

📖 --- READ OPERATIONS ---
   All books (5 total): ...

✏️  --- UPDATE OPERATION ---
   Before: Book(... price=$35.99)
   After:  Book(... price=$29.99)

🗑️  --- DELETE OPERATION ---
   Deleted: True
   Verify (should be None): None

✅ All CRUD operations completed successfully!
```

---

## Step 6 — Run the Tests

Make sure docker compose is up (the integration tests need Mongo).

```bash
pytest                                  # all tests
pytest tests/test_book.py               # one file
pytest -k "search"                      # tests matching "search"
pytest -x                               # stop at first failure
```

In **VS Code**: open the Testing panel (flask icon in the sidebar). Tests are
auto-discovered via `.vscode/settings.json` and `pyproject.toml`. Click the ▶
next to any `def test_...` to run it, or right-click → **Debug Test** to step
through with breakpoints.

The `tests/test_book.py` file holds pure unit tests (no DB, always runnable).
The `tests/test_book_repository.py` file holds integration tests that hit a
disposable `bookstore_test_db` database, dropped after each test.

---

## Key Python → C# Concept Mapping

| Python                          | C# Equivalent                          |
|---------------------------------|----------------------------------------|
| Folder + `__init__.py`          | `namespace`                            |
| `pyproject.toml`                | `.csproj`                              |
| `pip install -e .`              | Project reference in a `.sln`          |
| `*.egg-info/`                   | `obj/` build metadata                  |
| `pytest` + `conftest.py`        | xUnit/NUnit + `[SetUp]/[TearDown]`     |
| `@pytest.fixture`               | A test fixture or `[ClassFixture]`     |
| `@dataclass`                    | `record` / POCO class                  |
| `Optional[str]`                 | `string?` / nullable reference type    |
| `list[Book]`                    | `List<Book>`                           |
| `dict`                          | `Dictionary<string, object>`           |
| `__init__(self)`                | Constructor                            |
| `@classmethod`                  | `static` factory method                |
| `__repr__`                      | `ToString()`                           |
| `if __name__ == "__main__"`     | `static void Main()`                   |
| `try/except/finally`            | `try/catch/finally`                    |
| `None`                          | `null`                                 |
| `f"Hello {name}"`               | `$"Hello {name}"`                      |
| `python-dotenv`                 | `IConfiguration` / `appsettings.json`  |
| `pymongo`                       | `MongoDB.Driver` NuGet package         |
| `.venv`                         | per-project NuGet cache                |

---

## Stop MongoDB

```bash
docker compose down          # Stop containers (data persists in volume)
docker compose down -v       # Stop + wipe all data
```
