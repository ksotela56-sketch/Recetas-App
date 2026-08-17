"""Punto de entrada de Recetas-App."""

from recetas_app.app import create_app
from recetas_app.models.database import init_db


def main() -> None:
    init_db()
    app = create_app()
    print("Recetas-App corriendo en http://127.0.0.1:5000")
    app.run(debug=True)


if __name__ == "__main__":
    main()
