"""Conexión y esquema de la base de datos SQLite."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[3] / "data" / "recetas.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS category (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredient (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS recipe (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre             TEXT NOT NULL,
    descripcion        TEXT,
    tiempo_preparacion INTEGER,
    porciones          INTEGER,
    categoria_id       INTEGER REFERENCES category(id) ON DELETE SET NULL,
    created_at         TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS recipe_ingredient (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id     INTEGER NOT NULL REFERENCES recipe(id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredient(id) ON DELETE CASCADE,
    cantidad      REAL,
    unidad        TEXT
);

CREATE TABLE IF NOT EXISTS step (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id     INTEGER NOT NULL REFERENCES recipe(id) ON DELETE CASCADE,
    numero_orden  INTEGER NOT NULL,
    descripcion   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS meal_plan (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre       TEXT NOT NULL,
    fecha_inicio TEXT
);

CREATE TABLE IF NOT EXISTS meal_plan_entry (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_plan_id  INTEGER NOT NULL REFERENCES meal_plan(id) ON DELETE CASCADE,
    dia_semana    INTEGER NOT NULL,
    tipo_comida   TEXT NOT NULL,
    recipe_id     INTEGER NOT NULL REFERENCES recipe(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shopping_list (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_plan_id INTEGER REFERENCES meal_plan(id) ON DELETE SET NULL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS shopping_list_item (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    shopping_list_id  INTEGER NOT NULL REFERENCES shopping_list(id) ON DELETE CASCADE,
    ingredient_id     INTEGER NOT NULL REFERENCES ingredient(id) ON DELETE CASCADE,
    cantidad_total    REAL,
    unidad            TEXT,
    comprado          INTEGER NOT NULL DEFAULT 0
);
"""


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Abre una conexión a la base de datos con claves foráneas activadas."""
    db_path = db_path or DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def db_session(db_path: Path | None = None):
    """Context manager que abre una conexión y la cierra al salir del bloque."""
    connection = get_connection(db_path)
    try:
        yield connection
    finally:
        connection.close()


def init_db(db_path: Path | None = None) -> None:
    """Crea el esquema de base de datos si no existe."""
    connection = get_connection(db_path)
    try:
        connection.executescript(SCHEMA)
        connection.commit()
    finally:
        connection.close()
