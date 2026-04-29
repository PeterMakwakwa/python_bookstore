# conftest.py — pytest's "shared setup" file.
#
# C# equivalent: a base TestFixture class with [SetUp]/[TearDown] methods.
# Anything defined here is auto-discovered by pytest for files in this folder
# and below — you don't import it manually.
#
# Fixtures replace the [SetUp] pattern: a function declares the resource a test
# needs, and pytest wires it up when the test asks for it by parameter name.

import os
import sys

import pytest
from dotenv import load_dotenv
from pymongo import MongoClient

from bookstore.repositories import BookRepository

# Force UTF-8 stdout so emoji prints from the repo don't crash on Windows
# when pytest captures output. C# equivalent: setting Console.OutputEncoding.
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

load_dotenv()

TEST_DB_NAME = "bookstore_test_db"   # Separate from the real bookstore_db


@pytest.fixture(scope="session")
def mongo_client():
    """
    A MongoClient shared across the whole test session.

    scope="session" means: created once for the whole pytest run, reused everywhere.
    C# equivalent: a [OneTimeSetUp] / [ClassFixture] resource.
    """
    uri = os.getenv("MONGO_URI", "mongodb://admin:secret@localhost:27017/?authSource=admin")
    client = MongoClient(uri, serverSelectionTimeoutMS=2000)
    client.admin.command("ping")    # Fail fast if Mongo isn't running
    yield client                    # Tests run here
    client.close()                  # Teardown after all tests finish


@pytest.fixture
def db(mongo_client):
    """
    A fresh test database for each test, dropped afterward.

    Default scope is "function" — a new one per test, so tests are isolated.
    C# equivalent: [SetUp] creating a fresh in-memory DB and [TearDown] cleaning up.
    """
    test_db = mongo_client[TEST_DB_NAME]
    yield test_db
    mongo_client.drop_database(TEST_DB_NAME)


@pytest.fixture
def repo(db):
    """A BookRepository wired up to the throwaway test DB."""
    return BookRepository(db)
