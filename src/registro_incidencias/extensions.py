from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id: str):
    """Recupera un usuario autenticado a partir de su identificador."""
    from registro_incidencias.models import Usuario

    try:
        return db.session.get(Usuario, int(user_id))
    except (TypeError, ValueError):
        return None
