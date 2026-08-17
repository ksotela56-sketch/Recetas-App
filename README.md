# Recetas-App

Aplicación de recetas de cocina en Python (CLI), con arquitectura MVC y persistencia
en SQLite. Gestionada con [uv](https://docs.astral.sh/uv/).

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
  views/        # Presentación en consola (entrada/salida de texto)
  controllers/  # Lógica de orquestación entre modelo y vista
  main.py       # Punto de entrada
tests/          # Pruebas con pytest
```
