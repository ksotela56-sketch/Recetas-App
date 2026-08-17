"""Rutas web para la gestión de categorías."""

import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, url_for

from recetas_app.models import category as category_model
from recetas_app.models.database import db_session

category_bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@category_bp.get("")
def listado():
    with db_session() as connection:
        categorias = category_model.list_all(connection)
    return render_template("categorias/listado.html", categorias=categorias)


@category_bp.post("")
def crear():
    nombre = request.form.get("nombre", "").strip()
    if not nombre:
        flash("El nombre no puede estar vacío.", "error")
        return redirect(url_for("categorias.listado"))
    with db_session() as connection:
        try:
            category_model.create(connection, nombre)
            flash(f"Categoría '{nombre}' creada.", "success")
        except sqlite3.IntegrityError:
            flash(f"Ya existe una categoría llamada '{nombre}'.", "error")
    return redirect(url_for("categorias.listado"))


@category_bp.post("/<int:category_id>/eliminar")
def eliminar(category_id: int):
    with db_session() as connection:
        category_model.delete(connection, category_id)
    flash("Categoría eliminada. Las recetas que la usaban quedan sin categoría.", "success")
    return redirect(url_for("categorias.listado"))
