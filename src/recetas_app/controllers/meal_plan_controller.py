"""Controlador para la planificación semanal."""

import sqlite3

from recetas_app.models import meal_plan as meal_plan_model
from recetas_app.models import recipe as recipe_model
from recetas_app.views import meal_plan_view


def run(connection: sqlite3.Connection) -> None:
    while True:
        opcion = meal_plan_view.mostrar_menu()
        if opcion == "1":
            _crear_plan(connection)
        elif opcion == "2":
            _ver_plan(connection)
        elif opcion == "3":
            _asignar_receta(connection)
        elif opcion == "4":
            _quitar_asignacion(connection)
        elif opcion == "0":
            return
        else:
            meal_plan_view.mostrar_error("Opción no válida.")


def _crear_plan(connection: sqlite3.Connection) -> None:
    nombre, fecha_inicio = meal_plan_view.pedir_datos_plan()
    if not nombre:
        meal_plan_view.mostrar_error("El nombre no puede estar vacío.")
        return
    plan = meal_plan_model.create(connection, nombre, fecha_inicio)
    meal_plan_view.mostrar_mensaje(f"Plan '{plan.nombre}' creado (id {plan.id}).")


def _seleccionar_plan(connection: sqlite3.Connection) -> meal_plan_model.MealPlan | None:
    planes = meal_plan_model.list_all(connection)
    meal_plan_view.mostrar_planes(planes)
    if not planes:
        return None
    plan_id = meal_plan_view.pedir_id_plan()
    if plan_id is None:
        return None
    plan = meal_plan_model.get_by_id(connection, plan_id)
    if plan is None:
        meal_plan_view.mostrar_error("No existe un plan con ese id.")
        return None
    return plan


def _ver_plan(connection: sqlite3.Connection) -> None:
    plan = _seleccionar_plan(connection)
    if plan is None:
        return
    entradas = meal_plan_model.get_entries(connection, plan.id)
    meal_plan_view.mostrar_plan_semanal(plan, entradas)


def _asignar_receta(connection: sqlite3.Connection) -> None:
    plan = _seleccionar_plan(connection)
    if plan is None:
        return
    dia = meal_plan_view.pedir_dia()
    if dia is None:
        return
    tipo_comida = meal_plan_view.pedir_tipo_comida()
    if tipo_comida is None:
        return
    recetas = recipe_model.list_all(connection)
    recipe_id = meal_plan_view.pedir_receta(recetas)
    if recipe_id is None:
        return
    meal_plan_model.add_entry(connection, plan.id, dia, tipo_comida, recipe_id)
    meal_plan_view.mostrar_mensaje("Receta asignada al plan.")


def _quitar_asignacion(connection: sqlite3.Connection) -> None:
    plan = _seleccionar_plan(connection)
    if plan is None:
        return
    entradas = meal_plan_model.get_entries(connection, plan.id)
    meal_plan_view.mostrar_plan_semanal(plan, entradas)
    entry_id = meal_plan_view.pedir_id_entrada()
    if entry_id is None:
        return
    if entry_id not in {e.id for e in entradas}:
        meal_plan_view.mostrar_error("No existe esa asignación en este plan.")
        return
    meal_plan_model.remove_entry(connection, entry_id)
    meal_plan_view.mostrar_mensaje("Asignación eliminada.")
