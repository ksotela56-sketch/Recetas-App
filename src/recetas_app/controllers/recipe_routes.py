"""Rutas web para la gestión de recetas."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from recetas_app.models import category as category_model
from recetas_app.models import recipe as recipe_model
from recetas_app.models.database import db_session

recipe_bp = Blueprint("recetas", __name__, url_prefix="/recetas")


@recipe_bp.get("")
def listado():
    with db_session() as connection:
        recetas = recipe_model.list_all(connection)
    return render_template("recetas/listado.html", recetas=recetas)


@recipe_bp.get("/<int:recipe_id>")
def detalle(recipe_id: int):
    with db_session() as connection:
        receta = recipe_model.get_detail(connection, recipe_id)
    if receta is None:
        abort(404)
    return render_template("recetas/detalle.html", receta=receta)


@recipe_bp.get("/nueva")
def nueva():
    with db_session() as connection:
        categorias = category_model.list_all(connection)
    return render_template("recetas/formulario.html", receta=None, categorias=categorias)


@recipe_bp.post("/nueva")
def crear():
    datos = _leer_formulario(request)
    if datos is None:
        return redirect(url_for("recetas.nueva"))
    with db_session() as connection:
        recipe_id = recipe_model.create(connection, **datos)
    flash(f"Receta '{datos['nombre']}' creada.", "success")
    return redirect(url_for("recetas.detalle", recipe_id=recipe_id))


@recipe_bp.get("/<int:recipe_id>/editar")
def editar_formulario(recipe_id: int):
    with db_session() as connection:
        receta = recipe_model.get_detail(connection, recipe_id)
        categorias = category_model.list_all(connection)
    if receta is None:
        abort(404)
    return render_template("recetas/formulario.html", receta=receta, categorias=categorias)


@recipe_bp.post("/<int:recipe_id>/editar")
def editar(recipe_id: int):
    with db_session() as connection:
        if recipe_model.get_detail(connection, recipe_id) is None:
            abort(404)
        datos = _leer_formulario(request)
        if datos is None:
            return redirect(url_for("recetas.editar_formulario", recipe_id=recipe_id))
        recipe_model.update(connection, recipe_id, **datos)
    flash("Receta actualizada.", "success")
    return redirect(url_for("recetas.detalle", recipe_id=recipe_id))


@recipe_bp.post("/<int:recipe_id>/eliminar")
def eliminar(recipe_id: int):
    with db_session() as connection:
        recipe_model.delete(connection, recipe_id)
    flash("Receta eliminada.", "success")
    return redirect(url_for("recetas.listado"))


def _leer_formulario(req) -> dict | None:
    nombre = req.form.get("nombre", "").strip()
    if not nombre:
        flash("El nombre no puede estar vacío.", "error")
        return None

    descripcion = req.form.get("descripcion", "").strip() or None
    tiempo_preparacion = _entero_opcional(req.form.get("tiempo_preparacion", ""))
    porciones = _entero_opcional(req.form.get("porciones", ""))
    categoria_id = _entero_opcional(req.form.get("categoria_id", ""))

    ingredientes = _parsear_ingredientes(req.form.get("ingredientes", ""))
    pasos = [linea.strip() for linea in req.form.get("pasos", "").splitlines() if linea.strip()]

    return {
        "nombre": nombre,
        "descripcion": descripcion,
        "tiempo_preparacion": tiempo_preparacion,
        "porciones": porciones,
        "categoria_id": categoria_id,
        "ingredientes": ingredientes,
        "pasos": pasos,
    }


def _parsear_ingredientes(texto: str) -> list[tuple[str, float | None, str | None]]:
    ingredientes = []
    for linea in texto.splitlines():
        if not linea.strip():
            continue
        partes = [p.strip() for p in linea.split(",")]
        nombre = partes[0]
        if not nombre:
            continue
        cantidad = None
        if len(partes) > 1 and partes[1]:
            try:
                cantidad = float(partes[1])
            except ValueError:
                cantidad = None
        unidad = partes[2] if len(partes) > 2 and partes[2] else None
        ingredientes.append((nombre, cantidad, unidad))
    return ingredientes


def _entero_opcional(valor: str) -> int | None:
    valor = valor.strip()
    return int(valor) if valor.isdigit() else None
