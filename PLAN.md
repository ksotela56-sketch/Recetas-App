# Plan de implementación — Recetas-App (versión web)

Basado en [SPEC.md](./SPEC.md). El Modelo (fase 1 original, capa SQLite) ya está hecho y
no cambia. Este plan cubre la migración de Vista/Controlador de CLI a web con Flask.

## Fase A — Setup de Flask
- `uv add flask`.
- Crear `controllers/`/`views/` nuevos (Blueprints + plantillas Jinja2), retirar los
  módulos de CLI (`*_view.py` de texto, `*_controller.py` de menús, `main.py` antiguo).
- `app.py`: `create_app()` que registra los blueprints y configura `template_folder`/
  `static_folder` apuntando a `views/`.
- `main.py`: inicializa la BD (`init_db()`) y arranca `app.run(debug=True)`.

## Fase B — Recetas y Categorías (CRUD web)
- Plantilla base `base.html` con navegación a las 5 secciones.
- `category_routes.py` + plantillas `categorias/listado.html`: listar, crear (formulario
  inline), eliminar (formulario POST).
- `recipe_routes.py` + plantillas `recetas/{listado,detalle,formulario}.html`: listar, ver
  detalle, crear/editar (mismo formulario, con textarea para ingredientes y pasos línea a
  línea), eliminar.

## Fase C — Búsqueda
- `search_routes.py` + plantilla `buscar/resultados.html`: formulario con selector
  nombre/categoría/ingrediente y tabla de resultados en la misma página.

## Fase D — Planificación semanal
- `meal_plan_routes.py` + plantillas `planes/{listado,detalle}.html`: crear plan, ver
  tabla semanal (día x comida), formulario para asignar receta, botón para quitar
  asignación.

## Fase E — Lista de la compra
- `shopping_list_routes.py` + plantillas `listas/{listado,detalle}.html`: generar desde
  un plan, ver ítems con checkbox de comprado (toggle vía POST), eliminar lista.

## Fase F — Pruebas
- `tests/test_routes.py`: smoke tests con el Flask test client (`app.test_client()`) sobre
  los flujos principales (crear receta vía POST, ver listado, generar lista de compra).
- Mantener y ejecutar los tests de modelo ya existentes (`uv run pytest`).

## Fase G — Pulido
- CSS mínimo (`views/static/style.css`) para legibilidad (tipografía, tablas, formularios).
- Mensajes de error/confirmación visibles en las plantillas (flash messages de Flask).
- Actualizar `README.md`: `uv run python -m recetas_app.main` y abrir
  `http://localhost:5000`.

## Convención de commits por fase
Un commit por fase completada.
