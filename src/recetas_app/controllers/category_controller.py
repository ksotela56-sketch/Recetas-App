"""Controlador para la gestión de categorías."""

import sqlite3

from recetas_app.models import category as category_model
from recetas_app.views import category_view


def run(connection: sqlite3.Connection) -> None:
    while True:
        opcion = category_view.mostrar_menu()
        if opcion == "1":
            categorias = category_model.list_all(connection)
            category_view.mostrar_listado(categorias)
        elif opcion == "2":
            nombre = category_view.pedir_nombre()
            if not nombre:
                category_view.mostrar_error("El nombre no puede estar vacío.")
                continue
            try:
                category_model.create(connection, nombre)
                category_view.mostrar_mensaje(f"Categoría '{nombre}' creada.")
            except sqlite3.IntegrityError:
                category_view.mostrar_error(f"Ya existe una categoría llamada '{nombre}'.")
        elif opcion == "3":
            categorias = category_model.list_all(connection)
            category_view.mostrar_listado(categorias)
            category_id = category_view.pedir_id()
            if category_id is None:
                continue
            if category_model.get_by_id(connection, category_id) is None:
                category_view.mostrar_error("No existe una categoría con ese id.")
                continue
            category_model.delete(connection, category_id)
            category_view.mostrar_mensaje(
                "Categoría eliminada. Las recetas que la usaban quedan sin categoría."
            )
        elif opcion == "0":
            return
        else:
            category_view.mostrar_error("Opción no válida.")
