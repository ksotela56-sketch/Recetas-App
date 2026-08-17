"""Repositorio de acceso a datos para categorías."""

import sqlite3
from dataclasses import dataclass


@dataclass
class Category:
    id: int
    nombre: str


def create(connection: sqlite3.Connection, nombre: str) -> Category:
    cursor = connection.execute(
        "INSERT INTO category (nombre) VALUES (?)", (nombre,)
    )
    connection.commit()
    return Category(id=cursor.lastrowid, nombre=nombre)


def list_all(connection: sqlite3.Connection) -> list[Category]:
    rows = connection.execute("SELECT id, nombre FROM category ORDER BY nombre").fetchall()
    return [Category(id=row["id"], nombre=row["nombre"]) for row in rows]


def get_by_id(connection: sqlite3.Connection, category_id: int) -> Category | None:
    row = connection.execute(
        "SELECT id, nombre FROM category WHERE id = ?", (category_id,)
    ).fetchone()
    return Category(id=row["id"], nombre=row["nombre"]) if row else None


def delete(connection: sqlite3.Connection, category_id: int) -> None:
    connection.execute("DELETE FROM category WHERE id = ?", (category_id,))
    connection.commit()
