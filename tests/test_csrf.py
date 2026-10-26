from registro_incidencias import create_app


def test_registration_rejects_post_without_csrf_token():
    app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SECRET_KEY": "test-secret-key",
        }
    )

    client = app.test_client()

    response = client.post(
        "/registro",
        data={
            "nombre": "Ana Pérez",
            "correo": "ana@example.com",
            "password": "ClaveSegura123!",
            "confirmar_password": "ClaveSegura123!",
        },
    )

    assert response.status_code == 400


def test_login_rejects_post_without_csrf_token():
    app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SECRET_KEY": "test-secret-key",
        }
    )

    client = app.test_client()

    response = client.post(
        "/login",
        data={
            "correo": "ana@example.com",
            "password": "ClaveSegura123!",
        },
    )

    assert response.status_code == 400


def test_registration_form_contains_csrf_token():
    app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SECRET_KEY": "test-secret-key",
        }
    )

    client = app.test_client()
    response = client.get("/registro")

    assert response.status_code == 200
    assert b"csrf_token" in response.data