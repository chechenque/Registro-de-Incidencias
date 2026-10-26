from registro_incidencias import create_app
from registro_incidencias.extensions import db
from registro_incidencias.models import Comentario, Incidencia, Usuario


def test_password_is_hashed_and_can_be_verified():
    usuario = Usuario(
        nombre="Usuario de prueba",
        correo="prueba@example.com",
    )
    usuario.establecer_password("ClaveSegura123!")

    assert usuario.password_hash != "ClaveSegura123!"
    assert usuario.verificar_password("ClaveSegura123!")
    assert not usuario.verificar_password("ClaveIncorrecta")


def test_incident_and_comment_relationships():
    app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
        }
    )

    with app.app_context():
        db.create_all()

        usuario = Usuario(
            nombre="Ana Pérez",
            correo="ana@example.com",
            rol="reportante",
        )
        usuario.establecer_password("ClaveSegura123!")

        incidencia = Incidencia(
            titulo="Falla de acceso",
            descripcion="No es posible iniciar sesión.",
            reportante=usuario,
        )

        comentario = Comentario(
            contenido="Se comenzó a revisar el problema.",
            autor=usuario,
            incidencia=incidencia,
        )

        db.session.add(usuario)
        db.session.add(incidencia)
        db.session.add(comentario)
        db.session.commit()

        incidencia_guardada = db.session.get(Incidencia, incidencia.id)

        assert incidencia_guardada is not None
        assert incidencia_guardada.reportante.nombre == "Ana Pérez"
        assert len(incidencia_guardada.comentarios) == 1
        assert incidencia_guardada.comentarios[0].autor.correo == "ana@example.com"

        db.session.remove()
        db.drop_all()


def test_administrator_role():
    administrador = Usuario(
        nombre="Administrador",
        correo="admin@example.com",
        rol="administrador",
    )
    reportante = Usuario(
        nombre="Reportante",
        correo="reportante@example.com",
        rol="reportante",
    )

    assert administrador.es_administrador()
    assert not reportante.es_administrador()