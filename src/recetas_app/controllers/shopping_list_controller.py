"""Controlador para la lista de la compra."""

import sqlite3

from recetas_app.models import meal_plan as meal_plan_model
from recetas_app.models import shopping_list as shopping_list_model
from recetas_app.views import meal_plan_view, shopping_list_view


def run(connection: sqlite3.Connection) -> None:
    while True:
        opcion = shopping_list_view.mostrar_menu()
        if opcion == "1":
            _generar(connection)
        elif opcion == "2":
            _ver(connection)
        elif opcion == "3":
            _marcar_comprado(connection)
        elif opcion == "4":
            _eliminar(connection)
        elif opcion == "0":
            return
        else:
            shopping_list_view.mostrar_error("Opción no válida.")


def _seleccionar_lista(connection: sqlite3.Connection) -> shopping_list_model.ShoppingList | None:
    listas = shopping_list_model.list_all(connection)
    shopping_list_view.mostrar_listas(listas)
    if not listas:
        return None
    lista_id = shopping_list_view.pedir_id_lista()
    if lista_id is None:
        return None
    lista = shopping_list_model.get_by_id(connection, lista_id)
    if lista is None:
        shopping_list_view.mostrar_error("No existe una lista con ese id.")
        return None
    return lista


def _generar(connection: sqlite3.Connection) -> None:
    planes = meal_plan_model.list_all(connection)
    meal_plan_view.mostrar_planes(planes)
    if not planes:
        return
    plan_id = meal_plan_view.pedir_id_plan()
    if plan_id is None:
        return
    if meal_plan_model.get_by_id(connection, plan_id) is None:
        shopping_list_view.mostrar_error("No existe un plan con ese id.")
        return
    lista_id = shopping_list_model.generate_from_meal_plan(connection, plan_id)
    shopping_list_view.mostrar_mensaje(f"Lista de la compra generada (id {lista_id}).")


def _ver(connection: sqlite3.Connection) -> None:
    lista = _seleccionar_lista(connection)
    if lista is None:
        return
    items = shopping_list_model.get_items(connection, lista.id)
    shopping_list_view.mostrar_items(items)


def _marcar_comprado(connection: sqlite3.Connection) -> None:
    lista = _seleccionar_lista(connection)
    if lista is None:
        return
    items = shopping_list_model.get_items(connection, lista.id)
    shopping_list_view.mostrar_items(items)
    item_id = shopping_list_view.pedir_id_item()
    if item_id is None:
        return
    item = next((i for i in items if i.id == item_id), None)
    if item is None:
        shopping_list_view.mostrar_error("No existe ese ítem en esta lista.")
        return
    shopping_list_model.mark_purchased(connection, item_id, not item.comprado)
    shopping_list_view.mostrar_mensaje("Ítem actualizado.")


def _eliminar(connection: sqlite3.Connection) -> None:
    lista = _seleccionar_lista(connection)
    if lista is None:
        return
    if not shopping_list_view.confirmar("¿Seguro que quieres eliminar esta lista?"):
        return
    shopping_list_model.delete(connection, lista.id)
    shopping_list_view.mostrar_mensaje("Lista eliminada.")
