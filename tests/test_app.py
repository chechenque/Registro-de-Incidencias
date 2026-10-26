from registro_incidencias import create_app


def test_home_page_returns_success():
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False})
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Registro de incidencias" in response.data


def test_unknown_route_returns_404():
    app = create_app({"TESTING": True})
    client = app.test_client()

    response = client.get("/ruta-inexistente")

    assert response.status_code == 404
