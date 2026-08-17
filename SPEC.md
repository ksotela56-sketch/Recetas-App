# Especificación — Recetas-App

## 1. Resumen

Aplicación web de recetas de cocina en Python, servida en el navegador (HTML) mediante un
servidor local **Flask**, con persistencia en SQLite y arquitectura **MVC** (Modelo / Vista /
Controlador) en carpetas separadas. Gestión de dependencias y entorno con **uv**.

> Nota de revisión: la v1 se implementó como CLI de terminal. Se sustituyó por esta versión
> web porque la interfaz de texto no resultaba cómoda de usar. El Modelo (capa de acceso a
> datos SQLite) no cambió; solo cambiaron Vista y Controlador.

## 2. Funcionalidades

### 2.1 Gestión de recetas (CRUD)
- Crear receta: nombre, descripción, tiempo de preparación (min), porciones, categoría,
  lista de ingredientes (cantidad + unidad), lista de pasos ordenados.
- Ver detalle de una receta (ingredientes + pasos).
- Listar todas las recetas (vista resumida: nombre, categoría, tiempo).
- Editar receta (datos generales, ingredientes, pasos).
- Eliminar receta.

### 2.2 Categorías
- Crear, listar y eliminar categorías (ej. Desayuno, Almuerzo, Cena, Postre, Vegetariano).
- Asignar una categoría a cada receta.

### 2.3 Búsqueda y filtrado
- Buscar recetas por nombre (coincidencia parcial).
- Filtrar recetas por categoría.
- Filtrar recetas por ingrediente.

### 2.4 Planificación semanal
- Crear un plan semanal (nombre + fecha de inicio).
- Asignar recetas a días de la semana (lunes–domingo) y tipo de comida
  (desayuno / almuerzo / cena).
- Ver el plan semanal completo.
- Editar o quitar una asignación del plan.

### 2.5 Lista de la compra
- Generar una lista de la compra a partir de un plan semanal: se agregan y suman
  las cantidades de ingredientes repetidos entre recetas.
- Marcar ítems como comprados.
- Limpiar / eliminar una lista de la compra.

## 3. Modelo de datos (SQLite)

```
Category
  id            INTEGER PK
  nombre        TEXT UNIQUE NOT NULL

Ingredient
  id            INTEGER PK
  nombre        TEXT UNIQUE NOT NULL

Recipe
  id                  INTEGER PK
  nombre              TEXT NOT NULL
  descripcion         TEXT
  tiempo_preparacion  INTEGER   -- minutos
  porciones           INTEGER
  categoria_id        INTEGER FK -> Category.id
  created_at          TEXT

RecipeIngredient
  id            INTEGER PK
  recipe_id     INTEGER FK -> Recipe.id
  ingredient_id INTEGER FK -> Ingredient.id
  cantidad      REAL
  unidad        TEXT        -- g, ml, unidades, cucharadas...

Step
  id            INTEGER PK
  recipe_id     INTEGER FK -> Recipe.id
  numero_orden  INTEGER NOT NULL
  descripcion   TEXT NOT NULL

MealPlan
  id            INTEGER PK
  nombre        TEXT NOT NULL
  fecha_inicio  TEXT

MealPlanEntry
  id            INTEGER PK
  meal_plan_id  INTEGER FK -> MealPlan.id
  dia_semana    INTEGER   -- 0=lunes ... 6=domingo
  tipo_comida   TEXT      -- desayuno | almuerzo | cena
  recipe_id     INTEGER FK -> Recipe.id

ShoppingList
  id            INTEGER PK
  meal_plan_id  INTEGER FK -> MealPlan.id (nullable)
  created_at    TEXT

ShoppingListItem
  id                INTEGER PK
  shopping_list_id  INTEGER FK -> ShoppingList.id
  ingredient_id     INTEGER FK -> Ingredient.id
  cantidad_total    REAL
  unidad            TEXT
  comprado          INTEGER  -- boolean 0/1
```

## 4. Pantallas (páginas web)

```
/                          Inicio: enlaces a las 5 secciones

/recetas                   Listado de recetas
/recetas/nueva             Formulario: crear receta
/recetas/<id>               Detalle de receta (ingredientes + pasos)
/recetas/<id>/editar        Formulario: editar receta
/recetas/<id>/eliminar      (POST) elimina y vuelve al listado

/categorias                Listado de categorías + formulario para crear
/categorias/<id>/eliminar   (POST) elimina

/buscar                    Formulario de búsqueda (nombre / categoría / ingrediente) + resultados

/planes                    Listado de planes semanales + formulario para crear
/planes/<id>                 Vista semanal (día x tipo de comida) + formulario para asignar receta
/planes/<id>/entradas/<eid>/eliminar  (POST) quita una asignación

/listas                    Listado de listas de la compra + formulario para generar desde un plan
/listas/<id>                 Ítems de la lista con checkbox de comprado
/listas/<id>/eliminar        (POST) elimina la lista
```

## 5. Arquitectura (MVC en carpetas separadas)

```
recetas_app/
  models/              # Acceso a datos: conexión SQLite, esquema, repositorios CRUD
    database.py
    recipe.py
    category.py
    ingredient.py
    meal_plan.py
    shopping_list.py
  views/               # Solo presentación: plantillas HTML (Jinja2) y estáticos
    templates/
      base.html
      index.html
      recetas/...
      categorias/...
      buscar/...
      planes/...
      listas/...
    static/
      style.css
  controllers/          # Blueprints Flask: reciben la petición HTTP, llaman al modelo,
                         # eligen la plantilla a renderizar (sin lógica de negocio compleja
                         # ni acceso a la vista más allá de render_template)
    recipe_routes.py
    category_routes.py
    search_routes.py
    meal_plan_routes.py
    shopping_list_routes.py
  app.py                # Crea y configura la app Flask, registra los blueprints
  main.py                # Punto de entrada: inicializa la BD y arranca el servidor
tests/
  test_recipe_model.py
  test_shopping_list.py
  test_routes.py          # pruebas de las rutas Flask (smoke tests con el test client)
pyproject.toml            # gestionado con uv
data/
  recetas.db              # base de datos SQLite (creada en tiempo de ejecución)
```

**Regla de dependencias:** Vista → Controlador → Modelo (una sola dirección).
Las plantillas (Vista) no acceden a los modelos ni contienen lógica de negocio, solo
recorren los datos que el Controlador les pasa; los modelos no conocen a las vistas ni
a los controladores.

## 6. Fuera de alcance (v1)

- Autenticación / multiusuario.
- Interfaz gráfica o web.
- Importación/exportación de recetas (PDF, otros formatos).
- Imágenes de recetas.
