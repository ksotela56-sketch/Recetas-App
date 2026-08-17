"""Repositorio de acceso a datos para planes semanales."""

import sqlite3
from dataclasses import dataclass

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
TIPOS_COMIDA = ["desayuno", "almuerzo", "cena"]


@dataclass
class MealPlan:
    id: int
    nombre: str
    fecha_inicio: str | None


@dataclass
class MealPlanEntry:
    id: int
    dia_semana: int
    tipo_comida: str
    recipe_id: int
    recipe_nombre: str


def create(connection: sqlite3.Connection, nombre: str, fecha_inicio: str | None) -> MealPlan:
    cursor = connection.execute(
        "INSERT INTO meal_plan (nombre, fecha_inicio) VALUES (?, ?)", (nombre, fecha_inicio)
    )
    connection.commit()
    return MealPlan(id=cursor.lastrowid, nombre=nombre, fecha_inicio=fecha_inicio)


def list_all(connection: sqlite3.Connection) -> list[MealPlan]:
    rows = connection.execute(
        "SELECT id, nombre, fecha_inicio FROM meal_plan ORDER BY id DESC"
    ).fetchall()
    return [MealPlan(id=r["id"], nombre=r["nombre"], fecha_inicio=r["fecha_inicio"]) for r in rows]


def get_by_id(connection: sqlite3.Connection, meal_plan_id: int) -> MealPlan | None:
    row = connection.execute(
        "SELECT id, nombre, fecha_inicio FROM meal_plan WHERE id = ?", (meal_plan_id,)
    ).fetchone()
    return MealPlan(id=row["id"], nombre=row["nombre"], fecha_inicio=row["fecha_inicio"]) if row else None


def add_entry(
    connection: sqlite3.Connection, meal_plan_id: int, dia_semana: int, tipo_comida: str, recipe_id: int
) -> int:
    cursor = connection.execute(
        """INSERT INTO meal_plan_entry (meal_plan_id, dia_semana, tipo_comida, recipe_id)
           VALUES (?, ?, ?, ?)""",
        (meal_plan_id, dia_semana, tipo_comida, recipe_id),
    )
    connection.commit()
    return cursor.lastrowid


def remove_entry(connection: sqlite3.Connection, entry_id: int) -> None:
    connection.execute("DELETE FROM meal_plan_entry WHERE id = ?", (entry_id,))
    connection.commit()


def get_entries(connection: sqlite3.Connection, meal_plan_id: int) -> list[MealPlanEntry]:
    rows = connection.execute(
        """SELECT mpe.id, mpe.dia_semana, mpe.tipo_comida, mpe.recipe_id, r.nombre AS recipe_nombre
           FROM meal_plan_entry mpe
           JOIN recipe r ON r.id = mpe.recipe_id
           WHERE mpe.meal_plan_id = ?
           ORDER BY mpe.dia_semana, mpe.tipo_comida""",
        (meal_plan_id,),
    ).fetchall()
    return [
        MealPlanEntry(
            id=r["id"],
            dia_semana=r["dia_semana"],
            tipo_comida=r["tipo_comida"],
            recipe_id=r["recipe_id"],
            recipe_nombre=r["recipe_nombre"],
        )
        for r in rows
    ]
