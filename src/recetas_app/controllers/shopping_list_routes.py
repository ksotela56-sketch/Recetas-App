"""Rutas web para la lista de la compra."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from recetas_app.models import meal_plan as meal_plan_model
from recetas_app.models import shopping_list as shopping_list_model
from recetas_app.models.database import db_session

shopping_list_bp = Blueprint("listas", __name__, url_prefix="/listas")


@shopping_list_bp.get("")
def listado():
    with db_session() as connection:
        listas = shopping_list_model.list_all(connection)
        planes = meal_plan_model.list_all(connection)
    return render_template("listas/listado.html", listas=listas, planes=planes)


@shopping_list_bp.post("/generar")
def generar():
    plan_id = request.form.get("plan_id", type=int)
    if not plan_id:
        flash("Elige un plan semanal.", "error")
        return redirect(url_for("listas.listado"))
    with db_session() as connection:
        if meal_plan_model.get_by_id(connection, plan_id) is None:
            abort(404)
        lista_id = shopping_list_model.generate_from_meal_plan(connection, plan_id)
    flash("Lista de la compra generada.", "success")
    return redirect(url_for("listas.detalle", lista_id=lista_id))


@shopping_list_bp.get("/<int:lista_id>")
def detalle(lista_id: int):
    with db_session() as connection:
        lista = shopping_list_model.get_by_id(connection, lista_id)
        if lista is None:
            abort(404)
        items = shopping_list_model.get_items(connection, lista_id)
    return render_template("listas/detalle.html", lista=lista, items=items)


@shopping_list_bp.post("/<int:lista_id>/items/<int:item_id>/toggle")
def toggle_item(lista_id: int, item_id: int):
    with db_session() as connection:
        items = {item.id: item for item in shopping_list_model.get_items(connection, lista_id)}
        item = items.get(item_id)
        if item is None:
            abort(404)
        shopping_list_model.mark_purchased(connection, item_id, not item.comprado)
    return redirect(url_for("listas.detalle", lista_id=lista_id))


@shopping_list_bp.post("/<int:lista_id>/eliminar")
def eliminar(lista_id: int):
    with db_session() as connection:
        shopping_list_model.delete(connection, lista_id)
    flash("Lista eliminada.", "success")
    return redirect(url_for("listas.listado"))
