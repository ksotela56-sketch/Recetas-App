"""Creación y configuración de la aplicación Flask."""

from pathlib import Path

from flask import Flask, render_template

from recetas_app.controllers.category_routes import category_bp
from recetas_app.controllers.meal_plan_routes import meal_plan_bp
from recetas_app.controllers.recipe_routes import recipe_bp
from recetas_app.controllers.search_routes import search_bp
from recetas_app.controllers.shopping_list_routes import shopping_list_bp

VIEWS_DIR = Path(__file__).resolve().parent / "views"


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(VIEWS_DIR / "templates"),
        static_folder=str(VIEWS_DIR / "static"),
    )
    app.secret_key = "recetas-app-dev"
    app.jinja_env.globals["enumerate"] = enumerate

    app.register_blueprint(recipe_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(meal_plan_bp)
    app.register_blueprint(shopping_list_bp)

    @app.get("/")
    def index():
        return render_template("index.html")

    return app
