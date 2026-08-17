"""Rutas web para la búsqueda y filtrado de recetas."""

from flask import Blueprint, render_template, request

from recetas_app.models import category as category_model
from recetas_app.models import recipe as recipe_model
from recetas_app.models.database import db_session

search_bp = Blueprint("buscar", __name__, url_prefix="/buscar")


@search_bp.get("")
def buscar():
    tipo = request.args.get("tipo", "nombre")
    texto = request.args.get("q", "").strip()
    categoria_id = request.args.get("categoria_id", type=int)

    resultados = None
    with db_session() as connection:
        categorias = category_model.list_all(connection)
        if tipo == "nombre" and texto:
            resultados = recipe_model.search_by_name(connection, texto)
        elif tipo == "ingrediente" and texto:
            resultados = recipe_model.search_by_ingredient(connection, texto)
        elif tipo == "categoria" and categoria_id:
            resultados = recipe_model.search_by_category(connection, categoria_id)

    return render_template(
        "buscar/resultados.html",
        categorias=categorias,
        resultados=resultados,
        tipo=tipo,
        texto=texto,
        categoria_id=categoria_id,
    )
