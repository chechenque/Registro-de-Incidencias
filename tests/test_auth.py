from registro_incidencias import create_app
from registro_incidencias.extensions import db
from registro_incidencias.models import Usuario


def create_test_app():
    app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SECRET_KEY": "test-secret-key",
        }
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app


def test_registration_creates_reporter_account():
    app = create_test_app()
    client = app.test_client()

    response = client.post(
        "/registro",
        data={
            "nombre": "Ana Pérez",
            "correo": "ana@example.com",
            "password": "ClaveSegura123!",
            "confirmar_password": "ClaveSegura123!",
            "submit": "Crear cuenta",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        usuario = db.session.query(Usuario).filter_by(
            correo="ana@example.com"
        ).first()

        assert usuario is not None
        assert usuario.rol == "reportante"
        assert usuario.verificar_password("ClaveSegura123!")
        assert usuario.password_hash != "ClaveSegura123!"


def test_login_with_valid_credentials():
    app = create_test_app()

    with app.app_context():
        usuario = Usuario(
            nombre="Ana Pérez",
            correo="ana@example.com",
            rol="reportante",
        )
        usuario.establecer_password("ClaveSegura123!")
        db.session.add(usuario)
        db.session.commit()

    client = app.test_client()

    response = client.post(
        "/login",
        data={
            "correo": "ana@example.com",
            "password": "ClaveSegura123!",
            "submit": "Iniciar sesión",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Ana P" in response.data


def test_login_rejects_incorrect_password():
    app = create_test_app()

    with app.app_context():
        usuario = Usuario(
            nombre="Ana Pérez",
            correo="ana@example.com",
            rol="reportante",
        )
        usuario.establecer_password("ClaveSegura123!")
        db.session.add(usuario)
        db.session.commit()

    client = app.test_client()

    response = client.post(
        "/login",
        data={
            "correo": "ana@example.com",
            "password": "ContraseñaIncorrecta123!",
            "submit": "Iniciar sesión",
        },
    )

    assert response.status_code == 401


def test_logout_requires_authentication():
    app = create_test_app()
    client = app.test_client()

    response = client.post("/logout")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]