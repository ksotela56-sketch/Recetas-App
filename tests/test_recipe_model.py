from recetas_app.models import category as category_model
from recetas_app.models import recipe as recipe_model


def test_create_and_get_detail(connection):
    categoria = category_model.create(connection, "Postre")
    recipe_id = recipe_model.create(
        connection,
        nombre="Tarta de manzana",
        descripcion="Tarta casera",
        tiempo_preparacion=60,
        porciones=8,
        categoria_id=categoria.id,
        ingredientes=[("manzana", 4, "uds"), ("harina", 300, "g")],
        pasos=["Pelar manzanas", "Preparar masa", "Hornear"],
    )

    receta = recipe_model.get_detail(connection, recipe_id)

    assert receta is not None
    assert receta.nombre == "Tarta de manzana"
    assert receta.categoria_nombre == "Postre"
    assert [i.nombre for i in receta.ingredientes] == ["harina", "manzana"]
    assert [p.descripcion for p in receta.pasos] == ["Pelar manzanas", "Preparar masa", "Hornear"]


def test_update_replaces_ingredients_and_steps(connection):
    recipe_id = recipe_model.create(
        connection,
        nombre="Ensalada",
        descripcion=None,
        tiempo_preparacion=10,
        porciones=2,
        categoria_id=None,
        ingredientes=[("lechuga", 1, "und")],
        pasos=["Lavar", "Cortar"],
    )

    recipe_model.update(
        connection,
        recipe_id,
        nombre="Ensalada César",
        descripcion="Con pollo",
        tiempo_preparacion=15,
        porciones=2,
        categoria_id=None,
        ingredientes=[("pollo", 200, "g")],
        pasos=["Cocinar pollo"],
    )

    receta = recipe_model.get_detail(connection, recipe_id)
    assert receta.nombre == "Ensalada César"
    assert [i.nombre for i in receta.ingredientes] == ["pollo"]
    assert [p.descripcion for p in receta.pasos] == ["Cocinar pollo"]


def test_delete_recipe(connection):
    recipe_id = recipe_model.create(
        connection, "Sopa", None, 20, 4, None, [("sal", 1, "g")], ["Hervir"]
    )
    recipe_model.delete(connection, recipe_id)
    assert recipe_model.get_detail(connection, recipe_id) is None


def test_search_by_name_and_ingredient(connection):
    recipe_model.create(connection, "Pan integral", None, 90, 1, None, [("harina integral", 500, "g")], [])
    recipe_model.create(connection, "Pan blanco", None, 90, 1, None, [("harina", 500, "g")], [])

    por_nombre = recipe_model.search_by_name(connection, "integral")
    por_ingrediente = recipe_model.search_by_ingredient(connection, "harina")

    assert [r.nombre for r in por_nombre] == ["Pan integral"]
    assert {r.nombre for r in por_ingrediente} == {"Pan integral", "Pan blanco"}
