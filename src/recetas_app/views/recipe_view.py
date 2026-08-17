"""Vista (entrada/salida de texto) para recetas."""

from recetas_app.models.category import Category
from recetas_app.models.recipe import RecipeDetail, RecipeSummary


def mostrar_menu() -> str:
    print("\n--- Recetas ---")
    print("1. Listar recetas")
    print("2. Ver detalle de receta")
    print("3. Crear receta")
    print("4. Editar receta")
    print("5. Eliminar receta")
    print("0. Volver")
    return input("Elige una opción: ").strip()


def mostrar_listado(recetas: list[RecipeSummary]) -> None:
    if not recetas:
        print("No hay recetas registradas.")
        return
    print("\nId  Nombre                          Categoría        Tiempo")
    for r in recetas:
        categoria = r.categoria_nombre or "-"
        tiempo = f"{r.tiempo_preparacion} min" if r.tiempo_preparacion else "-"
        print(f"{r.id:<4}{r.nombre:<32}{categoria:<17}{tiempo}")


def mostrar_detalle(receta: RecipeDetail) -> None:
    print(f"\n{receta.nombre}  (id {receta.id})")
    if receta.categoria_nombre:
        print(f"Categoría: {receta.categoria_nombre}")
    if receta.tiempo_preparacion:
        print(f"Tiempo de preparación: {receta.tiempo_preparacion} min")
    if receta.porciones:
        print(f"Porciones: {receta.porciones}")
    if receta.descripcion:
        print(f"Descripción: {receta.descripcion}")

    print("\nIngredientes:")
    if not receta.ingredientes:
        print("  (sin ingredientes)")
    for item in receta.ingredientes:
        cantidad = f"{item.cantidad} {item.unidad or ''}".strip() if item.cantidad else ""
        print(f"  - {item.nombre} {cantidad}".rstrip())

    print("\nPasos:")
    if not receta.pasos:
        print("  (sin pasos)")
    for paso in receta.pasos:
        print(f"  {paso.numero_orden}. {paso.descripcion}")


def pedir_datos_generales() -> tuple[str, str | None, int | None, int | None]:
    nombre = input("Nombre de la receta: ").strip()
    descripcion = input("Descripción (opcional): ").strip() or None
    tiempo_preparacion = _pedir_entero_opcional("Tiempo de preparación en minutos (opcional): ")
    porciones = _pedir_entero_opcional("Porciones (opcional): ")
    return nombre, descripcion, tiempo_preparacion, porciones


def pedir_categoria(categorias: list[Category]) -> int | None:
    if not categorias:
        print("No hay categorías creadas todavía; la receta quedará sin categoría.")
        return None
    print("\nCategorías disponibles:")
    for c in categorias:
        print(f"  {c.id}. {c.nombre}")
    valor = input("Id de categoría (vacío para ninguna): ").strip()
    if not valor:
        return None
    if not valor.isdigit() or int(valor) not in {c.id for c in categorias}:
        mostrar_error("Id de categoría no válido; se guardará sin categoría.")
        return None
    return int(valor)


def pedir_ingredientes() -> list[tuple[str, float | None, str | None]]:
    print("\nIngredientes (deja el nombre vacío para terminar):")
    ingredientes: list[tuple[str, float | None, str | None]] = []
    while True:
        nombre = input(f"  Ingrediente #{len(ingredientes) + 1} - nombre: ").strip()
        if not nombre:
            break
        cantidad_raw = input("    Cantidad (opcional): ").strip()
        cantidad = float(cantidad_raw) if _es_numero(cantidad_raw) else None
        unidad = input("    Unidad (opcional, ej. g, ml, uds): ").strip() or None
        ingredientes.append((nombre, cantidad, unidad))
    return ingredientes


def pedir_pasos() -> list[str]:
    print("\nPasos (deja vacío para terminar):")
    pasos: list[str] = []
    while True:
        descripcion = input(f"  Paso {len(pasos) + 1}: ").strip()
        if not descripcion:
            break
        pasos.append(descripcion)
    return pasos


def pedir_id() -> int | None:
    valor = input("Id de la receta: ").strip()
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


def _pedir_entero_opcional(prompt: str) -> int | None:
    valor = input(prompt).strip()
    return int(valor) if valor.isdigit() else None


def _es_numero(valor: str) -> bool:
    try:
        float(valor)
        return True
    except ValueError:
        return False
