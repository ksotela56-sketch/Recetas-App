"""Controlador para la gestión de recetas."""

import sqlite3

from recetas_app.models import category as category_model
from recetas_app.models import recipe as recipe_model
from recetas_app.views import recipe_view


def run(connection: sqlite3.Connection) -> None:
    while True:
        opcion = recipe_view.mostrar_menu()
        if opcion == "1":
            _listar(connection)
        elif opcion == "2":
            _ver_detalle(connection)
        elif opcion == "3":
            _crear(connection)
        elif opcion == "4":
            _editar(connection)
        elif opcion == "5":
            _eliminar(connection)
        elif opcion == "0":
            return
        else:
            recipe_view.mostrar_error("Opción no válida.")


def _listar(connection: sqlite3.Connection) -> None:
    recetas = recipe_model.list_all(connection)
    recipe_view.mostrar_listado(recetas)


def _ver_detalle(connection: sqlite3.Connection) -> None:
    recipe_id = recipe_view.pedir_id()
    if recipe_id is None:
        return
    receta = recipe_model.get_detail(connection, recipe_id)
    if receta is None:
        recipe_view.mostrar_error("No existe una receta con ese id.")
        return
    recipe_view.mostrar_detalle(receta)


def _crear(connection: sqlite3.Connection) -> None:
    nombre, descripcion, tiempo_preparacion, porciones = recipe_view.pedir_datos_generales()
    if not nombre:
        recipe_view.mostrar_error("El nombre no puede estar vacío.")
        return
    categorias = category_model.list_all(connection)
    categoria_id = recipe_view.pedir_categoria(categorias)
    ingredientes = recipe_view.pedir_ingredientes()
    pasos = recipe_view.pedir_pasos()

    recipe_id = recipe_model.create(
        connection, nombre, descripcion, tiempo_preparacion, porciones, categoria_id, ingredientes, pasos
    )
    recipe_view.mostrar_mensaje(f"Receta '{nombre}' creada (id {recipe_id}).")


def _editar(connection: sqlite3.Connection) -> None:
    recipe_id = recipe_view.pedir_id()
    if recipe_id is None:
        return
    receta = recipe_model.get_detail(connection, recipe_id)
    if receta is None:
        recipe_view.mostrar_error("No existe una receta con ese id.")
        return

    recipe_view.mostrar_mensaje("Introduce los nuevos datos (se reemplazan ingredientes y pasos).")
    nombre, descripcion, tiempo_preparacion, porciones = recipe_view.pedir_datos_generales()
    if not nombre:
        recipe_view.mostrar_error("El nombre no puede estar vacío.")
        return
    categorias = category_model.list_all(connection)
    categoria_id = recipe_view.pedir_categoria(categorias)
    ingredientes = recipe_view.pedir_ingredientes()
    pasos = recipe_view.pedir_pasos()

    recipe_model.update(
        connection, recipe_id, nombre, descripcion, tiempo_preparacion, porciones, categoria_id, ingredientes, pasos
    )
    recipe_view.mostrar_mensaje("Receta actualizada.")


def _eliminar(connection: sqlite3.Connection) -> None:
    recipe_id = recipe_view.pedir_id()
    if recipe_id is None:
        return
    if recipe_model.get_detail(connection, recipe_id) is None:
        recipe_view.mostrar_error("No existe una receta con ese id.")
        return
    if not recipe_view.confirmar("¿Seguro que quieres eliminar esta receta?"):
        return
    recipe_model.delete(connection, recipe_id)
    recipe_view.mostrar_mensaje("Receta eliminada.")
