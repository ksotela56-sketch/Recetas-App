"""Repositorio de acceso a datos para recetas (receta + ingredientes + pasos)."""

import sqlite3
from dataclasses import dataclass, field

from recetas_app.models import ingredient as ingredient_model


@dataclass
class RecipeIngredientItem:
    ingredient_id: int
    nombre: str
    cantidad: float | None
    unidad: str | None


@dataclass
class RecipeStep:
    numero_orden: int
    descripcion: str


@dataclass
class RecipeSummary:
    id: int
    nombre: str
    tiempo_preparacion: int | None
    categoria_nombre: str | None


@dataclass
class RecipeDetail:
    id: int
    nombre: str
    descripcion: str | None
    tiempo_preparacion: int | None
    porciones: int | None
    categoria_id: int | None
    categoria_nombre: str | None
    ingredientes: list[RecipeIngredientItem] = field(default_factory=list)
    pasos: list[RecipeStep] = field(default_factory=list)


def create(
    connection: sqlite3.Connection,
    nombre: str,
    descripcion: str | None,
    tiempo_preparacion: int | None,
    porciones: int | None,
    categoria_id: int | None,
    ingredientes: list[tuple[str, float | None, str | None]],
    pasos: list[str],
) -> int:
    """Crea una receta junto con sus ingredientes y pasos. Devuelve el id creado."""
    cursor = connection.execute(
        """INSERT INTO recipe (nombre, descripcion, tiempo_preparacion, porciones, categoria_id)
           VALUES (?, ?, ?, ?, ?)""",
        (nombre, descripcion, tiempo_preparacion, porciones, categoria_id),
    )
    recipe_id = cursor.lastrowid
    _replace_ingredients(connection, recipe_id, ingredientes)
    _replace_steps(connection, recipe_id, pasos)
    connection.commit()
    return recipe_id


def update(
    connection: sqlite3.Connection,
    recipe_id: int,
    nombre: str,
    descripcion: str | None,
    tiempo_preparacion: int | None,
    porciones: int | None,
    categoria_id: int | None,
    ingredientes: list[tuple[str, float | None, str | None]],
    pasos: list[str],
) -> None:
    """Actualiza los datos generales de una receta y reemplaza sus ingredientes y pasos."""
    connection.execute(
        """UPDATE recipe
           SET nombre = ?, descripcion = ?, tiempo_preparacion = ?, porciones = ?, categoria_id = ?
           WHERE id = ?""",
        (nombre, descripcion, tiempo_preparacion, porciones, categoria_id, recipe_id),
    )
    _replace_ingredients(connection, recipe_id, ingredientes)
    _replace_steps(connection, recipe_id, pasos)
    connection.commit()


def delete(connection: sqlite3.Connection, recipe_id: int) -> None:
    connection.execute("DELETE FROM recipe WHERE id = ?", (recipe_id,))
    connection.commit()


def list_all(connection: sqlite3.Connection) -> list[RecipeSummary]:
    rows = connection.execute(
        """SELECT r.id, r.nombre, r.tiempo_preparacion, c.nombre AS categoria_nombre
           FROM recipe r
           LEFT JOIN category c ON c.id = r.categoria_id
           ORDER BY r.nombre"""
    ).fetchall()
    return [_row_to_summary(row) for row in rows]


