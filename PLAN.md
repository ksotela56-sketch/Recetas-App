# Plan de implementación — Recetas-App

Basado en [SPEC.md](./SPEC.md). Cada fase deja la app en un estado funcional y probable.

## Fase 0 — Setup del proyecto
- `uv init` para crear `pyproject.toml` y entorno virtual del proyecto.
- Añadir dependencias con `uv add` (stdlib `sqlite3` no requiere dependencia; `pytest` como
  dependencia de desarrollo con `uv add --dev pytest`).
- Crear estructura de carpetas `recetas_app/{models,views,controllers}` y `tests/`.
- Configurar `data/` (ignorada en git) para el archivo `recetas.db`.

## Fase 1 — Capa de Modelo base
- `models/database.py`: conexión SQLite, creación de esquema (todas las tablas de la SPEC),
  función `init_db()`.
- `models/category.py` y `models/ingredient.py`: repositorios CRUD simples.
- `models/recipe.py`: repositorio para Recipe + RecipeIngredient + Step (crear/leer/actualizar/
  eliminar receta completa, incluyendo sus ingredientes y pasos).

## Fase 2 — CRUD de Recetas y Categorías (Controlador + Vista)
- `controllers/category_controller.py` + `views/category_view.py`.
- `controllers/recipe_controller.py` + `views/recipe_view.py`: alta/edición interactiva
  (nombre, descripción, tiempo, porciones, categoría, ingredientes, pasos), listado y detalle.
- `views/main_menu_view.py` + `main.py`: menú principal navegable con las opciones 1 y 2.

## Fase 3 — Búsqueda y filtrado
- Métodos de consulta en `models/recipe.py` (por nombre, categoría, ingrediente).
- `controllers/search_controller.py` + `views/search_view.py`.
- Integrar opción 3 en el menú principal.

## Fase 4 — Planificación semanal
- `models/meal_plan.py`: repositorio para MealPlan + MealPlanEntry.
- `controllers/meal_plan_controller.py` + `views/meal_plan_view.py`: crear plan, asignar
  receta a día/comida, ver plan en formato tabla semanal, quitar asignación.
- Integrar opción 4 en el menú principal.

## Fase 5 — Lista de la compra
- `models/shopping_list.py`: repositorio para ShoppingList + ShoppingListItem.
- Lógica de agregación: sumar cantidades por ingrediente+unidad a partir de las recetas
  asignadas en un plan semanal.
- `controllers/shopping_list_controller.py` + `views/shopping_list_view.py`.
- Integrar opción 5 en el menú principal.

## Fase 6 — Pruebas
- `pytest` sobre repositorios de modelos (usar base de datos SQLite en memoria o archivo
  temporal por test).
- Pruebas de la lógica de agregación de la lista de la compra (caso con ingredientes
  repetidos en distintas unidades).
- Ejecutar con `uv run pytest`.

## Fase 7 — Pulido
- Validación de inputs en las vistas (números, opciones fuera de rango, campos vacíos).
- Manejo de errores de integridad (ej. eliminar categoría en uso).
- Actualizar `README.md` con instrucciones de instalación (`uv sync`) y ejecución
  (`uv run python -m recetas_app.main`).

## Convención de commits por fase
Un commit por fase completada, para poder revisar el avance incrementalmente.
