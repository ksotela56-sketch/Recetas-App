"""Repositorio de acceso a datos para ingredientes."""

import sqlite3
from dataclasses import dataclass


@dataclass
class Ingredient:
    id: int
    nombre: str


def get_or_create(connection: sqlite3.Connection, nombre: str) -> Ingredient:
    row = connection.execute(
        "SELECT id, nombre FROM ingredient WHERE nombre = ?", (nombre,)
    ).fetchone()
    if row:
        return Ingredient(id=row["id"], nombre=row["nombre"])
    cursor = connection.execute(
        "INSERT INTO ingredient (nombre) VALUES (?)", (nombre,)
    )
    connection.commit()
    return Ingredient(id=cursor.lastrowid, nombre=nombre)


def list_all(connection: sqlite3.Connection) -> list[Ingredient]:
    rows = connection.execute("SELECT id, nombre FROM ingredient ORDER BY nombre").fetchall()
    return [Ingredient(id=row["id"], nombre=row["nombre"]) for row in rows]


def get_by_id(connection: sqlite3.Connection, ingredient_id: int) -> Ingredient | None:
    row = connection.execute(
        "SELECT id, nombre FROM ingredient WHERE id = ?", (ingredient_id,)
    ).fetchone()
    return Ingredient(id=row["id"], nombre=row["nombre"]) if row else None
