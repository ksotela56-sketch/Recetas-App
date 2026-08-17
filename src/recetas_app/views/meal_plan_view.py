"""Vista para la planificación semanal."""

from recetas_app.models.meal_plan import DIAS_SEMANA, TIPOS_COMIDA, MealPlan, MealPlanEntry
from recetas_app.models.recipe import RecipeSummary


def mostrar_menu() -> str:
    print("\n--- Planificación semanal ---")
    print("1. Crear plan semanal")
    print("2. Ver plan semanal")
    print("3. Asignar receta a día/comida")
    print("4. Quitar asignación")
    print("0. Volver")
    return input("Elige una opción: ").strip()


def pedir_datos_plan() -> tuple[str, str | None]:
    nombre = input("Nombre del plan (ej. 'Semana del 18/08'): ").strip()
    fecha_inicio = input("Fecha de inicio (opcional, AAAA-MM-DD): ").strip() or None
    return nombre, fecha_inicio


def mostrar_planes(planes: list[MealPlan]) -> None:
    if not planes:
        print("No hay planes semanales registrados.")
        return
    print("\nId  Nombre                          Fecha inicio")
    for p in planes:
        print(f"{p.id:<4}{p.nombre:<32}{p.fecha_inicio or '-'}")


def pedir_id_plan() -> int | None:
    valor = input("Id del plan semanal: ").strip()
    if not valor.isdigit():
        mostrar_error("El id debe ser un número.")
        return None
    return int(valor)


def mostrar_plan_semanal(plan: MealPlan, entradas: list[MealPlanEntry]) -> None:
    print(f"\nPlan: {plan.nombre} (id {plan.id})")
    por_dia: dict[int, list[MealPlanEntry]] = {i: [] for i in range(7)}
    for entrada in entradas:
        por_dia[entrada.dia_semana].append(entrada)

    for dia_idx, dia_nombre in enumerate(DIAS_SEMANA):
        print(f"\n{dia_nombre}:")
        entradas_dia = por_dia[dia_idx]
        if not entradas_dia:
            print("  (sin recetas asignadas)")
            continue
        for entrada in sorted(entradas_dia, key=lambda e: TIPOS_COMIDA.index(e.tipo_comida)):
            print(f"  [{entrada.id}] {entrada.tipo_comida.capitalize()}: {entrada.recipe_nombre}")


def pedir_dia() -> int | None:
    print("\nDías: " + ", ".join(f"{i}={d}" for i, d in enumerate(DIAS_SEMANA)))
    valor = input("Día (0-6): ").strip()
    if not valor.isdigit() or int(valor) not in range(7):
        mostrar_error("Día no válido.")
        return None
    return int(valor)


def pedir_tipo_comida() -> str | None:
    print("Tipos de comida: " + ", ".join(TIPOS_COMIDA))
    valor = input("Tipo de comida: ").strip().lower()
    if valor not in TIPOS_COMIDA:
        mostrar_error("Tipo de comida no válido.")
        return None
    return valor


def pedir_receta(recetas: list[RecipeSummary]) -> int | None:
    if not recetas:
        mostrar_error("No hay recetas registradas todavía.")
        return None
    print("\nRecetas disponibles:")
    for r in recetas:
        print(f"  {r.id}. {r.nombre}")
    valor = input("Id de receta: ").strip()
    if not valor.isdigit() or int(valor) not in {r.id for r in recetas}:
        mostrar_error("Id de receta no válido.")
        return None
    return int(valor)


def pedir_id_entrada() -> int | None:
    valor = input("Id de la asignación a quitar: ").strip()
    if not valor.isdigit():
        mostrar_error("El id debe ser un número.")
        return None
    return int(valor)


def mostrar_mensaje(mensaje: str) -> None:
    print(mensaje)


def mostrar_error(mensaje: str) -> None:
    print(f"Error: {mensaje}")
