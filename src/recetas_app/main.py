"""Punto de entrada de Recetas-App."""

from recetas_app.controllers import (
    category_controller,
    meal_plan_controller,
    recipe_controller,
    search_controller,
    shopping_list_controller,
)
from recetas_app.models.database import init_db, get_connection
from recetas_app.views import main_menu_view


def main() -> None:
    init_db()
    connection = get_connection()
    try:
        while True:
            opcion = main_menu_view.mostrar_menu()
            if opcion == "1":
                recipe_controller.run(connection)
            elif opcion == "2":
                category_controller.run(connection)
            elif opcion == "3":
                search_controller.run(connection)
            elif opcion == "4":
                meal_plan_controller.run(connection)
            elif opcion == "5":
                shopping_list_controller.run(connection)
            elif opcion == "6":
                main_menu_view.despedida()
                return
            else:
                print("Opción no válida.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
