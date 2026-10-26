import os
from pathlib import Path

from flask import Flask

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

    return app
