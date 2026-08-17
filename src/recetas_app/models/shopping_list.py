"""Repositorio de acceso a datos para listas de la compra."""

import sqlite3
from dataclasses import dataclass


@dataclass
class ShoppingList:
    id: int
    meal_plan_id: int | None
    meal_plan_nombre: str | None
    created_at: str


@dataclass
class ShoppingListItem:
    id: int
    ingredient_id: int
    nombre: str
    cantidad_total: float | None
    unidad: str | None
    comprado: bool


def generate_from_meal_plan(connection: sqlite3.Connection, meal_plan_id: int) -> int:
    """Genera una lista de la compra agregando los ingredientes de todas las recetas
    asignadas a un plan semanal. Devuelve el id de la lista creada."""
    cursor = connection.execute(
        "INSERT INTO shopping_list (meal_plan_id) VALUES (?)", (meal_plan_id,)
    )
    shopping_list_id = cursor.lastrowid

    rows = connection.execute(
        """SELECT ri.ingredient_id, ri.cantidad, ri.unidad
           FROM meal_plan_entry mpe
           JOIN recipe_ingredient ri ON ri.recipe_id = mpe.recipe_id
           WHERE mpe.meal_plan_id = ?""",
        (meal_plan_id,),
    ).fetchall()

    agregados: dict[tuple[int, str], float] = {}
    for row in rows:
        clave = (row["ingredient_id"], row["unidad"] or "")
        agregados[clave] = agregados.get(clave, 0.0) + (row["cantidad"] or 0.0)

    for (ingredient_id, unidad), cantidad_total in agregados.items():
        connection.execute(
            """INSERT INTO shopping_list_item (shopping_list_id, ingredient_id, cantidad_total, unidad)
               VALUES (?, ?, ?, ?)""",
            (shopping_list_id, ingredient_id, cantidad_total, unidad or None),
        )
    connection.commit()
    return shopping_list_id


def list_all(connection: sqlite3.Connection) -> list[ShoppingList]:
    rows = connection.execute(
        """SELECT sl.id, sl.meal_plan_id, mp.nombre AS meal_plan_nombre, sl.created_at
           FROM shopping_list sl
           LEFT JOIN meal_plan mp ON mp.id = sl.meal_plan_id
           ORDER BY sl.id DESC"""
    ).fetchall()
    return [
        ShoppingList(
            id=r["id"],
            meal_plan_id=r["meal_plan_id"],
            meal_plan_nombre=r["meal_plan_nombre"],
            created_at=r["created_at"],
        )
        for r in rows
    ]


def get_by_id(connection: sqlite3.Connection, shopping_list_id: int) -> ShoppingList | None:
    row = connection.execute(
        """SELECT sl.id, sl.meal_plan_id, mp.nombre AS meal_plan_nombre, sl.created_at
           FROM shopping_list sl
           LEFT JOIN meal_plan mp ON mp.id = sl.meal_plan_id
           WHERE sl.id = ?""",
        (shopping_list_id,),
    ).fetchone()
    if not row:
        return None
    return ShoppingList(
        id=row["id"],
        meal_plan_id=row["meal_plan_id"],
        meal_plan_nombre=row["meal_plan_nombre"],
        created_at=row["created_at"],
    )


def get_items(connection: sqlite3.Connection, shopping_list_id: int) -> list[ShoppingListItem]:
    rows = connection.execute(
        """SELECT sli.id, sli.ingredient_id, i.nombre, sli.cantidad_total, sli.unidad, sli.comprado
           FROM shopping_list_item sli
           JOIN ingredient i ON i.id = sli.ingredient_id
           WHERE sli.shopping_list_id = ?
           ORDER BY i.nombre""",
        (shopping_list_id,),
    ).fetchall()
    return [
        ShoppingListItem(
            id=r["id"],
            ingredient_id=r["ingredient_id"],
            nombre=r["nombre"],
            cantidad_total=r["cantidad_total"],
            unidad=r["unidad"],
            comprado=bool(r["comprado"]),
        )
        for r in rows
    ]


def mark_purchased(connection: sqlite3.Connection, item_id: int, comprado: bool) -> None:
    connection.execute(
        "UPDATE shopping_list_item SET comprado = ? WHERE id = ?", (int(comprado), item_id)
    )
    connection.commit()


def delete(connection: sqlite3.Connection, shopping_list_id: int) -> None:
    connection.execute("DELETE FROM shopping_list WHERE id = ?", (shopping_list_id,))
    connection.commit()
