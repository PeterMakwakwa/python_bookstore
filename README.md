# 📚 Python + MongoDB Bookstore — C# Dev's Guide

## Project Structure

```
bookstore/
├── docker-compose.yml          # Spins up MongoDB + Mongo Express UI
├── .env                        # Config (like appsettings.json)
├── requirements.txt            # Dependencies (like .csproj PackageReferences)
├── main.py                     # Entry point (like Program.cs)
├── database/
│   └── connection.py           # MongoClient singleton
├── models/
│   └── book.py                 # @dataclass (like a C# record/POCO)
└── repositories/
    └── book_repository.py      # CRUD repository (like your C# Repository pattern)
```

---

## Step 1 — Install Python (if needed)

```bash
python3 --version     # You want 3.10+
# Install via https://python.org or via brew (macOS): brew install python
```

---

## Step 2 — Start MongoDB with Docker

```bash
cd bookstore
docker compose up -d
```

- MongoDB runs on **localhost:27017**
- Mongo Express UI runs on **http://localhost:8081** (visual database browser)

---

## Step 3 — Set Up Python Virtual Environment

```bash
# Create a virtual environment — like a scoped NuGet package cache per project
python3 -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate

# Your terminal prompt will change to show (.venv)
```

> **Why venv?** Without it, pip installs packages globally — like putting all NuGet
> packages in the GAC. venv isolates dependencies per project.

---

## Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5 — Run the App

```bash
python main.py
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

## Key Python → C# Concept Mapping

| Python                          | C# Equivalent                          |
|---------------------------------|----------------------------------------|
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
| `f"Hello {name}"`              | `$"Hello {name}"`                      |
| `module/__init__.py`            | namespace declaration                  |
| `requirements.txt` + `pip`     | `.csproj` + NuGet                      |
| `.venv`                         | per-project NuGet cache                |
| `python-dotenv`                 | `IConfiguration` / `appsettings.json`  |
| `pymongo`                       | `MongoDB.Driver` NuGet package         |

---

## Stop MongoDB

```bash
docker compose down          # Stop containers (data persists in volume)
docker compose down -v       # Stop + wipe all data
```
