"""Vista del menú principal."""


def mostrar_menu() -> str:
    print("\n===== Recetas-App =====")
    print("1. Recetas")
    print("2. Categorías")
    print("3. Buscar recetas")
    print("4. Planificación semanal")
    print("5. Lista de la compra")
    print("6. Salir")
    return input("Elige una opción: ").strip()


def despedida() -> None:
    print("¡Hasta pronto!")
