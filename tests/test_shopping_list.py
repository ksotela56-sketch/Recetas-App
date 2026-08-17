from recetas_app.models import meal_plan as meal_plan_model
from recetas_app.models import recipe as recipe_model
from recetas_app.models import shopping_list as shopping_list_model


def test_shopping_list_aggregates_repeated_ingredients(connection):
    receta1 = recipe_model.create(
        connection, "Pasta con tomate", None, 20, 2, None, [("tomate", 200, "g"), ("pasta", 250, "g")], []
    )
    receta2 = recipe_model.create(
        connection, "Ensalada de tomate", None, 10, 2, None, [("tomate", 150, "g")], []
    )

    plan = meal_plan_model.create(connection, "Semana de prueba", None)
    meal_plan_model.add_entry(connection, plan.id, dia_semana=0, tipo_comida="almuerzo", recipe_id=receta1)
    meal_plan_model.add_entry(connection, plan.id, dia_semana=1, tipo_comida="cena", recipe_id=receta2)

    lista_id = shopping_list_model.generate_from_meal_plan(connection, plan.id)
    items = {item.nombre: item for item in shopping_list_model.get_items(connection, lista_id)}

    assert items["tomate"].cantidad_total == 350
    assert items["tomate"].unidad == "g"
    assert items["pasta"].cantidad_total == 250
    assert all(not item.comprado for item in items.values())


def test_mark_purchased_toggles_item(connection):
    receta = recipe_model.create(connection, "Arroz", None, 20, 2, None, [("arroz", 200, "g")], [])
    plan = meal_plan_model.create(connection, "Semana", None)
    meal_plan_model.add_entry(connection, plan.id, 0, "almuerzo", receta)
    lista_id = shopping_list_model.generate_from_meal_plan(connection, plan.id)
    item = shopping_list_model.get_items(connection, lista_id)[0]

    shopping_list_model.mark_purchased(connection, item.id, True)

    item_actualizado = shopping_list_model.get_items(connection, lista_id)[0]
    assert item_actualizado.comprado is True
