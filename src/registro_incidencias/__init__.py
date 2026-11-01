import os
from pathlib import Path

from flask import Flask

from registro_incidencias.commands import crear_administrador
from registro_incidencias.extensions import csrf, db, login_manager


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-key-change-before-deployment"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL",
            f"sqlite:///{Path(app.instance_path) / 'incidencias.db'}",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from registro_incidencias import models

        db.create_all()

    login_manager.login_view = "main.login"
    login_manager.login_message = "Inicia sesión para acceder a esta sección."

    from registro_incidencias.routes import main

    app.register_blueprint(main)

    app.cli.add_command(crear_administrador)

    @app.errorhandler(403)
    def prohibido(error):
        from flask import render_template

        return (
            render_template(
                "error.html",
                codigo=403,
                titulo="Acceso no autorizado",
                mensaje="No tienes permisos para acceder a este recurso.",
            ),
            403,
        )

    @app.errorhandler(404)
    def no_encontrado(error):
        from flask import render_template

        return (
            render_template(
                "error.html",
                codigo=404,
                titulo="Página no encontrada",
                mensaje="El recurso que buscas no existe o ha sido movido.",
            ),
            404,
        )

    @app.errorhandler(500)
    def error_interno(error):
        from flask import render_template

        return (
            render_template(
                "error.html",
                codigo=500,
                titulo="Error interno del servidor",
                mensaje="Ocurrió un error inesperado. Por favor, intenta más tarde.",
            ),
            500,
        )

    return app


def main() -> None:
    app = create_app()
    app.run()

