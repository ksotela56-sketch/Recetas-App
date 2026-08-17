"""Rutas web para la planificación semanal."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from recetas_app.models import meal_plan as meal_plan_model
from recetas_app.models import recipe as recipe_model
from recetas_app.models.database import db_session

meal_plan_bp = Blueprint("planes", __name__, url_prefix="/planes")


@meal_plan_bp.get("")
def listado():
    with db_session() as connection:
        planes = meal_plan_model.list_all(connection)
    return render_template("planes/listado.html", planes=planes)


@meal_plan_bp.post("")
def crear():
    nombre = request.form.get("nombre", "").strip()
    fecha_inicio = request.form.get("fecha_inicio", "").strip() or None
    if not nombre:
        flash("El nombre no puede estar vacío.", "error")
        return redirect(url_for("planes.listado"))
    with db_session() as connection:
        plan = meal_plan_model.create(connection, nombre, fecha_inicio)
    flash(f"Plan '{plan.nombre}' creado.", "success")
    return redirect(url_for("planes.detalle", plan_id=plan.id))


@meal_plan_bp.get("/<int:plan_id>")
def detalle(plan_id: int):
    with db_session() as connection:
        plan = meal_plan_model.get_by_id(connection, plan_id)
        if plan is None:
            abort(404)
        entradas = meal_plan_model.get_entries(connection, plan_id)
        recetas = recipe_model.list_all(connection)
    return render_template(
        "planes/detalle.html",
        plan=plan,
        entradas=entradas,
        recetas=recetas,
        dias=meal_plan_model.DIAS_SEMANA,
        tipos_comida=meal_plan_model.TIPOS_COMIDA,
    )


@meal_plan_bp.post("/<int:plan_id>/asignar")
def asignar(plan_id: int):
    dia_semana = request.form.get("dia_semana", type=int)
    tipo_comida = request.form.get("tipo_comida", "")
    recipe_id = request.form.get("recipe_id", type=int)

    if dia_semana is None or tipo_comida not in meal_plan_model.TIPOS_COMIDA or not recipe_id:
        flash("Completa día, tipo de comida y receta.", "error")
        return redirect(url_for("planes.detalle", plan_id=plan_id))

    with db_session() as connection:
        if meal_plan_model.get_by_id(connection, plan_id) is None:
            abort(404)
        meal_plan_model.add_entry(connection, plan_id, dia_semana, tipo_comida, recipe_id)
    flash("Receta asignada al plan.", "success")
    return redirect(url_for("planes.detalle", plan_id=plan_id))


@meal_plan_bp.post("/<int:plan_id>/entradas/<int:entry_id>/eliminar")
def quitar_entrada(plan_id: int, entry_id: int):
    with db_session() as connection:
        meal_plan_model.remove_entry(connection, entry_id)
    flash("Asignación eliminada.", "success")
    return redirect(url_for("planes.detalle", plan_id=plan_id))
