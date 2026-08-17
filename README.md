# Recetas-App

Aplicación web de recetas de cocina en Python, con arquitectura MVC y persistencia
en SQLite. Servidor local con Flask. Gestionada con [uv](https://docs.astral.sh/uv/).

Ver [SPEC.md](./SPEC.md) para la especificación funcional y [PLAN.md](./PLAN.md) para
el plan de implementación por fases.

## Requisitos

- [uv](https://docs.astral.sh/uv/) instalado.

## Instalación

```bash
uv sync
```

## Ejecutar la aplicación

```bash
uv run python -m recetas_app.main
```

o, mediante el script instalado por el proyecto:

```bash
uv run recetas-app
```

Luego abre **http://127.0.0.1:5000** en tu navegador.

La base de datos SQLite se crea automáticamente en `data/recetas.db` la primera vez
que se ejecuta la aplicación.

## Ejecutar las pruebas

```bash
uv run pytest
```

## Estructura del proyecto (MVC)

```
src/recetas_app/
  models/       # Acceso a datos: esquema SQLite y repositorios CRUD
  views/        # Plantillas HTML (Jinja2) y estáticos (CSS)
  controllers/  # Blueprints Flask: reciben la petición, llaman al modelo, renderizan la vista
  app.py        # Crea y configura la app Flask
  main.py       # Punto de entrada: inicializa la BD y arranca el servidor
tests/          # Pruebas con pytest (modelo y rutas web)
```
