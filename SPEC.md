# Especificación — Recetas-App

## 1. Resumen

Aplicación de recetas de cocina en Python, con interfaz de línea de comandos (CLI),
persistencia en SQLite y arquitectura **MVC** (Modelo / Vista / Controlador) en carpetas
separadas. Gestión de dependencias y entorno con **uv**.

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

## 4. Pantallas (menús CLI)

```
Menú principal
 1. Recetas
    1.1 Listar recetas
    1.2 Ver detalle de receta
    1.3 Crear receta
    1.4 Editar receta
    1.5 Eliminar receta
 2. Categorías
    2.1 Listar categorías
    2.2 Crear categoría
    2.3 Eliminar categoría
 3. Buscar recetas
    3.1 Por nombre
    3.2 Por categoría
    3.3 Por ingrediente
 4. Planificación semanal
    4.1 Crear plan semanal
    4.2 Ver plan semanal
    4.3 Asignar receta a día/comida
    4.4 Quitar asignación
 5. Lista de la compra
    5.1 Generar desde un plan semanal
    5.2 Ver lista de la compra
    5.3 Marcar ítem como comprado
    5.4 Eliminar lista
 6. Salir
```

## 5. Arquitectura (MVC en carpetas separadas)

```
recetas_app/
  models/            # Acceso a datos: conexión SQLite, esquema, repositorios CRUD
    database.py
    recipe.py
    category.py
    ingredient.py
    meal_plan.py
    shopping_list.py
  views/             # Solo presentación: leer input, imprimir menús/resultados
    main_menu_view.py
    recipe_view.py
    category_view.py
    search_view.py
    meal_plan_view.py
    shopping_list_view.py
  controllers/        # Orquestan Modelo <-> Vista, validaciones, lógica de negocio
    recipe_controller.py
    category_controller.py
    search_controller.py
    meal_plan_controller.py
    shopping_list_controller.py
  main.py             # Punto de entrada
tests/
  test_recipe_model.py
  test_meal_plan_controller.py
  test_shopping_list.py
pyproject.toml         # gestionado con uv
data/
  recetas.db           # base de datos SQLite (creada en tiempo de ejecución)
```

**Regla de dependencias:** Vista → Controlador → Modelo (una sola dirección).
Las vistas no acceden a los modelos directamente ni contienen lógica de negocio;
los modelos no conocen a las vistas ni a los controladores.

## 6. Fuera de alcance (v1)

- Autenticación / multiusuario.
- Interfaz gráfica o web.
- Importación/exportación de recetas (PDF, otros formatos).
- Imágenes de recetas.
