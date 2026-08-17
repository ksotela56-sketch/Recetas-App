"""Vista (entrada/salida de texto) para categorías."""

from recetas_app.models.category import Category


def mostrar_menu() -> str:
    print("\n--- Categorías ---")
    print("1. Listar categorías")
    print("2. Crear categoría")
    print("3. Eliminar categoría")
    print("0. Volver")
    return input("Elige una opción: ").strip()


def mostrar_listado(categorias: list[Category]) -> None:
    if not categorias:
        print("No hay categorías registradas.")
        return
    print("\nId  Nombre")
    for c in categorias:
        print(f"{c.id:<4}{c.nombre}")


def pedir_nombre() -> str:
    return input("Nombre de la categoría: ").strip()


def pedir_id() -> int | None:
    valor = input("Id de la categoría: ").strip()
    if not valor.isdigit():
        mostrar_error("El id debe ser un número.")
        return None
    return int(valor)


def mostrar_mensaje(mensaje: str) -> None:
    print(mensaje)


def mostrar_error(mensaje: str) -> None:
    print(f"Error: {mensaje}")
