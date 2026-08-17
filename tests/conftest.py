import sqlite3

import pytest

from recetas_app.models.database import SCHEMA


@pytest.fixture
def connection():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.commit()
    yield conn
    conn.close()
