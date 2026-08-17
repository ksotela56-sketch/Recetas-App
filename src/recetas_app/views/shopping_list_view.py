"""Vista para la lista de la compra."""

from recetas_app.models.shopping_list import ShoppingList, ShoppingListItem


def mostrar_menu() -> str:
    print("\n--- Lista de la compra ---")
    print("1. Generar desde un plan semanal")
    print("2. Ver lista de la compra")
    print("3. Marcar ítem como comprado")
    print("4. Eliminar lista")
    print("0. Volver")
    return input("Elige una opción: ").strip()


def mostrar_listas(listas: list[ShoppingList]) -> None:
    if not listas:
        print("No hay listas de la compra registradas.")
        return
    print("\nId  Plan                            Creada")
    for lista in listas:
        plan = lista.meal_plan_nombre or "-"
        print(f"{lista.id:<4}{plan:<32}{lista.created_at}")


def pedir_id_lista() -> int | None:
    valor = input("Id de la lista de la compra: ").strip()
    if not valor.isdigit():
        mostrar_error("El id debe ser un número.")
        return None
    return int(valor)


def mostrar_items(items: list[ShoppingListItem]) -> None:
    if not items:
        print("La lista no tiene ítems.")
        return
    print("\nId  [x] Ingrediente                  Cantidad")
    for item in items:
        marca = "x" if item.comprado else " "
        cantidad = f"{item.cantidad_total} {item.unidad or ''}".strip() if item.cantidad_total else "-"
        print(f"{item.id:<4}[{marca}] {item.nombre:<28}{cantidad}")


def pedir_id_item() -> int | None:
    valor = input("Id del ítem: ").strip()
    if not valor.isdigit():
        mostrar_error("El id debe ser un número.")
        return None
    return int(valor)


def confirmar(mensaje: str) -> bool:
    return input(f"{mensaje} (s/n): ").strip().lower() == "s"


def mostrar_mensaje(mensaje: str) -> None:
    print(mensaje)


def mostrar_error(mensaje: str) -> None:
    print(f"Error: {mensaje}")
