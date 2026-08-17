"""Vista para la búsqueda y filtrado de recetas."""

from recetas_app.models.category import Category


def mostrar_menu() -> str:
    print("\n--- Buscar recetas ---")
    print("1. Por nombre")
    print("2. Por categoría")
    print("3. Por ingrediente")
    print("0. Volver")
    return input("Elige una opción: ").strip()


def pedir_texto(prompt: str) -> str:
    return input(prompt).strip()


def pedir_categoria(categorias: list[Category]) -> int | None:
    if not categorias:
        print("No hay categorías registradas.")
        return None
    print("\nCategorías disponibles:")
    for c in categorias:
        print(f"  {c.id}. {c.nombre}")
    valor = input("Id de categoría: ").strip()
    if not valor.isdigit():
        print("Error: el id debe ser un número.")
        return None
    return int(valor)
