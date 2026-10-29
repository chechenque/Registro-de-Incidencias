from flask.testing import FlaskClient

from registro_incidencias import create_app
from registro_incidencias.extensions import db
from registro_incidencias.models import Comentario, Incidencia, Usuario


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


def create_user(
    app,
    nombre: str,
    correo: str,
    rol: str = "reportante",
) -> int:
    with app.app_context():
        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            rol=rol,
        )
        usuario.establecer_password("ClaveSegura123!")

        db.session.add(usuario)
        db.session.commit()

        return usuario.id


def create_incident(
    app,
    reportante_id: int,
    titulo: str,
) -> int:
    with app.app_context():
        incidencia = Incidencia(
            titulo=titulo,
            descripcion="Descripción de prueba suficientemente extensa.",
            prioridad="media",
            estado="abierta",
            reportante_id=reportante_id,
        )

        db.session.add(incidencia)
        db.session.commit()

        return incidencia.id


def login(
    client: FlaskClient,
    correo: str,
) -> None:
    response = client.post(
        "/login",
        data={
            "correo": correo,
            "password": "ClaveSegura123!",
            "submit": "Iniciar sesión",
        },
    )

    assert response.status_code == 302


def test_reporter_can_create_incident():
    app = create_test_app()
    create_user(app, "Ana Pérez", "ana@example.com")

    client = app.test_client()
    login(client, "ana@example.com")

    response = client.post(
        "/incidencias/nueva",
        data={
            "titulo": "Error de acceso al sistema",
            "descripcion": (
                "El sistema rechaza mis credenciales "
                "aunque son correctas."
            ),
            "prioridad": "alta",
            "submit": "Registrar incidencia",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Error de acceso al sistema" in response.data

    with app.app_context():
        incidencia = db.session.scalar(
            db.select(Incidencia).where(
                Incidencia.titulo == "Error de acceso al sistema"
            )
        )

        assert incidencia is not None
        assert incidencia.reportante.correo == "ana@example.com"
        assert incidencia.estado == "abierta"
        assert incidencia.prioridad == "alta"


def test_reporter_sees_only_own_incidents():
    app = create_test_app()

    ana_id = create_user(app, "Ana Pérez", "ana@example.com")
    create_user(app, "Luis García", "luis@example.com")

    create_incident(app, ana_id, "Incidencia de Ana")

    with app.app_context():
        luis = db.session.scalar(
            db.select(Usuario).where(
                Usuario.correo == "luis@example.com"
            )
        )
        assert luis is not None
        luis_id = luis.id

    create_incident(app, luis_id, "Incidencia de Luis")

    client = app.test_client()
    login(client, "ana@example.com")

    response = client.get("/incidencias")

    assert response.status_code == 200
    assert b"Incidencia de Ana" in response.data
    assert b"Incidencia de Luis" not in response.data


def test_reporter_cannot_access_another_users_incident():
    app = create_test_app()

    ana_id = create_user(app, "Ana Pérez", "ana@example.com")
    incidencia_id = create_incident(
        app,
        ana_id,
        "Incidencia privada de Ana",
    )

    create_user(app, "Luis García", "luis@example.com")

    client = app.test_client()
    login(client, "luis@example.com")

    response = client.get(f"/incidencias/{incidencia_id}")

    assert response.status_code == 403


def test_administrator_can_see_all_incidents():
    app = create_test_app()

    ana_id = create_user(app, "Ana Pérez", "ana@example.com")
    admin_id = create_user(
        app,
        "Administrador",
        "admin@example.com",
        rol="administrador",
    )

    create_incident(app, ana_id, "Incidencia de Ana")
    create_incident(app, admin_id, "Incidencia administrativa")

    client = app.test_client()
    login(client, "admin@example.com")

    response = client.get("/incidencias")

    assert response.status_code == 200
    assert b"Incidencia de Ana" in response.data
    assert b"Incidencia administrativa" in response.data


def test_incident_comment_and_admin_status_update():
    app = create_test_app()

    ana_id = create_user(app, "Ana Pérez", "ana@example.com")
    incidencia_id = create_incident(
        app,
        ana_id,
        "Incidencia para seguimiento",
    )

    client = app.test_client()
    login(client, "ana@example.com")

    response = client.post(
        f"/incidencias/{incidencia_id}",
        data={
            "accion": "comentario",
            "contenido": "Ya se revisó el problema.",
            "submit": "Agregar comentario",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Ya se revis" in response.data

    with app.app_context():
        comentario = db.session.scalar(
            db.select(Comentario).where(
                Comentario.incidencia_id == incidencia_id
            )
        )

        assert comentario is not None
        assert comentario.autor.correo == "ana@example.com"

    response = client.post(
        f"/incidencias/{incidencia_id}/estado",
        data={
            "estado": "resuelta",
            "submit": "Actualizar estado",
        },
    )

    assert response.status_code == 403

    create_user(
        app,
        "Administrador",
        "admin@example.com",
        rol="administrador",
    )

    admin_client = app.test_client()
    login(admin_client, "admin@example.com")

    response = admin_client.post(
        f"/incidencias/{incidencia_id}/estado",
        data={
            "estado": "resuelta",
            "submit": "Actualizar estado",
        },
    )

    assert response.status_code == 302

    with app.app_context():
        incidencia = db.session.get(Incidencia, incidencia_id)

        assert incidencia is not None
        assert incidencia.estado == "resuelta"

def test_incident_rejects_invalid_priority():
    app = create_test_app()
    create_user(app, "Ana Pérez", "ana@example.com")

    client = app.test_client()
    login(client, "ana@example.com")

    response = client.post(
        "/incidencias/nueva",
        data={
            "titulo": "Error de acceso al sistema",
            "descripcion": (
                "El sistema rechaza mis credenciales "
                "aunque son correctas."
            ),
            "prioridad": "superadmin",
            "submit": "Registrar incidencia",
        },
    )

    assert response.status_code == 200

    with app.app_context():
        incidencias = db.session.scalars(
            db.select(Incidencia)
        ).all()

        assert len(incidencias) == 0

def test_admin_cannot_assign_invalid_incident_status():
    app = create_test_app()

    ana_id = create_user(app, "Ana Pérez", "ana@example.com")
    create_user(
        app,
        "Administrador",
        "admin@example.com",
        rol="administrador",
    )

    incidencia_id = create_incident(
        app,
        ana_id,
        "Incidencia de prueba",
    )

    client = app.test_client()
    login(client, "admin@example.com")

    response = client.post(
        f"/incidencias/{incidencia_id}/estado",
        data={
            "estado": "eliminada",
            "submit": "Actualizar estado",
        },
    )

    assert response.status_code == 302

    with app.app_context():
        incidencia = db.session.get(Incidencia, incidencia_id)

        assert incidencia is not None
        assert incidencia.estado == "abierta"

def test_registration_cannot_assign_administrator_role():
    app = create_test_app()
    client = app.test_client()

    response = client.post(
        "/registro",
        data={
            "nombre": "Usuario de prueba",
            "correo": "usuario@example.com",
            "password": "ClaveSegura123!",
            "confirmar_password": "ClaveSegura123!",
            "rol": "administrador",
            "submit": "Crear cuenta",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        usuario = db.session.scalar(
            db.select(Usuario).where(
                Usuario.correo == "usuario@example.com"
            )
        )

        assert usuario is not None
        assert usuario.rol == "reportante"
        assert not usuario.es_administrador()