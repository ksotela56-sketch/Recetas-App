import pytest

from recetas_app.app import create_app
from recetas_app.models import database


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", db_path)
    database.init_db()
    app = create_app()
    app.testing = True
    return app.test_client()


def test_index_lists_sections(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Recetas-App" in response.data


def test_create_category_and_recipe_flow(client):
    client.post("/categorias", data={"nombre": "Postre"})
    categorias = client.get("/categorias")
    assert b"Postre" in categorias.data

    response = client.post(
        "/recetas/nueva",
        data={
            "nombre": "Tarta de manzana",
            "descripcion": "Tarta casera",
            "tiempo_preparacion": "45",
            "porciones": "8",
            "categoria_id": "1",
            "ingredientes": "manzana, 4, uds\nharina, 300, g",
            "pasos": "Pelar manzanas\nPreparar masa\nHornear",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Tarta de manzana".encode() in response.data
    assert "manzana".encode() in response.data
    assert "Hornear".encode() in response.data


def test_shopping_list_generation_from_plan(client):
    client.post(
        "/recetas/nueva",
        data={
            "nombre": "Pasta con tomate",
            "ingredientes": "tomate, 200, g\npasta, 250, g",
            "pasos": "Cocinar",
        },
    )
    client.post("/planes", data={"nombre": "Semana 1", "fecha_inicio": "2026-08-17"})
    client.post("/planes/1/asignar", data={"dia_semana": "0", "tipo_comida": "almuerzo", "recipe_id": "1"})

    response = client.post("/listas/generar", data={"plan_id": "1"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"tomate" in response.data
    assert b"200.0" in response.data


def test_recipe_not_found_returns_404(client):
    response = client.get("/recetas/999")
    assert response.status_code == 404
