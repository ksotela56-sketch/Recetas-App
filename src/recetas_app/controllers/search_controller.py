"""Controlador para la búsqueda y filtrado de recetas."""

import sqlite3

from recetas_app.models import category as category_model
from recetas_app.models import recipe as recipe_model
from recetas_app.views import recipe_view, search_view


def run(connection: sqlite3.Connection) -> None:
    while True:
        opcion = search_view.mostrar_menu()
        if opcion == "1":
            texto = search_view.pedir_texto("Nombre (o parte del nombre): ")
            resultados = recipe_model.search_by_name(connection, texto)
            recipe_view.mostrar_listado(resultados)
        elif opcion == "2":
            categorias = category_model.list_all(connection)
            categoria_id = search_view.pedir_categoria(categorias)
            if categoria_id is None:
                continue
            resultados = recipe_model.search_by_category(connection, categoria_id)
            recipe_view.mostrar_listado(resultados)
        elif opcion == "3":
            texto = search_view.pedir_texto("Ingrediente (o parte del nombre): ")
            resultados = recipe_model.search_by_ingredient(connection, texto)
            recipe_view.mostrar_listado(resultados)
        elif opcion == "0":
            return
        else:
            recipe_view.mostrar_error("Opción no válida.")
