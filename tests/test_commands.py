from registro_incidencias import create_app
from registro_incidencias.extensions import db
from registro_incidencias.models import Usuario


def test_crear_administrador_comando():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SECRET_KEY": "test-key",
            "WTF_CSRF_ENABLED": False,
        }
    )

    runner = app.test_cli_runner()

    result = runner.invoke(
        args=["crear-administrador"],
        input="Admin Root\nadmin@sistema.local\nClaveSeguraSuper123!\nClaveSeguraSuper123!\n",
    )

    assert result.exit_code == 0
    assert "Administrador creado correctamente." in result.output

    with app.app_context():
        admin = db.session.query(Usuario).filter_by(correo="admin@sistema.local").first()
        assert admin is not None
        assert admin.rol == "administrador"
        assert admin.verificar_password("ClaveSeguraSuper123!")


def test_crear_administrador_rechaza_correo_duplicado():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SECRET_KEY": "test-key",
            "WTF_CSRF_ENABLED": False,
        }
    )

    with app.app_context():
        usuario = Usuario(
            nombre="Existente",
            correo="duplicado@sistema.local",
            rol="reportante",
        )
        usuario.establecer_password("PasswordSeguro123!")
        db.session.add(usuario)
        db.session.commit()

    runner = app.test_cli_runner()

    result = runner.invoke(
        args=["crear-administrador"],
        input="Admin Duplicado\nduplicado@sistema.local\n",
    )

    assert result.exit_code == 0
    assert "Ya existe una cuenta con ese correo." in result.output


def test_crear_administrador_rechaza_clave_corta():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SECRET_KEY": "test-key",
            "WTF_CSRF_ENABLED": False,
        }
    )

    runner = app.test_cli_runner()

    result = runner.invoke(
        args=["crear-administrador"],
        input="Admin Corto\ncorto@sistema.local\n123456\n123456\n",
    )

    assert result.exit_code == 0
    assert "La contraseña debe tener al menos 12 caracteres." in result.output