def get_detail(connection: sqlite3.Connection, recipe_id: int) -> RecipeDetail | None:
    row = connection.execute(
        """SELECT r.id, r.nombre, r.descripcion, r.tiempo_preparacion, r.porciones,
                  r.categoria_id, c.nombre AS categoria_nombre
           FROM recipe r
           LEFT JOIN category c ON c.id = r.categoria_id
           WHERE r.id = ?""",
        (recipe_id,),
    ).fetchone()
    if not row:
        return None

    ingredient_rows = connection.execute(
        """SELECT i.id AS ingredient_id, i.nombre, ri.cantidad, ri.unidad
           FROM recipe_ingredient ri
           JOIN ingredient i ON i.id = ri.ingredient_id
           WHERE ri.recipe_id = ?
           ORDER BY i.nombre""",
        (recipe_id,),
    ).fetchall()
    step_rows = connection.execute(
        """SELECT numero_orden, descripcion FROM step
           WHERE recipe_id = ? ORDER BY numero_orden""",
        (recipe_id,),
    ).fetchall()

    return RecipeDetail(
        id=row["id"],
        nombre=row["nombre"],
        descripcion=row["descripcion"],
        tiempo_preparacion=row["tiempo_preparacion"],
        porciones=row["porciones"],
        categoria_id=row["categoria_id"],
        categoria_nombre=row["categoria_nombre"],
        ingredientes=[
            RecipeIngredientItem(
                ingredient_id=r["ingredient_id"],
                nombre=r["nombre"],
                cantidad=r["cantidad"],
                unidad=r["unidad"],
            )
            for r in ingredient_rows
        ],
        pasos=[RecipeStep(numero_orden=r["numero_orden"], descripcion=r["descripcion"]) for r in step_rows],
    )


def search_by_name(connection: sqlite3.Connection, texto: str) -> list[RecipeSummary]:
    rows = connection.execute(
        """SELECT r.id, r.nombre, r.tiempo_preparacion, c.nombre AS categoria_nombre
           FROM recipe r
           LEFT JOIN category c ON c.id = r.categoria_id
           WHERE r.nombre LIKE ?
           ORDER BY r.nombre""",
        (f"%{texto}%",),
    ).fetchall()
    return [_row_to_summary(row) for row in rows]


def search_by_category(connection: sqlite3.Connection, categoria_id: int) -> list[RecipeSummary]:
    rows = connection.execute(
        """SELECT r.id, r.nombre, r.tiempo_preparacion, c.nombre AS categoria_nombre
           FROM recipe r
           LEFT JOIN category c ON c.id = r.categoria_id
           WHERE r.categoria_id = ?
           ORDER BY r.nombre""",
        (categoria_id,),
    ).fetchall()
    return [_row_to_summary(row) for row in rows]


def search_by_ingredient(connection: sqlite3.Connection, texto: str) -> list[RecipeSummary]:
    rows = connection.execute(
        """SELECT DISTINCT r.id, r.nombre, r.tiempo_preparacion, c.nombre AS categoria_nombre
           FROM recipe r
           LEFT JOIN category c ON c.id = r.categoria_id
           JOIN recipe_ingredient ri ON ri.recipe_id = r.id
           JOIN ingredient i ON i.id = ri.ingredient_id
           WHERE i.nombre LIKE ?
           ORDER BY r.nombre""",
        (f"%{texto}%",),
    ).fetchall()
    return [_row_to_summary(row) for row in rows]


def _row_to_summary(row: sqlite3.Row) -> RecipeSummary:
    return RecipeSummary(
        id=row["id"],
        nombre=row["nombre"],
        tiempo_preparacion=row["tiempo_preparacion"],
        categoria_nombre=row["categoria_nombre"],
    )


def _replace_ingredients(
    connection: sqlite3.Connection,
    recipe_id: int,
    ingredientes: list[tuple[str, float | None, str | None]],
) -> None:
    connection.execute("DELETE FROM recipe_ingredient WHERE recipe_id = ?", (recipe_id,))
    for nombre, cantidad, unidad in ingredientes:
        ing = ingredient_model.get_or_create(connection, nombre)
        connection.execute(
            """INSERT INTO recipe_ingredient (recipe_id, ingredient_id, cantidad, unidad)
               VALUES (?, ?, ?, ?)""",
            (recipe_id, ing.id, cantidad, unidad),
        )


def _replace_steps(connection: sqlite3.Connection, recipe_id: int, pasos: list[str]) -> None:
    connection.execute("DELETE FROM step WHERE recipe_id = ?", (recipe_id,))
    for numero, descripcion in enumerate(pasos, start=1):
        connection.execute(
            "INSERT INTO step (recipe_id, numero_orden, descripcion) VALUES (?, ?, ?)",
            (recipe_id, numero, descripcion),
        )
