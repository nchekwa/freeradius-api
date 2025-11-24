import os
import sqlite3
import pytest
from contextlib import closing
from freeradius.database import init_db, cleanup_db, init_test_data

# Set environment variables for testing if not set
# This ensures local runs also use sqlite if they don't explicitly override it
if "DB_DRIVER" not in os.environ:
    os.environ["DB_DRIVER"] = "sqlite3"
if "DB_NAME" not in os.environ:
    os.environ["DB_NAME"] = "test_raddb.sqlite"
if "ITEMS_PER_PAGE" not in os.environ:
    os.environ["ITEMS_PER_PAGE"] = "100"


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Initialize the test database before running tests.
    This ensures the API tests have a database to talk to.
    """
    db_name = os.environ.get("DB_NAME", "test_raddb.sqlite")

    # Initialize schema
    init_db(db_name)

    # Populate test data
    with closing(sqlite3.connect(db_name)) as connection:
        init_test_data(connection)
        connection.commit()

    yield

    # Cleanup after tests
    cleanup_db(db_name)
